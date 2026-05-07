#!/usr/bin/env python3
"""
Xreal One Pro → Stretch 3 Head Control Bridge
Runs on YOUR PC. Sends head pan/tilt commands over TCP to stretch_relay.py on the robot.

Usage:
  1. On Stretch: python3 stretch_relay.py
  2. Connect Xreal One Pro via USB-C
  3. On PC: python3 stretch_head_control.py

Controls:
  T  - Zero view (set current head position as neutral)
  R  - Recalibrate gyroscope (keep glasses still)
  L  - Lock/unlock head tracking
  Q  - Quit

No ROS2 needed on this PC.
"""

import sys
import os
import time
import socket
import json
import threading
import tty
import termios

from src.imu_data import IMUData
from src.head_tracker import HeadTracker
from src.imu_reader_fixed import IMUReaderFixed as IMUReader

# ── Configuration ──────────────────────────────────────────────

STRETCH_IP = "172.22.243.8"
RELAY_PORT = 9090

# Stretch head joint limits (radians)
HEAD_PAN_MIN = -3.9
HEAD_PAN_MAX = 1.5
HEAD_TILT_MIN = -1.53
HEAD_TILT_MAX = 0.79

# Mapping: head degrees → joint radians
HEAD_PAN_SCALE = 0.025
HEAD_TILT_SCALE = 0.015

# Command rate limiting
COMMAND_INTERVAL = 0.05  # 20Hz

# ── Base control (DRIVE mode) ────────────────────────────────
BASE_LINEAR_MAX = 0.3       # m/s max forward/reverse speed
BASE_ANGULAR_MAX = 0.5      # rad/s max rotation speed
BASE_DEADZONE = 5.0         # degrees — no movement within this range
BASE_MAX_ANGLE = 30.0       # degrees — full speed at this angle
SPACE_TIMEOUT = 0.2         # seconds — space "released" after this


def map_angle_to_velocity(angle_deg, deadzone, max_angle, max_vel):
    """Map head angle to velocity with dead zone. Returns 0 inside dead zone,
    linearly scales from deadzone to max_angle, clamps at max_vel."""
    if abs(angle_deg) < deadzone:
        return 0.0
    sign = 1.0 if angle_deg > 0 else -1.0
    scaled = (abs(angle_deg) - deadzone) / (max_angle - deadzone)
    return sign * min(1.0, max(0.0, scaled)) * max_vel


class StretchTCPClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None
        self.locked = False
        self.last_command_time = 0.0

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        self.sock.connect((self.ip, self.port))
        print(f"  Connected to Stretch relay at {self.ip}:{self.port}")

    def send_head_command(self, pan_rad, tilt_rad):
        now = time.time()
        if now - self.last_command_time < COMMAND_INTERVAL:
            return
        self.last_command_time = now

        pan_rad = max(HEAD_PAN_MIN, min(HEAD_PAN_MAX, pan_rad))
        tilt_rad = max(HEAD_TILT_MIN, min(HEAD_TILT_MAX, tilt_rad))

        msg = json.dumps({"pan": round(pan_rad, 4), "tilt": round(tilt_rad, 4)}) + "\n"
        try:
            self.sock.sendall(msg.encode())
        except (BrokenPipeError, OSError) as e:
            print(f"\n  Connection lost: {e}")

    def send_base_command(self, linear, angular):
        """Send base velocity command. Rate-limited same as head commands."""
        now = time.time()
        if now - self.last_command_time < COMMAND_INTERVAL:
            return
        self.last_command_time = now

        msg = json.dumps({"linear": round(linear, 4), "angular": round(angular, 4)}) + "\n"
        try:
            self.sock.sendall(msg.encode())
        except (BrokenPipeError, OSError) as e:
            print(f"\n  Connection lost: {e}")

    def send_stop(self):
        """Send immediate zero-velocity base command (bypasses rate limit)."""
        msg = json.dumps({"linear": 0.0, "angular": 0.0}) + "\n"
        try:
            self.sock.sendall(msg.encode())
        except (BrokenPipeError, OSError):
            pass

    def close(self):
        if self.sock:
            self.sock.close()


class XrealStretchBridge:
    def __init__(self):
        self.head_tracker = HeadTracker()
        self.head_tracker.pitch_scale = 1.0
        self.head_tracker.yaw_scale = 1.0
        self.head_tracker.roll_scale = 1.0

        self.client = StretchTCPClient(STRETCH_IP, RELAY_PORT)

        # Mode: "LOOK" (head pan/tilt) or "DRIVE" (base velocity)
        self.mode = "LOOK"
        self.space_held = False
        self.last_space_time = 0.0

        self.client.connect()

    def imu_callback(self, imu_data: IMUData, message_count: int, rate: float):
        if not self.head_tracker.is_calibrated:
            self.head_tracker.calibrate_gyroscope(imu_data)
            if message_count % 100 == 0:
                pct = self.head_tracker.get_calibration_progress()
                print(f"\r  Calibrating... {pct:.0f}%", end="", flush=True)
            if self.head_tracker.is_calibrated:
                print("\n  Calibration complete! Press T to zero your view.")
            return

        self.head_tracker.update(imu_data)
        orient = self.head_tracker.get_relative_orientation()
        pitch = orient['pitch']
        yaw = orient['yaw']
        roll = orient['roll']

        if self.client.locked:
            if message_count % 100 == 0:
                print(f"\r  [LOCKED] pitch={pitch:+6.1f}  roll={roll:+6.1f}", end="", flush=True)
            return

        if self.mode == "LOOK":
            # Yaw = left/right head turns (pan), pitch = up/down (inverted tilt)
            pan_rad = -yaw * HEAD_PAN_SCALE
            tilt_rad = -pitch * HEAD_TILT_SCALE

            self.client.send_head_command(pan_rad, tilt_rad)

            if message_count % 50 == 0:
                print(
                    f"\r  [LOOK] pan={pan_rad:+.2f}rad  tilt={tilt_rad:+.2f}rad  "
                    f"pitch={pitch:+6.1f}  yaw={yaw:+6.1f}  ({rate:.0f}Hz)  ",
                    end="", flush=True
                )

        elif self.mode == "DRIVE":
            # Check if spacebar is still held (key repeat within timeout)
            self.space_held = (time.time() - self.last_space_time) < SPACE_TIMEOUT

            if self.space_held:
                # Yaw (look left/right) → angular velocity
                # Pitch (look down) → forward, (look up) → reverse
                linear = map_angle_to_velocity(-pitch, BASE_DEADZONE, BASE_MAX_ANGLE, BASE_LINEAR_MAX)
                angular = map_angle_to_velocity(-yaw, BASE_DEADZONE, BASE_MAX_ANGLE, BASE_ANGULAR_MAX)
                self.client.send_base_command(linear, angular)

                if message_count % 50 == 0:
                    print(
                        f"\r  [DRIVE] lin={linear:+.2f}m/s  ang={angular:+.2f}rad/s  "
                        f"pitch={pitch:+6.1f}  yaw={yaw:+6.1f}  ({rate:.0f}Hz)  ",
                        end="", flush=True
                    )
            else:
                self.client.send_base_command(0.0, 0.0)
                if message_count % 200 == 0:
                    print(
                        f"\r  [DRIVE] STOPPED — hold SPACE to move  ({rate:.0f}Hz)  ",
                        end="", flush=True
                    )

    def run(self):
        print("=" * 60)
        print("  XREAL ONE PRO → STRETCH 3 TELEOP")
        print("=" * 60)
        print()
        print("  M = toggle LOOK/DRIVE | SPACE = hold to drive")
        print("  T = zero view | R = recalibrate | L = lock | Q = quit")
        print()
        print("  Keep glasses still for calibration...")
        print()

        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            key_thread = threading.Thread(target=self._key_loop, daemon=True)
            key_thread.start()

            with IMUReader(callback=self.imu_callback) as reader:
                reader.run()
        except KeyboardInterrupt:
            print("\n  Shutting down...")
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            self.client.close()

    def _key_loop(self):
        while True:
            try:
                ch = sys.stdin.read(1)
                if ch == ' ':
                    self.last_space_time = time.time()
                    continue

                ch = ch.lower()
                if ch == 't':
                    self.head_tracker.zero_view()
                    print(f"\n  VIEW ZEROED [{self.mode}]")
                elif ch == 'r':
                    self.head_tracker.reset_calibration()
                    print("\n  RECALIBRATING — keep still...")
                elif ch == 'l':
                    self.client.locked = not self.client.locked
                    if self.client.locked and self.mode == "DRIVE":
                        self.client.send_stop()
                    print(f"\n  {'LOCKED' if self.client.locked else 'UNLOCKED'}")
                elif ch == 'm':
                    if self.mode == "LOOK":
                        self.mode = "DRIVE"
                        print("\n  MODE: DRIVE — hold SPACE to move, head steers")
                    else:
                        self.client.send_stop()
                        self.mode = "LOOK"
                        print("\n  MODE: LOOK — head controls camera pan/tilt")
                elif ch == 'q' or ch == '\x03':
                    print("\n  Quitting...")
                    self.client.send_stop()
                    os._exit(0)
            except Exception:
                break


if __name__ == "__main__":
    XrealStretchBridge().run()
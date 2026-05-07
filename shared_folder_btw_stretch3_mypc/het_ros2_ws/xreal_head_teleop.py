#!/usr/bin/env python3
"""
XReal One Pro Head Tracking → Stretch 3 Teleop

Reads head orientation from XRLinuxDriver (OpenTrack UDP) and maps:
- Yaw (left/right head turn) → robot base rotation
- Pitch (head tilt up/down) → robot head tilt joint
- Roll (head tilt sideways) → unused (reserved for future)

Run on your PC with XReal glasses connected.
Robot must have stretch_driver running.
"""

import struct
import socket
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

import math


class XRealHeadTeleop(Node):
    def __init__(self):
        super().__init__('xreal_head_teleop')

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/stretch/cmd_vel', 10)
        self.joint_cmd_pub = self.create_publisher(JointState, '/joint_pose_cmd', 10)

        # UDP socket for OpenTrack data
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 4242))
        self.sock.settimeout(0.1)

        # Control parameters
        self.yaw_deadzone = 5.0       # degrees — ignore small head movements
        self.pitch_deadzone = 5.0
        self.max_angular_vel = 0.5    # rad/s for base rotation
        self.max_head_tilt = 0.5      # rad for head tilt joint

        # Reference orientation (set on first frame or recenter)
        self.ref_yaw = None
        self.ref_pitch = None

        # Timer to read UDP and publish commands at 30Hz
        self.timer = self.create_timer(1.0 / 30.0, self.update)

        self.get_logger().info("XReal Head Teleop started. Move your head to control the robot.")
        self.get_logger().info("Press Ctrl+C to stop.")

    def update(self):
        try:
            data, _ = self.sock.recvfrom(256)
        except socket.timeout:
            return

        if len(data) < 48:
            return

        x, y, z, yaw, pitch, roll = struct.unpack('<6d', data[:48])

        # Set reference on first frame
        if self.ref_yaw is None:
            self.ref_yaw = yaw
            self.ref_pitch = pitch
            self.get_logger().info(f"Reference set: yaw={yaw:.1f}° pitch={pitch:.1f}°")
            return

        # Relative to reference
        rel_yaw = yaw - self.ref_yaw
        rel_pitch = pitch - self.ref_pitch

        # --- Base rotation from yaw ---
        twist = Twist()
        if abs(rel_yaw) > self.yaw_deadzone:
            # Normalize: map head yaw to angular velocity
            # Negative yaw = turn left, positive = turn right
            normalized = max(-1.0, min(1.0, rel_yaw / 45.0))
            twist.angular.z = -normalized * self.max_angular_vel
        self.cmd_vel_pub.publish(twist)

        # --- Head tilt from pitch ---
        if abs(rel_pitch) > self.pitch_deadzone:
            joint_msg = JointState()
            joint_msg.name = ['joint_head_tilt']
            # Map pitch to head tilt range (roughly -0.5 to 0.2 rad)
            normalized_pitch = max(-1.0, min(1.0, rel_pitch / 30.0))
            tilt_value = -normalized_pitch * self.max_head_tilt
            joint_msg.position = [tilt_value]
            self.joint_cmd_pub.publish(joint_msg)

    def destroy_node(self):
        # Stop the robot on shutdown
        twist = Twist()
        self.cmd_vel_pub.publish(twist)
        self.sock.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = XRealHeadTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

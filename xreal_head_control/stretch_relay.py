#!/usr/bin/env python3
"""
Runs ON THE STRETCH ROBOT.
Listens for head pose commands over a simple TCP socket from your PC,
and drives the Stretch head pan/tilt using move_to_pose.

Usage (on Stretch):
    python3 stretch_relay.py
"""

import socket
import json
import threading
import hello_helpers.hello_misc as hm

HOST = "0.0.0.0"
PORT = 9090


class StretchRelay(hm.HelloNode):
    def __init__(self):
        hm.HelloNode.__init__(self)
        self.latest_cmd = None
        self.lock = threading.Lock()

    def tcp_server(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(1)
        print(f"Waiting for connection on port {PORT}...")

        while True:
            conn, addr = srv.accept()
            print(f"Connected: {addr}")
            buf = b""
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    buf += data
                    while b"\n" in buf:
                        line, buf = buf.split(b"\n", 1)
                        try:
                            cmd = json.loads(line)
                            with self.lock:
                                self.latest_cmd = cmd
                        except json.JSONDecodeError:
                            pass
            except Exception as e:
                print(f"Connection error: {e}")
            print("Client disconnected, waiting for reconnect...")

    def command_loop(self):
        import time
        while True:
            cmd = None
            with self.lock:
                if self.latest_cmd:
                    cmd = self.latest_cmd
                    self.latest_cmd = None

            if cmd:
                try:
                    pose = {}
                    if "pan" in cmd:
                        pose["joint_head_pan"] = cmd["pan"]
                    if "tilt" in cmd:
                        pose["joint_head_tilt"] = cmd["tilt"]
                    if pose:
                        self.move_to_pose(pose, blocking=False)
                except Exception as e:
                    print(f"Move error: {e}")

            time.sleep(0.05)  # 20Hz

    def main(self):
        hm.HelloNode.main(self, 'xreal_relay', 'xreal_relay',
                          wait_for_first_pointcloud=False)
        print("Stretch relay ready!")
        print(f"Listening on TCP port {PORT}")

        t = threading.Thread(target=self.tcp_server, daemon=True)
        t.start()

        self.command_loop()


if __name__ == "__main__":
    node = StretchRelay()
    node.main()

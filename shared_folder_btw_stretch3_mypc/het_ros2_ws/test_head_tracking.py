#!/usr/bin/env python3
"""Test script to read XReal One Pro head tracking via XRLinuxDriver OpenTrack UDP."""

import struct
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 4242))

print("Listening for XReal head tracking data on port 4242...")
print("Move your head to see yaw/pitch/roll values.\n")

while True:
    data, addr = sock.recvfrom(256)
    if len(data) >= 48:
        x, y, z, yaw, pitch, roll = struct.unpack('<6d', data[:48])
        frame = 0
        if len(data) >= 52:
            frame = struct.unpack('<I', data[48:52])[0]
        print(f"\rframe={frame:6d}  yaw={yaw:7.2f}°  pitch={pitch:7.2f}°  roll={roll:7.2f}°", end="", flush=True)

#!/usr/bin/env python3
"""Minimal WebSocket server that streams Xreal One Pro head tracking to a browser."""

import asyncio
import json
import threading
import websockets
from src.imu_reader_fixed import IMUReaderFixed
from src.head_tracker import HeadTracker

latest = {"pitch": 0, "yaw": 0, "roll": 0, "rate": 0, "calibrating": True, "cal_progress": 0}
tracker = HeadTracker()
tracker.pitch_scale = 1.0
tracker.yaw_scale = 1.0
tracker.roll_scale = 1.0

commands = []  # thread-safe command queue

def imu_callback(imu_data, msg_count, rate):
    # Process commands from websocket clients
    while commands:
        cmd = commands.pop(0)
        if cmd == "recalibrate":
            tracker.reset_calibration()
            latest["calibrating"] = True
            print("Recalibrating... keep glasses still")
        elif cmd == "zero":
            tracker.zero_view()
            print("View zeroed")

    if not tracker.is_calibrated:
        tracker.calibrate_gyroscope(imu_data)
        latest["cal_progress"] = round(tracker.get_calibration_progress())
        if tracker.is_calibrated:
            latest["calibrating"] = False
            print("Calibrated!")
        return
    tracker.update(imu_data)
    o = tracker.get_relative_orientation()
    latest["pitch"] = round(o["pitch"], 1)
    latest["yaw"] = round(o["yaw"], 1)
    latest["roll"] = round(o["roll"], 1)
    latest["rate"] = round(rate)

def imu_thread():
    with IMUReaderFixed(callback=imu_callback) as reader:
        reader.run()

async def handler(ws):
    async for msg in ws:
        data = json.loads(msg)
        if data.get("cmd") in ("recalibrate", "zero"):
            commands.append(data["cmd"])

async def sender(ws):
    while True:
        await ws.send(json.dumps(latest))
        await asyncio.sleep(0.033)  # ~30fps

async def duplex_handler(ws):
    await asyncio.gather(sender(ws), handler(ws))

async def main():
    t = threading.Thread(target=imu_thread, daemon=True)
    t.start()
    print("WebSocket on ws://localhost:8765")
    print("Open imu_viz.html in your browser")
    async with websockets.serve(duplex_handler, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

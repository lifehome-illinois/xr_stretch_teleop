# Xreal One Pro — Direct IMU Access for Robot Control

Two approaches to get raw head tracking data (pitch, yaw, roll) from the Xreal One Pro glasses.

**Ready-to-run Stretch bridge:** `~/lab/life_home/xreal_head_control/start.sh`

---

## Approach 1: Python (Recommended for Stretch/ROS) — SETUP COMPLETE

**Repo:** https://github.com/SamiMitwalli/One-Pro-IMU-Retriever-Demo

### Prerequisites
- Python 3.7+
- Xreal One Pro connected via USB-C
- Enable ethernet in glasses developer menu
- Glasses must be reachable at `169.254.2.1`

### Install

```bash
git clone https://github.com/SamiMitwalli/One-Pro-IMU-Retriever-Demo.git
cd One-Pro-IMU-Retriever-Demo
pip install pygame PyOpenGL PyOpenGL_accelerate numpy
```

### Run

```bash
# Console mode (best for piping to ROS)
python console_head_tracking.py

# 3D visualization (for testing)
python head_tracking_3d.py

# Or use the launcher
python launcher.py
```

### How It Works
1. Connects to glasses via TCP at `169.254.2.1:52998`
2. Decodes binary IMU protocol
3. Calibrates gyroscope (500 samples at startup — keep glasses still)
4. Fuses sensors with complementary filter (96% gyro, 4% accel)
5. Outputs pitch, yaw, roll in degrees

### Output Axes

| Axis       | Movement              |
|------------|-----------------------|
| Pitch (X)  | Look up/down          |
| Yaw (Y)    | Look left/right       |
| Roll (Z)   | Tilt head sideways    |

### Controls

| Key       | Action                                  |
|-----------|-----------------------------------------|
| T         | Set current orientation as forward      |
| R         | Recalibrate gyroscope                   |
| Q / ESC   | Quit                                    |
| +/= (3D)  | Increase sensitivity                   |
| - (3D)    | Decrease sensitivity                    |

### Tuning Responsiveness

Edit `HeadTracker.__init__()`:

```python
self.pitch_scale = 3.0     # up/down
self.yaw_scale = 60.0      # left/right
self.roll_scale = 1.0      # tilt
```

### Performance
- Sensor update rate: ~1000Hz
- Display refresh: 60Hz (3D), 10Hz (console)
- End-to-end latency: <10ms
- Calibration duration: ~0.5s

### Bridging to Stretch ROS (Example)

```python
import rospy
from geometry_msgs.msg import Twist
from head_tracker import HeadTracker

tracker = HeadTracker()
pub = rospy.Publisher('/stretch/cmd_vel', Twist, queue_size=1)

while not rospy.is_shutdown():
    pitch, yaw, roll = tracker.get_orientation()

    cmd = Twist()
    cmd.angular.z = yaw * scale_factor    # head left/right -> rotate base
    cmd.linear.x = pitch * scale_factor   # head up/down -> drive forward/back
    pub.publish(cmd)
```

### Troubleshooting
- Verify `169.254.2.1` is reachable (ping it)
- Enable ethernet in glasses developer menu
- Keep glasses stationary on flat surface during calibration
- Press R to recalibrate if tracking drifts

---

## Approach 2: Android Native (one-xr Library)

**Repo:** https://github.com/Skarian/one-xr

Best if you want an Android phone as the bridge between glasses and robot.

### Prerequisites
- Android device
- ADB installed
- Xreal One Pro connected via USB-C to Android device

### Install

```bash
git clone https://github.com/Skarian/one-xr.git
cd one-xr
./gradlew :onexr:testDebugUnitTest :onexr:lintDebug :app:assembleDebug :app:lintDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n io.onexr.demo/.HomeActivity
```

### Core API — `io.onexr.OneXrClient`

4 observable streams:

| Stream        | Data                              |
|---------------|-----------------------------------|
| sessionState  | Connection/lifecycle status       |
| sensorData    | Raw IMU + magnetometer vectors    |
| poseData      | Processed orientation in degrees  |
| biasState     | Calibration state                 |

### Pose Modes
- `RAW_IMU` — unfiltered orientation
- `SMOOTH_IMU` — filtered relative orientation (better for robot control)

Toggle with `setPoseDataMode(...)`.

### Workflow
1. Set glasses display mode to **Follow** (disable stabilization)
2. Call `start()` — keep glasses still during calibration
3. Call **Zero View** when facing your neutral forward direction
4. Select `SMOOTH_IMU` mode for robot control
5. Call `recalibrate()` if drift occurs

### Networking Note
Uses Android's `Network.socketFactory` for link-local routing. Binary framing with magic bytes + big-endian length headers.

### Documentation
Full integration guide in `docs/android-library.md` inside the repo, covering lifecycle management, permissions, control/config APIs, and troubleshooting.

---

## Head Gesture → Robot Action Mapping Ideas

| Head Gesture     | Robot Action                         |
|------------------|--------------------------------------|
| Look left/right  | Pan head camera or rotate base       |
| Look up/down     | Tilt head camera or move arm up/down |
| Nod              | Confirm / execute action             |
| Tilt head        | Switch control mode                  |

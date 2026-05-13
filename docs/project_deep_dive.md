# LIFE Home — XREAL-Controlled Stretch 3
## A Deep-Dive Reference for Presentation Preparation

> A complete, NotebookLM-ready reference for the `life_home` project: a
> head-tracking teleoperation system that lets a person wearing **XREAL One Pro**
> AR glasses remotely drive a **Hello Robot Stretch 3** mobile manipulator —
> using only head movements, with no hand input and no voice required.

---

## 1. Project Mission & Accessibility Framing

### 1.1 The core idea
This project turns a pair of consumer AR glasses (XREAL One Pro) into a
**hands-free, voice-free body interface** for controlling a real-world robot
assistant (Hello Robot Stretch 3) inside a home environment ("LIFE Home").

The user does not type, click, speak, or move their hands. They simply
**move their head**, and the robot:

- pans and tilts its camera/head to follow their gaze, so they can "see through
  the robot's eyes",
- drives forward, backward, and turns based on head pitch and yaw,
- (in the planned roadmap) navigates to gazed-at locations and grasps
  gazed-at objects on confirmation from a sip-and-puff switch.

### 1.2 Who this is for
The system is explicitly designed as an assistive technology for people who
cannot use their hands or voice in conventional ways:

- Individuals with high-level spinal cord injury (e.g. C1–C4 tetraplegia)
- People with advanced ALS or other progressive motor neuron diseases
- Users with severe cerebral palsy or locked-in syndrome
- Anyone who has retained reliable head movement but lost reliable hand control
  and/or speech

For these users, conventional teleop interfaces (keyboards, joysticks,
touchscreens, voice assistants) are unusable or unreliable. **Residual head
motion**, however, is one of the last motor capabilities to be lost — making it
a uniquely robust input channel for a robot assistant.

### 1.3 Why XREAL + Stretch 3
- **XREAL One Pro** glasses contain a high-rate (~1 kHz) IMU and stream raw
  inertial data over a USB-C ethernet link. They are commodity, lightweight,
  socially-acceptable hardware that doubles as a wearable display for camera
  feeds from the robot.
- **Hello Robot Stretch 3** is a research-grade mobile manipulator with a
  pannable/tiltable head camera, an arm, a gripper, and a differential-drive
  base — all controllable from ROS 2 (Humble). It is purpose-built for
  in-home assistive tasks.
- Both pieces of hardware are open enough to be wired together directly, with
  no proprietary middleware, so the entire pipeline can be reproduced and
  extended by other research groups.

### 1.4 Mission statement
> Enable a person with no usable hand or voice control to operate a mobile
> robot assistant in their home — to fetch objects, navigate to other rooms,
> and look around the environment — using only the natural movement of their
> head, complemented by a single binary switch (sip-and-puff) for confirmation
> actions.

---

## 2. System Architecture (High Level)

### 2.1 Three machines, three roles

```
┌──────────────────────┐    USB-C     ┌──────────────────────┐  Wi-Fi/LAN  ┌──────────────────────┐
│   XREAL One Pro      │ ───────────► │   USER'S PC          │ ──────────► │   Stretch 3 Robot    │
│   AR glasses         │  (link-local │   (Linux + Python)   │  (TCP 9090) │   (Ubuntu + ROS 2)   │
│   IMU @ ~1000 Hz     │   ethernet   │                      │             │                      │
│                      │   169.254.   │   • IMU reader       │             │   • stretch_relay.py │
│   Worn on the user's │   2.1:52998) │   • Head tracker     │             │   • stretch_driver   │
│   head               │              │   • Mode/key handler │             │   • web_video_server │
└──────────────────────┘              │   • TCP client       │             │   • dual cameras     │
                                      └──────────────────────┘             └──────────────────────┘
                                              ▲                                       │
                                              │             MJPEG video               │
                                              └───────────────────────────────────────┘
                                                    (browser ↔ port 8080)
```

The user wears the glasses, sits in front of (or away from) the PC, and the PC
acts as the **brain that interprets head motion and forwards commands to the
robot**. The robot streams its dual camera feeds back, which the user views
either on the PC monitor or directly inside the AR glasses display.

### 2.2 Why a relay PC instead of running on-robot?
1. The XREAL glasses currently expose their IMU only over a **link-local USB-C
   ethernet** at `169.254.2.1`. This connection is point-to-point — the
   glasses can only be addressed by the machine they're plugged into.
2. The Stretch 3 has limited compute and runs ROS 2 in a constrained Python
   environment (Anaconda must be deactivated for `rclpy` to import cleanly).
   Doing IMU decoding and sensor fusion on the robot would compete with
   real-time motor control.
3. Splitting compute lets the PC do **per-user calibration, sensor fusion,
   and UI/visualization** while the robot does only **pure motor execution**.

### 2.3 Two implemented control architectures
The repo contains two parallel implementations of the head→robot pipeline,
representing two different paths the project explored:

| # | Path | IMU access | Wire format | Robot side |
|---|------|------------|-------------|------------|
| **A** | **Direct TCP IMU** *(primary, currently active)* | Custom Python TCP client → glasses' raw sensor port `52998` | Direct binary IMU frames decoded in Python (`imu_reader_fixed.py`) | `stretch_relay.py` listens on TCP 9090, calls `move_to_pose` via `hello_helpers` |
| **B** | **XRLinuxDriver + OpenTrack** *(alternative, in `shared_folder_btw_stretch3_mypc/`)* | Open-source `XRLinuxDriver` (Wheaney) reads glasses, broadcasts OpenTrack UDP packets to `127.0.0.1:4242` | OpenTrack 6-double UDP format `<6d>` | ROS 2 node `xreal_head_teleop.py` publishes `Twist` and `JointState` |

Path A sidesteps the `XRLinuxDriver` entirely and talks to the glasses
directly — useful because XREAL One/One Pro support in `XRLinuxDriver` requires
specific firmware and the disable-stabilizer workaround. Path B fits more
naturally into a ROS 2 ecosystem.

---

## 3. Hardware Components

### 3.1 XREAL One Pro AR glasses
- 6-DoF IMU streaming at ~999–1000 Hz over the USB-C ethernet interface
- Reachable at **`169.254.2.1`** when "ethernet" is enabled in the developer menu
- Sensor data port: **`52998`** (TCP)
- Worn on the user's head; doubles as a transparent display for the robot's
  camera feeds (via the user's preferred display mode)
- **Important constraint**: stabilization / anchor features in the glasses
  must be disabled, or the IMU output will drift relative to the world

### 3.2 Hello Robot Stretch 3
- IP on the project's LAN: **`172.22.243.8`** (referenced throughout the code)
- Head joint limits used by this project (radians):
  - `HEAD_PAN_MIN = -3.9`, `HEAD_PAN_MAX = 1.5`
  - `HEAD_TILT_MIN = -1.53`, `HEAD_TILT_MAX = 0.79`
- Cameras: Intel RealSense **D435** (head) + **D405** (gripper); arducam at
  `/dev/video6` is also wired up via `v4l2_camera`
- ROS 2 distribution: **Humble**
- Action server: `/stretch_controller/follow_joint_trajectory`
  (the relay's action-server name is configurable; `26march_todo.md` records
  one early debugging session where it had to be discovered with
  `ros2 action list`)

### 3.3 User's PC
- Linux (the project specifies Ubuntu 22.04 / ROS 2 Humble)
- Connected to glasses by **USB-C** (link-local ethernet) and to the robot
  over **Wi-Fi/LAN**
- Used as the bridge; runs the Python head-control app

### 3.4 Planned hardware (future / roadmap)
The progress tracker (`data/progress_tracker.csv`) lays out an extended setup
with extra accessibility hardware:
- **Sip-and-puff (SNP) switch** — provides a binary "click" signal for the
  user, wired into an **Xbox Adaptive Controller** and paired over Bluetooth.
- **Earbuds** for confirmation tones, error alerts, task status announcements.
- **Quest 3 (originally explored)** — earlier weeks of the plan considered
  Quest 3 for hand-tracking baseline (OPEN TEACH) before the project pivoted
  to XREAL for a true head-only interface.

---

## 4. Repository Structure (Annotated)

```
life_home/
├── README.md                       # Top-level project & reproduction guide
├── .gitmodules                     # XRLinuxDriver pinned as a submodule
├── .gitignore                      # Blocks *.pem, *.key, .env*, secrets/
│
├── docs/
│   ├── rendered/                   # Polished PDFs (committed)
│   │   ├── Project Proposal - Full.pdf
│   │   ├── Project Proposal - Short.pdf
│   │   ├── GazeBot Proposal.pdf
│   │   ├── Stretch Robot GitHub Survey.pdf
│   │   └── XREAL-Stretch System Architecture (Flowcharts).pdf
│   ├── references/                 # Third-party / reference material
│   │   ├── GazeBot - Original.pdf
│   │   ├── Hello Robot Stretch Research Guide.docx
│   │   ├── 26march_todo.md         # First debugging session log
│   │   └── xreal_one_pro_imu_access.md  # Two-approach IMU integration guide
│   └── (sources/ exists locally for LaTeX/HTML inputs but is gitignored)
│
├── scripts/                        # Helper scripts
│   ├── create_stretch_doc.py       # Generates the Stretch research guide
│   └── generate_github_report.py   # Generates the GitHub survey PDF
│
├── data/
│   └── progress_tracker.csv        # 8-week milestone plan (the project roadmap)
│
├── shared_folder_btw_stretch3_mypc/
│   └── het_ros2_ws/                # Local mirror (SFTP) of the robot's
│                                   # ~/het_ros2_ws workspace:
│       ├── xreal_head_teleop.py    # ROS 2 node (Path B: OpenTrack-based)
│       ├── test_head_tracking.py   # Standalone OpenTrack listener (port 4242)
│       └── dual_camera_view.html   # Browser viewer for D435 + D405 streams
│
├── XRLinuxDriver/                  # Submodule: wheaney/XRLinuxDriver
│                                   # Open-source Linux driver for many AR
│                                   # glasses (XREAL, VITURE, Rokid, RayNeo).
│                                   # Provides OpenTrack-style UDP output.
│
└── xreal_head_control/             # The head-control app (Path A: primary)
    ├── stretch_head_control.py     # Main bridge — runs on the PC
    ├── stretch_relay.py            # Action receiver — runs on the robot
    ├── imu_server.py               # WebSocket bridge for the browser viz
    ├── imu_viz.html                # 3D cube head-tracking viz
    ├── console_head_tracking.py    # Console-mode demo (pre-Stretch)
    ├── head_tracking_3d.py         # OpenGL 3D demo (pre-Stretch)
    ├── launcher.py                 # Menu-based demo launcher
    ├── start.sh                    # One-shot script: ping glasses, start bridge
    ├── HOW_TO_USE.txt              # Plain-English operator guide
    ├── README.md                   # Demo-app README (by Daniel Sami Mitwalli)
    ├── requirements.txt            # numpy, pygame, PyOpenGL
    ├── knowledge_transfer/         # One-pager + reproduction guide PDFs
    └── src/
        ├── imu_data.py             # @dataclass IMUData (gx,gy,gz,ax,ay,az)
        ├── imu_reader.py           # Original reader (does NOT work on One Pro)
        ├── imu_reader_fixed.py     # Het Patel's fixed reader (header-to-header)
        ├── head_tracker.py         # Sensor fusion (complementary filter)
        ├── keyboard_handler.py     # Cross-thread key reader
        └── display_manager.py      # Console UI helpers
```

### 4.1 Submodule status
- **`XRLinuxDriver/`** is a real git submodule pointing at
  `https://github.com/wheaney/XRLinuxDriver.git`.
- **`xreal_head_control/`** is *currently a separate clone* of
  `https://github.com/het915/stretch_gazebot.git`, gitignored at the umbrella
  level until the local uncommitted changes are pushed; the README documents
  the conversion procedure.

---

## 5. The IMU Pipeline (Path A — Primary)

This is the most technically distinctive part of the project: getting IMU
data out of the XREAL One Pro **without** the official SDK.

### 5.1 The wire-level protocol
The glasses emit a binary stream over TCP. A custom message-framing scheme is
used, discovered by reverse-engineering:

```
HEADER     = 0x28 36 00 00 00 80    # 6-byte boundary marker
SENSOR_MSG = 0x00 40 1f 00 00 40    # 6-byte sensor-message tag
IMU_START  = 26                     # offset where IMU data begins
                                    # (header:6 + session:8 + invariant:2 + static:10)
```

Each message is roughly 134 bytes. The reader (`imu_reader_fixed.py`) splits
the incoming stream **header-to-header** and within each message:

1. Locates the `SENSOR_MSG` tag.
2. Slices the IMU section from `IMU_START` to the sensor tag.
3. Skips 8 bytes of flags/counter (when the section is long enough).
4. Reads **6 little-endian floats**:
   - `gx, gy, gz` — gyroscope rates, **converted from rad/s to deg/s**.
   - `ax, ay, az` — accelerometer values; note the axis swap on read:
     `ax=values[5], ay=values[4], az=values[3]`. This empirically matches the
     glasses' physical orientation when worn.

### 5.2 The IMUData type
```python
@dataclass
class IMUData:
    gx: float  # Gyroscope X (pitch rate, deg/s)
    gy: float  # Gyroscope Y (yaw rate,   deg/s)
    gz: float  # Gyroscope Z (roll rate,  deg/s)
    ax: float  # Accelerometer X
    ay: float  # Accelerometer Y
    az: float  # Accelerometer Z
```

### 5.3 Bias calibration
A pure gyroscope integration would drift dramatically over time because of
**bias** — a small constant offset in each gyro axis. The tracker eliminates
this by averaging the first **500 samples** (~0.5 s at 1 kHz) while the
glasses lie still:

```python
self.gyro_bias_x = mean(samples.gx)   # ditto for y, z
self.is_calibrated = True
```

Bias is later subtracted on every update:
`gyro_x = imu_data.gx - self.gyro_bias_x`.

### 5.4 Sensor fusion (complementary filter)
- **Gyro integration** is short-term accurate but drifts.
- **Accelerometer** can recover absolute pitch and roll relative to gravity
  but is noisy/unstable short-term, and **provides no information about yaw**.

The tracker fuses them with a complementary filter, weighted **96% gyro,
4% accelerometer**:

```python
alpha = 0.96
self.pitch = alpha * pitch_gyro + (1 - alpha) * pitch_accel
self.roll  = alpha * roll_gyro  + (1 - alpha) * roll_accel
```

Yaw cannot be corrected by the accelerometer, so a special **decay rule**
prevents long-term drift while the user holds their head still:

```python
if abs(gyro_y) < self.yaw_deadzone:   # 0.3 deg/s
    self.yaw = yaw_gyro * self.yaw_decay   # 0.98 every step
else:
    self.yaw = yaw_gyro
```

### 5.5 Zero-view (T key)
The user's "neutral forward" pose is captured on demand:

```python
def zero_view(self):
    self.zero_pitch = self.pitch
    self.zero_yaw   = self.yaw
    self.zero_roll  = self.roll
```

`get_relative_orientation()` then returns `(pitch - zero_pitch, yaw - zero_yaw,
roll - zero_roll)`, wrapped to ±180°.

### 5.6 Performance characteristics
- IMU rate: ~999 Hz
- Display refresh: 60 Hz (3D viz), 10 Hz (console)
- End-to-end latency (glasses → screen): <10 ms
- Calibration: ~0.5 s (500 samples)

---

## 6. The PC Bridge (`stretch_head_control.py`)

This is the heart of Path A. It runs on the user's PC, instantiates the IMU
reader and head tracker, opens a TCP socket to the robot, and translates head
orientation into robot motion at **20 Hz** (`COMMAND_INTERVAL = 0.05 s`).

### 6.1 Two operating modes
A single key press toggles between modes:

| Mode | What head motion controls | Activation |
|------|---------------------------|------------|
| **LOOK** *(default)* | Robot **head joints**: pan from yaw, tilt from pitch | Default at startup |
| **DRIVE** | Robot **base velocity**: forward/back from pitch, rotation from yaw | Press **M**, then **hold SPACE** to actually move |

### 6.2 LOOK mode — head pan/tilt mapping

```python
HEAD_PAN_SCALE  = 0.025   # head-degrees → joint radians
HEAD_TILT_SCALE = 0.015

pan_rad  = -yaw   * HEAD_PAN_SCALE
tilt_rad = -pitch * HEAD_TILT_SCALE
```

The negative signs invert axes so that "look right" pans the robot's head
right, "look down" tilts the camera down — i.e. the robot's head mirrors the
user's head intuitively. Values are clamped to `HEAD_PAN_*` / `HEAD_TILT_*`
limits before being JSON-encoded and sent.

### 6.3 DRIVE mode — base velocity mapping
DRIVE mode uses **dead-band-with-linear-ramp** velocity mapping, the same
shape used in many wheelchair joysticks:

```python
def map_angle_to_velocity(angle_deg, deadzone, max_angle, max_vel):
    if abs(angle_deg) < deadzone:           # no motion within ±5°
        return 0.0
    sign = 1.0 if angle_deg > 0 else -1.0
    scaled = (abs(angle_deg) - deadzone) / (max_angle - deadzone)
    return sign * min(1.0, max(0.0, scaled)) * max_vel
```

with these tuning constants:
```python
BASE_LINEAR_MAX  = 0.3   # m/s
BASE_ANGULAR_MAX = 0.5   # rad/s
BASE_DEADZONE    = 5.0   # deg
BASE_MAX_ANGLE   = 30.0  # deg → full speed
SPACE_TIMEOUT    = 0.2   # s
```

The **SPACE-must-be-held** behavior is implemented by tracking
`last_space_time`; the user has to keep generating space-key events (most
terminals auto-repeat held keys) for the robot to move. Releasing the key
times out within 200 ms and the robot stops.

This serves a critical safety role: the robot **cannot drive on head
movement alone**. The user must explicitly assert intent to move via a
secondary input, which in the planned roadmap will be replaced by the SNP
switch instead of SPACE.

### 6.4 Wire format to the robot
Every command is a single line of JSON, newline-terminated:

```
{"pan": 0.12, "tilt": -0.05}\n          # LOOK mode
{"linear": 0.20, "angular": -0.30}\n    # DRIVE mode
{"linear": 0.0,  "angular": 0.0}\n      # explicit stop
```

A 5-second TCP timeout is set on connect; rate-limiting (`COMMAND_INTERVAL`)
prevents the command stream from saturating the link.

### 6.5 Keyboard controls
Implemented in raw cbreak mode (`tty.setcbreak`) so single keypresses are
captured without ENTER:

| Key | Action |
|-----|--------|
| **T** | Zero view (set current head pose as neutral) |
| **R** | Recalibrate gyroscope (must keep glasses still) |
| **L** | Lock / unlock — pauses sending commands without quitting |
| **M** | Toggle LOOK ↔ DRIVE; auto-stops on transition |
| **SPACE (hold)** | DRIVE-mode movement enable |
| **Q** | Quit; sends a final stop command |

Locking has a special interaction: if the user is in DRIVE and locks,
`send_stop()` is called immediately (bypassing rate limiting) so the robot
halts before the lock takes effect.

---

## 7. The Robot Side (`stretch_relay.py`)

Runs on the Stretch 3 itself. A small ROS 2 node built on
`hello_helpers.hello_misc.HelloNode`:

- Listens on `0.0.0.0:9090` for newline-delimited JSON commands.
- A background thread (`tcp_server`) accumulates lines and stores the
  most recent command in `self.latest_cmd` under a lock.
- A foreground loop (`command_loop`) polls at 20 Hz and, for any new command,
  builds a pose dict like:
  ```python
  pose["joint_head_pan"]  = cmd["pan"]
  pose["joint_head_tilt"] = cmd["tilt"]
  self.move_to_pose(pose, blocking=False)
  ```
- `blocking=False` is essential: the next pose can supersede the current one
  before motion finishes, giving smooth tracking instead of stuttery moves.

The relay is intentionally **stateless** beyond holding the latest command,
which makes it robust to packet bursts, brief disconnects, and operator
re-starts.

---

## 8. The Browser Visualizer (`imu_server.py` + `imu_viz.html`)

A diagnostic tool, not on the control path. Useful for:
- showing a stakeholder what the head-tracking system "sees",
- verifying axes/calibration before plugging into the robot,
- debugging drift or mis-mapping issues without needing the robot powered up.

**Server side (`imu_server.py`)**
- Reuses the same `IMUReaderFixed` + `HeadTracker` stack.
- Streams the latest pitch/yaw/roll over a WebSocket on `ws://localhost:8765`
  at ~30 Hz.
- Accepts JSON commands from the browser (`{"cmd":"recalibrate"}` or
  `{"cmd":"zero"}`).

**Browser side (`imu_viz.html`)**
- Pure HTML/CSS/JS, no build step.
- Renders a 3D CSS cube with three axis arrows (red pitch, green yaw, cyan
  roll).
- Shows numeric pitch/yaw/roll, sample rate, and a calibration progress
  overlay.
- Buttons / keys: **T** = zero view, **R** = recalibrate.

This is what the operator typically opens first to sanity-check the glasses.

---

## 9. Path B — XRLinuxDriver + OpenTrack (Alternative)

The folder `shared_folder_btw_stretch3_mypc/het_ros2_ws/` (mounted from the
robot via SFTP) contains an alternative implementation that uses the
open-source `XRLinuxDriver` instead of speaking to the glasses directly.

### 9.1 How it differs
- `XRLinuxDriver` runs as a system service on the PC, decodes glasses IMU
  data, and re-broadcasts it as **OpenTrack-formatted UDP** packets to
  `127.0.0.1:4242`.
- OpenTrack format = 6 little-endian doubles: `(x, y, z, yaw, pitch, roll)`,
  i.e. 48 bytes; an optional 4-byte frame counter follows.
- A ROS 2 node (`xreal_head_teleop.py`) binds that UDP port and publishes:
  - `geometry_msgs/Twist` to `/stretch/cmd_vel` for base rotation,
  - `sensor_msgs/JointState` to `/joint_pose_cmd` for head tilt.

### 9.2 Why both exist
Path B is closer to "stock" ROS 2 but inherits XRLinuxDriver's quirks for
XREAL One/One Pro support (firmware requirements, the stabilization-disable
caveat). Path A bypasses the driver and is the path that has been getting
recent active development (head + base modes, 3D viz, browser tools).

### 9.3 The ROS 2 mapping (Path B)
```python
self.yaw_deadzone   = 5.0    # deg
self.pitch_deadzone = 5.0    # deg
self.max_angular_vel = 0.5   # rad/s
self.max_head_tilt   = 0.5   # rad

# yaw → angular velocity (negated to match user expectation)
twist.angular.z = -clamp(rel_yaw / 45.0, -1, 1) * max_angular_vel

# pitch → head tilt joint position
joint_msg.position = [-clamp(rel_pitch / 30.0, -1, 1) * max_head_tilt]
```

The reference orientation (`ref_yaw`, `ref_pitch`) is auto-set from the first
incoming UDP packet, so the user just has to look forward when the node
starts.

---

## 10. Camera Streaming (Robot → User)

`shared_folder_btw_stretch3_mypc/het_ros2_ws/dual_camera_view.html` is a
zero-dependency HTML page that displays both Stretch cameras side-by-side:

- **Head camera (D435)** at
  `http://172.22.243.8:8080/stream?topic=/camera/color/image_raw&type=mjpeg&quality=80`
  — rotated 90° in CSS to match the way the camera is mounted.
- **Gripper camera (D405)** at
  `http://172.22.243.8:8080/stream?topic=/gripper_camera/color/image_rect_raw&type=mjpeg&quality=80`

Both feeds are served by `web_video_server` on the robot. The page auto-retries
on stream errors (the JS reloads the `src` after 3 s).

The intended workflow is to launch the page **fullscreen in Chromium kiosk
mode** so the user sees only the camera feeds:

```bash
google-chrome --kiosk file:///.../dual_camera_view.html
```

In the future, this is what gets piped into the AR glasses display so the
user perceives the world from the robot's vantage.

---

## 11. Required Robot-Side Launches

Per `xreal_head_control/HOW_TO_USE.txt`, the operator opens two SSH sessions
on the Stretch (each with `conda deactivate` first, because `rclpy` does not
coexist with the robot's Anaconda):

```bash
# Session 1 — core driver
ssh hello-robot@172.22.243.8
conda deactivate
stretch_free_robot_process.py        # optional: release stuck motors
stretch_robot_home.py                # optional: home all joints
ros2 launch stretch_core stretch_driver.launch.py

# Session 2 — the relay this project depends on
ssh hello-robot@172.22.243.8
conda deactivate
python3 ~/het_ros2_ws/stretch_relay.py
# wait for: "Waiting for connection on port 9090..."
```

If the trajectory action server name differs from
`/stretch_controller/follow_joint_trajectory`, discover it with
`ros2 action list` and update line 33 of `~/het_ros2_ws/stretch_relay.py`.

For the optional dual-camera view, a single launch file bundles everything
needed:

```bash
conda deactivate
ros2 launch ~/het_ros2_ws/stretch_dual_camera.launch.py
```

which internally runs:

```bash
ros2 launch stretch_core stretch_driver.launch.py mode:=navigation
ros2 launch stretch_core d435i_high_resolution.launch.py     # head camera
ros2 launch stretch_core d405_basic.launch.py                # gripper camera
ros2 run v4l2_camera v4l2_camera_node \
    --ros-args -p video_device:="/dev/video6" -r image_raw:=/arducam/image_raw
ros2 run web_video_server web_video_server
```

---

## 12. Setup & Reproduction (Quick Path)

### 12.1 Glasses
1. Plug XREAL One Pro into the PC via USB-C.
2. In the glasses' **developer menu**, enable ethernet.
3. Verify on the PC:
   ```bash
   ping 169.254.2.1
   ```

### 12.2 PC
```bash
git clone --recurse-submodules <this-repo-url> life_home
cd life_home
git clone https://github.com/het915/stretch_gazebot.git xreal_head_control   # until submoduled

cd xreal_head_control
pip install -r requirements.txt

# Quick visualization to verify glasses
python3 imu_server.py
xdg-open imu_viz.html
```

### 12.3 Robot
Two SSH sessions; password kept locally, never committed.
```bash
# Session 1
ssh hello-robot@172.22.243.8
conda deactivate
ros2 launch stretch_core stretch_driver.launch.py

# Session 2
ssh hello-robot@172.22.243.8
conda deactivate
python3 ~/het_ros2_ws/stretch_relay.py
```

### 12.4 Run the bridge (on the PC)
```bash
python3 ~/xreal_head_control/stretch_head_control.py
# wait for "Calibration complete!", then press T to zero view
# (optional) open dual_camera_view.html for the robot's camera feeds
```

### 12.5 SFTP mount (development only — so PC edits land on the robot)
```bash
sshfs hello-robot@172.22.243.8:/home/hello-robot/het_ros2_ws \
      ~/lab/life_home/shared_folder_btw_stretch3_mypc/het_ros2_ws
```

`.vscode/sftp.json` is committed with a placeholder password; the real
password is set locally and never committed.

---

## 13. Project Roadmap (from `data/progress_tracker.csv`)

The 8-week milestone plan baked into the repo lays out the path from
"basic teleop" to "full assistive robot system":

| Week | Milestone | Representative tasks |
|------|-----------|----------------------|
| **1** | Stretch controllable via Quest 3 hand tracking (OPEN TEACH baseline) | Configure Stretch 3 with `stretch_body` / `stretch_ai`, set up Unity + Meta XR SDK, run OPEN TEACH |
| **2** | User sees through robot's eyes and controls camera view with head movements | Build Unity Quest 3 head-pose reader (90 Hz OpenXR), stream Stretch head camera over WebRTC, map head rotation to head pan/tilt |
| **3** | Full hands-free input chain — head-gaze + sip/puff across all modes | Pair SNP via Xbox Adaptive Controller, distinguish soft/hard sip/puff, implement 4 control modes (Look, Navigate, Manipulate, Menu), MR HUD |
| **4** | Look at a point in the LIFE Home, sip, robot autonomously navigates there | Integrate Nav2, convert head-gaze ray + depth to 3D world coordinate, show MR path preview |
| **5** | Look at object, sip twice, robot picks it up and brings it to the wheelchair | Integrate `stretch_ai` YOLO/SAM, head-gaze object highlighting, autonomous grasp planning (FUNMAP), "bring to me" |
| **6** | Complete system with preset ADL tasks, audio feedback, and reliable safety stops | Preset task library (Fetch, Open Door, Clear Path, Get Water), gaze menu, audio confirmations, hard-puff emergency stop |
| **7** | Quantitative evaluation data | 5 tasks × 3 trials, baseline against `stretch_web_teleop`, NASA-TLX, SUS, fix critical usability issues |
| **8** | Demo + report + paper outline | Demo video, technical report, GitHub release, lab presentation, ASSETS 2026 / HRI 2027 paper outline |

The current code matches **late Week 2 / early Week 3** state — head-controlled
LOOK/DRIVE works; sip/puff, gaze-targeted Nav2, and autonomous grasping are
the next major arcs.

### 13.1 The four planned control modes
1. **Look mode** — head pose drives camera pan/tilt; user looks around.
2. **Navigate mode** — head-gaze ray hits a depth-image point; sip sets a
   Nav2 goal; robot autonomously drives there.
3. **Manipulate mode** — head-gaze ray highlights detected objects; double
   sip triggers an autonomous grasp pipeline (`stretch_ai` / FUNMAP).
4. **Menu mode** — head-gaze cursor over an MR menu of preset ADL tasks
   ("Fetch object", "Open door", "Clear path", "Get water"), confirmed
   by sip.

A **hard puff** is reserved as the always-on emergency stop.

### 13.2 Evaluation plan (Week 7)
- Quantitative: success rate, completion time, input count.
- Subjective: NASA-TLX (cognitive workload) and SUS (system usability).
- Comparison baseline: `stretch_web_teleop` (keyboard/mouse).
- Target venues: **ASSETS 2026** (accessibility) or **HRI 2027** (human-robot
  interaction).

---

## 14. Naming, Branding, Provenance

- **"GazeBot"** — an early code name for the project; surviving in
  `docs/references/GazeBot - Original.pdf` and
  `docs/rendered/GazeBot Proposal.pdf`. The project later evolved beyond pure
  gaze input.
- **"LIFE Home"** — the physical home-lab environment where the robot is
  evaluated.
- **`het_ros2_ws`** — Het Patel's ROS 2 workspace on the robot.
- **`stretch_gazebot`** — the GitHub repo backing `xreal_head_control/`.
- **`life_home`** — this umbrella repo.

### 14.1 Credits / upstream
- IMU reader, head tracker, console & 3D demos: originally **Daniel Sami
  Mitwalli** (`One-Pro-IMU-Retriever-Demo`, MIT-style license file present).
- Fixed reader (`imu_reader_fixed.py`) adapted to use header-to-header
  framing for the 134-byte messages: **Het Patel** (this project).
- `XRLinuxDriver`: **Wayne Heaney** (`wheaney/XRLinuxDriver`), Apache /
  reverse-engineered work credited to Tobias Frisch and Matt Smith.
- Stretch 3, ROS 2 stack, `hello_helpers`, `stretch_core`, `stretch_ai`:
  **Hello Robot Inc.**

---

## 15. Limitations, Known Issues, Failure Modes

- **Yaw drift**: there is no absolute reference for yaw. The decay rule
  helps, but long teleop sessions still need an occasional T-press to
  re-zero. The roadmap considers magnetometer fusion or visual yaw lock
  via the head camera.
- **Calibration sensitivity**: gyro bias is captured at startup. If the
  glasses are picked up during the half-second calibration window, the
  bias is wrong and tracking drifts. The R key recovers from this.
- **Stabilization conflict**: XREAL's display stabilization features must
  be disabled, or they pre-process the IMU and the values become a
  filtered/lagged version of head motion rather than raw motion.
- **Connection robustness**: the TCP socket between PC and robot is
  unencrypted and has no auth. Fine on a private LAN; not appropriate
  beyond it.
- **Trajectory action server name** can vary by Stretch firmware/launch
  config; the relay's action-server reference may need updating per setup
  (`ros2 action list` to discover).
- **Conda vs. ROS**: `rclpy` will import the wrong `_rclpy` shared lib if
  Anaconda is active. Always `conda deactivate` before any ROS 2 Python
  on the robot.
- **Single binary input gate** (SPACE in DRIVE mode) is a placeholder for
  the SNP switch. The robot **must not move on head input alone** — this
  is a hard safety rule baked into the design.

---

## 16. Security Notes

- `.gitignore` blocks `*.pem`, `*.key`, `.env*`, and any `secrets/` directory.
- `.vscode/sftp.json` is committed with a placeholder password; the real
  password is set locally and never committed.
- An earlier version of `xreal_head_control/HOW_TO_USE.txt` contained a
  plaintext SSH password alongside the robot's IP. The current file replaces
  every password occurrence with the placeholder `# password: ask lab admin`;
  the upstream `het915/stretch_gazebot` history still contains the leaked
  string and must be scrubbed before that repo is made public. This document
  deliberately omits the password.
- Submodule conversion of `xreal_head_control` is gated on first scrubbing
  the password and pushing the cleaned commit history.

---

## 17. Suggested Presentation Narrative

A possible flow when presenting from this document in NotebookLM-driven
slides:

1. **Hook** — millions of people retain head movement after losing hand and
   voice control. They deserve agency in their own home. Existing assistive
   robots demand inputs they no longer have.
2. **The vision** — an AR-glasses + mobile-manipulator pairing where
   *head movement is the entire interface*, paired with one binary
   confirmation switch (sip-and-puff) for safety and intent.
3. **Why it's possible now** — XREAL One Pro exposes a high-rate IMU; Hello
   Robot Stretch 3 is open and ROS 2-native; the missing piece is the
   bridge — and that's what this project builds.
4. **Live demo** — operator wears glasses; calibrates in 0.5 s; presses T;
   robot's head mirrors theirs; presses M, holds SPACE, drives across the
   room; toggles back to LOOK to look around.
5. **System tour** — the three-machine architecture, the 6-byte message
   framing trick that unlocks IMU access, the 96/4 complementary filter,
   the LOOK/DRIVE toggle.
6. **Roadmap** — the 8-week plan: today we have head-driven LOOK/DRIVE;
   next milestones add gaze-set Nav2 goals, autonomous grasping, ADL menu,
   hard-puff e-stop; finally a structured user study.
7. **Why it matters** — the same pipeline that drives this single robot
   generalizes to any mobile manipulator. The interface is **the user's
   own body**, no learning curve, no specialized hardware in their mouth or
   eye, just glasses they could plausibly wear in public.

---

## 18. One-Sentence Summary

> The repository wires a 1-kHz IMU stream from off-the-shelf XREAL AR
> glasses through a sensor-fusion pipeline on a Linux PC into a ROS 2 relay
> on a Hello Robot Stretch 3, giving a person who can move only their head
> the ability to look around and drive a mobile robot assistant in their
> home — the foundation for a hands-free, voice-free assistive robotics
> stack aimed at users with paralysis.

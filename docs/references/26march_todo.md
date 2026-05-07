# 26 March 2026 — Progress & Next Steps

## What Works
- [x] Xreal One Pro detected on USB, reachable at `169.254.2.1`
- [x] IMU streaming at ~999Hz via fixed reader (`src/imu_reader_fixed.py`)
- [x] Head tracking (pitch/yaw/roll) working
- [x] Web viz working (`imu_server.py` + `imu_viz.html`)
- [x] Axis mapping fixed: roll = left/right turns, -pitch = up/down when worn

## What's Blocked
- [ ] **Stretch relay can't find trajectory action server**
  - `FollowJointTrajectory` at `/stretch_controller/follow_joint_trajectory` not available
  - Driver is running but action server isn't listed
  - **NEXT TIME: run `ros2 action list` on Stretch to find the correct action server name**
  - Then update `stretch_relay.py` line 33 with the correct action server path

## Next Session TODO
1. SSH into Stretch, run `ros2 action list` to find available action servers
2. Update `stretch_relay.py` with correct action server name
3. Test relay: `conda deactivate && python3 ~/het_ros2_ws/stretch_relay.py`
4. Test bridge on PC: `python3 ~/lab/life_home/xreal_head_control/stretch_head_control.py`
5. Put on glasses, wait for calibration, press T to zero view
6. Test head pan (look left/right) and tilt (look up/down)

## Tuning (if needed)
Edit `~/lab/life_home/xreal_head_control/stretch_head_control.py`:
- `HEAD_PAN_SCALE = 0.025` — increase for faster pan response
- `HEAD_TILT_SCALE = 0.015` — increase for faster tilt response

## Files
- PC bridge: `~/lab/life_home/xreal_head_control/stretch_head_control.py`
- Robot relay: `~/het_ros2_ws/stretch_relay.py` (via SSHFS mount)
- IMU viz: `~/lab/life_home/xreal_head_control/imu_viz.html` + `imu_server.py`
- Fixed IMU reader: `~/lab/life_home/xreal_head_control/src/imu_reader_fixed.py`
- Docs: `~/lab/life_home/useful_docs/xreal_one_pro_imu_access.md`

# life_home

Workspace for the **XREAL-Controlled Stretch 3** project — head-tracking
teleoperation of a Hello Robot Stretch 3 using XREAL One Pro AR glasses.

This repository is the umbrella that glues the moving parts together:
the open-source XR Linux driver, the head-control application, the
ROS 2 workspace synced to the robot, and the project documentation.

---

## Repository layout

```
life_home/
├── docs/
│   ├── rendered/         Polished, titled PDFs ready to read
│   └── references/       Third-party / no-source reference material
│   (docs/sources/ exists locally with .tex/.html/.md inputs;
│    it is gitignored — see "Regenerating documents" below)
├── scripts/              Helper scripts that generate documentation
├── data/                 Datasets / trackers (e.g. progress_tracker.csv)
├── shared_folder_btw_stretch3_mypc/
│                         Local mirror of the robot's ~/het_ros2_ws
│                         (synced over SFTP — see .vscode/sftp.json)
├── XRLinuxDriver/        Submodule: third-party wheaney/XRLinuxDriver
└── xreal_head_control/   The head-control app (sources, build script
                          for the knowledge_transfer PDFs, and HOW_TO_USE)
```

---

## Cloning (for collaborators)

```bash
git clone --recurse-submodules <this-repo-url> life_home
cd life_home
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

---

## Reproducing the project

1. Build the XR Linux driver (`XRLinuxDriver/`) — see its own
   `README.md`. Provides AR-glasses IMU access on Linux.
2. Run the head-control app from `xreal_head_control/` — follow its
   `HOW_TO_USE.txt`.
3. Mount the robot's ROS 2 workspace at
   `shared_folder_btw_stretch3_mypc/het_ros2_ws/` over SFTP using
   `.vscode/sftp.json` (set the password locally; it is **not**
   stored in this repo).

---

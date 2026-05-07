#!/bin/bash
# Quick start: Xreal One Pro → Stretch 3 Head Control
#
# Prerequisites:
#   1. Xreal One Pro connected via USB-C, ethernet enabled in developer menu
#   2. Stretch driver running: ros2 launch stretch_core stretch_driver.launch.py
#
# Usage: ./start.sh

set -e

# Source ROS2
if [ -f /opt/ros/humble/setup.bash ]; then
    source /opt/ros/humble/setup.bash
fi

# Source Stretch workspace if available
if [ -f ~/ament_ws/install/setup.bash ]; then
    source ~/ament_ws/install/setup.bash
elif [ -f ~/catkin_ws/install/setup.bash ]; then
    source ~/catkin_ws/install/setup.bash
fi

# Check glasses connectivity
echo "Checking Xreal One Pro connectivity..."
if ping -c 1 -W 2 169.254.2.1 > /dev/null 2>&1; then
    echo "  Xreal One Pro reachable at 169.254.2.1"
else
    echo "  WARNING: Cannot reach 169.254.2.1"
    echo "  Make sure:"
    echo "    - Glasses are connected via USB-C"
    echo "    - Ethernet is enabled in glasses developer menu"
    echo ""
    read -p "  Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the bridge
cd "$(dirname "$0")"
python3 stretch_head_control.py

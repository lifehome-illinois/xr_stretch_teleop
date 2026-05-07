#!/usr/bin/env python3
"""
Generate comprehensive PDF report on Hello Robot Stretch GitHub repositories
with GazeBot project recommendations.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, KeepTogether
)
from reportlab.lib import colors
import datetime

# ============================================================
# SETUP
# ============================================================
output_path = "/home/het/lab/life_home/github_stretch_robot.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch,
    leftMargin=0.75*inch,
    rightMargin=0.75*inch,
)

styles = getSampleStyleSheet()

# Custom styles
UIUC_BLUE = HexColor('#13294B')
UIUC_ORANGE = HexColor('#E84727')
DARK_BLUE = HexColor('#006699')
LIGHT_GRAY = HexColor('#F5F5F5')
MED_GRAY = HexColor('#E0E0E0')

styles.add(ParagraphStyle(
    'CoverTitle', parent=styles['Title'],
    fontSize=28, leading=34, textColor=UIUC_BLUE,
    alignment=TA_CENTER, spaceAfter=12
))
styles.add(ParagraphStyle(
    'CoverSubtitle', parent=styles['Normal'],
    fontSize=14, leading=18, textColor=HexColor('#666666'),
    alignment=TA_CENTER, spaceAfter=6
))
styles.add(ParagraphStyle(
    'SectionHead', parent=styles['Heading1'],
    fontSize=18, leading=22, textColor=UIUC_BLUE,
    spaceBefore=20, spaceAfter=10, borderWidth=1,
    borderColor=UIUC_BLUE, borderPadding=4
))
styles.add(ParagraphStyle(
    'SubHead', parent=styles['Heading2'],
    fontSize=14, leading=17, textColor=DARK_BLUE,
    spaceBefore=14, spaceAfter=6
))
styles.add(ParagraphStyle(
    'SubSubHead', parent=styles['Heading3'],
    fontSize=12, leading=15, textColor=HexColor('#333333'),
    spaceBefore=10, spaceAfter=4
))
styles.add(ParagraphStyle(
    'BodyText2', parent=styles['Normal'],
    fontSize=10, leading=14, alignment=TA_JUSTIFY,
    spaceAfter=6
))
styles.add(ParagraphStyle(
    'BulletText', parent=styles['Normal'],
    fontSize=10, leading=13, leftIndent=20, spaceAfter=2
))
styles.add(ParagraphStyle(
    'CodeStyle', parent=styles['Normal'],
    fontName='Courier', fontSize=8, leading=10,
    leftIndent=20, spaceAfter=4, backColor=LIGHT_GRAY
))
styles.add(ParagraphStyle(
    'TableHeader', parent=styles['Normal'],
    fontSize=9, leading=11, textColor=white, fontName='Helvetica-Bold'
))
styles.add(ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontSize=8.5, leading=11
))
styles.add(ParagraphStyle(
    'SmallNote', parent=styles['Normal'],
    fontSize=8, leading=10, textColor=HexColor('#888888')
))
styles.add(ParagraphStyle(
    'RecommendTitle', parent=styles['Heading2'],
    fontSize=14, leading=17, textColor=UIUC_ORANGE,
    spaceBefore=14, spaceAfter=6
))

story = []

def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    hdr_style = styles['TableHeader']
    cell_style = styles['TableCell']
    data = [[Paragraph(h, hdr_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), cell_style) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), UIUC_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.5, MED_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t

def bullet(text):
    return Paragraph(f"&bull; {text}", styles['BulletText'])

def body(text):
    return Paragraph(text, styles['BodyText2'])

def section(text):
    return Paragraph(text, styles['SectionHead'])

def subsec(text):
    return Paragraph(text, styles['SubHead'])

def subsubsec(text):
    return Paragraph(text, styles['SubSubHead'])

def sp(h=6):
    return Spacer(1, h)

# ============================================================
# COVER PAGE
# ============================================================
story.append(Spacer(1, 2*inch))
story.append(Paragraph("Hello Robot Stretch", styles['CoverTitle']))
story.append(Paragraph("Comprehensive GitHub Repository<br/>& Open-Source Code Research Report", styles['CoverTitle']))
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph("With GazeBot Project Recommendations", styles['CoverSubtitle']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(f"Prepared: {datetime.date.today().strftime('%B %d, %Y')}", styles['CoverSubtitle']))
story.append(Paragraph("McKechnie Family LIFE Home | University of Illinois Urbana-Champaign", styles['CoverSubtitle']))
story.append(PageBreak())

# ============================================================
# TABLE OF CONTENTS
# ============================================================
story.append(section("Table of Contents"))
toc = [
    "1. Executive Summary",
    "2. GitHub Organization Overview",
    "3. stretch_ai -- AI & Intelligent Behaviors",
    "4. stretch_ros2 -- ROS 2 Packages",
    "5. stretch_ros -- ROS 1 Legacy Packages",
    "6. stretch_body -- Python Hardware SDK",
    "7. stretch_firmware -- Arduino Firmware",
    "8. stretch_tutorials -- Educational Resources",
    "9. stretch_dex_teleop -- Dexterous Teleoperation",
    "10. stretch_tool_share -- Community Tools & Accessories",
    "11. stretch_community -- Community Portal & Projects",
    "12. Additional Repositories (Install, Factory, Diagnostics, Hardware Guides)",
    "13. Academic Publications & Research Papers",
    "14. GazeBot Project: Repository Recommendations & Usage Guide",
    "15. Sources & References",
]
for item in toc:
    story.append(Paragraph(item, styles['BodyText2']))
story.append(PageBreak())

# ============================================================
# 1. EXECUTIVE SUMMARY
# ============================================================
story.append(section("1. Executive Summary"))
story.append(body(
    "Hello Robot Inc. maintains an extensive open-source software ecosystem for the Stretch family of mobile manipulators, "
    "hosted on GitHub under the organization <b>github.com/hello-robot</b>. With <b>34+ repositories</b>, the ecosystem spans "
    "low-level hardware drivers, ROS 1/2 integration, AI-powered manipulation, simulation, teleoperation, tutorials, and "
    "community contributions. Nearly all code is released under permissive licenses (Apache 2.0, MIT, LGPL)."
))
story.append(sp())
story.append(body(
    "This report provides a comprehensive analysis of every major repository, including architecture, key modules, APIs, "
    "dependencies, and capabilities. It also catalogs 30+ peer-reviewed publications from ICRA, IROS, CoRL, HRI, NeurIPS, "
    "CVPR, and RSS that leverage the Stretch platform. A dedicated section maps these repositories to the GazeBot project's "
    "needs -- a head-gaze + sip-and-puff shared autonomy system being developed at the UIUC LIFE Home."
))
story.append(PageBreak())

# ============================================================
# 2. GITHUB ORGANIZATION OVERVIEW
# ============================================================
story.append(section("2. GitHub Organization Overview"))
story.append(body("The hello-robot GitHub organization (github.com/hello-robot) hosts 34+ repositories. The key repositories are:"))
story.append(sp())
story.append(make_table(
    ["Repository", "Description", "Stars", "License", "Language"],
    [
        ["stretch_ai", "AI behaviors, LLM agents, grasping, navigation", "219", "Apache 2.0", "Python"],
        ["stretch_ros2", "ROS 2 Humble packages (Nav2, MoveIt2, SLAM)", "111", "Apache 2.0", "Python"],
        ["stretch_ros", "ROS 1 Noetic packages (legacy)", "185", "Apache 2.0", "Python"],
        ["stretch_body", "Python SDK for hardware control", "--", "LGPLv3", "Python"],
        ["stretch_firmware", "Arduino firmware for custom PCBAs", "--", "GPLv3", "C++"],
        ["stretch_tutorials", "40+ tutorials (Python, ROS 2)", "15", "--", "Jupyter"],
        ["stretch_dex_teleop", "6-DOF dexterous teleoperation", "--", "--", "Python"],
        ["stretch_tool_share", "Community grippers, tools, CAD files", "34", "Apache 2.0", "Python"],
        ["stretch_community", "Community portal, papers, third-party repos", "13", "--", "Markdown"],
        ["stretch_install", "Installation and setup scripts", "--", "--", "Shell"],
        ["stretch_factory", "Factory calibration and debug tools", "--", "--", "Python"],
        ["stretch_diagnostics", "Diagnostic and health check tools", "--", "--", "Python"],
        ["stretch_hardware_guides", "Hardware documentation for all models", "--", "CC BY-NC-SA", "Markdown"],
        ["stretch_urdf", "URDF models and meshes", "--", "--", "URDF/Xacro"],
        ["stretch_pyfunmap", "Python FUNMAP nav+manipulation planner", "--", "--", "Python"],
        ["stretch_web_teleop", "Web-based remote teleoperation (WebRTC)", "--", "--", "JS/Python"],
        ["stretch_mujoco", "MuJoCo simulation stack", "--", "BSD 3-Clause", "Python"],
        ["stretch_isaacsim", "NVIDIA Isaac Sim integration", "--", "Apache 2.0", "Python"],
        ["stretch_forcesight", "Text-guided manipulation (ICRA 2024)", "--", "--", "Python"],
        ["stretch_visual_servoing", "Visual servoing via gripper camera", "--", "--", "Python"],
        ["stretch_docking", "Autonomous docking via visual servoing", "--", "--", "Python"],
    ],
    col_widths=[1.3*inch, 2.6*inch, 0.5*inch, 0.9*inch, 0.7*inch]
))
story.append(PageBreak())

# ============================================================
# 3. STRETCH_AI
# ============================================================
story.append(section("3. stretch_ai -- AI & Intelligent Behaviors"))
story.append(body(
    "<b>Repository:</b> github.com/hello-robot/stretch_ai | <b>Stars:</b> 219 | <b>Forks:</b> 47 | "
    "<b>License:</b> Apache 2.0 (+ MIT for Meta HomeRobot components)<br/>"
    "<b>Lead:</b> Chris Paxton, Senior Embodied AI Lead at Hello Robot (prev. NVIDIA Research, Meta FAIR)"
))
story.append(sp())
story.append(body(
    "Stretch AI is the flagship software framework for building intelligent robot behaviors on Stretch 3. "
    "It provides integrated tools for grasping, manipulation, 3D mapping, navigation, LLM-based task planning, "
    "speech processing, and embodied question answering."
))

story.append(subsec("3.1 Architecture"))
story.append(body(
    "<b>Distributed client-server design:</b> The robot runs a ROS 2 environment with a ZMQ-enabled server. "
    "A separate GPU workstation (connected via WiFi) runs compute-intensive AI models. Communication happens "
    "over a ZMQ network bridge."
))
story.append(sp())
story.append(make_table(
    ["Directory", "Purpose"],
    [
        ["src/stretch/agent/", "Robot agent orchestration, ZMQ client, manipulation operations, task FSMs"],
        ["src/stretch/app/", "22+ runnable applications (ai_pickup, grasp_object, mapping, chat, etc.)"],
        ["src/stretch/perception/", "Vision & object detection (OWLv2, SAMv2, YOLO)"],
        ["src/stretch/mapping/", "3D voxel mapping & DynaMem spatio-semantic memory"],
        ["src/stretch/motion/", "Motion planning (A*, RRT, RRT-Connect)"],
        ["src/stretch/llms/", "LLM clients (Qwen2.5, OpenAI GPT-4o, Gemma, Gemini)"],
        ["src/stretch/audio/", "Whisper speech-to-text, text-to-speech"],
        ["src/stretch/simulation/", "MuJoCo simulation integration"],
        ["src/stretch_ros2_bridge/", "ROS 2 to ZMQ bridge for AI workstation communication"],
    ],
    col_widths=[2*inch, 4.5*inch]
))

story.append(subsec("3.2 Core API -- RobotClient"))
story.append(Paragraph(
    "<font face='Courier' size='8'>"
    "from stretch.agent import RobotClient<br/>"
    "robot = RobotClient(robot_ip='192.168.1.15')<br/>"
    "robot.move_to_nav_posture()<br/>"
    "robot.move_base_to([0.5, 0, 0], relative=True)<br/>"
    "robot.move_to_manip_posture()<br/>"
    "robot.arm_to([0.1, 0.5, 0, 0, 0, 0])<br/>"
    "</font>",
    styles['CodeStyle']
))

story.append(subsec("3.3 AI Capabilities"))
story.append(make_table(
    ["Capability", "Details"],
    [
        ["Navigation & Mapping", "Frontier-based/value-based exploration, 3D voxel maps from RGB-D, A*/RRT planning, open-vocab object localization"],
        ["Manipulation", "Language-directed pick-and-place, visual servoing, AnyGrasp 6-DOF grasps, OWLv2+SAMv2 target selection"],
        ["Voice & Language", "OpenAI Whisper STT, TTS feedback, LLM command parsing (Qwen2.5/GPT-4o), multi-turn chat"],
        ["DynaMem", "Dynamic spatio-semantic memory, handles moving objects, 70% pick-and-drop success on non-stationary objects"],
        ["Learning from Demo", "ACT, VQ-BeT, Diffusion Policy architectures via HuggingFace LeRobot, ~50 episodes recommended"],
        ["Embodied QA", "Robot explores to answer questions, uses VLMs + Gemini for multimodal reasoning"],
        ["LLM Agent", "Finite state machines with operations: pickup(), explore(), place(), say(), wave(), find()"],
    ],
    col_widths=[1.5*inch, 5*inch]
))

story.append(subsec("3.4 Key Applications"))
story.append(make_table(
    ["Application", "Command", "Description"],
    [
        ["AI Pickup", "python -m stretch.app.ai_pickup --use_llm --use_voice", "Language-directed pick-and-place with voice"],
        ["Mapping", "python -m stretch.app.mapping --explore-iter 10", "Autonomous 3D environment mapping"],
        ["Grasp Object", "python -m stretch.app.grasp_object --target '...'", "Single object grasping by name"],
        ["DynaMem", "python -m stretch.app.run_dynamem", "Dynamic semantic memory system"],
        ["Voice Chat", "python -m stretch.app.chat --voice", "Conversational LLM agent"],
        ["Keyboard Teleop", "python -m stretch.app.keyboard_teleop", "WASD robot control"],
        ["Dex Teleop", "python -m stretch.app.dex_teleop.ros2_leader", "Demonstration data collection"],
        ["EQA", "python -m stretch.app.run_eqa", "Embodied question answering"],
    ],
    col_widths=[1.1*inch, 3.2*inch, 2.2*inch]
))

story.append(subsec("3.5 Dependencies"))
story.append(body(
    "<b>Hardware:</b> Stretch 3, Ubuntu 22.04 workstation with NVIDIA GPU (tested RTX 4090), dedicated WiFi AP.<br/>"
    "<b>Key Python:</b> torch>=2.6, ultralytics (YOLO), openai-clip, transformers>=4.50, openai>=1.88, "
    "pin (Pinocchio IK), rerun-sdk, librosa, PyAudio, openai-whisper, open3d, hydra-core.<br/>"
    "<b>Docker:</b> Available as hellorobotinc/stretch-ai_cuda-11.8:latest"
))
story.append(PageBreak())

# ============================================================
# 4. STRETCH_ROS2
# ============================================================
story.append(section("4. stretch_ros2 -- ROS 2 Packages"))
story.append(body(
    "<b>Repository:</b> github.com/hello-robot/stretch_ros2 | <b>Stars:</b> 111 | <b>Forks:</b> 65 | "
    "<b>Branch:</b> humble | <b>ROS 2:</b> Humble Hawksbill (Ubuntu 22.04)"
))

story.append(subsec("4.1 All Packages (11 total)"))
story.append(make_table(
    ["Package", "License", "Description"],
    [
        ["stretch_core", "Apache 2.0", "Core ROS 2 drivers, hardware interface via stretch_body SDK. Modes: position, navigation, trajectory, homing, stowing, runstopped"],
        ["stretch_description", "BSD 3-Clause", "URDF/xacro robot description files and STL meshes"],
        ["stretch_nav2", "Apache 2.0", "Nav2 navigation stack (SLAM via slam_toolbox, localization via AMCL, path planning)"],
        ["stretch_calibration", "GPLv3", "Generates calibrated URDF models unique to each physical robot"],
        ["stretch_deep_perception", "Apache 2.0", "Deep learning perception demos (face, object, body detection)"],
        ["stretch_demos", "Apache 2.0", "Autonomous manipulation demonstrations (hello_world, open_drawer, clean_surface, handover)"],
        ["stretch_funmap", "LGPLv3", "Fast Unified Navigation, Manipulation And Planning tools"],
        ["stretch_octomap", "Apache 2.0", "3D probabilistic mapping using octrees"],
        ["stretch_rtabmap", "Apache 2.0", "Real-Time Appearance-Based 3D Mapping and visual navigation"],
        ["stretch_simulation", "Apache 2.0", "MuJoCo-based simulation (not Gazebo), supports RoboCasa kitchen environments"],
        ["hello_helpers", "Apache 2.0", "Shared Python utilities (HelloNode class, move_to_pose, plane fitting)"],
    ],
    col_widths=[1.3*inch, 0.9*inch, 4.3*inch]
))

story.append(subsec("4.2 Key Nodes (stretch_core)"))
story.append(make_table(
    ["Node", "Description"],
    [
        ["stretch_driver.py", "Core node communicating with stretch_body. Modes: position, navigation, trajectory, homing, stowing, runstopped"],
        ["joint_trajectory_server.py", "Action server for MoveIt2 and other trajectory planners"],
        ["keyboard_teleop.py", "Keyboard control with integrated demo triggers"],
        ["detect_aruco_markers.py", "ArUco marker detection and pose estimation"],
        ["d435i_*.py", "Intel RealSense D435i 3D camera nodes (high/low resolution)"],
    ],
    col_widths=[2*inch, 4.5*inch]
))

story.append(subsec("4.3 Key Launch Files"))
story.append(make_table(
    ["Launch File", "Package", "Purpose"],
    [
        ["stretch_driver.launch.py", "stretch_core", "Main driver + robot_state_publisher + joint_state_publisher"],
        ["offline_mapping.launch.py", "stretch_nav2", "SLAM-based mapping with slam_toolbox"],
        ["navigation.launch.py", "stretch_nav2", "Autonomous navigation with Nav2 + AMCL"],
        ["visual_mapping.launch.py", "stretch_rtabmap", "3D RGBD-based environment mapping"],
        ["visual_navigation.launch.py", "stretch_rtabmap", "Visual navigation in pre-mapped spaces"],
        ["stretch_mujoco_driver.launch.py", "stretch_simulation", "MuJoCo simulation driver"],
        ["display.launch.py", "stretch_description", "Quick URDF visualization in RViz"],
    ],
    col_widths=[2.2*inch, 1.3*inch, 3*inch]
))

story.append(subsec("4.4 Nav2 Integration"))
story.append(body(
    "Uses <b>slam_toolbox</b> for SLAM mapping, <b>AMCL</b> for localization in pre-mapped environments, "
    "RPlidar LaserScan for obstacle avoidance. Maps saved as .pgm + .yaml at ${HELLO_FLEET_PATH}/maps/. "
    "Recovery behaviors include 180-degree spin or backup. Supports programmatic goals via <b>Nav2 Simple Commander API</b>."
))

story.append(subsec("4.5 MoveIt2 Integration"))
story.append(body(
    "Three planning groups: <b>stretch_arm</b>, <b>stretch_gripper</b>, <b>stretch_head</b>. "
    "Mobile base adds 2 additional DOF for whole-body planning (arm + base simultaneously). "
    "Uses joint_trajectory_server.py action server for execution."
))

story.append(subsec("4.6 Key Topics & Services"))
story.append(make_table(
    ["Type", "Name", "Description"],
    [
        ["Topic", "/mode", "Current driver mode (15 Hz)"],
        ["Topic", "/battery", "Battery state (voltage, current)"],
        ["Topic", "/is_homed", "Encoder homing status"],
        ["Service", "/home_the_robot", "30-second homing sequence"],
        ["Service", "/stow_the_robot", "Stow arm into base footprint"],
        ["Service", "/stop_the_robot", "Immediate stop"],
        ["Service", "/runstop", "Programmatic emergency stop (SetBool)"],
        ["Service", "/funmap/trigger_*", "FUNMAP actions (head_scan, drive_to_scan, reach_until_contact, etc.)"],
    ],
    col_widths=[0.7*inch, 2.3*inch, 3.5*inch]
))
story.append(PageBreak())

# ============================================================
# 5. STRETCH_ROS (Legacy)
# ============================================================
story.append(section("5. stretch_ros -- ROS 1 Legacy Packages"))
story.append(body(
    "<b>Repository:</b> github.com/hello-robot/stretch_ros | <b>Stars:</b> 185 | <b>Forks:</b> 95 | "
    "<b>ROS:</b> Noetic (EOL May 2025) | <b>12 packages</b>"
))
story.append(sp())
story.append(make_table(
    ["Aspect", "stretch_ros (ROS 1)", "stretch_ros2 (ROS 2)"],
    [
        ["Navigation", "move_base + gmapping", "Nav2 + slam_toolbox"],
        ["Manipulation", "Not integrated", "MoveIt2 (whole-body planning)"],
        ["Simulation", "Gazebo Classic (ros_control)", "MuJoCo (+ RoboCasa kitchens)"],
        ["Driver Modes", "position, navigation", "position, navigation, trajectory (new)"],
        ["Dashboard", "GUI dashboard included", "No dashboard"],
        ["Build System", "catkin", "colcon"],
        ["Communication", "TCPROS", "DDS (with QoS profiles)"],
        ["Status", "Mature but EOL", "Active development, LTS until May 2027"],
    ],
    col_widths=[1.3*inch, 2.6*inch, 2.6*inch]
))
story.append(body(
    "<b>Note:</b> For new projects (including GazeBot), stretch_ros2 is strongly recommended. "
    "stretch_ros is documented here for completeness and backward compatibility reference."
))
story.append(PageBreak())

# ============================================================
# 6. STRETCH_BODY
# ============================================================
story.append(section("6. stretch_body -- Python Hardware SDK"))
story.append(body(
    "<b>Repository:</b> github.com/hello-robot/stretch_body | <b>License:</b> LGPLv3<br/>"
    "<b>Packages:</b> hello-robot-stretch-body (core) + hello-robot-stretch-body-tools (CLI utilities)"
))

story.append(subsec("6.1 Class Hierarchy"))
story.append(Paragraph(
    "<font face='Courier' size='8'>"
    "Device (base class)<br/>"
    "&nbsp;&nbsp;+-- Robot (top-level orchestrator)<br/>"
    "&nbsp;&nbsp;+-- Stepper (stepper motor interface)<br/>"
    "&nbsp;&nbsp;+-- PrismaticJoint -> Arm, Lift<br/>"
    "&nbsp;&nbsp;+-- Base (differential drive)<br/>"
    "&nbsp;&nbsp;+-- Pimu (power/IMU board)<br/>"
    "&nbsp;&nbsp;+-- Wacc (wrist accelerometer)<br/>"
    "&nbsp;&nbsp;+-- DynamixelXChain -> Head, EndOfArm<br/>"
    "&nbsp;&nbsp;+-- DynamixelHelloXL430 -> WristYaw, WristPitch, WristRoll, StretchGripper<br/>"
    "</font>",
    styles['CodeStyle']
))

story.append(subsec("6.2 Key API Patterns"))
story.append(make_table(
    ["Joint Type", "Command Methods", "Execution Model"],
    [
        ["Arm, Lift, Base (steppers)", "move_to(), move_by(), set_velocity()", "Queued: push_command() then wait_command()"],
        ["Head, Wrist, Gripper (Dynamixels)", "move_to('joint', val), set_velocity(v)", "Immediate execution"],
    ],
    col_widths=[1.8*inch, 2.2*inch, 2.5*inch]
))
story.append(sp())
story.append(Paragraph(
    "<font face='Courier' size='8'>"
    "import stretch_body.robot<br/>"
    "robot = stretch_body.robot.Robot()<br/>"
    "robot.startup()<br/>"
    "robot.arm.move_to(0.3)  # meters<br/>"
    "robot.lift.move_to(0.5)  # meters<br/>"
    "robot.push_command()<br/>"
    "robot.wait_command()<br/>"
    "robot.head.move_to('head_pan', 0.5)  # radians, immediate<br/>"
    "robot.end_of_arm.move_to('stretch_gripper', 50)  # percent open<br/>"
    "</font>",
    styles['CodeStyle']
))

story.append(subsec("6.3 Sensor Access"))
story.append(make_table(
    ["Sensor", "Access Path", "Data"],
    [
        ["Joint Encoders", "robot.arm/lift/base.status['pos']", "Position (m/rad), velocity, force/effort"],
        ["Base IMU (BNO085)", "robot.pimu.status", "9-DOF: accel, gyro, magnetometer"],
        ["Base Odometry", "robot.base.status['x'/'y'/'theta']", "X, Y (meters), heading (radians)"],
        ["Cliff Sensors (4x IR)", "robot.pimu.status", "Floor drop-off detection"],
        ["Battery", "robot.pimu.status", "Voltage, current, charger state"],
        ["Wrist Accel (ADXL343)", "robot.wacc.status", "3-axis accel, tap/bump detection"],
        ["Wrist Analog/Digital I/O", "robot.wacc.status", "a0 (analog), d0-d3 (digital)"],
    ],
    col_widths=[1.5*inch, 2.3*inch, 2.7*inch]
))

story.append(subsec("6.4 Motion Control"))
story.append(body(
    "<b>Position control:</b> Absolute (move_to) and relative (move_by) for all joints. "
    "<b>Velocity control:</b> set_velocity() for continuous motion. "
    "<b>Trajectory following:</b> Cubic-spline interpolation with waypoints (time, position, velocity). "
    "<b>Guarded contact:</b> Current-sensing halts motion on effort threshold (protects against collisions). "
    "<b>Collision avoidance:</b> RobotCollision manager dynamically limits joint ranges at ~10 Hz. "
    "<b>Units:</b> SI throughout -- meters, radians, seconds, Newtons."
))

story.append(subsec("6.5 Command-Line Tools"))
story.append(make_table(
    ["Tool", "Purpose"],
    [
        ["stretch_robot_home.py", "Calibrate/home all joints after boot"],
        ["stretch_robot_stow.py", "Return arm/tool to safe position"],
        ["stretch_robot_system_check.py", "Scan all hardware, validate bus connections"],
        ["stretch_robot_keyboard_teleop.py", "Keyboard teleoperation"],
        ["stretch_xbox_controller_teleop.py", "Xbox gamepad teleoperation"],
        ["stretch_robot_jog.py", "Interactive jogging of all joints"],
        ["stretch_robot_battery_check.py", "Battery voltage/current status"],
        ["REx_firmware_updater.py", "Firmware update utility"],
    ],
    col_widths=[2.5*inch, 4*inch]
))
story.append(PageBreak())

# ============================================================
# 7. STRETCH_FIRMWARE
# ============================================================
story.append(section("7. stretch_firmware -- Arduino Firmware"))
story.append(body(
    "<b>Repository:</b> github.com/hello-robot/stretch_firmware | <b>License:</b> GPLv3<br/>"
    "<b>MCU:</b> Atmel SAMD21G18A-AUT (ARM Cortex-M0+, 32-bit, 48 MHz)"
))

story.append(subsec("7.1 Firmware Components"))
story.append(make_table(
    ["Component", "Files", "Purpose"],
    [
        ["hello_stepper", "30 files", "Stepper motor controller: closed-loop current control, trapezoidal trajectory generation, multi-motor sync, guarded contact"],
        ["hello_pimu", "27 files", "Power/IMU board: BNO085 IMU, cliff sensors, battery monitoring, runstop logic, sync pulse generation, buzzer/LED control"],
        ["hello_wacc", "11 files", "Wrist accelerometer: ADXL343 driver, tap/bump detection, analog/digital I/O"],
    ],
    col_widths=[1.3*inch, 0.7*inch, 4.5*inch]
))

story.append(subsec("7.2 Communication Protocol"))
story.append(body(
    "Uses <b>COBS</b> (Consistent Overhead Byte Stuffing) for zero-free packet framing over USB serial, "
    "with <b>CRC16</b> for data integrity. Custom RPC protocol with packed C structs. "
    "Protocol versions P0-P6 supported. Asyncio support for non-blocking stepper communication."
))

story.append(subsec("7.3 PIMU Safety Monitoring (100 Hz)"))
story.append(make_table(
    ["Monitor", "Sensor", "Threshold/Action"],
    [
        ["Voltage", "Battery ADC", "Low alert at 10.5V; runstop on critical low"],
        ["Current", "Current sensor / e-fuse", "Alert at 6A; overcurrent protection"],
        ["Tilt", "IMU accelerometer", "Tilt detection triggers runstop"],
        ["Cliff", "4x Sharp IR sensors", "Floor drop-off triggers runstop"],
        ["Watchdog", "Timer", "11ms timeout, automatic reset on hang"],
    ],
    col_widths=[1*inch, 1.5*inch, 4*inch]
))
story.append(PageBreak())

# ============================================================
# 8. STRETCH_TUTORIALS
# ============================================================
story.append(section("8. stretch_tutorials -- Educational Resources"))
story.append(body(
    "<b>Repository:</b> github.com/hello-robot/stretch_tutorials | <b>Stars:</b> 15 | 469 commits<br/>"
    "Organized into three progressive tracks with 40+ tutorials."
))

story.append(subsec("8.1 Tutorial Tracks"))
story.append(make_table(
    ["Track", "Focus", "Key Topics"],
    [
        ["Track A: Developing with Stretch", "Foundational", "CLI tools, networking, system startup, basics"],
        ["Track B: Python Tutorials", "stretch_body API", "Motion control, sensors (RealSense), audio, inverse kinematics, visual servoing"],
        ["Track C: ROS 2 Tutorials (40+)", "ROS 2 integration", "11 basics + 6 advanced + 12 examples (see below)"],
    ],
    col_widths=[2*inch, 1.2*inch, 3.3*inch]
))

story.append(subsec("8.2 ROS 2 Tutorial Topics"))
story.append(body(
    "<b>Basics (11):</b> Packages/Nodes, Simulation, Teleop, RViz, Joint Trajectory, HelloNode, Robot Driver, "
    "Twist Control, Sensors, Nav2 Stack, Deep Perception.<br/>"
    "<b>Advanced (6):</b> ArUco Detection, Offloading Computation, Race Conditions, Autonomy Demos, FUNMAP, Perception.<br/>"
    "<b>Examples (12):</b> Voice-to-Text, Voice Teleop, Laser Scan Filtering, ArUco Localization, Print Joint States, "
    "Store Effort, Tf2 Broadcaster/Listener, Image Capture, Collision Avoidance, Obstacle Avoider."
))
story.append(PageBreak())

# ============================================================
# 9. STRETCH_DEX_TELEOP
# ============================================================
story.append(section("9. stretch_dex_teleop -- Dexterous Teleoperation"))
story.append(body(
    "Enables 6-DOF dexterous teleoperation of Stretch 3 using modified kitchen tongs with ArUco visual markers "
    "tracked by a webcam. Translates hand motions into target poses + gripper commands at 15+ Hz."
))

story.append(subsec("9.1 Capabilities"))
story.append(bullet("6-DOF end-effector control: position via IK, orientation via wrist joints, grip via gripper"))
story.append(bullet("Single-arm and bimanual operation (two Stretch 3 robots simultaneously)"))
story.append(bullet("Slow mode (default, conservative) and Fast mode (maximum speed, reduced contact sensitivity)"))
story.append(bullet("Data collection platform for robot learning -- integrated with HuggingFace LeRobot"))
story.append(bullet("Multiprocessing: sensor acquisition decoupled from motor control via shared memory"))

story.append(subsec("9.2 Hardware Kit ($295)"))
story.append(body(
    "Logitech C930e webcam (1080p), LED ring light, adjustable stand/tripod, ArUco tongs, Stretch 3 with dex wrist. "
    "Bimanual setup requires two kits with distinct ArUco marker IDs."
))
story.append(PageBreak())

# ============================================================
# 10. STRETCH_TOOL_SHARE
# ============================================================
story.append(section("10. stretch_tool_share -- Community Tools & Accessories"))
story.append(body(
    "<b>Repository:</b> github.com/hello-robot/stretch_tool_share | <b>Stars:</b> 34 | <b>21 tools</b>"
))
story.append(sp())
story.append(make_table(
    ["Category", "Tools"],
    [
        ["Computing & Sensing", "NVIDIA Jetson Orin AGX mount, wrist USB board camera"],
        ["Dexterous Manipulation", "Dex Wrist (RE1/RE2 add-on), Dex Wrist Beta, ReactorX wrist"],
        ["Accessories", "Phone holder, dry erase holder, Swiffer mount, tray/cup holder, button pusher, puller, card holder, arm tray, swivel tablet mount, adapted spoon"],
        ["Infrastructure", "Docking station, teleop kit (2x fish-eye cameras), shoulder joint"],
        ["Reference Models", "Stretch 2 STEP, RE1 arm/head models"],
    ],
    col_widths=[1.5*inch, 5*inch]
))
story.append(body(
    "Design files include STL (3D printing), STEP (CAD), URDF+meshes (ROS), and Gazebo support. "
    "Robot components: CC BY-NC-SA 4.0. Tool accessories: Apache 2.0."
))
story.append(PageBreak())

# ============================================================
# 11. STRETCH_COMMUNITY
# ============================================================
story.append(section("11. stretch_community -- Community Portal"))
story.append(body("Curated portal of third-party projects, publications, simulations, and educational resources."))

story.append(subsec("11.1 Featured Community Projects"))
story.append(make_table(
    ["Organization", "Project", "Description"],
    [
        ["Meta AI + CMU", "Semantic Navigation", "Find object instances in unseen home environments"],
        ["UW HCR Lab", "stretch-web-app", "Enhanced web teleoperation interface (Prof. Maya Cakmak)"],
        ["Meta AI", "Fairo", "Unified robotics platform (led by Soumith Chintala)"],
        ["Avanade", "emtech-stretch-labs", "NextMind BCI, Azure IoT, DroneDeploy integration"],
        ["Johns Hopkins", "icl_stretch_ros", "Tool retrieval for hospital sterile processing"],
        ["UMass Lowell", "stretch_gui / stretch_uml", "Semi-autonomous teleoperation interfaces"],
    ],
    col_widths=[1.2*inch, 1.5*inch, 3.8*inch]
))

story.append(subsec("11.2 Simulation Environments"))
story.append(make_table(
    ["Source", "Platform", "Details"],
    [
        ["U. Washington", "Gazebo", "Improved indoor environment + object models"],
        ["Meta AI (Chris Paxton)", "Habitat2", "Training home assistant behaviors"],
        ["CMU (Prof. Erickson)", "OpenAI Gym", "assistive-gym -- assistive robotics tasks"],
        ["Cardiff University", "Gazebo Harmonic", "ROS 2 integration"],
    ],
    col_widths=[1.5*inch, 1.3*inch, 3.7*inch]
))
story.append(PageBreak())

# ============================================================
# 12. ADDITIONAL REPOSITORIES
# ============================================================
story.append(section("12. Additional Repositories"))

story.append(subsec("12.1 stretch_install"))
story.append(body(
    "<b>License:</b> GPLv3 | <b>Language:</b> Shell (96.1%), Python (3.9%)<br/>"
    "Automates software setup for Stretch robots across three installation paths:"
))
story.append(make_table(
    ["Script", "Purpose", "Runtime"],
    [
        ["stretch_new_robot_install.sh", "Full OS + software stack deployment on fresh robot", "20-30 min (wired)"],
        ["stretch_new_user_install.sh", "Provisions new Ubuntu user account with all Stretch packages", "~10 min"],
        ["stretch_update_ros_workspace.sh", "Creates/recompiles ROS1 catkin or ROS2 ament workspaces", "~5 min"],
    ],
    col_widths=[2.2*inch, 3*inch, 1.3*inch]
))
story.append(body(
    "<b>Supported Ubuntu versions:</b> 18.04 (Melodic), 20.04 (Noetic), 22.04 (Humble).<br/>"
    "<b>Requirements:</b> Wired USB keyboard/mouse (Bluetooth incompatible with BIOS), monitor, "
    "2 USB flash drives (one >8GB), Ethernet recommended. Robot model codes: 're1' (RE1), 're2' (Stretch 2), 'se3' (Stretch 3)."
))

story.append(subsec("12.2 stretch_factory"))
story.append(body(
    "<b>License:</b> Proprietary (U.S. Patent 11,230,000) | <b>Install:</b> pip install hello-robot-stretch-factory<br/>"
    "Low-level factory calibration and debug tools (all prefixed with <b>REx_</b>), intended for use under Hello Robot support guidance."
))
story.append(make_table(
    ["Category", "Tools"],
    [
        ["Base & IMU Calibration", "REx_base_calibrate_imu_collect/process, REx_base_calibrate_wheel_separation"],
        ["Dynamixel Management", "REx_dynamixel_id_scan/change/jog/reboot/set_baud, REx_hello_dynamixel_jog"],
        ["Stepper Operations", "REx_stepper_jog/gains/ctrl_tuning/calibration_run/type, flash-to-YAML and YAML-to-flash calibration export"],
        ["Sensor Calibration", "REx_calibrate_guarded_contact, REx_calibrate_range, REx_cliff_sensor_calibrate, REx_gripper_calibrate, REx_wacc_calibrate"],
        ["System & Firmware", "REx_firmware_updater, REx_discover_hello_devices, REx_usb_reset, REx_D435i_check"],
    ],
    col_widths=[1.5*inch, 5*inch]
))
story.append(body("Includes 18 documented factory update procedures (001-018) covering hardware modifications, servo swaps, and calibration sequences."))

story.append(subsec("12.3 stretch_diagnostics (ARCHIVED Feb 2026)"))
story.append(body(
    "<b>Status:</b> Archived -- superseded by stretch_system_check.py in stretch_body.<br/>"
    "<b>Install:</b> pip3 install hello-robot-stretch-diagnostics<br/>"
    "CLI tool <b>stretch_diagnostic_check.py</b> with test suite flags:"
))
story.append(make_table(
    ["Flag", "Tests", "Count"],
    [
        ["--simple", "Accessories, filesystem, firmware, params, PIMU, RealSense, RPLidar, software, steppers, udev, USB, wacc, wifi", "17"],
        ["--power", "Battery health, battery loading, charger", "3"],
        ["--realsense", "Cable integrity, frame rate", "2"],
        ["--stepper", "Calibration data match, power, runstop, sync", "4"],
        ["--dynamixel", "Zero position, hardware, efforts, range of motion", "4"],
        ["--ros", "Calibration, sourced distro, URDF", "3"],
        ["--cpu", "CPU usage and temperature", "1"],
        ["--arm / --lift", "Effort through range of motion", "1 each"],
    ],
    col_widths=[1*inch, 3.7*inch, 0.5*inch]
))

story.append(subsec("12.4 stretch_hardware_guides"))
story.append(body(
    "Hardware documentation for all Stretch models. Key documents: Safety Guide, Battery Maintenance Guide, "
    "Hardware Guide, and Dex Wrist Guide (per model). Published under CC BY-NC-SA."
))
story.append(make_table(
    ["Feature", "RE1", "RE2 / Stretch 2", "Stretch 3"],
    [
        ["Arm Material", "Carbon fiber", "Carbon fiber", "Aluminum"],
        ["Base IMU", "FXOS8700+FXAS21002", "Same", "BNO085 (9 DOF)"],
        ["Head Camera", "D435i", "D435i", "D435if + Arducam B0385 (140° FOV)"],
        ["Gripper Camera", "None", "None", "Intel RealSense D405"],
        ["Dex Wrist", "Optional add-on", "Optional add-on", "Built-in (3 DOF standard)"],
        ["Head Tilt Servo", "XL430-W250-T", "XL430-W250-T", "XC430-W240-T (upgraded)"],
        ["Lift Brake", "None", "None", "Yes (engages on power loss)"],
        ["Battery", "2x 12V AGM SLA, 18AH", "Same", "Same (2-5 hr runtime)"],
    ],
    col_widths=[1.3*inch, 1.5*inch, 1.5*inch, 2.2*inch]
))

story.append(subsec("12.5 Other Notable Repositories"))
story.append(make_table(
    ["Repository", "Description"],
    [
        ["stretch_urdf", "URDF models and meshes for all Stretch variants, source assets for stretch_description"],
        ["stretch_pyfunmap", "Python FUNMAP: combined navigation + manipulation using geometric models and computer vision"],
        ["stretch_web_teleop", "Remote web teleoperation via browser (ROS2, WebRTC, Nav2, TypeScript). Works locally or over internet."],
        ["stretch_mujoco", "MuJoCo simulation: position control (arm/head/gripper), velocity control (base), calibrated camera RGB+depth, 2D lidar. ROS2 compatible with Nav2/Web Teleop. BSD 3-Clause."],
        ["stretch_isaacsim", "NVIDIA Isaac Sim integration for Stretch (Apache 2.0)"],
        ["stretch_forcesight", "Pre-trained ForceSight model for text-guided manipulation with visual-force goals (ICRA 2024)"],
        ["stretch_visual_servoing", "Visual servoing using Stretch 3's gripper D405 camera"],
        ["stretch_docking", "Autonomous docking demo via visual servoing"],
        ["stretch_deep_perception_models", "Pre-trained deep learning models for perception (faces, objects, bodies)"],
        ["stretch_show_tablet", "Tablet interface for Stretch"],
        ["stretch_ctrl_dev", "Experimental controls research"],
        ["lerobot (fork)", "Hello Robot's fork of HuggingFace LeRobot for imitation learning (stretch-act branch)"],
        ["ros2_numpy", "Tools for converting ROS messages to/from numpy arrays (MIT)"],
    ],
    col_widths=[1.8*inch, 4.7*inch]
))
story.append(PageBreak())

# ============================================================
# 13. ACADEMIC PUBLICATIONS
# ============================================================
story.append(section("13. Academic Publications & Research Papers"))
story.append(body(
    "The Stretch platform has generated 30+ peer-reviewed publications at top venues. Below are the most significant."
))

story.append(subsec("13.1 Foundational Papers (Hello Robot Team)"))
story.append(make_table(
    ["Title", "Authors/Affiliation", "Venue", "Key Contribution"],
    [
        ["The Design of Stretch", "Kemp, Edsinger, Clever (Georgia Tech / Hello Robot)", "ICRA 2022", "Core design paper: 23 kg, &lt;$20K, 8 prototype iterations, home deployment evaluation"],
        ["ForceSight", "Collins, Houff, Tan, Kemp", "ICRA 2024", "Text-guided manipulation with visual-force goals, 81% success on 10 household tasks"],
        ["Robots for Humanity", "Ranganeni, Nguyen, Evans (UW/Hello Robot)", "HRI 2024", "In-home deployment with Henry Evans (quadriplegia), 3 one-week participatory sessions"],
        ["Immersive Participatory Design", "Olatunji, Nguyen, Cakmak, Kemp, Rogers, Mahajan", "Ergonomics 2024", "4-week in-home deployment, 68% performance increase, 72% satisfaction improvement"],
    ],
    col_widths=[1.3*inch, 1.8*inch, 0.8*inch, 2.6*inch]
))

story.append(subsec("13.2 Major Conference Papers"))
story.append(make_table(
    ["Title", "Venue", "Key Result"],
    [
        ["Harmonic Mobile Manipulation", "IROS 2024 (Best Paper)", "End-to-end nav+manipulation, 17.6% improvement, sim-to-real transfer on Stretch"],
        ["PoliFormer", "CoRL 2024 (Outstanding Paper)", "RGB-only navigation, 85.5% success, 28.5% improvement, zero-shot sim-to-real"],
        ["HomeRobot OVMM", "NeurIPS 2023 Challenge", "Open-vocab mobile manipulation benchmark, Stretch RE2 real-world stack"],
        ["SPOC", "CVPR 2024", "Text instruction following, trained on 200K houses, zero-shot sim-to-real"],
        ["OK-Robot", "arXiv 2024", "Zero-shot pick-and-drop, 58.5% success (1.8x prior SOTA), 82% uncluttered"],
        ["Robot Utility Models (RUMs)", "arXiv 2024 (NYU/Hello Robot/Meta)", "Zero-shot deployment, 90% success in novel environments"],
        ["VRB: Affordances from Videos", "CVPR 2023 (CMU)", "12 tasks learned from internet videos, 25-min adaptation per task"],
        ["WHIRL", "RSS 2022 (CMU)", "Human-to-robot imitation, one-shot generalization across 20 tasks"],
        ["Dobb-E: Bringing Robots Home", "arXiv 2023 (NYU/Meta)", "81% success with 5 min demos, 22 NYC homes, open-source"],
        ["Open X-Embodiment (RT-X)", "ICRA 2024 (34 labs)", "Multi-robot dataset, 50% improvement across 5 robots, Stretch included"],
    ],
    col_widths=[1.8*inch, 1.5*inch, 3.2*inch]
))

story.append(subsec("13.3 Assistive Robotics & Healthcare"))
story.append(make_table(
    ["Title", "Venue", "Key Contribution"],
    [
        ["Bodies Uncovered (blanket manipulation)", "RA-L 2022 (CMU/GT)", "Sim-to-real blanket manipulation on Stretch, uncovering body parts"],
        ["RoBE (graph-based blanket dynamics)", "RA-L 2023 (CMU)", "Graph-based cloth dynamics, 12-person human study"],
        ["HAT: Head-Worn Assistive Teleop", "arXiv 2023 (CMU)", "Head-worn interface for Henry Evans, week-long in-home study"],
        ["Bimanual HD-EMG Control", "arXiv 2026 (CMU)", "12-day in-home study, quadriplegia user, muscle-signal control of Stretch"],
        ["Accessible Remote Tele-operation", "RO-MAN 2021 (UW)", "Browser-based accessible interface, 18-participant study"],
        ["AccessTeleopKit", "UIST 2024 (UW)", "Open-source toolkit for accessible web-based tele-operation"],
        ["Robotic Support for Older Adults", "Frontiers 2025", "Feasibility assessment, participatory design, social connection"],
    ],
    col_widths=[2.2*inch, 1.3*inch, 3*inch]
))

story.append(subsec("13.4 Key Research Institutions"))
story.append(make_table(
    ["Institution", "Key Researchers", "Focus"],
    [
        ["Allen Institute for AI (AI2)", "Ehsani, Kembhavi, Weihs", "Embodied AI, sim-to-real (SPOC, PoliFormer, HarmonicMM)"],
        ["New York University", "Pinto, Shafiullah", "Imitation learning, home robots (Dobb-E, RUMs, VINN, OK-Robot)"],
        ["Carnegie Mellon University", "Pathak, Bahl, Erickson", "Human video imitation, assistive robotics (WHIRL, VRB, HAT, EMG)"],
        ["Georgia Tech", "Kemp (now Hello Robot CTO)", "Core Stretch design, Healthcare Robotics Lab"],
        ["University of Washington", "Cakmak, Srinivasa", "Tele-operation, accessible interfaces (CREATE lab)"],
        ["UIUC", "Rogers, Mahajan", "Aging/disability support, participatory design (LIFE Home)"],
        ["Meta FAIR", "Chintala, Paxton", "HomeRobot benchmark, RT-X, foundation models"],
    ],
    col_widths=[1.5*inch, 1.5*inch, 3.5*inch]
))
story.append(PageBreak())

# ============================================================
# 14. GAZEBOT PROJECT RECOMMENDATIONS
# ============================================================
story.append(section("14. GazeBot Project: Repository Recommendations & Usage Guide"))
story.append(body(
    "This section maps the Hello Robot Stretch GitHub ecosystem to the specific needs of <b>GazeBot</b> -- "
    "a head-gaze and sip-and-puff shared autonomy system for assistive robot manipulation, being developed "
    "at the UIUC McKechnie Family LIFE Home. GazeBot uses Hello Robot Stretch 3 + Meta Quest 3 to enable "
    "individuals with severe motor disabilities (ALS, high-level SCI, locked-in syndrome) to perform "
    "activities of daily living through head movements and oral motor control."
))

# --- 14.1 Primary Repos ---
story.append(Paragraph("14.1 Primary Repositories (Must-Use)", styles['RecommendTitle']))
story.append(sp())

# stretch_ros2
story.append(subsubsec("stretch_ros2 -- Core Robot Control Layer"))
story.append(body(
    "<b>GazeBot Role:</b> Foundation of the entire robot control stack. Every GazeBot command ultimately "
    "flows through stretch_ros2.<br/>"
    "<b>Specific packages needed:</b>"
))
story.append(make_table(
    ["Package", "GazeBot Usage"],
    [
        ["stretch_core", "Main driver node in 'position' and 'navigation' modes. The stretch_driver publishes /mode, /battery, /is_homed topics your Unity app monitors. /runstop service is the E-stop backend for hard-puff."],
        ["stretch_nav2", "Autonomous navigation backbone. User looks at destination via head-gaze -> Unity converts gaze ray + depth to 3D world coordinate -> sends Nav2 goal via Simple Commander API. SLAM mapping (offline_mapping.launch.py) creates the LIFE Home map. navigation.launch.py runs AMCL localization."],
        ["stretch_description", "URDF for robot visualization in MR overlay. Could render robot state in Quest 3 via WebSocket."],
        ["stretch_funmap", "Whole-body grasping planner. /funmap/trigger_reach_until_contact and /funmap/trigger_head_scan services are directly usable for GazeBot's manipulation pipeline."],
        ["stretch_demos", "/handover_object/trigger_handover_object service is the \"bring to me\" action -- user sips to confirm, robot autonomously brings grasped object to wheelchair position."],
        ["stretch_simulation", "MuJoCo sim for development when Stretch is unavailable. RoboCasa kitchen environments approximate LIFE Home layout."],
        ["hello_helpers", "HelloNode class for rapid prototyping of new GazeBot ROS 2 nodes (head-gaze target converter, sip-puff action mapper)."],
    ],
    col_widths=[1.3*inch, 5.2*inch]
))

# stretch_ai
story.append(subsubsec("stretch_ai -- AI & Perception Layer"))
story.append(body(
    "<b>GazeBot Role:</b> Powers the shared autonomy intelligence -- object detection, grasp planning, "
    "and semantic understanding.<br/>"
    "<b>Critical components:</b>"
))
story.append(make_table(
    ["Component", "GazeBot Usage"],
    [
        ["OWLv2 + SAMv2 perception", "Object detection and segmentation when user's head-gaze ray highlights an object. User looks at cup -> gaze ray intersects with detected object bounding box -> visual confirmation in MR overlay."],
        ["AnyGrasp / grasp planning", "Generates collision-free 6-DOF gripper poses after user sips to confirm object selection. Grasp preview shown in MR view before execution approval."],
        ["RobotClient API", "High-level commands (move_to_nav_posture, move_to_manip_posture, arm_to) simplify GazeBot's control logic. ZMQ bridge enables offloading AI inference to GPU workstation."],
        ["stretch.app.grasp_object", "Reference implementation for single-object grasping by name -- directly adaptable for GazeBot's 'Manipulate' mode."],
        ["stretch.app.mapping", "Autonomous 3D mapping of the LIFE Home environment for navigation and semantic understanding."],
        ["DynaMem", "Dynamic memory tracks objects that move (e.g., user asks robot to fetch cup that was moved). Essential for real home environments where objects are not static."],
        ["Whisper STT / TTS", "Audio feedback via Bluetooth earbuds -- confirmation tones, status announcements, error alerts. Can also enable optional voice commands for users who retain speech."],
    ],
    col_widths=[1.5*inch, 5*inch]
))

# stretch_body
story.append(subsubsec("stretch_body -- Low-Level Hardware Access"))
story.append(body(
    "<b>GazeBot Role:</b> Direct hardware control beneath ROS 2, especially for custom behaviors.<br/>"
    "<b>Key uses:</b>"
))
story.append(bullet("<b>Emergency stop implementation:</b> Hard puff -> robot.stop() halts all motion immediately. Monitor robot.pimu.status for runstop state."))
story.append(bullet("<b>Head pan/tilt control:</b> robot.head.move_to('head_pan', rad) maps directly to user's head-gaze yaw in 'Look' mode. Sub-degree precision matches Quest 3's 90 Hz head tracking."))
story.append(bullet("<b>Gripper control:</b> robot.end_of_arm.move_to('stretch_gripper', pct) for grasp execution after shared autonomy approval."))
story.append(bullet("<b>Battery monitoring:</b> robot.pimu.status battery data displayed in MR HUD (head-up display)."))
story.append(bullet("<b>Sensor access:</b> Cliff sensors, IMU, wrist accelerometer for safety monitoring and contextual feedback to user."))

# --- 14.2 Secondary Repos ---
story.append(Paragraph("14.2 Secondary Repositories (Highly Recommended)", styles['RecommendTitle']))
story.append(sp())

story.append(subsubsec("stretch_tutorials -- Learning & Rapid Prototyping"))
story.append(body(
    "<b>Week 1 resource.</b> Follow Track C ROS 2 tutorials in order: (1) Robot Driver, (2) Teleop, "
    "(3) Nav2 Stack, (4) Follow Joint Trajectory, (5) HelloNode, (6) Deep Perception. "
    "The 'Offloading Computation' tutorial is critical for GazeBot's GPU workstation architecture. "
    "Voice-to-Text and Voice Teleop examples inform audio feedback implementation."
))

story.append(subsubsec("stretch_web_teleop -- WebRTC Video Streaming"))
story.append(body(
    "<b>GazeBot Role:</b> Provides the <b>WebRTC video streaming infrastructure</b> that GazeBot's Unity app "
    "builds upon. The proposal explicitly references this: 'WebRTC (via stretch_web_teleop infrastructure)'. "
    "Streams Stretch head camera and gripper camera feeds to Quest 3 via WebRTC. Also serves as the "
    "baseline comparison system for Week 7 evaluation (keyboard/mouse control vs. GazeBot)."
))

story.append(subsubsec("stretch_dex_teleop -- Data Collection for Future Learning"))
story.append(body(
    "<b>Future direction.</b> If GazeBot evolves to include adaptive autonomy (Section 11, Future Directions), "
    "dex_teleop enables collecting manipulation demonstrations for training imitation learning policies "
    "(ACT, Diffusion Policy via LeRobot). The $295 teleop kit is already compatible with Stretch 3."
))

# --- 14.3 Reference Repos ---
story.append(Paragraph("14.3 Reference Repositories", styles['RecommendTitle']))
story.append(sp())
story.append(make_table(
    ["Repository", "GazeBot Relevance"],
    [
        ["stretch_tool_share", "The adapted_spoon_V1 tool is directly relevant to assistive feeding. The swivel_tablet_mount could hold a Quest 3 charging dock. Custom tools could be designed for specific ADL tasks (door opener, light switch pusher)."],
        ["stretch_community", "CMU WeHelp (shared autonomy for wheelchair users) and UW stretch-web-app (enhanced teleoperation) are directly related prior work. The Meta AI Habitat2 sim environment enables large-scale testing."],
        ["stretch_hardware_guides", "Essential reference for understanding physical limits, wiring, and maintenance of the LIFE Home's Stretch robot."],
        ["stretch_pyfunmap", "Python-native FUNMAP implementation -- alternative to ROS 2 funmap package for simpler integration with custom Python scripts."],
        ["stretch_simulation (MuJoCo)", "Development and testing when robot is booked. RoboCasa kitchen environments approximate LIFE Home layout."],
    ],
    col_widths=[1.5*inch, 5*inch]
))

# --- 14.4 Integration Architecture ---
story.append(Paragraph("14.4 Recommended Integration Architecture", styles['RecommendTitle']))
story.append(sp())
story.append(body("<b>Data flow for a typical GazeBot 'fetch object' task:</b>"))
story.append(sp())
story.append(make_table(
    ["Step", "User Action", "Software Component", "Repository"],
    [
        ["1", "User looks at object (head-gaze ray)", "Unity/OpenXR app -> WebSocket", "Custom (GazeBot)"],
        ["2", "Object detection & highlighting", "OWLv2 + SAMv2 perception pipeline", "stretch_ai"],
        ["3", "User sips to confirm object", "Sip-and-puff -> Xbox Adaptive -> Quest 3", "Custom (GazeBot)"],
        ["4", "Grasp planning & preview", "AnyGrasp + FUNMAP", "stretch_ai + stretch_ros2"],
        ["5", "User sips to approve grasp", "MR overlay shows trajectory preview", "Custom (GazeBot)"],
        ["6", "Robot executes grasp", "joint_trajectory_server + stretch_driver", "stretch_ros2 + stretch_body"],
        ["7", "User looks at destination (self)", "Head-gaze -> 3D coordinate conversion", "Custom (GazeBot)"],
        ["8", "Robot navigates to user", "Nav2 Simple Commander API", "stretch_ros2 (stretch_nav2)"],
        ["9", "Robot hands over object", "/handover_object service", "stretch_ros2 (stretch_demos)"],
        ["10", "Audio confirmation", "Whisper TTS via Bluetooth earbuds", "stretch_ai (audio module)"],
    ],
    col_widths=[0.4*inch, 1.5*inch, 2.2*inch, 2.4*inch]
))

# --- 14.5 Weekly Repo Usage ---
story.append(Paragraph("14.5 Repository Usage by Project Week", styles['RecommendTitle']))
story.append(sp())
story.append(make_table(
    ["Week", "Task", "Primary Repos", "Specific Files/Modules"],
    [
        ["1", "Environment Setup", "stretch_ros2, stretch_body, stretch_ai, stretch_tutorials", "stretch_driver.launch.py, Track C tutorials, install.sh"],
        ["2", "Head-Gaze Control", "stretch_body, stretch_web_teleop", "robot.head.move_to(), WebRTC streaming, head pan/tilt API"],
        ["3", "Sip-and-Puff + Modes", "stretch_body, stretch_ros2", "robot.pimu (runstop for e-stop), /mode topic, HelloNode class"],
        ["4", "Autonomous Navigation", "stretch_ros2 (stretch_nav2)", "offline_mapping.launch.py, navigation.launch.py, Nav2 Simple Commander"],
        ["5", "Shared Autonomy Manipulation", "stretch_ai, stretch_ros2 (stretch_funmap)", "grasp_object app, OWLv2+SAMv2, /funmap/trigger_* services"],
        ["6", "Task Presets + Audio", "stretch_ai, stretch_ros2 (stretch_demos)", "Whisper TTS, /handover_object, DynaMem for dynamic environments"],
        ["7", "Evaluation", "stretch_web_teleop (baseline), all above", "Web teleop as keyboard/mouse baseline comparison system"],
        ["8", "Documentation + Demo", "stretch_community (reference)", "Community portal for publishing GazeBot as open-source contribution"],
    ],
    col_widths=[0.5*inch, 1.5*inch, 1.8*inch, 2.7*inch]
))

# --- 14.6 Key Risks & Mitigations ---
story.append(Paragraph("14.6 Repository-Specific Risks & Mitigations", styles['RecommendTitle']))
story.append(sp())
story.append(make_table(
    ["Risk", "Repository", "Mitigation"],
    [
        ["stretch_ai requires GPU workstation with RTX 4090", "stretch_ai", "Use WiFi Access Point ($995) for reliable connection. DynaMem has CPU-only mode (CLIP ViT-B/16)."],
        ["AnyGrasp is closed-source", "stretch_ai", "Fallback to FUNMAP whole-body grasping (/funmap/trigger_reach_until_contact) which is fully open-source."],
        ["MuJoCo sim doesn't perfectly match real robot", "stretch_ros2 simulation", "Use MuJoCo for nav/logic testing only; validate manipulation on real robot during booked sessions."],
        ["ROS 2 bridge adds latency to AI pipeline", "stretch_ai (ros2_bridge)", "Profile ZMQ bridge latency early (Week 1). If >100ms, consider running AI models directly on robot NUC 12."],
        ["Nav2 may struggle in cluttered LIFE Home", "stretch_ros2 (stretch_nav2)", "Tune costmap inflation radius (default 0.20m). Use RTAB-Map for 3D visual navigation as fallback."],
    ],
    col_widths=[1.8*inch, 1.3*inch, 3.4*inch]
))

# --- 14.7 Relevant Publications ---
story.append(Paragraph("14.7 Most Relevant Publications for GazeBot", styles['RecommendTitle']))
story.append(sp())
story.append(make_table(
    ["Paper", "GazeBot Relevance"],
    [
        ["Immersive Participatory Design (Olatunji, Mahajan et al., 2024)", "Direct predecessor at LIFE Home. Same PI (Mahajan), same robot, same mission. GazeBot extends to users who cannot use hands or voice."],
        ["HAT: Head-Worn Assistive Teleop (CMU, 2023)", "Most directly comparable system: head-worn interface for Henry Evans. GazeBot improves on this with XR integration and shared autonomy."],
        ["Bimanual HD-EMG Control (CMU, 2026)", "Alternative input modality (muscle signals vs. head-gaze). 12-day in-home study methodology is a model for GazeBot's future longitudinal deployment."],
        ["Accessible Remote Tele-operation (UW, 2021)", "Browser-based accessible interface study. Informs GazeBot's usability evaluation design (NASA-TLX, SUS)."],
        ["AccessTeleopKit (UW, UIST 2024)", "Open-source accessible tele-operation toolkit. Could complement GazeBot as fallback interface."],
        ["OK-Robot (NYU/Meta, 2024)", "Zero-shot pick-and-drop architecture. GazeBot could adopt this modular approach for manipulation."],
        ["ForceSight (Hello Robot, ICRA 2024)", "Text-guided manipulation with visual-force goals. Could enhance GazeBot's grasping with force feedback."],
        ["Shared Autonomy with Learned Latent Actions (Jeon, RSS 2020)", "Theoretical foundation for GazeBot's shared autonomy paradigm. 2-DOF input controlling 7-DOF robot."],
    ],
    col_widths=[2.5*inch, 4*inch]
))
story.append(PageBreak())

# ============================================================
# 15. SOURCES & REFERENCES
# ============================================================
story.append(section("15. Sources & References"))
sources = [
    ("Hello Robot GitHub Organization", "https://github.com/hello-robot"),
    ("stretch_ai Repository", "https://github.com/hello-robot/stretch_ai"),
    ("stretch_ros2 Repository", "https://github.com/hello-robot/stretch_ros2"),
    ("stretch_ros Repository", "https://github.com/hello-robot/stretch_ros"),
    ("stretch_body Repository", "https://github.com/hello-robot/stretch_body"),
    ("stretch_firmware Repository", "https://github.com/hello-robot/stretch_firmware"),
    ("stretch_tutorials Repository", "https://github.com/hello-robot/stretch_tutorials"),
    ("stretch_dex_teleop Repository", "https://github.com/hello-robot/stretch_dex_teleop"),
    ("stretch_tool_share Repository", "https://github.com/hello-robot/stretch_tool_share"),
    ("stretch_community Repository", "https://github.com/hello-robot/stretch_community"),
    ("Stretch Documentation (v0.3)", "https://docs.hello-robot.com/0.3/"),
    ("Stretch Documentation (v0.2)", "https://docs.hello-robot.com/0.2/"),
    ("Stretch AI Product Page", "https://hello-robot.com/stretch-ai"),
    ("Stretch 3 Product Page", "https://hello-robot.com/stretch-3-product"),
    ("Stretch Community Resources", "https://docs.hello-robot.com/0.3/getting_started/community_resources/"),
    ("Stretch Forum", "https://forum.hello-robot.com"),
    ("The Design of Stretch (arXiv:2109.10892)", "https://arxiv.org/abs/2109.10892"),
    ("DynaMem Paper (arXiv:2411.04999)", "https://arxiv.org/abs/2411.04999"),
    ("OK-Robot (arXiv:2401.12202)", "https://arxiv.org/abs/2401.12202"),
    ("ForceSight (arXiv:2309.12312)", "https://arxiv.org/abs/2309.12312"),
    ("HomeRobot OVMM (arXiv:2306.11565)", "https://arxiv.org/abs/2306.11565"),
    ("HAT Interface (arXiv:2312.15071)", "https://arxiv.org/abs/2312.15071"),
    ("Robot Utility Models (arXiv:2409.05865)", "https://arxiv.org/abs/2409.05865"),
    ("Harmonic Mobile Manipulation (arXiv:2312.06639)", "https://arxiv.org/abs/2312.06639"),
    ("PoliFormer (arXiv:2406.20083)", "https://arxiv.org/abs/2406.20083"),
    ("SPOC (CVPR 2024)", "https://spoc-robot.github.io/"),
    ("Dobb-E (arXiv:2311.16098)", "https://arxiv.org/abs/2311.16098"),
    ("Open X-Embodiment (arXiv:2310.08864)", "https://arxiv.org/abs/2310.08864"),
    ("Bimanual EMG Control (arXiv:2602.02773)", "https://arxiv.org/abs/2602.02773"),
    ("IEEE Spectrum: Stretch 3 Review", "https://spectrum.ieee.org/hello-robot-stretch-3"),
    ("Introducing Stretch AI (Chris Paxton Substack)", "https://itcanthink.substack.com/p/introducing-stretch-ai"),
]
for title, url in sources:
    story.append(Paragraph(f"<b>{title}</b><br/><font color='#0066CC' size='8'>{url}</font>", styles['BodyText2']))

story.append(sp(20))
story.append(Paragraph(
    "<i>Report generated for the GazeBot project at the McKechnie Family LIFE Home, "
    "University of Illinois Urbana-Champaign.</i>",
    styles['SmallNote']
))

# ============================================================
# BUILD PDF
# ============================================================
doc.build(story)
print(f"PDF saved to: {output_path}")

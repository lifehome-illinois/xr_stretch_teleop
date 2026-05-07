#!/usr/bin/env python3
"""
Generates two PDFs in this directory:
  - Stretch_GazeBot_Reproduction_Guide.pdf   (detailed, multi-page)
  - Stretch_GazeBot_OnePager.pdf             (single-page summary)
"""

import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem, HRFlowable
)
from reportlab.pdfgen import canvas

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Shared styles ----------
def get_styles():
    base = getSampleStyleSheet()

    title = ParagraphStyle(
        "TitleBig", parent=base["Title"],
        fontSize=22, leading=26, spaceAfter=6,
        textColor=colors.HexColor("#0B3D91"),
        alignment=TA_LEFT,
    )
    subtitle = ParagraphStyle(
        "Subtitle", parent=base["Normal"],
        fontSize=12, leading=15, spaceAfter=12,
        textColor=colors.HexColor("#444444"), italic=True,
    )
    h1 = ParagraphStyle(
        "H1", parent=base["Heading1"],
        fontSize=15, leading=18, spaceBefore=14, spaceAfter=6,
        textColor=colors.HexColor("#0B3D91"),
    )
    h2 = ParagraphStyle(
        "H2", parent=base["Heading2"],
        fontSize=12, leading=15, spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor("#1F4E79"),
    )
    body = ParagraphStyle(
        "Body", parent=base["BodyText"],
        fontSize=10, leading=13.5, spaceAfter=6, alignment=TA_LEFT,
    )
    bullet = ParagraphStyle(
        "Bullet", parent=body, leftIndent=14, bulletIndent=2,
    )
    code = ParagraphStyle(
        "Code", parent=base["Code"],
        fontName="Courier", fontSize=9, leading=11,
        leftIndent=10, rightIndent=10,
        backColor=colors.HexColor("#F4F6FA"),
        borderColor=colors.HexColor("#D0D7E2"),
        borderWidth=0.5, borderPadding=6,
        spaceBefore=4, spaceAfter=8,
        textColor=colors.HexColor("#222222"),
    )
    note = ParagraphStyle(
        "Note", parent=body,
        backColor=colors.HexColor("#FFF8E1"),
        borderColor=colors.HexColor("#E0C97F"),
        borderWidth=0.5, borderPadding=6,
        leftIndent=4, rightIndent=4,
        spaceBefore=6, spaceAfter=8,
    )
    small = ParagraphStyle(
        "Small", parent=body, fontSize=8.5, leading=11,
        textColor=colors.HexColor("#555555"),
    )
    return dict(
        title=title, subtitle=subtitle, h1=h1, h2=h2,
        body=body, bullet=bullet, code=code, note=note, small=small
    )


# ---------- Helpers ----------
def code_block(text, styles):
    # Escape HTML and preserve newlines using <br/>
    escaped = (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
    )
    return Paragraph(escaped, styles["code"])


def bullets(items, styles):
    flow = []
    for it in items:
        flow.append(Paragraph(f"• {it}", styles["bullet"]))
    return flow


def hr():
    return HRFlowable(width="100%", thickness=0.6,
                      color=colors.HexColor("#BBBBBB"),
                      spaceBefore=4, spaceAfter=8)


# ---------- Footer / header on each page ----------
def add_page_decorations(canv: canvas.Canvas, doc):
    canv.saveState()
    canv.setFont("Helvetica", 8)
    canv.setFillColor(colors.HexColor("#777777"))
    canv.drawString(0.75 * inch, 0.5 * inch,
                    "Stretch GazeBot — Knowledge Transfer")
    canv.drawRightString(LETTER[0] - 0.75 * inch, 0.5 * inch,
                         f"Page {doc.page}")
    canv.setStrokeColor(colors.HexColor("#CCCCCC"))
    canv.line(0.75 * inch, 0.65 * inch,
              LETTER[0] - 0.75 * inch, 0.65 * inch)
    canv.restoreState()


# ---------- Detailed reproduction PDF ----------
def build_detailed():
    out = os.path.join(OUT_DIR, "Stretch_GazeBot_Reproduction_Guide.pdf")
    doc = SimpleDocTemplate(
        out, pagesize=LETTER,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.8 * inch, bottomMargin=0.8 * inch,
        title="Stretch GazeBot — Reproduction Guide",
        author="het@operationautopilot.com",
    )
    s = get_styles()
    story = []

    # ----- Cover -----
    story.append(Paragraph("Stretch GazeBot", s["title"]))
    story.append(Paragraph(
        "Control a Hello Robot Stretch 3 with your head, using Xreal One Pro AR glasses.",
        s["subtitle"],
    ))
    story.append(hr())

    meta = Table(
        [
            ["Project folder",   "~/lab/life_home/xreal_head_control"],
            ["Robot",            "Hello Robot Stretch 3"],
            ["AR glasses",       "Xreal One Pro (USB-C, ethernet over USB)"],
            ["PC OS",            "Linux (tested on Ubuntu 22.04)"],
            ["Robot OS",         "Ubuntu 22.04 + ROS 2 Humble"],
            ["Author / Owner",   "het@operationautopilot.com"],
            ["Document version", "Apr 2026"],
        ],
        colWidths=[1.6 * inch, 4.6 * inch],
    )
    meta.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 9),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F3F8")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta)
    story.append(Spacer(1, 0.15 * inch))

    # ----- Section 1: What this is -----
    story.append(Paragraph("1. What this project does", s["h1"]))
    story.append(Paragraph(
        "Stretch GazeBot is a teleoperation bridge. You wear Xreal One Pro AR glasses on "
        "your PC. The glasses stream their IMU (gyroscope + accelerometer) data over a USB-C "
        "ethernet link to your PC. A Python program on the PC reads that stream, computes head "
        "pitch / yaw / roll, and forwards pan / tilt commands to a relay program running on "
        "the Stretch 3 robot. The relay translates those into ROS 2 joint commands for the "
        "robot's head. The result: turn your head, and the robot's head turns the same way "
        "(near real-time, &lt; 10 ms IMU latency).",
        s["body"],
    ))
    story.append(Paragraph(
        "There is also a DRIVE mode, where holding SPACE makes the robot's mobile base move "
        "based on head tilt (pitch → forward / reverse, yaw → turn).",
        s["body"],
    ))

    story.append(Paragraph("System architecture", s["h2"]))
    story.append(code_block(
        "[Xreal One Pro glasses]\n"
        "      |  USB-C ethernet (TCP 169.254.2.1:52998)\n"
        "      v\n"
        "[Your PC]  stretch_head_control.py\n"
        "      |  TCP JSON commands (port 9090)\n"
        "      v\n"
        "[Stretch 3]  stretch_relay.py  -->  ROS 2 follow_joint_trajectory action\n"
        "                              -->  joint_head_pan / joint_head_tilt",
        s,
    ))

    story.append(Paragraph("Repository layout", s["h2"]))
    files = Table(
        [
            ["File", "Where it runs", "Purpose"],
            ["stretch_head_control.py", "Your PC",
             "Main bridge. Reads glasses IMU, computes head pose, sends TCP commands."],
            ["stretch_relay.py", "Stretch 3",
             "ROS 2 node. Receives TCP commands and moves head pan / tilt."],
            ["imu_server.py / imu_viz.html", "Your PC",
             "Optional: 3D visualizer in browser to verify glasses work."],
            ["src/imu_reader_fixed.py", "Your PC",
             "Reads raw IMU stream from glasses over TCP."],
            ["src/head_tracker.py", "Your PC",
             "Sensor fusion: raw IMU → calibrated pitch / yaw / roll."],
            ["src/imu_data.py", "Your PC",
             "Dataclass holding a single IMU sample."],
            ["start.sh", "Your PC",
             "Convenience launcher — pings glasses, then runs the bridge."],
            ["requirements.txt", "Your PC",
             "Python deps: numpy, pygame, PyOpenGL (visualizer only)."],
        ],
        colWidths=[1.7 * inch, 1.0 * inch, 3.5 * inch],
    )
    files.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 8.5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B3D91")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#FFFFFF"), colors.HexColor("#F4F6FA")]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(files)

    story.append(PageBreak())

    # ----- Section 2: Hardware -----
    story.append(Paragraph("2. Hardware checklist", s["h1"]))
    for line in [
        "<b>Xreal One Pro</b> AR glasses (the regular One has not been tested and may not work).",
        "<b>USB-C cable</b> (data + power capable). The glasses expose a USB ethernet adapter.",
        "<b>Hello Robot Stretch 3</b> on the same Wi-Fi or LAN as your PC.",
        "<b>Linux PC</b> with Python 3.7+ (Ubuntu 22.04 recommended).",
        "<b>Network reachability</b>: your PC must be able to reach the robot at "
        "<font face='Courier'>172.22.243.8</font>. If your robot has a different IP, write it "
        "down — you will need to update <font face='Courier'>STRETCH_IP</font> in "
        "<font face='Courier'>stretch_head_control.py</font> (line 35).",
    ]:
        story.append(Paragraph(f"• {line}", s["bullet"]))

    story.append(Paragraph("3. Initial PC setup (one-time)", s["h1"]))

    story.append(Paragraph("3.1 Clone the repo", s["h2"]))
    story.append(code_block(
        "mkdir -p ~/lab/life_home && cd ~/lab/life_home\n"
        "git clone <your-fork-url> xreal_head_control\n"
        "cd xreal_head_control",
        s,
    ))
    story.append(Paragraph(
        "If you received this code as a tarball/zip instead, extract it to "
        "<font face='Courier'>~/lab/life_home/xreal_head_control</font> so the relative paths "
        "in the helper scripts continue to work.",
        s["body"],
    ))

    story.append(Paragraph("3.2 Install Python dependencies", s["h2"]))
    story.append(code_block(
        "# (Optional but recommended) virtualenv\n"
        "python3 -m venv .venv && source .venv/bin/activate\n"
        "\n"
        "pip install -r requirements.txt",
        s,
    ))
    story.append(Paragraph(
        "<b>Note:</b> <font face='Courier'>numpy</font> is the only hard requirement for the "
        "head-control bridge. <font face='Courier'>pygame</font> and "
        "<font face='Courier'>PyOpenGL</font> are only needed for the optional 3D visualizer.",
        s["note"],
    ))

    story.append(Paragraph("3.3 Plug in the glasses and verify the link", s["h2"]))
    for line in [
        "Connect the Xreal One Pro to your PC with USB-C.",
        "On the glasses, open <i>Settings → Developer Menu → Enable Ethernet</i> (only needed once).",
        "On your PC, confirm the link:",
    ]:
        story.append(Paragraph(f"• {line}", s["bullet"]))
    story.append(code_block("ping 169.254.2.1", s))
    story.append(Paragraph(
        "You should see replies. If not, try a different USB-C port, re-toggle ethernet in "
        "the developer menu, or check <font face='Courier'>ip addr</font> for an interface "
        "with a 169.254.x.x address.",
        s["body"],
    ))

    story.append(Paragraph("3.4 (Optional) Test the glasses on their own", s["h2"]))
    story.append(code_block(
        "cd ~/lab/life_home/xreal_head_control\n"
        "python3 imu_server.py            # in one terminal\n"
        "xdg-open imu_viz.html            # opens a 3D cube in your browser",
        s,
    ))
    story.append(Paragraph(
        "Move the glasses — the cube should follow. Press Ctrl+C in the terminal to stop.",
        s["body"],
    ))

    story.append(PageBreak())

    # ----- Section 3: Robot setup -----
    story.append(Paragraph("4. Robot setup (Stretch 3)", s["h1"]))

    story.append(Paragraph("4.1 SSH into the robot", s["h2"]))
    story.append(code_block(
        "ssh hello-robot@172.22.243.8\n"
        "# password: <ask lab admin>",
        s,
    ))
    story.append(Paragraph(
        "<b>Substitute your robot's IP if different.</b> Get the robot's password from your lab admin and "
        "<font face='Courier'>change it for production use.</font>",
        s["note"],
    ))

    story.append(Paragraph("4.2 Copy the relay script onto the robot", s["h2"]))
    story.append(Paragraph(
        "From your PC, copy <font face='Courier'>stretch_relay.py</font> into the robot's "
        "ROS 2 workspace:",
        s["body"],
    ))
    story.append(code_block(
        "scp ~/lab/life_home/xreal_head_control/stretch_relay.py \\\n"
        "    hello-robot@172.22.243.8:~/het_ros2_ws/stretch_relay.py",
        s,
    ))
    story.append(Paragraph(
        "(Create the directory on the robot first if needed: "
        "<font face='Courier'>mkdir -p ~/het_ros2_ws</font>.)",
        s["body"],
    ))

    story.append(Paragraph("4.3 Start the Stretch driver (terminal A on the robot)", s["h2"]))
    story.append(code_block(
        "ssh hello-robot@172.22.243.8\n"
        "conda deactivate              # IMPORTANT — rclpy lives in the system Python\n"
        "ros2 launch stretch_core stretch_driver.launch.py",
        s,
    ))
    story.append(Paragraph(
        "Wait for the driver to finish initializing (you should see joint state messages).",
        s["body"],
    ))

    story.append(Paragraph("4.4 Start the relay (terminal B on the robot)", s["h2"]))
    story.append(code_block(
        "ssh hello-robot@172.22.243.8\n"
        "conda deactivate\n"
        "\n"
        "# Confirm the action server name the driver advertises:\n"
        "ros2 action list\n"
        "# Look for: /stretch_controller/follow_joint_trajectory\n"
        "\n"
        "# If your action server name differs, edit ~/het_ros2_ws/stretch_relay.py\n"
        "# (see the import of hello_helpers.hello_misc — move_to_pose uses the standard\n"
        "#  Stretch action server, so usually no edit is needed).\n"
        "\n"
        "python3 ~/het_ros2_ws/stretch_relay.py",
        s,
    ))
    story.append(Paragraph(
        "When you see <font face='Courier'>Waiting for connection on port 9090...</font>, the "
        "robot side is ready.",
        s["body"],
    ))

    # ----- Section 4: Run -----
    story.append(Paragraph("5. Running the bridge on your PC", s["h1"]))
    story.append(code_block(
        "cd ~/lab/life_home/xreal_head_control\n"
        "python3 stretch_head_control.py\n"
        "# (or)\n"
        "./start.sh                       # also pings the glasses first",
        s,
    ))
    story.append(Paragraph("First-run procedure:", s["h2"]))
    for line in [
        "Place the glasses on a flat surface and keep them <b>completely still</b> for ~0.5 s "
        "while gyro calibration runs (you'll see a percentage).",
        "When you see <i>Calibration complete</i>, put the glasses on.",
        "Press <b>T</b> to set your current head pose as 'center'.",
        "Move your head left / right → robot pans. Tilt up / down → robot tilts.",
    ]:
        story.append(Paragraph(f"• {line}", s["bullet"]))

    story.append(Paragraph("5.1 Keyboard controls", s["h2"]))
    keys = Table(
        [
            ["Key", "Mode", "Action"],
            ["M",      "Both",  "Toggle LOOK ↔ DRIVE mode"],
            ["Space",  "DRIVE", "Hold to enable base motion (head steers)"],
            ["T",      "Both",  "Zero view — set current head pose as neutral"],
            ["R",      "Both",  "Recalibrate gyroscope (keep glasses still)"],
            ["L",      "Both",  "Lock / unlock — pause sending commands"],
            ["Q",      "Both",  "Quit cleanly"],
        ],
        colWidths=[0.7 * inch, 0.9 * inch, 4.6 * inch],
    )
    keys.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B3D91")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#FFFFFF"), colors.HexColor("#F4F6FA")]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(keys)

    story.append(PageBreak())

    # ----- Section 5: Tuning -----
    story.append(Paragraph("6. Tuning sensitivity and direction", s["h1"]))
    story.append(Paragraph(
        "All tunables live near the top of "
        "<font face='Courier'>stretch_head_control.py</font>:",
        s["body"],
    ))
    story.append(code_block(
        "STRETCH_IP        = \"172.22.243.8\"   # robot IP\n"
        "RELAY_PORT        = 9090\n"
        "\n"
        "HEAD_PAN_MIN      = -3.9             # robot joint limits (rad)\n"
        "HEAD_PAN_MAX      =  1.5\n"
        "HEAD_TILT_MIN     = -1.53\n"
        "HEAD_TILT_MAX     =  0.79\n"
        "\n"
        "HEAD_PAN_SCALE    = 0.025            # bigger = more sensitive left/right\n"
        "HEAD_TILT_SCALE   = 0.015            # bigger = more sensitive up/down\n"
        "\n"
        "COMMAND_INTERVAL  = 0.05             # seconds between commands (20 Hz)\n"
        "\n"
        "BASE_LINEAR_MAX   = 0.3              # m/s   — max forward/reverse in DRIVE\n"
        "BASE_ANGULAR_MAX  = 0.5              # rad/s — max rotation in DRIVE\n"
        "BASE_DEADZONE     = 5.0              # deg   — no motion within this range\n"
        "BASE_MAX_ANGLE    = 30.0             # deg   — angle that maps to full speed",
        s,
    ))
    story.append(Paragraph(
        "If pan or tilt moves the wrong way, flip the sign in the assignment near "
        "<font face='Courier'>stretch_head_control.py</font> lines 163–164:",
        s["body"],
    ))
    story.append(code_block(
        "pan_rad  = -yaw   * HEAD_PAN_SCALE   # flip sign of yaw\n"
        "tilt_rad = -pitch * HEAD_TILT_SCALE  # flip sign of pitch",
        s,
    ))

    # ----- Section 6: Troubleshooting -----
    story.append(Paragraph("7. Troubleshooting", s["h1"]))
    tbl = Table(
        [
            ["Symptom", "Most likely cause / fix"],
            ["Cannot ping 169.254.2.1",
             "Ethernet not enabled in glasses developer menu, or USB-C cable is power-only. "
             "Try a different cable / port."],
            ["“Connection refused” when starting the PC bridge",
             "stretch_relay.py is not running on the robot. Start it first."],
            ["“Trajectory server not found” on the robot",
             "stretch_driver.launch.py is not running, or its action server name doesn't match. "
             "Run `ros2 action list` and confirm /stretch_controller/follow_joint_trajectory."],
            ["“No module named rclpy” on the robot",
             "Conda is active and shadowing the system Python. Run `conda deactivate` first."],
            ["Robot head moves the wrong direction",
             "Flip the sign on stretch_head_control.py line 163 or 164."],
            ["Tracking drifts after a minute",
             "Press R to recalibrate (keep glasses still). Drift is inherent to gyro-only "
             "tracking — short sessions work best."],
            ["Too sensitive / not sensitive enough",
             "Adjust HEAD_PAN_SCALE and HEAD_TILT_SCALE."],
            ["“T / R / Q does nothing”",
             "Make sure the bridge terminal is focused. Some terminals require a single "
             "keypress (cbreak mode is set, so don't press Enter)."],
        ],
        colWidths=[2.2 * inch, 4.0 * inch],
    )
    tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B3D91")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#FFFFFF"), colors.HexColor("#F4F6FA")]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#DDDDDD")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tbl)

    story.append(PageBreak())

    # ----- Section 7: Optional extras -----
    story.append(Paragraph("8. Optional extras (used during development)", s["h1"]))

    story.append(Paragraph("8.1 Mount the robot's ROS workspace over SSHFS", s["h2"]))
    story.append(Paragraph(
        "Useful for editing files on the robot from your PC:",
        s["body"],
    ))
    story.append(code_block(
        "mkdir -p ~/lab/life_home/shared_folder_btw_stretch3_mypc/het_ros2_ws\n"
        "sshfs hello-robot@172.22.243.8:/home/hello-robot/het_ros2_ws \\\n"
        "      ~/lab/life_home/shared_folder_btw_stretch3_mypc/het_ros2_ws",
        s,
    ))

    story.append(Paragraph("8.2 Robot reset / homing", s["h2"]))
    story.append(code_block(
        "# On the robot, before starting the driver:\n"
        "stretch_free_robot_process.py    # release any stuck driver locks\n"
        "stretch_robot_home.py            # home all joints",
        s,
    ))

    story.append(Paragraph("8.3 Camera streams the robot exposes", s["h2"]))
    story.append(code_block(
        "# (each in its own SSH terminal, after `conda deactivate`)\n"
        "ros2 launch stretch_core d435i_high_resolution.launch.py     # head RGB-D\n"
        "ros2 launch stretch_core d405_basic.launch.py                # gripper cam\n"
        "ros2 run v4l2_camera v4l2_camera_node \\\n"
        "    --ros-args -p video_device:=\"/dev/video6\" \\\n"
        "               -r image_raw:=/arducam/image_raw                # arducam\n"
        "ros2 run web_video_server web_video_server                    # browser viewer\n"
        "ros2 launch ~/het_ros2_ws/stretch_dual_camera.launch.py       # combined dual cam",
        s,
    ))
    story.append(Paragraph(
        "Open the dual-camera HTML viewer on your PC:",
        s["body"],
    ))
    story.append(code_block(
        "google-chrome --kiosk \\\n"
        "  file:///home/het/lab/life_home/shared_folder_btw_stretch3_mypc/het_ros2_ws/dual_camera_view.html",
        s,
    ))

    # ----- Section 8: Going further -----
    story.append(Paragraph("9. How the code works (for the curious)", s["h1"]))
    for line in [
        "<b>IMU stream:</b> <font face='Courier'>src/imu_reader_fixed.py</font> opens a TCP "
        "connection to <font face='Courier'>169.254.2.1:52998</font> and decodes binary IMU "
        "frames (~1000 Hz).",
        "<b>Sensor fusion:</b> <font face='Courier'>src/head_tracker.py</font> calibrates the "
        "gyro bias from the first ~500 samples while you hold still, then integrates gyro and "
        "fuses with accelerometer using a complementary filter (96% gyro / 4% accel).",
        "<b>Mapping:</b> Yaw → robot pan, pitch → robot tilt, both scaled and clamped to the "
        "Stretch joint limits.",
        "<b>Transport:</b> Newline-delimited JSON over a single TCP socket (port 9090).",
        "<b>Robot side:</b> <font face='Courier'>stretch_relay.py</font> is a "
        "<font face='Courier'>hello_helpers.HelloNode</font> ROS 2 node. It calls "
        "<font face='Courier'>move_to_pose({'joint_head_pan': pan, 'joint_head_tilt': tilt}, "
        "blocking=False)</font> at 20 Hz.",
        "<b>DRIVE mode:</b> When SPACE is held, head pitch / yaw map to base "
        "<font face='Courier'>linear</font> / <font face='Courier'>angular</font> velocities "
        "with a deadzone, sent as the same JSON shape "
        "(<font face='Courier'>{linear, angular}</font>).",
    ]:
        story.append(Paragraph(f"• {line}", s["bullet"]))

    # ----- Section 9: Safety -----
    story.append(Paragraph("10. Safety notes", s["h1"]))
    for line in [
        "Always keep one hand near the Stretch e-stop while teleoperating.",
        "Press <b>L</b> to lock tracking before adjusting the glasses on your face.",
        "In DRIVE mode, releasing SPACE for ~0.2 s sends a stop command automatically.",
        "If the network drops, the relay simply stops getting commands; the robot will hold "
        "its last commanded pose. Press the e-stop if you need it to halt immediately.",
    ]:
        story.append(Paragraph(f"• {line}", s["bullet"]))

    story.append(Paragraph("11. Quick reference (cheat sheet)", s["h1"]))
    story.append(code_block(
        "# 1. Robot, terminal A:\n"
        "ssh hello-robot@172.22.243.8 'conda deactivate; \\\n"
        "  ros2 launch stretch_core stretch_driver.launch.py'\n"
        "\n"
        "# 2. Robot, terminal B:\n"
        "ssh hello-robot@172.22.243.8 'conda deactivate; \\\n"
        "  python3 ~/het_ros2_ws/stretch_relay.py'\n"
        "\n"
        "# 3. PC:\n"
        "cd ~/lab/life_home/xreal_head_control && python3 stretch_head_control.py",
        s,
    ))

    story.append(Paragraph(
        "Built from <font face='Courier'>HOW_TO_USE.txt</font> and the project source. "
        "Credits: One Pro IMU Retriever Demo by Daniel Sami Mitwalli; Stretch integration by "
        "het@operationautopilot.com.",
        s["small"],
    ))

    doc.build(story, onFirstPage=add_page_decorations,
              onLaterPages=add_page_decorations)
    return out


# ---------- One-pager ----------
def build_one_pager():
    out = os.path.join(OUT_DIR, "Stretch_GazeBot_OnePager.pdf")
    doc = SimpleDocTemplate(
        out, pagesize=LETTER,
        leftMargin=0.5 * inch, rightMargin=0.5 * inch,
        topMargin=0.45 * inch, bottomMargin=0.45 * inch,
        title="Stretch GazeBot — One-Page Reproduction Guide",
    )
    base = getSampleStyleSheet()
    styles = dict(
        title=ParagraphStyle("T", parent=base["Title"],
                             fontSize=16, leading=18, spaceAfter=2,
                             textColor=colors.HexColor("#0B3D91"),
                             alignment=TA_LEFT),
        sub=ParagraphStyle("S", parent=base["Normal"],
                           fontSize=8.5, leading=10, spaceAfter=6,
                           textColor=colors.HexColor("#444444")),
        h=ParagraphStyle("H", parent=base["Heading2"],
                         fontSize=10, leading=12, spaceBefore=4, spaceAfter=2,
                         textColor=colors.HexColor("#0B3D91")),
        body=ParagraphStyle("B", parent=base["BodyText"],
                            fontSize=8.5, leading=11, spaceAfter=2),
        code=ParagraphStyle("C", parent=base["Code"],
                            fontName="Courier", fontSize=7.8, leading=9.5,
                            leftIndent=4, rightIndent=4,
                            backColor=colors.HexColor("#F4F6FA"),
                            borderColor=colors.HexColor("#D0D7E2"),
                            borderWidth=0.4, borderPadding=4,
                            spaceBefore=2, spaceAfter=4),
    )
    story = []
    story.append(Paragraph("Stretch GazeBot — Reproduce in 1 Page", styles["title"]))
    story.append(Paragraph(
        "Control a Hello Robot Stretch 3 with your head using Xreal One Pro AR glasses. "
        "Project: <font face='Courier'>~/lab/life_home/xreal_head_control</font>",
        styles["sub"],
    ))
    story.append(HRFlowable(width="100%", thickness=0.6,
                            color=colors.HexColor("#BBBBBB"),
                            spaceBefore=0, spaceAfter=4))

    # Two-column layout: left = setup, right = run + tune
    left_col = []
    left_col.append(Paragraph("1. You need", styles["h"]))
    for it in [
        "Xreal One Pro + USB-C cable (data)",
        "Hello Robot Stretch 3 reachable on LAN (default 172.22.243.8)",
        "Linux PC, Python 3.7+",
    ]:
        left_col.append(Paragraph(f"• {it}", styles["body"]))

    left_col.append(Paragraph("2. PC — one-time setup", styles["h"]))
    left_col.append(Paragraph(
        "Clone repo, install deps, enable glasses ethernet (Settings → Developer → Ethernet).",
        styles["body"],
    ))
    left_col.append(Paragraph(
        "git clone &lt;repo&gt; ~/lab/life_home/xreal_head_control<br/>"
        "cd ~/lab/life_home/xreal_head_control<br/>"
        "pip install -r requirements.txt<br/>"
        "ping 169.254.2.1   # must reply",
        styles["code"],
    ))

    left_col.append(Paragraph("3. Robot — start two SSH terminals", styles["h"]))
    left_col.append(Paragraph(
        "<b>scp</b> stretch_relay.py to the robot once:",
        styles["body"],
    ))
    left_col.append(Paragraph(
        "scp stretch_relay.py hello-robot@172.22.243.8:~/het_ros2_ws/",
        styles["code"],
    ))
    left_col.append(Paragraph(
        "<b>Terminal A</b> (driver):",
        styles["body"],
    ))
    left_col.append(Paragraph(
        "ssh hello-robot@172.22.243.8   # pw: &lt;ask lab admin&gt;<br/>"
        "conda deactivate<br/>"
        "ros2 launch stretch_core stretch_driver.launch.py",
        styles["code"],
    ))
    left_col.append(Paragraph(
        "<b>Terminal B</b> (relay):",
        styles["body"],
    ))
    left_col.append(Paragraph(
        "ssh hello-robot@172.22.243.8<br/>"
        "conda deactivate<br/>"
        "python3 ~/het_ros2_ws/stretch_relay.py<br/>"
        "# wait for: \"Waiting for connection on port 9090...\"",
        styles["code"],
    ))

    right_col = []
    right_col.append(Paragraph("4. PC — run the bridge", styles["h"]))
    right_col.append(Paragraph(
        "cd ~/lab/life_home/xreal_head_control<br/>"
        "python3 stretch_head_control.py",
        styles["code"],
    ))
    right_col.append(Paragraph(
        "Hold the glasses still ~0.5 s for calibration → put them on → press <b>T</b> to "
        "zero your view. Move your head, robot follows.",
        styles["body"],
    ))

    right_col.append(Paragraph("5. Keys", styles["h"]))
    right_col.append(Paragraph(
        "<b>M</b> toggle LOOK/DRIVE • <b>SPACE</b> hold to drive (DRIVE) • "
        "<b>T</b> zero view • <b>R</b> recalibrate • <b>L</b> lock • <b>Q</b> quit",
        styles["body"],
    ))

    right_col.append(Paragraph("6. Tune (top of stretch_head_control.py)", styles["h"]))
    right_col.append(Paragraph(
        "STRETCH_IP        = \"172.22.243.8\"  # robot IP<br/>"
        "HEAD_PAN_SCALE    = 0.025           # ↑ = more sensitive L/R<br/>"
        "HEAD_TILT_SCALE   = 0.015           # ↑ = more sensitive U/D<br/>"
        "# Wrong direction? flip sign on line 163 or 164",
        styles["code"],
    ))

    right_col.append(Paragraph("7. Common fixes", styles["h"]))
    for it in [
        "Connection refused → relay not running on robot.",
        "Trajectory server not found → driver not running, or `ros2 action list` shows different name.",
        "rclpy import error → run `conda deactivate` on the robot first.",
        "Cannot ping 169.254.2.1 → enable ethernet in glasses dev menu / try another USB-C port.",
        "Drift → press R, hold still.",
    ]:
        right_col.append(Paragraph(f"• {it}", styles["body"]))

    right_col.append(Paragraph("8. Files at a glance", styles["h"]))
    right_col.append(Paragraph(
        "<b>PC:</b> stretch_head_control.py · src/imu_reader_fixed.py · src/head_tracker.py<br/>"
        "<b>Robot:</b> stretch_relay.py (in ~/het_ros2_ws/)<br/>"
        "<b>Test:</b> imu_server.py + imu_viz.html (3D cube in browser)",
        styles["body"],
    ))

    cols = Table(
        [[left_col, right_col]],
        colWidths=[3.65 * inch, 3.65 * inch],
    )
    cols.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LINEBETWEEN", (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
    ]))
    story.append(cols)

    story.append(HRFlowable(width="100%", thickness=0.4,
                            color=colors.HexColor("#CCCCCC"),
                            spaceBefore=4, spaceAfter=2))
    story.append(Paragraph(
        "Architecture: <b>[Glasses]</b> →USB-C TCP→ <b>[PC bridge]</b> →TCP JSON :9090→ "
        "<b>[Robot relay]</b> →ROS 2 action→ head pan/tilt joints. "
        "See Stretch_GazeBot_Reproduction_Guide.pdf for full detail.",
        ParagraphStyle("foot", parent=base["Normal"],
                       fontSize=7.5, leading=9,
                       textColor=colors.HexColor("#666666")),
    ))

    doc.build(story)
    return out


if __name__ == "__main__":
    a = build_detailed()
    b = build_one_pager()
    print("Wrote:")
    print(" ", a)
    print(" ", b)

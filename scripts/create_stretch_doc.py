from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import datetime

doc = Document()

# --- Styles ---
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# --- Title Page ---
for _ in range(6):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('Hello Robot Stretch\nComplete Options & Research Guide')
run.bold = True
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0, 102, 153)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run(f'Prepared: {datetime.date.today().strftime("%B %d, %Y")}')
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(100, 100, 100)

doc.add_page_break()

# --- Table of Contents placeholder ---
doc.add_heading('Table of Contents', level=1)
toc_items = [
    '1. Executive Summary',
    '2. Product Lineup Overview',
    '3. Stretch 3 — Current Flagship',
    '4. Stretch 2 (RE2) — Previous Generation',
    '5. Stretch RE1 — Original Model',
    '6. Generation Comparison Table',
    '7. Accessories & Add-Ons',
    '8. Upgrade Paths',
    '9. Software & Open-Source Ecosystem',
    '10. GitHub Repositories',
    '11. Use Cases & Applications',
    '12. Pricing Summary',
    '13. Sources & References',
]
for item in toc_items:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(2)

doc.add_page_break()

# ==============================
# 1. EXECUTIVE SUMMARY
# ==============================
doc.add_heading('1. Executive Summary', level=1)
doc.add_paragraph(
    'Hello Robot is a robotics company founded by former Georgia Tech researchers that designs '
    'open-source mobile manipulators for research, education, and assistive applications. Their '
    'flagship product line, Stretch, is a lightweight, affordable robot designed to operate safely '
    'in human environments such as homes, offices, and care facilities.'
)
doc.add_paragraph(
    'This document provides a comprehensive overview of all available Hello Robot Stretch models, '
    'accessories, upgrade options, software ecosystem, and use cases to assist in evaluating the '
    'platform for research or deployment purposes.'
)

# ==============================
# 2. PRODUCT LINEUP OVERVIEW
# ==============================
doc.add_heading('2. Product Lineup Overview', level=1)
doc.add_paragraph(
    'Hello Robot has released three generations of the Stretch robot:'
)
items = [
    ('Stretch RE1', 'The original research edition, launched July 2020.'),
    ('Stretch RE2 / Stretch 2', 'Second generation with improved arm and wrist capabilities.'),
    ('Stretch 3', 'Current flagship model (launched 2024), with significant hardware and sensor upgrades.'),
]
for name, desc in items:
    p = doc.add_paragraph()
    run = p.add_run(name + ': ')
    run.bold = True
    p.add_run(desc)

# ==============================
# 3. STRETCH 3 — CURRENT FLAGSHIP
# ==============================
doc.add_heading('3. Stretch 3 — Current Flagship', level=1)

doc.add_heading('3.1 Overview', level=2)
doc.add_paragraph(
    'Stretch 3 is the latest and most capable model in the Stretch lineup, priced at $24,950 USD. '
    'It includes several features that were previously optional add-ons, such as the dexterous wrist kit '
    'and the gripper-mounted depth camera.'
)

doc.add_heading('3.2 Physical Specifications', level=2)
specs_table = doc.add_table(rows=1, cols=2, style='Light Grid Accent 1')
specs_table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = specs_table.rows[0].cells
hdr[0].text = 'Specification'
hdr[1].text = 'Value'
specs = [
    ('Weight', '24.5 kg (54 lbs)'),
    ('Base Footprint', '33 × 34 cm'),
    ('Height', '141 cm'),
    ('Arm Vertical Reach', '43.3 inches (110 cm)'),
    ('Arm Horizontal Reach', '20.5 inches (52 cm)'),
    ('Payload Capacity', '2 kg'),
    ('Arm Construction', 'Aluminum telescoping (5 links)'),
    ('Gripper Opening', '40% wider than previous generations'),
    ('Runtime', '2–5 hours'),
    ('Degrees of Freedom', '6 DOF (with dexterous wrist)'),
    ('Drive', 'Differential drive base'),
]
for spec, val in specs:
    row = specs_table.add_row().cells
    row[0].text = spec
    row[1].text = val

doc.add_heading('3.3 Sensors & Perception', level=2)
sensors = [
    'Intel RealSense D435if Depth + RGB Camera — mounted on pan-tilt head, wide FOV, range up to 10m, active IR projector and global shutter depth sensor',
    'Intel RealSense D405 Depth Camera — mounted on gripper, ideal range 7–50 cm for in-hand manipulation',
    '140° FOV RGB Camera — part of pan-tilt unit for situational awareness and teleoperation',
    'BNO085 9-DOF IMU — on the base for orientation and motion sensing',
    'ADXL343 3-axis Accelerometer — on the wrist for bump and tap detection',
    'Four Cliff Sensors — for detection of stairs, thresholds, and drop-offs',
]
for s in sensors:
    doc.add_paragraph(s, style='List Bullet')

doc.add_heading('3.4 Computing', level=2)
doc.add_paragraph(
    'Stretch 3 features an Intel NUC 12 with an Intel Core i5-1240P processor (12 physical cores), '
    'providing 2–3x more computation than the previous generation NUC with the Intel Core i5-8257U (4 cores). '
    'This enables on-board neural network inference, SLAM, and real-time perception.'
)

doc.add_heading('3.5 Software', level=2)
sw_items = [
    'ROS 2 (Humble) support with Nav2 navigation stack',
    'Python SDK (stretch_body) for direct hardware control',
    'Stretch AI — high-level AI behaviors and task planning',
    'Open-source codebase (Apache 2.0 license)',
    'Ubuntu 22.04 LTS pre-installed',
]
for s in sw_items:
    doc.add_paragraph(s, style='List Bullet')

# ==============================
# 4. STRETCH 2 (RE2)
# ==============================
doc.add_heading('4. Stretch 2 (RE2) — Previous Generation', level=1)
doc.add_paragraph(
    'The Stretch RE2 (also marketed as Stretch 2) was the second-generation model featuring:'
)
re2_features = [
    '5 telescoping carbon fiber arm links on rollers',
    'Proprietary stepper motor drive train with closed-loop control and current sensing',
    'Contact sensitivity during motion for safe human interaction',
    'Optional Dex Wrist add-on (pitch and roll DOF)',
    'Intel NUC with Core i5-8257U (4 cores)',
    '6 M4 threaded inserts on base for mounting user accessories (e.g., tray)',
]
for f in re2_features:
    doc.add_paragraph(f, style='List Bullet')
doc.add_paragraph(
    'Stretch 2 is no longer sold as a new unit but can be upgraded to near-Stretch 3 capability '
    'via the Stretch 2 Upgrade Kit.'
)

# ==============================
# 5. STRETCH RE1
# ==============================
doc.add_heading('5. Stretch RE1 — Original Model', level=1)
doc.add_paragraph(
    'The Stretch RE1, launched in July 2020, was Hello Robot\'s debut product — a compact, low-cost '
    'mobile manipulator designed for researchers. Key characteristics:'
)
re1_features = [
    '4 degrees of freedom (telescoping arm, prismatic lift, differential drive base)',
    '50 cm horizontal arm reach',
    '110 cm vertical lift reach',
    '34 × 34 cm compact base footprint',
    'Lightweight and designed for safe operation around people in home/office environments',
]
for f in re1_features:
    doc.add_paragraph(f, style='List Bullet')

# ==============================
# 6. GENERATION COMPARISON TABLE
# ==============================
doc.add_heading('6. Generation Comparison Table', level=1)
comp_table = doc.add_table(rows=1, cols=4, style='Light Grid Accent 1')
comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = comp_table.rows[0].cells
hdr[0].text = 'Feature'
hdr[1].text = 'RE1'
hdr[2].text = 'RE2 / Stretch 2'
hdr[3].text = 'Stretch 3'
comparisons = [
    ('Arm Material', 'Carbon fiber', 'Carbon fiber', 'Aluminum'),
    ('Gripper Camera', 'No', 'Optional', 'Standard (D405)'),
    ('Dexterous Wrist', 'No', 'Optional add-on', 'Included'),
    ('Head Cameras', '1 (D435i)', '1 (D435i)', '2 (D435if + 140° RGB)'),
    ('Compute', 'NUC (i5-8257U)', 'NUC (i5-8257U)', 'NUC 12 (i5-1240P)'),
    ('CPU Cores', '4', '4', '12'),
    ('ROS Support', 'ROS 1 (Melodic/Noetic)', 'ROS 1/2', 'ROS 2 (Humble)'),
    ('Nav Stack', 'ROS Nav', 'ROS Nav/Nav2', 'Nav2'),
    ('Gripper Width', 'Standard', 'Standard', '40% wider'),
    ('Price (at launch)', '~$17,950', '~$19,950', '$24,950'),
    ('Status', 'Discontinued', 'Upgrade available', 'Currently sold'),
]
for row_data in comparisons:
    row = comp_table.add_row().cells
    for i, val in enumerate(row_data):
        row[i].text = val

# ==============================
# 7. ACCESSORIES & ADD-ONS
# ==============================
doc.add_heading('7. Accessories & Add-Ons', level=1)

doc.add_heading('7.1 Dexterous Teleop Kit — $295 USD', level=2)
doc.add_paragraph(
    'Allows control of the full 6-DOF pose and grasp of the Stretch 3 gripper in real-time. '
    'Ideal for collecting dexterous manipulation training data for learning-based approaches.'
)
teleop_items = [
    'Camera for operator view',
    'Light ring for visual feedback',
    'Teleoperation tool (hand-held controller)',
    'Open-source teleoperation software (stretch_dex_teleop)',
]
for t in teleop_items:
    doc.add_paragraph(t, style='List Bullet')

doc.add_heading('7.2 WiFi Access Point — $995 USD', level=2)
doc.add_paragraph(
    'A NETGEAR Nighthawk Pro Gaming Router, preconfigured and tested at the factory for Stretch. '
    'Simplifies connecting Stretch to a remote GPU workstation or laptop for offboard computation.'
)

doc.add_heading('7.3 Community Tool Share', level=2)
doc.add_paragraph(
    'The stretch_tool_share GitHub repository contains alternative grippers, tools, and accessories '
    'designed by both Hello Robot and the community. Examples include custom end-effectors, trays, '
    'and specialized manipulation tools.'
)

# ==============================
# 8. UPGRADE PATHS
# ==============================
doc.add_heading('8. Upgrade Paths', level=1)

doc.add_heading('8.1 Stretch 2 Upgrade Kit — $4,950 USD', level=2)
doc.add_paragraph(
    'Existing Stretch 2 owners can upgrade their robot to near-Stretch 3 capability. The kit includes:'
)
upgrade_items = [
    'DexWrist 3 (new dexterous wrist mechanism)',
    'Stretch Gripper 3 with integrated Intel RealSense D405 depth camera',
    'Wide-angle head camera',
]
for u in upgrade_items:
    doc.add_paragraph(u, style='List Bullet')

doc.add_paragraph(
    'After upgrading, the Stretch 2 becomes kinematically identical to a Stretch 3, making training '
    'data fully transferable between the two. The only remaining difference is the older NUC computer '
    'with somewhat lower computational performance.'
)

# ==============================
# 9. SOFTWARE & OPEN-SOURCE ECOSYSTEM
# ==============================
doc.add_heading('9. Software & Open-Source Ecosystem', level=1)
doc.add_paragraph(
    'Nearly all software Hello Robot writes for Stretch is open-source and freely available. '
    'The ecosystem includes:'
)

doc.add_heading('9.1 Core Software Stack', level=2)
sw_stack = [
    ('stretch_body', 'Python SDK for direct hardware interaction and low-level control'),
    ('stretch_ros2', 'ROS 2 Humble packages for navigation, manipulation, and perception'),
    ('stretch_ros', 'Legacy ROS 1 Noetic packages (for RE1/RE2)'),
    ('stretch_ai', 'High-level AI behaviors, task planning, and intelligent manipulation for Stretch 3'),
    ('stretch_firmware', 'Arduino-based firmware for onboard microcontrollers'),
    ('stretch_install', 'Installation and setup scripts'),
]
for name, desc in sw_stack:
    p = doc.add_paragraph()
    run = p.add_run(name + ': ')
    run.bold = True
    run.font.name = 'Consolas'
    p.add_run(desc)

doc.add_heading('9.2 Stretch AI', level=2)
doc.add_paragraph(
    'Stretch AI is a dedicated software package designed for building intelligent robot behaviors. '
    'It supports autonomous navigation, object manipulation, voice interaction, and learning from '
    'demonstration. Licensed under Apache 2.0.'
)

# ==============================
# 10. GITHUB REPOSITORIES
# ==============================
doc.add_heading('10. GitHub Repositories', level=1)
doc.add_paragraph(
    'The Hello Robot GitHub organization (github.com/hello-robot) hosts 34+ repositories. '
    'Key repositories include:'
)

repo_table = doc.add_table(rows=1, cols=3, style='Light Grid Accent 1')
repo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = repo_table.rows[0].cells
hdr[0].text = 'Repository'
hdr[1].text = 'Description'
hdr[2].text = 'URL'
repos = [
    ('stretch_ai', 'AI behaviors & intelligent manipulation', 'github.com/hello-robot/stretch_ai'),
    ('stretch_ros2', 'ROS 2 Humble packages', 'github.com/hello-robot/stretch_ros2'),
    ('stretch_ros', 'ROS 1 Noetic packages', 'github.com/hello-robot/stretch_ros'),
    ('stretch_body', 'Python hardware SDK', 'github.com/hello-robot/stretch_body'),
    ('stretch_tutorials', 'Programming tutorials', 'github.com/hello-robot/stretch_tutorials'),
    ('stretch_firmware', 'Arduino firmware', 'github.com/hello-robot/stretch_firmware'),
    ('stretch_tool_share', 'Community grippers & accessories', 'github.com/hello-robot/stretch_tool_share'),
    ('stretch_dex_teleop', 'Dexterous teleoperation code', 'github.com/hello-robot/stretch_dex_teleop'),
    ('stretch_install', 'Installation scripts', 'github.com/hello-robot/stretch_install'),
    ('stretch_community', 'Community portal & resources', 'github.com/hello-robot/stretch_community'),
    ('stretch_hardware_guides', 'Hardware user manuals', 'github.com/hello-robot/stretch_hardware_guides'),
    ('stretch_diagnostics', 'Diagnostic tools', 'github.com/hello-robot/stretch_diagnostics'),
    ('stretch_factory', 'Factory debug & calibration', 'github.com/hello-robot/stretch_factory'),
]
for name, desc, url in repos:
    row = repo_table.add_row().cells
    row[0].text = name
    row[1].text = desc
    row[2].text = url

# ==============================
# 11. USE CASES & APPLICATIONS
# ==============================
doc.add_heading('11. Use Cases & Applications', level=1)

doc.add_heading('11.1 Research & Academia', level=2)
doc.add_paragraph(
    'Stretch is one of the most widely-used platforms for indoor mobile manipulation research. '
    'Publications regularly appear at top conferences including ICRA, IROS, CoRL, HRI, and NeurIPS.'
)
research_uses = [
    'Embodied AI and learning from demonstration',
    'Autonomous navigation in cluttered indoor environments',
    'Object grasping and manipulation',
    'Human-robot interaction studies',
    'SLAM and perception research',
]
for r in research_uses:
    doc.add_paragraph(r, style='List Bullet')

doc.add_heading('11.2 Assistive & Healthcare', level=2)
healthcare_uses = [
    'NIH-funded study: Assisting older adults with early-stage dementia to age in place',
    'ALS Association partnership: Researching specific needs of ALS patients',
    'Physical therapy: Leading stretching exercise games for older adults with Parkinson\'s Disease',
    'General home assistance: picking up items, moving laundry, fetching objects',
]
for h in healthcare_uses:
    doc.add_paragraph(h, style='List Bullet')

doc.add_heading('11.3 Education', level=2)
doc.add_paragraph(
    'Hello Robot actively supports educational use. Students work with the same tools as top '
    'researchers, and the open-source nature of the platform makes it suitable for university '
    'courses in robotics, AI, and computer vision.'
)

doc.add_heading('11.4 Emerging Applications', level=2)
emerging = [
    'Precision agriculture',
    'Retail (shelf stocking, inventory)',
    'Workplace sanitation (wiping surfaces)',
    'Entertainment and social interaction',
]
for e in emerging:
    doc.add_paragraph(e, style='List Bullet')

# ==============================
# 12. PRICING SUMMARY
# ==============================
doc.add_heading('12. Pricing Summary', level=1)
price_table = doc.add_table(rows=1, cols=3, style='Light Grid Accent 1')
price_table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr = price_table.rows[0].cells
hdr[0].text = 'Item'
hdr[1].text = 'Price (USD)'
hdr[2].text = 'Notes'
prices = [
    ('Stretch 3 (Robot)', '$24,950', 'Current flagship, includes dex wrist & gripper camera'),
    ('Stretch 2 Upgrade Kit', '$4,950', 'Upgrades Stretch 2 to near-Stretch 3 capability'),
    ('Dexterous Teleop Kit', '$295', '6-DOF teleoperation for data collection'),
    ('WiFi Access Point', '$995', 'Pre-configured NETGEAR Nighthawk router'),
]
for item, price, note in prices:
    row = price_table.add_row().cells
    row[0].text = item
    row[1].text = price
    row[2].text = note

# ==============================
# 13. SOURCES & REFERENCES
# ==============================
doc.add_heading('13. Sources & References', level=1)
sources = [
    ('Hello Robot — Stretch 3 Product Page', 'https://hello-robot.com/stretch-3-product'),
    ('Hello Robot — Purchase Page', 'https://hello-robot.com/purchase'),
    ('Hello Robot — Stretch Accessories', 'https://hello-robot.com/stretch-accessories'),
    ('Hello Robot — Stretch 3 What\'s New', 'https://hello-robot.com/stretch-3-whats-new'),
    ('Hello Robot — Stretch 2 Upgrade Kit', 'https://hello-robot.com/stretch-2-upgrade'),
    ('Hello Robot — Dexterous Teleop Kit', 'https://hello-robot.com/stretch-dex-teleop-kit'),
    ('Hello Robot — WiFi Access Point', 'https://hello-robot.com/stretch-access-point'),
    ('Hello Robot — Education', 'https://hello-robot.com/stretch-education'),
    ('Stretch 3 Hardware Guide (Docs)', 'https://docs.hello-robot.com/0.3/hardware/hardware_guide_stretch_3/'),
    ('Stretch RE2 Hardware Guide (Docs)', 'https://docs.hello-robot.com/0.2/stretch-hardware-guides/docs/hardware_guide_re2/'),
    ('Hello Robot GitHub Organization', 'https://github.com/hello-robot'),
    ('Stretch AI Repository', 'https://github.com/hello-robot/stretch_ai'),
    ('IEEE Spectrum — Stretch 3 Review', 'https://spectrum.ieee.org/hello-robot-stretch-3'),
    ('The Robot Report — Stretch 3', 'https://www.therobotreport.com/stretch-3-mobile-manipulator-hello-robot-designed-open-source-development/'),
    ('The Robot Report — Assistive Robots', 'https://www.therobotreport.com/rbr50-company-2025/stretch-3-brings-assistive-robots-into-the-home/'),
    ('Stretch Community Resources', 'https://docs.hello-robot.com/0.3/getting_started/community_resources/'),
]
for title, url in sources:
    p = doc.add_paragraph()
    run = p.add_run(title)
    run.bold = True
    p.add_run(f'\n{url}')
    p.paragraph_format.space_after = Pt(4)

# Save
output_path = '/home/het/lab/life_home/Hello_Robot_Stretch_Research_Guide.docx'
doc.save(output_path)
print(f'Document saved to: {output_path}')

# -*- coding: utf-8 -*-
"""Figure 4: functional architecture of the three dual-track
concepts as Perception-Cognition-Action loops with an acceptance layer
(Reviewer 3, comment 1). Content is taken verbatim from the disclosed
condition-A concept sheets (Supplementary Note 1)."""
import sys, io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "figures", "Figure4.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.rcParams.update({"font.family": "Arial", "figure.dpi": 300,
                     "savefig.dpi": 300, "savefig.bbox": "tight"})

C_P, C_C, C_A, C_S, C_B = "#dce8f5", "#fdf3d8", "#e2efe4", "#ededed", "#f7e2e2"
E_P, E_C, E_A, E_S, E_B = "#2563a8", "#c9a227", "#2f7d5e", "#777777", "#c0394b"
GREY = "#444444"
FS = 7.8
LH = 0.255

CONCEPTS = [
    dict(
        title="a  SinkStation Pro (counter-anchored dish specialist)",
        attrs="A1 linear screw · A2 dexterous sealed hand · A3 visual servoing · A4 vision + tactile · A5 sealed shell\n"
              "B1 dishes · B2 voice · B3 visible safety controls · B4 brand credibility",
        perception=["Head RGB-D + wrist cameras:", "segmentation / 6-DoF pose of wet,", "specular tableware",
                    "Tactile fingertip arrays:", "contact geometry, incipient slip"],
        cognition=["Task planner: clear → rinse →", "rack → store (learned primitives)",
                   "60 Hz visual-servoing controller", "Force layer: slip → grip-force update",
                   "Safety node: workspace envelope,", "speed cap 0.5 m/s near people"],
        action=["Two 7-DoF ball-screw arms", "(~3 kg payload, ±0.5 mm)",
                "Two 12-DoF IP65 dexterous hands", "Counter anchor, sealed torso shell",
                "with thermal management"],
        structure=["Faceless, appliance-styled torso; quick-release counter anchor; LLM voice interface"],
        accept=["Anchored base: cannot approach the user", "Projected 'active-zone' line makes the safety envelope visible",
                "Slow-down / pause when a person enters the zone; counter-height e-stop",
                "No anthropomorphic head → sidesteps the uncanny valley", "Narrow, verifiable scope → claims match observable performance"],
    ),
    dict(
        title="b  LaundryLoop (laundry specialist with compliant grippers)",
        attrs="A1 linear screw · A2 soft gripper · A3 visual servoing · A4 tactile + vision · A5 sealed shell\n"
              "B1 laundry · B2 voice · B3 visible safety controls · B4 brand credibility",
        perception=["Torso + wrist RGB-D cameras:", "cloth-state network (class, edges,", "corners, wrinkle field)",
                    "Tactile pads in gripper jaws:", "thickness, layer count, grip security"],
        cognition=["Hierarchical planner: classify", "garment → select skill (unfold,",
                   "fold, hang, load / unload)", "30 Hz servoing re-targets grasp",
                   "points as fabric deforms", "Grip failure → re-perceive, re-grasp"],
        action=["Two 7-DoF screw-actuated arms", "(~2 kg), compliant wrists",
                "Tendon-driven soft grippers,", "0.5-15 N bounded pinch force",
                "Wheeled base ≤ 0.6 m/s"],
        structure=["Humidity-tolerant sealed shell with thermal management; faceless appliance styling"],
        accept=["Hardware 'hands-off' lever mechanically cuts arm power", "Illuminated e-stop; pinch force bounded by construction",
                "Faceless body → no uncanny-valley trigger", "Co-branding with an established appliance maker transfers trust",
                "Announces each step by voice; declines delicate items"],
    ),
    dict(
        title="c  Errand Mate Mini (small, low-cost fetch-and-carry biped)",
        attrs="A1 electric geared motors · A2 underactuated hand · A3 ZMP balance · A4 obstacle mapping · A5 self-docking\n"
              "B1 affordability + errands · B2 voice · B3 predictable, legible behaviour · B4 capability milestones",
        perception=["Stereo depth + dual fisheye", "cameras → local elevation and",
                    "obstacle map, persistent home SLAM", "Microphone array (spoken requests)", "IMU, leg joint-torque sensing"],
        cognition=["LLM interpreter: errand → waypoints", "+ grasp goals",
                   "ZMP / capture-point gait engine with", "model-predictive step placement",
                   "Grasp planner: approach pose only", "(hand adapts mechanically)"],
        action=["1.2 m, ~30 kg biped, 23-27 DoF", "quasi-direct-drive geared joints",
                "One-motor underactuated 3-finger", "hands, 2 kg carry payload",
                "Walking ≤ 0.5 m/s indoors; self-dock"],
        structure=["Child-height but explicitly robotic styling; chest LED intent display; commodity supply chain"],
        accept=["Sub-adult stature: cannot loom over the user", "Every action announced and mirrored on the intent display",
                "Slow, rule-governed motion; user-defined no-go zones", "Monthly unedited milestone videos answer 'no staging'",
                "Target price in the used-car band (affordability cluster)"],
    ),
]

fig, axes = plt.subplots(3, 1, figsize=(10.0, 15.0))
for ax, c in zip(axes, CONCEPTS):
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.75); ax.axis("off")
    ax.text(0.05, 4.62, c["title"], fontsize=FS + 2.2, fontweight="bold", va="center")
    ax.text(0.05, 4.22, c["attrs"], fontsize=FS - 0.3, va="center", color="#333333", linespacing=1.35)

    def box(x, y, w, h, head, lines, fc, ec):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03", fc=fc, ec=ec, lw=1.3))
        ax.text(x + w / 2, y + h - 0.21, head, ha="center", va="center", fontsize=FS + 0.6, fontweight="bold", color=ec)
        for i, ln in enumerate(lines):
            ax.text(x + 0.12, y + h - 0.48 - i * LH, ln, ha="left", va="center", fontsize=FS)

    ytop, hh = 1.8, 2.1
    box(0.1, ytop, 3.05, hh, "Perception (sensing)", c["perception"], C_P, E_P)
    box(3.45, ytop, 3.15, hh, "Cognition (decision)", c["cognition"], C_C, E_C)
    box(6.9, ytop, 3.0, hh, "Action (actuation)", c["action"], C_A, E_A)
    # forward arrows P -> C -> A
    for x1, x2 in ((3.15, 3.45), (6.6, 6.9)):
        ax.add_patch(FancyArrowPatch((x1, ytop + hh / 2), (x2, ytop + hh / 2), arrowstyle="-|>",
                                     mutation_scale=13, color=GREY, lw=1.4))
    # feedback loop A -> P (environment) beneath the boxes
    ax.plot([8.4, 8.4, 1.6, 1.6], [ytop, ytop - 0.22, ytop - 0.22, ytop - 0.02], color=GREY, lw=1.1, ls="--")
    ax.add_patch(FancyArrowPatch((1.6, ytop - 0.1), (1.6, ytop), arrowstyle="-|>", mutation_scale=11, color=GREY, lw=1.1, ls="--"))
    ax.text(5.0, ytop - 0.22, "closed loop through the environment (contact, slip, object state, map updates)",
            fontsize=FS - 0.6, ha="center", va="center", color=GREY, bbox=dict(fc="white", ec="none", pad=1))
    # structure strip
    ax.add_patch(FancyBboxPatch((0.1, 1.02), 9.8, 0.36, boxstyle="round,pad=0.03", fc=C_S, ec=E_S, lw=1.1))
    ax.text(0.22, 1.2, "Structure / embodiment:", fontsize=FS, fontweight="bold", va="center", color=E_S)
    ax.text(1.95, 1.2, c["structure"][0], fontsize=FS, va="center")
    # acceptance layer
    ah = 0.92
    ax.add_patch(FancyBboxPatch((0.1, 0.05), 9.8, ah, boxstyle="round,pad=0.03", fc=C_B, ec=E_B, lw=1.3))
    ax.text(0.22, 0.05 + ah - 0.16, "Acceptance layer (discourse-derived requirements, Track B)", fontsize=FS + 0.3,
            fontweight="bold", va="center", color=E_B)
    col = [c["accept"][:3], c["accept"][3:]]
    for j, items in enumerate(col):
        for i, ln in enumerate(items):
            ax.text(0.25 + j * 4.9, 0.05 + ah - 0.4 - i * 0.22, "• " + ln, fontsize=FS - 0.6, va="center")

fig.subplots_adjust(hspace=0.08)
fig.savefig(OUT)
print("saved", OUT)

# -*- coding: utf-8 -*-
"""Figure 5: morphological-chart comparison of the nine
evaluated concepts (dual-track vs technology-push vs unconstrained) across
the 36 attributes of the dual-track matrix. Selections are taken from the
disclosed concept sheets (Supplementary Note 1)."""
import sys, io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "figures", "Figure5.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.rcParams.update({"font.family": "Arial", "figure.dpi": 300,
                     "savefig.dpi": 300, "savefig.bbox": "tight"})

DIMS = [
    ("A1 Actuation", ["Electric geared motor drive", "Hydraulic actuator", "Pneumatic artificial muscle", "Linear screw actuator"]),
    ("A2 Manipulation", ["Dexterous multi-finger hand", "Underactuated linkage hand", "Modular arm assembly", "Soft gripper"]),
    ("A3 Control", ["Model-based balance (ZMP/centroid)", "Whole-body motion planning", "Reinforcement-learning locomotion", "Vision-guided follow-up control"]),
    ("A4 Perception", ["3D point-cloud sensing (LiDAR/depth)", "Vision-based object recognition", "Obstacle detection and mapping", "Tactile/force sensing"]),
    ("A5 Structure", ["Expressive facial head module", "Protective shell, thermal management", "Integrated charging/docking", "Human-friendly exterior styling"]),
    ("B1 Task needs", ["Household chores (dishes/tidying)", "Clothing and laundry handling", "Affordable consumer price point", "Personal errand assistance"]),
    ("B2 Interaction", ["Natural voice conversation", "Human-like speech prosody", "Real-time speech-to-speech reasoning", "Expressive face/gesture cues"]),
    ("B3 Acceptance", ["Calibrated human-likeness (uncanny-safe)", "Visible safety controls", "Capability transparency (no staging)", "Predictable, legible behaviour"]),
    ("B4 Projection", ["Brand credibility", "Futuristic tech symbolism", "Pop-culture-aware positioning", "Demonstrable capability milestones"]),
]
# concept -> set of (dim index, attribute index) taken from the concept sheets
CONCEPTS = [
    ("SinkStation Pro", "DT", {(0, 3), (1, 0), (2, 3), (3, 1), (3, 3), (4, 1), (5, 0), (6, 0), (7, 1), (8, 0)}),
    ("LaundryLoop", "DT", {(0, 3), (1, 3), (2, 3), (3, 3), (3, 1), (4, 1), (5, 1), (6, 0), (7, 1), (8, 0)}),
    ("Errand Mate Mini", "DT", {(0, 0), (1, 1), (2, 0), (3, 2), (4, 2), (5, 2), (5, 3), (6, 0), (7, 3), (8, 3)}),
    ("ATLASWORK", "TP", {(0, 0), (0, 3), (1, 1), (2, 1), (2, 0), (3, 0), (4, 2)}),
    ("DEXTRA-LAB", "TP", {(0, 0), (0, 3), (1, 0), (2, 3), (2, 1), (3, 1), (3, 3), (4, 2)}),
    ("SENTINEL-24", "TP", {(0, 0), (1, 1), (2, 1), (2, 0), (3, 2), (3, 0), (4, 2), (4, 1)}),
    ("Transparent Household Helper", "UC", {(0, 0), (1, 1), (2, 0), (3, 3), (4, 0), (5, 0), (6, 3), (7, 2), (8, 3)}),
    ("Approachable Consumer Companion", "UC", {(0, 3), (1, 0), (2, 2), (3, 0), (4, 3), (5, 2), (6, 0), (7, 0), (8, 1)}),
    ("Errand-Running Docked Assistant", "UC", {(0, 1), (1, 2), (2, 3), (3, 2), (4, 2), (5, 3), (6, 1), (7, 3), (8, 2)}),
]
COND_COL = {"DT": "#2f7d5e", "TP": "#2563a8", "UC": "#888888"}
COND_NAME = {"DT": "Dual-track (proposed)", "TP": "Technology-push baseline", "UC": "Unconstrained baseline"}

rows = [(d, a) for d, (dn, attrs) in enumerate(DIMS) for a, _ in enumerate(attrs)]
nrow, ncol = len(rows), len(CONCEPTS)
fig, ax = plt.subplots(figsize=(10.2, 11.2))
ax.set_xlim(-5.3, ncol + 0.2); ax.set_ylim(-0.6, nrow + 2.6); ax.axis("off")
FS = 9.0

# column headers (rotated)
for j, (name, cond, _) in enumerate(CONCEPTS):
    ax.text(j + 0.5, nrow + 0.25, name, rotation=60, ha="left", va="bottom", fontsize=FS + 0.3,
            color=COND_COL[cond], fontweight="bold")
# condition brackets above headers
for cond, (j0, j1) in (("DT", (0, 3)), ("TP", (3, 6)), ("UC", (6, 9))):
    ax.plot([j0 + 0.1, j1 - 0.1], [nrow + 0.05, nrow + 0.05], color=COND_COL[cond], lw=2.5, solid_capstyle="butt")

# rows
y = nrow
for d, (dn, attrs) in enumerate(DIMS):
    track_col = "#dce8f5" if dn.startswith("A") else "#f7e2e2"
    ax.add_patch(Rectangle((-5.3, y - len(attrs)), 5.3 + ncol, len(attrs), fc=track_col if d % 2 == 0 else "white",
                           ec="none", alpha=0.55, zorder=0))
    ax.text(-5.25, y - len(attrs) / 2, dn, fontsize=FS, fontweight="bold", va="center", ha="left")
    for a, at in enumerate(attrs):
        yy = y - a - 0.5
        ax.text(-3.55, yy, at, fontsize=FS - 0.6, va="center", ha="left")
        for j, (name, cond, sel) in enumerate(CONCEPTS):
            ax.add_patch(Rectangle((j, yy - 0.5), 1, 1, fc="none", ec="#cccccc", lw=0.5, zorder=1))
            if (d, a) in sel:
                ax.add_patch(Rectangle((j + 0.14, yy - 0.36), 0.72, 0.72, fc=COND_COL[cond], ec="none", zorder=2))
    y -= len(attrs)
    ax.plot([-5.3, ncol], [y, y], color="#999999", lw=0.8, zorder=3)
ax.plot([-5.3, ncol], [nrow - 20, nrow - 20], color="#333333", lw=1.6, zorder=4)
ax.text(ncol + 0.15, nrow - 10, "Track A\n(technological)", fontsize=FS, rotation=270, va="center", ha="left", color="#2563a8")
ax.text(ncol + 0.15, nrow - 28, "Track B\n(experiential)", fontsize=FS, rotation=270, va="center", ha="left", color="#c0394b")

# legend / reading aid
ly = -0.35
for k, cond in enumerate(("DT", "TP", "UC")):
    ax.add_patch(Rectangle((-5.25 + k * 4.4, ly - 0.22), 0.45, 0.45, fc=COND_COL[cond], ec="none"))
    ax.text(-4.7 + k * 4.4, ly, COND_NAME[cond], fontsize=FS, va="center")
fig.savefig(OUT)
print("saved", OUT)

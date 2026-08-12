# -*- coding: utf-8 -*-
"""Fig 1: research framework schematic (replaces the old PPT figure, which
carried outdated K values and typos). Box heights are computed from line
counts so text cannot overflow."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "output" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "Arial", "figure.dpi": 300,
                     "savefig.dpi": 300, "savefig.bbox": "tight"})

C_A, C_B, C_MID, C_OUT = "#dce8f5", "#f7e2e2", "#fdf3d8", "#e2efe4"
E_A, E_B, E_MID, E_OUT = "#2563a8", "#c0394b", "#c9a227", "#2f7d5e"
LH = 0.36  # line height

fig, ax = plt.subplots(figsize=(9.4, 5.8))
ax.set_xlim(0, 10); ax.set_ylim(2.4, 10.45); ax.axis("off")

def box(x, y_top, w, title, lines, fc, ec):
    """Anchor at TOP edge; height derived from content. Returns y_bottom."""
    h = 0.34 + LH * len(lines) + 0.22
    ax.add_patch(FancyBboxPatch((x, y_top - h), w, h,
                                boxstyle="round,pad=0.06", fc=fc, ec=ec, lw=1.5))
    cy = y_top - 0.34
    ax.text(x + w/2, cy, title, ha="center", va="center",
            fontsize=9.5, fontweight="bold")
    for ln in lines:
        cy -= LH
        ax.text(x + w/2, cy, ln, ha="center", va="center", fontsize=8.3)
    return y_top - h

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, color="#444444", lw=1.2))

def step_label(x, y, s):
    ax.text(x, y, s, fontsize=9.5, fontweight="bold", ha="center",
            zorder=6, bbox=dict(fc="white", ec="none", pad=2.0))

# Step 1 (top anchor 9.85)
a1_bot = box(0.35, 9.85, 2.1, "Track A: Supply",
             ["Invention patents", "(WINTELIPS)", "2,638 \u2192 824"], C_A, E_A)
b1_bot = box(2.75, 9.85, 2.1, "Track B: Discourse",
             ["YouTube comments,", "4 verified videos", "3,484 \u2192 2,789"], C_B, E_B)

# Step 2 (top anchor 6.45)
a2_bot = box(0.35, 6.45, 2.1, "Topic modeling",
             ["BERTopic, K*=14", "(NPMI coherence)", "5 technological dims"], C_A, E_A)
b2_bot = box(2.75, 6.45, 2.1, "Topic modeling",
             ["BERTopic, K*=15", "(NPMI coherence)", "4 experiential dims,", "VADER sentiment"], C_B, E_B)

# comparison box
cmp_bot = box(0.35, 4.05, 4.5, "Descriptive two-track comparison",
              ["supply: movement-centric (81.1%)  vs.",
               "discourse: projection + acceptance (80.2%)"], "#f2f2f2", "#888888")

# Step 3 (top anchor 6.45)
m_bot = box(6.1, 6.45, 3.1, "Dual-track morphological matrix",
            ["9 dimensions \u00d7 4 attributes", "(c-TF-IDF top terms,", "synonyms merged)"],
            C_MID, E_MID)

# Step 4
eng_bot = box(6.1, 8.35, 3.1, "Claude LLM inference engine",
              ["3 conditions, independent sessions,", "2-turn protocol, full transcripts"],
              C_MID, E_MID)
out_bot = box(6.1, 9.85, 3.1, "Final outcome",
              ["3 dual-track concepts + baselines"], C_OUT, E_OUT)

arrow(1.4, a1_bot, 1.4, 6.45)
arrow(3.8, b1_bot, 3.8, 6.45)
arrow(1.4, a2_bot, 1.4, 4.05)
arrow(3.8, b2_bot, 3.8, 4.05)
arrow(4.85, 5.6, 6.1, 5.6)
arrow(8.5, 6.45, 8.5, eng_bot)
arrow(8.5, 8.35, 8.5, out_bot)

step_label(2.6, 10.15, "Step 1  Heterogeneous data collection")
step_label(2.6, 6.75, "Step 2  Dimension derivation")
step_label(7.6, 6.75, "Step 3  Matrix construction")
step_label(7.6, 10.15, "Step 4  LLM generative inference")

fig.savefig(FIG / "fig1_framework.png")
print("fig1_framework.png")

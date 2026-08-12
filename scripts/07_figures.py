# -*- coding: utf-8 -*-
"""
Step 6: Manuscript figures from the rebuilt pipeline.

  fig2_coherence.png   - NPMI coherence vs K, both tracks (replaces Figs 2-3)
  fig4_twotrack.png    - descriptive two-track comparison (replaces the
                         radar/gap-score figure; no cross-track arithmetic)
  fig_flow.png         - data preparation flow (PRISMA-style), both tracks

No titles inside figures (captions carry titles). 16.5 cm width class.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Arial", "font.size": 9.5, "axes.spines.top": False,
    "axes.spines.right": False, "axes.axisbelow": True,
    "axes.grid": True, "axes.grid.axis": "y", "grid.linestyle": "--",
    "grid.alpha": 0.35, "figure.dpi": 300, "savefig.dpi": 300,
    "savefig.bbox": "tight"})

C_TECH = "#2563a8"   # supply / Track A
C_USER = "#c0394b"   # discourse / Track B
C_GREY = "#9aa0a6"
C_POS, C_NEU, C_NEG = "#2f7d5e", "#c9cdd3", "#b3413f"

# ---- fig2: coherence curves ---------------------------------------------
ca = pd.read_csv(OUT / "trackA_coherence_curve.csv")
cb = pd.read_csv(OUT / "trackB_coherence_curve.csv")
fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.6))
for ax, cur, col, lab in ((axes[0], ca, C_TECH, "Track A (patents)"),
                          (axes[1], cb, C_USER, "Track B (comments)")):
    ax.plot(cur["K"], cur["coherence_npmi"], "-o", color=col, ms=3.5, lw=1.4)
    k_star = int(cur.loc[cur["coherence_npmi"].idxmax(), "K"])
    y_star = cur["coherence_npmi"].max()
    ax.scatter([k_star], [y_star], s=70, facecolor="none",
               edgecolor="#333333", lw=1.4, zorder=5)
    ax.annotate(f"K* = {k_star}", (k_star, y_star),
                xytext=(10, -14), textcoords="offset points", fontsize=9)
    ax.set_xlabel("Number of topics (K)")
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    ax.set_title(lab, fontsize=9.5, loc="left", pad=8)
axes[0].set_ylabel("NPMI coherence")
fig.tight_layout()
fig.savefig(FIG / "fig2_coherence.png"); plt.close(fig)
print("fig2_coherence.png")

# ---- fig4: descriptive two-track comparison ------------------------------
dimA = pd.read_csv(OUT / "trackA_dimensions.csv").sort_values("share")
dimB = pd.read_csv(OUT / "trackB_dimensions.csv").sort_values("share")
sent = pd.read_csv(OUT / "trackB_dim_sentiment.csv")

fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.9),
                         gridspec_kw={"width_ratios": [1, 1, 1.15]})

ax = axes[0]
ax.barh(dimA["dimension"], dimA["share"], color=C_TECH, edgecolor="white")
for y, v in enumerate(dimA["share"]):
    ax.text(v + 0.8, y, f"{v:.1f}%", va="center", fontsize=8.5)
ax.set_xlabel("Share of patent corpus (%)")
ax.set_xlim(0, dimA["share"].max() * 1.22)
ax.grid(axis="x", linestyle="--", alpha=0.35); ax.grid(axis="y", visible=False)
ax.set_title("a  Technology supply (Track A)", fontsize=9.5, loc="left", pad=4)

ax = axes[1]
ax.barh(dimB["dimension"], dimB["share"], color=C_USER, edgecolor="white")
for y, v in enumerate(dimB["share"]):
    ax.text(v + 1.2, y, f"{v:.1f}%", va="center", fontsize=8.5)
ax.set_xlabel("Share of comment corpus (%)")
ax.set_xlim(0, dimB["share"].max() * 1.22)
ax.grid(axis="x", linestyle="--", alpha=0.35); ax.grid(axis="y", visible=False)
ax.set_title("b  Public discourse (Track B)", fontsize=9.5, loc="left", pad=4)

ax = axes[2]
s = sent.set_index("dimension").loc[
    ["Projection", "Acceptance", "Task needs", "Interaction"]]
left = np.zeros(len(s))
for col, c in (("positive", C_POS), ("neutral", C_NEU), ("negative", C_NEG)):
    ax.barh(s.index, s[col], left=left, color=c, edgecolor="white", label=col)
    left += s[col].values
for y, v in enumerate(s["negative"]):
    ax.text(101, y, f"neg {v:.0f}%", va="center", fontsize=8, color=C_NEG)
ax.set_xlim(0, 118); ax.set_xlabel("VADER sentiment (%)")
ax.invert_yaxis()
ax.grid(axis="x", linestyle="--", alpha=0.35); ax.grid(axis="y", visible=False)
ax.legend(frameon=False, fontsize=8, loc="lower right",
          bbox_to_anchor=(1.0, -0.52), ncol=3)
ax.set_title("c  Sentiment by discourse dimension", fontsize=9.5, loc="left", pad=4)

fig.tight_layout()
fig.savefig(FIG / "fig4_twotrack.png"); plt.close(fig)
print("fig4_twotrack.png")

# ---- fig_flow: PRISMA-style preparation flow -----------------------------
A_STEPS = [("WINTELIPS export", "2,638 records"),
           ("Application date 2020-2024", "1,531  (-1,107)"),
           ("Invention patents only\n(design rights removed)", "1,330  (-201)"),
           ("Family deduplication", "893  (-437)"),
           ("Relevance filter", "824  (-69)")]
B_STEPS = [("Original collection + verified\nAmeca re-collection", "3,484 comments"),
           ("Non-empty, >=3 tokens,\nHTML/URL stripped", "3,257  (-227)"),
           ("English only (langdetect)", "2,801  (-456)"),
           ("Spam/promotion filter\n(final corpus)", "2,789  (-12)")]

fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.6))
for ax, steps, col, lab in ((axes[0], A_STEPS, C_TECH, "Track A: patents"),
                            (axes[1], B_STEPS, C_USER, "Track B: comments")):
    ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    n = len(steps)
    for i, (txt, cnt) in enumerate(steps):
        y = 1 - (i + 0.5) / n
        box = FancyBboxPatch((0.08, y - 0.075), 0.84, 0.15,
                             boxstyle="round,pad=0.012",
                             fc="white", ec=col, lw=1.3)
        ax.add_patch(box)
        ax.text(0.5, y + 0.022, txt, ha="center", va="center", fontsize=8.6)
        ax.text(0.5, y - 0.042, cnt, ha="center", va="center",
                fontsize=8.6, fontweight="bold", color=col)
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((0.5, y - 0.085), (0.5, y - 0.115),
                                         arrowstyle="-|>", mutation_scale=11,
                                         color="#555555"))
    ax.set_title(lab, fontsize=9.5, loc="left")
fig.tight_layout()
fig.savefig(FIG / "fig_flow.png"); plt.close(fig)
print("fig_flow.png")

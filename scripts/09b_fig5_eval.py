# -*- coding: utf-8 -*-
"""
Step 9b: Figure 5 — expert evaluation results (N=20, three conditions).

Panel (a): condition x dimension means with 95% CI (evaluator-level).
Panel (b): per-concept overall means (blinded IDs), colored by condition.

Style follows 07_figures.py (Arial, no in-figure titles, 300 dpi).
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "data" / "eval_responses_deidentified.xlsx"
FIG = ROOT / "output" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Arial", "font.size": 9.5, "axes.spines.top": False,
    "axes.spines.right": False, "axes.axisbelow": True,
    "axes.grid": True, "axes.grid.axis": "y", "grid.linestyle": "--",
    "grid.alpha": 0.35, "figure.dpi": 300, "savefig.dpi": 300,
    "savefig.bbox": "tight"})

KEY = {"R1": "A", "R5": "A", "R8": "A",
       "R4": "B", "R7": "B", "R9": "B",
       "R2": "C", "R3": "C", "R6": "C"}
COND = {"A": "Dual-track", "B": "Technology-push", "C": "Unconstrained"}
COLORS = {"A": "#2563a8", "B": "#7f9bb3", "C": "#c9cdd3"}
DIMS = {"Feasibility": ["Q1", "Q2"], "Market acceptance": ["Q3", "Q4"],
        "Novelty": ["Q5", "Q6"]}
QCOLS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]

xl = pd.ExcelFile(XLSX)
rows = []
for sheet in xl.sheet_names:
    raw = xl.parse(sheet, header=None)
    for r in range(2, 11):
        rec = {"evaluator": str(raw.iloc[0, 1]), "concept": raw.iloc[r, 0]}
        for qi, q in enumerate(QCOLS, start=1):
            rec[q] = float(raw.iloc[r, qi])
        rows.append(rec)
df = pd.DataFrame(rows)
df["condition"] = df["concept"].map(KEY)
for dim, qs in DIMS.items():
    df[dim] = df[qs].mean(axis=1)
df["Overall"] = df[QCOLS].mean(axis=1)
DIMALL = list(DIMS) + ["Overall"]

ev = df.groupby(["evaluator", "condition"])[DIMALL].mean().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.1),
                         gridspec_kw={"width_ratios": [1.25, 1]})

# ---- (a) condition x dimension means with 95% CI -------------------------
ax = axes[0]
x = np.arange(len(DIMALL))
w = 0.26
for i, c in enumerate(["A", "B", "C"]):
    m, err = [], []
    for dim in DIMALL:
        v = ev.loc[ev.condition == c, dim]
        m.append(v.mean())
        err.append(stats.t.ppf(0.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v)))
    ax.bar(x + (i - 1) * w, m, w, color=COLORS[c], edgecolor="white",
           label=COND[c])
    ax.errorbar(x + (i - 1) * w, m, yerr=err, fmt="none", ecolor="#333333",
                elinewidth=1.0, capsize=2.5)
ax.set_xticks(x)
ax.set_xticklabels(DIMALL)
ax.set_ylim(1, 7.6)
ax.set_yticks(range(1, 8))
ax.set_ylabel("Mean rating (1-7)")
ax.legend(frameon=False, fontsize=8.5, loc="upper center", ncol=3,
          bbox_to_anchor=(0.5, 1.02), columnspacing=1.2, handlelength=1.4)
ax.set_title("(a) Condition means with 95% CI (N = 20 experts)",
             fontsize=9.5, loc="left", pad=8)

# ---- (b) per-concept overall means ---------------------------------------
ax = axes[1]
cm = (df.groupby(["condition", "concept"])["Overall"].mean()
        .reset_index().sort_values(["condition", "concept"]))
ypos = np.arange(len(cm))[::-1]
ax.barh(ypos, cm["Overall"], color=[COLORS[c] for c in cm["condition"]],
        edgecolor="white", height=0.72)
for y, v in zip(ypos, cm["Overall"]):
    ax.text(v + 0.06, y, f"{v:.2f}", va="center", fontsize=8)
ax.set_yticks(ypos)
ax.set_yticklabels(cm["concept"])
ax.set_xlim(1, 7)
ax.set_xlabel("Overall mean rating (1-7)")
ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.grid(axis="y", visible=False)
ax.set_title("(b) Per-concept overall means (blinded IDs)",
             fontsize=9.5, loc="left", pad=8)

fig.tight_layout(w_pad=2.0)
fig.savefig(FIG / "fig5_eval.png")
print("written:", FIG / "fig5_eval.png")

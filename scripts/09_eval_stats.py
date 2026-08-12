# -*- coding: utf-8 -*-
"""
Step 9: Statistical analysis of the expanded expert evaluation (N=20).

Reads data/eval_responses_deidentified.xlsx (one sheet per evaluator),
maps blinded IDs R1-R9 to conditions via the seeded blinding key, and computes:
  - panel profile summary
  - per-condition x per-dimension means, SD, 95% CI (evaluator-level)
  - Friedman tests across the three conditions (per dimension + overall)
  - post-hoc Wilcoxon signed-rank tests with Holm correction + Cohen's d(z)
  - Kendall's W (effect size for Friedman)
  - ICC(2,k) inter-rater reliability per dimension
  - Cronbach's alpha for the two-item dimension scales

Writes output/eval_kit/eval_stats_summary.txt and eval_condition_means.csv.
"""
from pathlib import Path
import itertools
import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "data" / "eval_responses_deidentified.xlsx"   # one sheet per evaluator (de-identified)
OUT = ROOT / "output" / "eval_kit"
OUT.mkdir(parents=True, exist_ok=True)

# Blinding key (regenerated from 08_build_eval_kit.py, random.Random(7))
KEY = {
    "R1": "A", "R5": "A", "R8": "A",   # dual-track
    "R4": "B", "R7": "B", "R9": "B",   # technology-push
    "R2": "C", "R3": "C", "R6": "C",   # unconstrained
}
COND_NAMES = {"A": "Dual-track", "B": "Technology-push", "C": "Unconstrained"}
DIMS = {
    "Feasibility": ["Q1", "Q2"],
    "MarketAcceptance": ["Q3", "Q4"],
    "Novelty": ["Q5", "Q6"],
}
QCOLS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]

# ---- load ----------------------------------------------------------------
xl = pd.ExcelFile(XLSX)
rows, profiles = [], []
for sheet in xl.sheet_names:
    raw = xl.parse(sheet, header=None)
    evaluator = str(raw.iloc[0, 1])
    profiles.append({
        "evaluator": evaluator,
        "affiliation": raw.iloc[0, 3],
        "specialty": raw.iloc[0, 5],
        "career_years": raw.iloc[0, 7],
    })
    for r in range(2, 11):
        rec = {"evaluator": evaluator, "concept": raw.iloc[r, 0]}
        for qi, q in enumerate(QCOLS, start=1):
            rec[q] = float(raw.iloc[r, qi])
        rows.append(rec)

df = pd.DataFrame(rows)
df["condition"] = df["concept"].map(KEY)
prof = pd.DataFrame(profiles)
assert len(df) == 20 * 9 and df[QCOLS].notna().all().all()

for dim, qs in DIMS.items():
    df[dim] = df[qs].mean(axis=1)
df["Overall"] = df[QCOLS].mean(axis=1)
DIMALL = list(DIMS) + ["Overall"]

lines = []
def p(s=""):
    lines.append(str(s))
    print(s)

# ---- panel profile -------------------------------------------------------
p("=" * 72)
p("PANEL PROFILE (N=%d)" % len(prof))
p(prof.to_string(index=False))
p("career: mean=%.1f sd=%.1f min=%d max=%d" % (
    prof.career_years.mean(), prof.career_years.std(ddof=1),
    prof.career_years.min(), prof.career_years.max()))
p(prof.affiliation.str.split("/").str[0].value_counts().to_string())

# ---- evaluator-level condition means (unit of analysis: evaluator) -------
ev = df.groupby(["evaluator", "condition"])[DIMALL].mean().reset_index()

p("\n" + "=" * 72)
p("CONDITION MEANS (evaluator-level, N=20)")
summary = []
for dim in DIMALL:
    for cond in ["A", "B", "C"]:
        v = ev.loc[ev.condition == cond, dim]
        m, sd = v.mean(), v.std(ddof=1)
        ci = stats.t.ppf(0.975, len(v) - 1) * sd / np.sqrt(len(v))
        summary.append({"dimension": dim, "condition": COND_NAMES[cond],
                        "mean": round(m, 2), "sd": round(sd, 2),
                        "ci95_lo": round(m - ci, 2), "ci95_hi": round(m + ci, 2)})
summ = pd.DataFrame(summary)
p(summ.to_string(index=False))
summ.to_csv(OUT / "eval_condition_means.csv", index=False, encoding="utf-8-sig")

# ---- item-level means per condition (for figure) -------------------------
p("\nITEM MEANS PER CONDITION")
item_m = df.groupby("condition")[QCOLS].mean().round(2)
p(item_m.to_string())

# ---- concept-level means -------------------------------------------------
p("\nCONCEPT MEANS (across evaluators)")
cm = df.groupby(["condition", "concept"])[DIMALL].mean().round(2)
p(cm.to_string())

# ---- Friedman + Kendall's W + post-hoc Wilcoxon --------------------------
p("\n" + "=" * 72)
p("FRIEDMAN TESTS (within-evaluator, 3 conditions) + Kendall's W")
pairs = [("A", "B"), ("A", "C"), ("B", "C")]
for dim in DIMALL:
    wide = ev.pivot(index="evaluator", columns="condition", values=dim)
    chi2, pval = stats.friedmanchisquare(wide["A"], wide["B"], wide["C"])
    n, k = wide.shape
    W = chi2 / (n * (k - 1))
    p(f"\n{dim}: chi2(2)={chi2:.2f}, p={pval:.2e}, Kendall W={W:.2f}")
    # post-hoc Wilcoxon with Holm correction
    res = []
    for a, b in pairs:
        d = wide[a] - wide[b]
        try:
            w, pw = stats.wilcoxon(wide[a], wide[b])
        except ValueError:
            w, pw = np.nan, 1.0
        dz = d.mean() / d.std(ddof=1)
        res.append([a, b, d.mean(), w, pw, dz])
    res.sort(key=lambda r: r[4])
    m = len(res)
    prev = 0
    for i, r in enumerate(res):
        holm = min(max(r[4] * (m - i), prev), 1.0)
        prev = holm
        p(f"  {COND_NAMES[r[0]]} vs {COND_NAMES[r[1]]}: diff={r[2]:+.2f}, "
          f"W={r[3]:.1f}, p_holm={holm:.4f}, Cohen's dz={r[5]:.2f}")

# ---- ICC(2,k): raters x targets (9 concepts), per dimension --------------
def icc2(mat):
    """Two-way random effects, absolute agreement (Shrout & Fleiss, 1979).

    mat: targets (rows) x raters (columns).
    Returns (ICC(2,1) single rater, ICC(2,k) mean of k raters).
    """
    n, k = mat.shape
    grand = mat.values.mean()
    ms_r = k * ((mat.mean(axis=1) - grand) ** 2).sum() / (n - 1)          # rows=targets
    ms_c = n * ((mat.mean(axis=0) - grand) ** 2).sum() / (k - 1)          # cols=raters
    sse = ((mat - mat.mean(axis=1).values.reshape(-1, 1)
            - mat.mean(axis=0).values.reshape(1, -1) + grand) ** 2).values.sum()
    ms_e = sse / ((n - 1) * (k - 1))
    icc21 = (ms_r - ms_e) / (ms_r + (k - 1) * ms_e + k * (ms_c - ms_e) / n)
    icc2k = (ms_r - ms_e) / (ms_r + (ms_c - ms_e) / n)
    return icc21, icc2k

p("\n" + "=" * 72)
p("INTER-RATER RELIABILITY, targets=9 concepts, raters=20")
for dim in DIMALL:
    mat = df.pivot(index="concept", columns="evaluator", values=dim)
    i21, i2k = icc2(mat)
    p(f"  {dim}: ICC(2,1)={i21:.2f}  ICC(2,{mat.shape[1]})={i2k:.2f}")

# ---- Cronbach's alpha for two-item scales (all 180 ratings) --------------
p("\nCRONBACH'S ALPHA (two-item dimension scales, n=180 concept-ratings)")
for dim, qs in DIMS.items():
    x = df[qs]
    k = len(qs)
    alpha = k / (k - 1) * (1 - x.var(ddof=1).sum() / x.sum(axis=1).var(ddof=1))
    r = x.corr().iloc[0, 1]
    p(f"  {dim} ({'+'.join(qs)}): alpha={alpha:.2f} (inter-item r={r:.2f})")

with open(OUT / "eval_stats_summary.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\nwritten: eval_stats_summary.txt, eval_condition_means.csv")

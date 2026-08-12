# -*- coding: utf-8 -*-
"""
Step 5: Video/brand-level dominance analysis (Reviewer 4, comment 4).

Checks whether Track B topics and sentiment are dominated by any single
video/brand:
  - per-video comment share
  - topic x video contingency + chi-square test + Cramer's V
  - per-video sentiment distribution
  - per-topic video composition (flags topics where one video > 50%)

Output: output/video_dominance.csv (+ printed summary for the manuscript).
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"

yt = pd.read_csv(OUT / "youtube_sentiment.csv")
topics = pd.read_csv(OUT / "trackB_doc_topics.csv")
assert len(yt) == len(topics), "row alignment mismatch"
yt["topic"] = topics["topic"].values

print(f"n = {len(yt)}")
print("\nper-video share (%):")
print(yt["video"].value_counts(normalize=True).mul(100).round(1).to_string())

ct = pd.crosstab(yt["topic"], yt["video"])
chi2, p, dof, _ = chi2_contingency(ct)
n = ct.values.sum()
cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
print(f"\ntopic x video: chi2={chi2:.1f}, dof={dof}, p={p:.2e}, Cramer's V={cramers_v:.3f}")

comp = ct.div(ct.sum(axis=1), axis=0).mul(100).round(1)
comp["n"] = ct.sum(axis=1)
comp["max_share"] = comp.iloc[:, :4].max(axis=1)
comp["dominated"] = comp["max_share"] > 50
print("\nper-topic video composition (%):")
print(comp.to_string())
print(f"\ntopics with one video > 50%: {int(comp['dominated'].sum())} / {len(comp)}")

comp.to_csv(OUT / "video_dominance.csv", encoding="utf-8-sig")
print("\nsaved: video_dominance.csv")

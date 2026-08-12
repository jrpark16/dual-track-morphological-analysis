# -*- coding: utf-8 -*-
"""
Step 3: VADER sentiment analysis on Track B comments.

VADER is applied to the near-raw comment text (URLs stripped only), because
capitalization, punctuation and emoji carry sentiment signal that VADER is
designed to exploit (Hutto & Gilbert, 2014).

Classification thresholds (standard): compound >= 0.05 positive,
compound <= -0.05 negative, otherwise neutral.

Output: output/youtube_sentiment.csv, per-video summary printed.
"""
from pathlib import Path
import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"

df = pd.read_csv(OUT / "youtube_clean.csv")
an = SentimentIntensityAnalyzer()

# the cleaned text keeps case, punctuation and emoji, which VADER exploits;
# HTML tags/entities and URLs are already stripped
df["compound"] = df["comment"].map(lambda s: an.polarity_scores(str(s))["compound"])
df["sentiment"] = pd.cut(df["compound"], [-1.01, -0.05, 0.05, 1.01],
                         labels=["negative", "neutral", "positive"])

df.to_csv(OUT / "youtube_sentiment.csv", index=False, encoding="utf-8-sig")

print(f"n = {len(df)}")
print("\noverall sentiment:")
print(df["sentiment"].value_counts(normalize=True).mul(100).round(1).to_string())
print("\nper-video sentiment (%):")
print(pd.crosstab(df["video"], df["sentiment"], normalize="index")
      .mul(100).round(1).to_string())
print("\nmean compound by video:")
print(df.groupby("video")["compound"].mean().round(3).to_string())

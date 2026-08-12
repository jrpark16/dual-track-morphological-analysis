# -*- coding: utf-8 -*-
"""
Step 1b: YouTube comment preprocessing (Track B).

Input : data/youtube_comments_raw.xlsx  (original collection, 4 videos)
Output: output/youtube_clean.csv

Stages:
  S0 raw comments
  S1 drop empty / whitespace-only
  S2 strip HTML tags/entities, URLs, excessive whitespace; drop < 3 tokens
  S3 English filter (langdetect, seeded for determinism)
  S4 spam/promo filter (rule-based: links already gone, repeated-char spam,
     self-promotion patterns)
"""
from pathlib import Path
import re, html
import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 42


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "youtube_comments_raw.xlsx"   # original comment collection (see data/README.md)
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(RAW, dtype={"Video_ID": str, "Comment": str, "Likes": "Int64", "Source_Video": str})
print(f"S0 raw comments (original collection): {len(df)}")

# Data-integrity fix: the original "Ameca" comments were collected from
# RIz3klPET3o, which is "Line Rider - Mountain King" (DoodleChaos), not an
# Ameca video. They are replaced with comments from the genuine official
# demo IPukuYb9xWw (see 00_collect_ameca.py).
n_bad = (df["Source_Video"] == "Ameca").sum()
df = df[df["Source_Video"] != "Ameca"]
ameca = pd.read_csv(OUT / "ameca_comments_recollected.csv",
                    dtype={"Video_ID": str, "Comment": str, "Source_Video": str})
df = pd.concat([df, ameca], ignore_index=True)
print(f"S0' dropped {n_bad} mis-attributed 'Ameca' comments, "
      f"added {len(ameca)} from genuine video: {len(df)}")

df = df[df["Comment"].notna() & df["Comment"].str.strip().ne("")]
print(f"S1 non-empty: {len(df)}")

def clean(s):
    s = html.unescape(html.unescape(s))          # &amp;#39; -> &#39; -> '
    s = re.sub(r"<[^>]+>", " ", s)               # HTML tags incl. <br>, <a href>
    s = re.sub(r"https?://\S+|www\.\S+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

df["clean"] = df["Comment"].map(clean)
df = df[df["clean"].str.split().str.len() >= 3]
print(f"S2 cleaned, >=3 tokens: {len(df)}")

def is_english(s):
    try:
        return detect(s) == "en"
    except LangDetectException:
        return False

df = df[df["clean"].map(is_english)]
print(f"S3 English filter (langdetect): {len(df)}")

spam = df["clean"].str.contains(
    r"(?i)check out my|subscribe to|visit my channel|(.)\1{9,}", regex=True)
df = df[~spam]
print(f"S4 spam filter: {len(df)}")

df = df.rename(columns={"Video_ID": "video_id", "Comment": "comment_raw",
                        "Likes": "likes", "Source_Video": "video", "clean": "comment"})
df[["video_id", "video", "likes", "comment_raw", "comment"]].to_csv(
    OUT / "youtube_clean.csv", index=False, encoding="utf-8-sig")
print(f"\nsaved: youtube_clean.csv ({len(df)})")
print("\nper-video distribution:")
print(df["video"].value_counts().to_string())

# -*- coding: utf-8 -*-
"""
Step 0: Re-collection of Ameca comments (data-integrity fix).

The original Track B dataset attributed video ID RIz3klPET3o to "Ameca";
verification (2026-08-11) shows that ID is "Line Rider - Mountain King"
(DoodleChaos), unrelated to humanoid robots. All 835 comments under the
"Ameca" label are therefore invalid and are replaced by comments collected
from pathlib import Path
from the genuine official demonstration video:

  IPukuYb9xWw  "Ameca Humanoid Robot AI Platform" (Engineered Arts, 4.4M views)

Comments are collected in YouTube's "top comments" ordering, capped at 900
to keep the per-video volume comparable to the other three videos.

Output: output/ameca_comments_recollected.csv
"""
import re, itertools
import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
VIDEO_ID = "IPukuYb9xWw"
CAP = 900

dl = YoutubeCommentDownloader()
gen = dl.get_comments(VIDEO_ID, sort_by=SORT_BY_POPULAR)
rows = []
for c in gen:
    if len(rows) >= CAP:
        break
    if c.get("reply"):
        continue  # top-level comments only, matching the original collection
    # votes arrive locale-formatted ("3.1K", "3.1천", "1.2만", "1,234")
    raw = str(c.get("votes", "0")).replace(",", "")
    m = re.match(r"([\d.]+)", raw)
    num = float(m.group(1)) if m else 0.0
    mult = 1
    for suf, f in (("K", 1e3), ("M", 1e6), ("천", 1e3), ("만", 1e4)):
        if suf in raw[len(m.group(1)) if m else 0:]:
            mult = f
            break
    votes = int(num * mult)
    rows.append({"Video_ID": VIDEO_ID, "Comment": c.get("text", ""),
                 "Likes": votes, "Source_Video": "Ameca"})

df = pd.DataFrame(rows)
df.to_csv(OUT / "ameca_comments_recollected.csv", index=False, encoding="utf-8-sig")
print(f"collected {len(df)} top-level comments from {VIDEO_ID}")
print(df.head(5).to_string())

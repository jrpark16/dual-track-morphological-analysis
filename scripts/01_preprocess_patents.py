# -*- coding: utf-8 -*-
"""
Step 1a: Patent data preprocessing (Track A).

Input : data/patents_wintelips_export.xlsx  (WINTELIPS export, 2,638 records)
Output: output/patents_clean.csv

Filtering stages (each logged for the PRISMA-style flow diagram):
  S0 raw export
  S1 application date within 2020-01-01 .. 2024-12-31
  S1b exclude design-right documents (CN document-kind code 'S' and
      design-registration boilerplate abstracts) - these are ornamental
      design registrations, not invention patents
  S2 English abstract present (>= 30 chars)
  S3 family dedup (keep earliest application per WIPS family ID)
  S4 relevance: humanoid/bipedal robot context in title+abstract,
     exclusion terms (toy, vacuum cleaner) absent
"""
from pathlib import Path
import re
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "patents_wintelips_export.xlsx"   # WINTELIPS export (not redistributable; see data/README.md)
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(RAW, dtype=str)
df.columns = [c.strip() for c in df.columns]
print(f"S0 raw export: {len(df)}")

# --- diagnostics ---------------------------------------------------------
df["app_date"] = pd.to_datetime(df["출원일"], errors="coerce")
print("\ncountry distribution:")
print(df["국가코드"].value_counts().to_string())
print("\napplication year distribution:")
print(df["app_date"].dt.year.value_counts().sort_index().to_string())
print(f"\nunique WIPS family IDs: {df['WIPS패밀리 ID'].nunique()}")

abst = df["요약"].fillna("")
is_ascii = abst.str.len().gt(30) & abst.apply(
    lambda s: bool(re.search(r"[A-Za-z]{3}", s[:200])) if s else False
)
print(f"records with English-looking abstract: {is_ascii.sum()}")

# --- S1 date window ------------------------------------------------------
m1 = df["app_date"].between("2020-01-01", "2024-12-31")
df1 = df[m1].copy()
print(f"\nS1 date window 2020-2024: {len(df1)}  (excluded {len(df)-len(df1)})")

# --- S1b exclude design-right documents ----------------------------------
is_design = (df1["문헌종류 코드"].str.strip() == "S") | \
    df1["요약"].fillna("").str.contains(
        r"(?i)design product|appearance design|exterior design|present design")
df1 = df1[~is_design].copy()
print(f"S1b design-right documents excluded: {len(df1)}  (removed {int(is_design.sum())})")

# --- S2 English abstract -------------------------------------------------
def eng_abstract(row):
    for col in ("요약", "요약-번역문"):
        s = str(row.get(col) or "")
        if len(s) >= 30 and re.search(r"[A-Za-z]{3}", s[:200]) and not re.search(r"[가-힣]", s[:200]):
            return s
    return ""

df1["abstract_en"] = df1.apply(eng_abstract, axis=1)
df2 = df1[df1["abstract_en"].str.len() >= 30].copy()
print(f"S2 English abstract present: {len(df2)}  (excluded {len(df1)-len(df2)})")

# --- S3 family dedup -----------------------------------------------------
df2 = df2.sort_values("app_date")
df3 = df2.drop_duplicates(subset="WIPS패밀리 ID", keep="first").copy()
print(f"S3 family dedup: {len(df3)}  (removed {len(df2)-len(df3)})")

# --- S4 relevance --------------------------------------------------------
text = (df3["발명의 명칭"].fillna("") + " " + df3["abstract_en"]).str.lower()
incl = text.str.contains(r"humanoid|biped|bipedal|human-like robot|anthropomorph")
excl = text.str.contains(r"\btoy\b|vacuum clean")
df4 = df3[incl & ~excl].copy()
print(f"S4 relevance filter: {len(df4)}  (excluded {len(df3)-len(df4)}: "
      f"{(~incl).sum()} no-keyword, {(incl & excl).sum()} exclusion-term)")

# --- save ----------------------------------------------------------------
keep = df4[["WINTELIPS KEY", "국가코드", "출원번호", "app_date", "발명의 명칭",
            "abstract_en", "출원인", "WIPS패밀리 ID"]].rename(columns={
    "WINTELIPS KEY": "key", "국가코드": "country", "출원번호": "app_no",
    "발명의 명칭": "title", "출원인": "applicant", "WIPS패밀리 ID": "family_id"})
keep.to_csv(OUT / "patents_clean.csv", index=False, encoding="utf-8-sig")
print(f"\nsaved: patents_clean.csv  ({len(keep)} records)")
print("\ncountry distribution (final):")
print(keep["country"].value_counts().to_string())

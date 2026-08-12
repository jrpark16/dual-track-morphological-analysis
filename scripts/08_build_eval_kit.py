# -*- coding: utf-8 -*-
"""
Step 7: Build the blinded expert-evaluation kit.

Reads the three condition transcripts (output/llm_runs/), extracts the nine
final concept sheets, assigns blinded IDs in a seeded random order, and
writes:
  output/eval_kit/evaluation_booklet_blinded.docx  - instructions + 9 blinded sheets (Korean, the actual instrument)
  output/eval_kit/scoring_template.xlsx           - scoring grid (9 concepts x 6 items)
  output/eval_kit/blinding_key.csv       - ID -> condition/concept (authors only)

Blinding: condition labels are never shown; presentation order is randomized
once (random.Random(7)) and identical for all evaluators (documented design
choice; per-evaluator order permutation can be enabled with PER_EVALUATOR).
"""
from pathlib import Path
import re, random
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "llm_runs"          # condition_{A,B,C}_transcript.md (see llm_runs/README.md)
KIT = ROOT / "output" / "eval_kit"
KIT.mkdir(parents=True, exist_ok=True)

# ---- parse concept sheets ------------------------------------------------
def extract_sheets(path, condition):
    text = open(path, encoding="utf-8").read()
    turn2 = text.split("## Turn 2 — Response", 1)[1]
    blocks = re.split(r"\n## (?!Turn)", turn2)
    sheets = []
    for b in blocks:
        if "**One-line value proposition:**" in b:
            name = b.strip().splitlines()[0].strip().lstrip("#").strip()
            body = "\n".join(b.strip().splitlines()[1:]).strip()
            body = re.sub(r"\(~?\d+ words?\)\s*$", "", body.strip())
            sheets.append({"condition": condition, "name": name, "body": body})
    return sheets

sheets = (extract_sheets(RUNS / "condition_A_transcript.md", "A_dual_track")
          + extract_sheets(RUNS / "condition_B_transcript.md", "B_tech_push")
          + extract_sheets(RUNS / "condition_C_transcript.md", "C_random"))
assert len(sheets) == 9, f"expected 9 sheets, got {len(sheets)}"

rng = random.Random(7)
order = list(range(9))
rng.shuffle(order)
for i, idx in enumerate(order):
    sheets[idx]["blind_id"] = f"R{i+1}"
sheets_by_id = sorted(sheets, key=lambda s: int(s["blind_id"][1:]))

pd.DataFrame([{ "blind_id": s["blind_id"], "condition": s["condition"],
                "concept": s["name"]} for s in sheets_by_id]).to_csv(
    KIT / "blinding_key.csv", index=False, encoding="utf-8-sig")

# ---- booklet docx --------------------------------------------------------
import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document()
style = doc.styles["Normal"]
style.font.name = "Malgun Gothic"
style.font.size = Pt(10)

h = doc.add_heading("휴머노이드 로봇 제품 컨셉 전문가 평가", level=0)
doc.add_paragraph(
    "본 평가는 데이터 기반 형태분석(morphological analysis) 방법론 연구의 일환으로, "
    "서로 다른 절차로 생성된 휴머노이드 로봇 제품 컨셉 9개(R1~R9)의 품질을 평가합니다. "
    "각 컨셉이 어떤 절차로 생성되었는지는 공개되지 않으며(블라인드), 제시 순서는 무작위입니다.")
doc.add_paragraph(
    "각 컨셉을 읽으신 후, 평가지(엑셀)의 6개 문항에 대해 7점 척도"
    "(1 = 전혀 그렇지 않다, 4 = 보통, 7 = 매우 그렇다)로 응답해 주십시오. "
    "컨셉 간 비교보다는 각 컨셉을 독립적으로 평가해 주시고, "
    "모든 컨셉을 한 번 훑어본 뒤 본 평가를 시작하시는 것을 권장합니다. "
    "예상 소요 시간은 30-40분입니다.")
doc.add_paragraph("평가 문항:")
for q in ["Q1. 이 컨셉에 적용된 기술 조합은 물리적·공학적으로 실현 가능한가?",
          "Q2. 향후 5년 내 상용화가 가능한 수준의 기술인가?",
          "Q3. 이 컨셉은 잠재 사용자의 실제 니즈/페인포인트를 다루는가?",
          "Q4. 사용자들이 심리적 거부감 없이 이 로봇을 구매할 의향이 있겠는가?",
          "Q5. 이 컨셉은 시장의 기존 제품과 명확히 차별화되는가?",
          "Q6. 기술과 시장 니즈의 융합이 창의적으로 이루어졌는가?"]:
    p = doc.add_paragraph(q)
    p.paragraph_format.left_indent = Cm(0.5)

for s in sheets_by_id:
    doc.add_page_break()
    doc.add_heading(f"{s['blind_id']}. {s['name']}", level=1)
    for line in s["body"].split("\n"):
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("- "):
            p = doc.add_paragraph(re.sub(r"\*\*(.+?)\*\*", r"\1", line[2:]),
                                  style="List Bullet")
        else:
            p = doc.add_paragraph()
            pos = 0
            for m in re.finditer(r"\*\*(.+?)\*\*", line):
                if m.start() > pos:
                    p.add_run(line[pos:m.start()])
                r = p.add_run(m.group(1)); r.bold = True
                pos = m.end()
            if pos < len(line):
                p.add_run(line[pos:])

doc.save(KIT / "evaluation_booklet_blinded.docx")
print("evaluation_booklet_blinded.docx written")

# ---- scoring workbook ----------------------------------------------------
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "평가지"
QUESTIONS = ["Q1 기술조합 실현가능성", "Q2 5년내 상용화 가능성",
             "Q3 실제 니즈 부합", "Q4 구매의향(거부감 없음)",
             "Q5 기존제품 차별성", "Q6 융합의 창의성"]
ws.append(["평가자 성함:", "", "소속/직위:", "", "전문분야:", "", "경력(년):", ""])
ws.append([])
ws.append(["컨셉 ID"] + QUESTIONS + ["자유 의견 (선택)"])
hdr = ws[3]
for c in hdr:
    c.font = Font(bold=True)
    c.fill = PatternFill("solid", fgColor="DCE6F1")
    c.alignment = Alignment(wrap_text=True, vertical="center")
for i in range(1, 10):
    ws.append([f"R{i}"] + [""] * 7)
dv = DataValidation(type="whole", operator="between", formula1=1, formula2=7,
                    allow_blank=True, errorTitle="입력 오류",
                    error="1~7 사이의 정수를 입력해 주세요")
ws.add_data_validation(dv)
dv.add("B4:G12")
ws.column_dimensions["A"].width = 10
for col in "BCDEFG":
    ws.column_dimensions[col].width = 14
ws.column_dimensions["H"].width = 40
wb.save(KIT / "scoring_template.xlsx")
print("scoring_template.xlsx written")

print("\nblinding key:")
for s in sheets_by_id:
    print(f"  {s['blind_id']}: [{s['condition']}] {s['name']}")

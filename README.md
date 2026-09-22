# Dual-Track Morphological Analysis for Humanoid Robot Technology Opportunity Discovery

Analysis code for the manuscript:

> Park, J., & Shin, K. *Technology Opportunity Discovery for Humanoid Robots Using
> Dual-Track Morphological Analysis Integrating Technological Feasibility and
> Social Acceptance.* (under review, *Scientific Reports*)

The pipeline integrates a technology-supply track (patent data) and a public-discourse
track (YouTube comments on flagship humanoid robot demonstration videos), derives
morphological dimensions from each track with BERTopic, fuses them into a dual-track
morphological matrix, generates product concepts with an LLM under three controlled
conditions, and analyzes a blinded expert evaluation of the resulting concepts.
Every statistic, table, and figure in the manuscript is produced by this code.

## Pipeline

| Step | Script | Purpose |
|---|---|---|
| 0 | `scripts/00_collect_ameca.py` | Re-collection of the Ameca comment subset from the verified official video (data-integrity fix disclosed in the manuscript, Section 3.1) |
| 1a | `scripts/01_preprocess_patents.py` | Patent screening funnel: study window, design-right removal, family deduplication, relevance filter (2,638 → 824) |
| 1b | `scripts/02_preprocess_youtube.py` | Comment cleaning funnel: HTML/URL stripping, length filter, language filter, spam filter (3,484 → 2,789) |
| 2 | `scripts/03_topic_modeling.py` | BERTopic per track: all-MiniLM-L6-v2 embeddings, UMAP (seeded), K-means, NPMI-coherence-based selection of K (K*=14 / K*=15) |
| 3 | `scripts/04_sentiment_vader.py` | VADER sentiment on Track B comments |
| 4 | `scripts/05_dimension_mapping.py` | Explicit topic-to-dimension mapping (Supplementary Table S1) and dimension-level tables |
| 5 | `scripts/06_video_dominance.py` | Video/brand dominance robustness analysis (manuscript Section 4.6) |
| 6 | `scripts/07_figures.py` | Manuscript Figures 2 and 3 (data funnel; two-track comparison) and Supplementary Fig. S1 (coherence) |
| 7 | `scripts/08_build_eval_kit.py` | Blinded expert-evaluation kit: booklet, scoring workbook, seeded blinding key |
| 8 | `scripts/09_eval_stats.py` | Expert-evaluation statistics: condition means with 95% CIs, Friedman + Holm-corrected Wilcoxon, Kendall's W, Cohen's dz, ICC(2,1)/ICC(2,k), Cronbach's alpha |
| 9 | `scripts/09b_fig5_eval.py` | Figure 6 (expert evaluation results) |
| 10 | `scripts/10_fig1_flowchart.py` | Figure 1: flowchart of the framework with decision points and feedback paths |
| 11 | `scripts/11_fig4_architecture.py` | Figure 4: functional architecture of the three dual-track concepts |
| 12 | `scripts/12_fig5_morphchart.py` | Figure 5: morphological chart comparing the nine evaluated concepts |

Scripts are numbered in execution order and communicate through CSV files in
`output/`. The same scripts are provided as Jupyter notebooks in `notebooks/`.

## Reproducibility

All stochastic components are seeded: UMAP and K-means (`SEED = 42` in
`03_topic_modeling.py`), the language detector (`langdetect`, seed 42), the
unconstrained-condition attribute sampling (seed 42), and the blinding-key shuffle
(`random.Random(7)` in `08_build_eval_kit.py`). Given the same input data, the topic
solutions, blinding key, and all downstream statistics reproduce exactly.

The LLM concept-generation step (manuscript Section 3.4, Table 9) was executed as a
single-pass, two-turn protocol per condition with Claude Fable 5 via the Claude Agent
SDK; the complete prompts and unedited transcripts are provided in `llm_runs/` and in
the Supplementary Material of the manuscript. Note that LLM generation is inherently
stochastic across runs; the transcripts document the exact run used in the study.

## Data availability

Raw inputs cannot be redistributed and are therefore **not** included in this
repository (see `data/README.md` for details and file layout):

- **Patent data** (Track A) were exported from the commercial WINTELIPS database and
  cannot be redistributed under its license. The exact query, collection date, and
  screening criteria required to reconstruct the corpus are given in the manuscript
  (Section 3.1) and implemented in `01_preprocess_patents.py`.
- **YouTube comment texts** (Track B) are subject to platform terms. The four video
  identifiers and the collection procedure are documented in the manuscript and in
  `00_collect_ameca.py`; the preprocessing is implemented in
  `02_preprocess_youtube.py`.
- **Expert-evaluation responses** are provided in de-identified form
  (`data/eval_responses_deidentified.xlsx`; evaluator pseudonyms S01–S20).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Place the input files described in `data/README.md`, then run the scripts in order:

```bash
python scripts/01_preprocess_patents.py
python scripts/02_preprocess_youtube.py
python scripts/03_topic_modeling.py
python scripts/04_sentiment_vader.py
python scripts/05_dimension_mapping.py
python scripts/06_video_dominance.py
python scripts/07_figures.py
python scripts/10_fig1_flowchart.py
python scripts/09_eval_stats.py
python scripts/09b_fig5_eval.py
```

(`00_collect_ameca.py` re-runs the live comment collection and is only needed to
rebuild the raw comment file; `08_build_eval_kit.py` rebuilds the evaluation kit from
the LLM transcripts.)

## License

MIT — see `LICENSE`.

## Citation

See `CITATION.cff`. Please cite the manuscript once published.

# Derived datasets

Processed, licence-safe outputs of the analysis pipeline, released so that every
number, table and figure of the manuscript can be checked without access to the raw
inputs. Raw inputs are **not** included: patent titles and abstracts come from the
commercial WINTELIPS database and cannot be redistributed under its licence, and
YouTube comment texts are subject to platform terms (see `../data/README.md`). The
files below therefore carry public identifiers (patent application numbers) or
fingerprints (SHA-256 of the cleaned comment) in place of the texts, together with
every assignment the pipeline produced for each document.

| File | Rows | Contents | Manuscript |
|---|---|---|---|
| `trackA_patent_topic_assignments.csv` | 824 | One row per valid patent after the four-stage screening: `jurisdiction`, public `application_no`, `application_date`, WIPS `family_id` (used for family-level deduplication), `applicant`, assigned BERTopic `topic` (K* = 14) and mapped `dimension` | Section 3.1, Fig. 2, Table 3 |
| `trackB_comment_topic_sentiment_assignments.csv` | 2,789 | One row per cleaned comment: `video_id`, `video`, `likes`, `comment_sha256` (SHA-256 of the UTF-8 cleaned comment text), `comment_n_chars`, assigned `topic` (K* = 15), mapped `dimension`, VADER `vader_compound` and three-class `sentiment` | Sections 3.1, 3.3, Fig. 2, Tables 3-4 |
| `trackA_topics_Kstar14.csv`, `trackB_topics_Kstar15.csv` | 14 / 15 | Selected topic solutions: document `count`, `share` (%), ten highest c-TF-IDF `top_words`, mapped `dimension` | Sections 4.1-4.2, Supplementary Table S1 |
| `alternative_k/*.csv` | - | Topic solutions at the alternative K values inspected during model selection (Track A: K = 6, 11; Track B: K = 6, 8) | Section 3.2 |
| `topic_to_dimension_mapping.csv` | 29 | The explicit topic-to-dimension mapping with the defining c-TF-IDF terms and document counts (identical to `scripts/05_dimension_mapping.py`) | Supplementary Table S1 |
| `dimension_shares.csv` | 9 | Document count and share per dimension and track | Table 3 |
| `trackB_dimension_sentiment.csv` | 4 | VADER sentiment distribution (%) per Track B dimension | Table 4 |
| `npmi_coherence_curves.csv` | 34 | NPMI coherence for every scanned K per track; `selected` marks K* | Section 3.2, Supplementary Fig. S1 |
| `dual_track_morphological_matrix.csv` | 36 | The 9 dimensions x 4 attributes of the integrated matrix (long format) | Table 5, Fig. 5 |
| `trackB_video_dominance.csv` | 15 | Share of each source video within each Track B topic and the dominance flag used in the robustness analysis | Section 4.6 |

Related material elsewhere in the repository: de-identified expert-evaluation
responses in `../data/eval_responses_deidentified.xlsx`; complete LLM prompts and
transcripts in `../llm_runs/`.

## How the files were produced

`trackA_patent_topic_assignments.csv` joins `output/patents_clean.csv`
(`01_preprocess_patents.py`) with `output/trackA_doc_topics.csv`
(`03_topic_modeling.py`) and drops the title and abstract columns.
`trackB_comment_topic_sentiment_assignments.csv` joins `output/youtube_sentiment.csv`
(`04_sentiment_vader.py`) with `output/trackB_doc_topics.csv` and replaces the comment
text by its SHA-256 fingerprint. Dimensions are added with the mapping in
`05_dimension_mapping.py`. Re-running the pipeline on a re-collected corpus will not
reproduce the comment fingerprints exactly, because comments can be edited or deleted
on the platform after collection; the fingerprints allow an independent collection to
be matched to the released assignments where the texts coincide.

## Licence

Released under the repository's MIT licence. The patent bibliographic fields
(application number, date, jurisdiction, applicant) are public register data.

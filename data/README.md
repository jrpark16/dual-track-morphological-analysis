# Input data

The pipeline expects the following files in this directory. Raw third-party data
cannot be redistributed and are therefore not included in the repository.

| File | Contents | Included? |
|---|---|---|
| `patents_wintelips_export.xlsx` | WINTELIPS patent export (2,638 records). Query: `("humanoid" OR "bipedal") AND "robot" NOT ("toy" OR "vacuum")`, abstracts, collected December 2025. Column names follow the Korean WINTELIPS export schema. | No — commercial license. Reconstruct with the query/criteria in the manuscript (Section 3.1). |
| `youtube_comments_raw.xlsx` | Original top-level comment collection from the four verified official demonstration videos (columns: `Video_ID`, `Comment`, `Likes`, `Source_Video`). | No — platform terms. Video IDs and the collection procedure are documented in the manuscript and `scripts/00_collect_ameca.py`. |
| `eval_responses_deidentified.xlsx` | De-identified expert-evaluation responses: one sheet per evaluator (pseudonyms S01–S20); row 1 holds evaluator metadata, rows 4–12 hold the R1–R9 ratings on Q1–Q6. | Yes. |

Derived datasets (cleaned corpora with topic and sentiment assignments, dimension
tables, coherence curves, evaluation statistics) are written to `output/` by the
pipeline and are also archived with the Zenodo release.

# Distribution shift in agricultural machine learning — systematic review

**How much performance do agricultural machine-learning models lose out of distribution? A systematic review and quantitative synthesis**
Abinash Pant and Binayak Prakash Mishra

Deliverables: `output/distribution_shift_review_v1.0.docx` (Word, line-numbered) and `output/distribution_shift_review_v1.0.pdf`.

## Layout

| Path | Contents |
|---|---|
| `review/PROTOCOL.md` | Protocol fixed on 2026-10-01 before searching, with the dated deviation log |
| `review/search/` | Database exports (OpenAlex, Semantic Scholar) and the deduplicated pool |
| `review/screening/` | Title/abstract decisions, full-text candidates, duplicate links |
| `review/extraction/` | Full-text and abstract-level decisions (`ft_decisions.csv`), one row per ID–OOD comparison (`comparisons.csv`), appraisal (`appraisal.csv`), extraction rules |
| `review/analysis/` | `results.json` (every number in the paper) and summary tables |
| `review/RETRIEVAL_LIST.csv` | Studies whose full text could not be retrieved, in priority order |
| `review/scripts/` | Search, deduplication, retrieval, recording and `synthesis.py` |
| `manuscript/review.md` | Manuscript source. A template: `{{ ... }}` expressions are filled from `results.json` at build time, so no number is typed by hand |
| `manuscript/make_tables.py`, `figures/make_prisma.py` | Tables 1–5, Appendix C, the included-study bibliography and Fig. 1 |
| `LEDGER.md`, `REVIEW.md`, `readiness.json` | Claim–evidence ledger, adversarial pre-submission review, readiness scorecard |

## Rebuild

```bash
cd paper
make all        # synthesis -> figures and results.json -> Word and PDF
make check      # prose metrics, citation verification (needs network), gate tokens
make score      # gated readiness verdict
```

Requires Python 3 with numpy, matplotlib, pypandoc (bundled pandoc) and python-docx, and Chrome or Chromium for the PDF.

## Status (2026-10-02)

Readiness: **NOT READY (gated)**, 64/100 (`manuscript/readiness_report.txt`). What remains is listed in `LEDGER.md` under Open items; the ones that change the outcome are:

1. Human verification of study selection and data extraction (protocol §5) — the review was screened and extracted by one LLM-assisted reviewer.
2. The six `[AUTHOR DECISION]` items in the manuscript: affiliations/ORCID/corresponding author, AI-use attestation, data DOI, funding, competing interests, CRediT.
3. Full texts of paywalled studies (`review/RETRIEVAL_LIST.csv`), digitising the 40 figure-only studies, citation chasing, and Scopus/Web of Science searches.
4. Citation verification with network access (`make cites`).

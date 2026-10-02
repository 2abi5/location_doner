# Ledger — distribution shift in agricultural machine learning (systematic review)

venue: not chosen (VENUE.md) | stage: S9 | updated: 2026-10-02 | manuscript: manuscript/review.md (template) → output/distribution_shift_review_v1.0.{docx,pdf}

## Story spine
1. TASK      — Crop-production models are evaluated on data from their training domain, then used on other fields, seasons and sensors.
2. GAP       — Primary studies report ID and OOD results in incompatible units and designs, **because** no synthesis converts them to a common effect size across tasks.
3. INSIGHT   — Retention (OOD/ID on the same model and metric) is computable for any study that reports both values, so evidence from six tasks becomes comparable.
4. METHOD    — PRISMA 2020 systematic review, 178 studies, 572 comparisons; study-level medians, cluster bootstrap, within-study contrasts; appraisal of six practice items.
5. EVIDENCE  — Median retention 0.82 (0.73 full text); acquisition, sensor and compound shifts cost most; target fine-tuning recovers 89% of the gap, UDA 28%.
6. SO WHAT   — An ID score must be read with the expected retention for the shift; OOD evaluations need a minimum reporting set (Table 6).

## Contribution claims (every number rendered from review/analysis/results.json)
| # | Claim | Type | Evidence | Location | Status |
|---|---|---|---|---|---|
| C1 | 178 studies contribute 572 ID–OOD comparisons | empirical | Fig. 1, Table 1, Appendix C | §3.1–3.2 | supported |
| C2 | Median retention 0.82 (95% CI 0.74–0.89); 0.73 in full-text studies | empirical | Table 2, Table 5 | §3.3, §3.6 | supported |
| C3 | Acquisition (0.56), sensor (0.55, n = 4) and compound (0.67) shifts retain less than location (0.87) and time (0.91) | empirical | Table 2, Fig. 2a | §3.3 | supported (sensor n = 4 stated) |
| C4 | Within studies, compound shifts retain less than single-factor shifts (8 of 9) | comparative | within_study_contrasts | §3.3 | supported, post hoc, unadjusted p = 0.039, not significant after Bonferroni (stated) |
| C5 | Weed recognition retains least (0.61); mapping (0.92) and organ detection (0.95) most | empirical | Table 2, Table 3 | §3.3 | supported |
| C6 | Fine-tuning recovers 89% of the gap, UDA 28% | empirical | Table 4, Fig. 4 | §3.4 | supported |
| C7 | 71% single run; 77% model selection not stated | empirical | Fig. 5 | §3.5 | supported |
| C8 | Abstract-only studies report higher retention than full-text studies within task | empirical | ret_abstract_vs_fulltext_by_task | §3.6 | supported; two explanations given, neither tested |
| C9 | Transformers retain more than CNNs within studies (14 of 17) | comparative | within_study_contrasts | §3.3, §4.1 | supported, post hoc, caveat on proposed-model bias stated |

## Provenance
| Table/Figure | Source file | Script |
|---|---|---|
| Fig. 1 | manuscript/figures/counts.json | figures/make_prisma.py |
| Fig. 2–5, Tables 1–5, C1 | review/analysis/results.json, comparisons_with_effects.csv | review/scripts/synthesis.py, manuscript/make_tables.py |
| Every in-text number | review/analysis/results.json, figures/counts.json | manuscript/build.py (template rendering) |

## Gates (see readiness.json and manuscript/readiness_report.txt)
| Gate | Status | Blocking issues |
|---|---|---|
| G1 claim/evidence | PASS | — |
| G2 citations | BLOCKED | network to Crossref/OpenAlex/arXiv/S2 denied in this environment; 29/30 core refs verified on 2026-10-01 |
| G3 venue compliance | NOT RUN | no journal chosen |
| G4 readiness | NOT READY (gated) | score 64/100; G-TOKEN fails on 6 [AUTHOR DECISION] items |

## Terminology (fixed)
retention ρ · gap Δ · gap recovered g · oracle-referenced g_o · source-only · oracle · shift type (acquisition, location, time, sensor, biological, compound) · INCLUDE / INCLUDE-O / INCLUDE-A / FIG

## Open items (in order of what changes the outcome)
- [ ] Human verification: re-screen a random 20% of title/abstract decisions and all full-text decisions; report Cohen's κ (protocol §5)
- [ ] Double-extract a random 20% of comparisons and correct errors; re-run `make all`
- [ ] Retrieve paywalled full texts (review/RETRIEVAL_LIST.csv, priority 1 first) and re-assess INCLUDE-A and E4 records
- [ ] Digitise the 40 FIG studies and re-run synthesis
- [ ] Citation chasing of the included studies; Scopus and Web of Science searches
- [ ] Read R02966, R06651, R07003 in full; confirm the distinction sentence in §1
- [ ] Re-run `make cites` with network access (Gate 2)
- [ ] Choose the journal; check its live guide for authors (VENUE.md)
- [ ] Fill the six [AUTHOR DECISION] items: affiliations/ORCID/corresponding author, AI-use attestation, data DOI, funding, competing interests, CRediT

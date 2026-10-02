# Distribution shift in agricultural machine learning: a systematic review and quantitative synthesis

Scaffolded 2026-10-01. Deadline: [TBD].

## Order of work

1. `LEDGER.md` — fill the story spine. Six lines. Do this before any prose.
2. `VENUE.md` — confirm the venue and re-verify its live rules.
3. Evidence plan in `LEDGER.md` — one experiment per claim, decided before drafting.
4. Draft `sections/` — one paragraph at a time; reverse-outline each section after.
5. `make tables` — every number generated from `results/`, never typed.
6. `make check` — run at the end of EVERY session, not the day before the deadline.
7. `make score` — the gated readiness verdict.

## Rules this layout enforces

- Numbers live in `results/`, become `tables/*.tex` via `scripts/make_tables.py`,
  and are `\input` by the sections. A hand-typed number is a number that will
  disagree with its run.
- Figures come from committed sources in `figures/src/` and land in `figures/out/`
  as vector PDFs, re-exported at the target width rather than scaled down.
- Anonymity is one `\anontrue`/`\anonfalse` line in `main.tex`.
- Nothing ships with `[TBD]`, `[NEEDS SOURCE]`, `[NEEDS EXPERIMENT]`,
  `[AUTHOR DECISION]`, or `[VERIFY]` in it. `make tokens` checks.

## Venue

No venue set. Set one before drafting: it decides length, structure,
anonymity, and required sections.


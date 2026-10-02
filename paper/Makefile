# Distribution shift in agricultural machine learning: a systematic review and quantitative synthesis
# S is this machine's path to the research-pro scripts. Override per machine with
#   make check S=/your/path/to/skills/research-pro/scripts
S      ?= ../abinash_research/skills/research-pro/scripts
VENUE  ?= neurips
MAIN   ?= main
TARGET_PT ?= 237     # one column of a two-column paper

.PHONY: pdf check cites prose figs lint venue score tokens tables clean overleaf-pull overleaf-push

pdf:
	latexmk -pdf -interaction=nonstopmode $(MAIN).tex

tables:
	python3 scripts/make_tables.py && python3 scripts/make_figures.py

check: lint cites prose figs venue tokens
	@echo "--- all checks run ---"

lint:
	python3 $(S)/latex_lint.py $(MAIN).tex --venue $(VENUE) --no-strict

cites:
	python3 $(S)/verify_citations.py refs.bib --tex $(MAIN).tex sections/*.tex \
	  --report out/citations.md --no-strict

prose:
	python3 $(S)/prose_metrics.py $(MAIN).tex --no-strict

figs:
	python3 $(S)/figure_audit.py figures/out --target-pt $(TARGET_PT) --no-strict

venue:
	python3 $(S)/venue_check.py --venue $(VENUE) --paper $(MAIN).tex --no-strict

score:
	python3 $(S)/score_readiness.py readiness.json --venue $(VENUE)

tokens:
	@grep -rnE '\[(NEEDS SOURCE|TBD|NEEDS EXPERIMENT|AUTHOR DECISION|VERIFY)\]' \
	  sections/ *.tex 2>/dev/null || echo "no gap tokens"

overleaf-pull:
	git pull --no-rebase

overleaf-push:
	$(MAKE) check && git add -A && git commit -m "$(M)" && git push

clean:
	latexmk -C

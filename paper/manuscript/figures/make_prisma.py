"""PRISMA 2020 flow diagram from counts.json. Writes fig1_prisma.png (Word) and fig1_prisma.svg (PDF).
Usage: ../.venv/bin/python figures/make_prisma.py   (run from paper/manuscript)"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

c = json.load(open("figures/counts.json"))
fmt = lambda v: f"{v:,}" if isinstance(v, int) else str(v)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5})
fig, ax = plt.subplots(figsize=(7.2, 6.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
GREY, BLUE = "#F2F2F2", "#E8F1F8"


def box(x, y, w, h, text, fc=GREY):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc=fc, ec="black", lw=0.6))
    ax.text(x + 1.2, y + h - 1.2, text, va="top", ha="left", wrap=True, linespacing=1.35)


def arrow(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", lw=0.6, color="black"))


def band(y, h, label):
    ax.add_patch(FancyBboxPatch((0, y), 3.2, h, boxstyle="square,pad=0", fc=BLUE, ec="black", lw=0.6))
    ax.text(1.6, y + h / 2, label, rotation=90, va="center", ha="center", fontweight="bold")


band(78, 20, "Identification"); band(30, 46, "Screening"); band(2, 26, "Included")
box(5, 80, 42, 18, "Records identified from databases:\n"
    f"  OpenAlex (n = {fmt(c['openalex'])})\n"
    f"  Semantic Scholar (n = {fmt(c['s2'])})\n"
    f"  Earlier OpenAlex search iteration (n = {fmt(c['earlier'])})")
box(55, 84, 43, 10, f"Records removed before screening:\n  Duplicate records (n = {fmt(c['duplicates'])})")
box(5, 64, 42, 9, f"Records screened (title/abstract)\n(n = {fmt(c['screened'])})")
box(55, 64, 43, 9, f"Records excluded\n(n = {fmt(c['excluded_ta'])})")
box(5, 48, 42, 11, f"Reports sought for retrieval\n(n = {fmt(c['sought'])}; {fmt(c['studies'])} studies after\nlinking {fmt(c['dup_reports'])} duplicate reports)")
box(55, 50, 43, 8, f"Reports not retrieved\n(n = {fmt(c['not_retrieved'])})")
box(5, 32, 42, 11, f"Reports assessed for eligibility\n(n = {fmt(c['assessed'])})")
box(55, 28, 43, 18, "Reports excluded:\n" + "\n".join(f"  {k} (n = {fmt(v)})" for k, v in c["ft_reasons"].items()))
box(5, 6, 42, 16, f"Studies included in review\n(n = {fmt(c['included'])})\n"
    f"  from database searches (n = {fmt(c['included_db'])})\n"
    f"  from citation chasing (n = {fmt(c['included_cc'])})")
box(55, 8, 43, 12, f"Records from citation chasing\n(n = {fmt(c['cc_records'])}); reports assessed\n(n = {fmt(c['cc_assessed'])})")
arrow(26, 80, 26, 73); arrow(47, 89, 55, 89)
arrow(26, 64, 26, 59); arrow(47, 68.5, 55, 68.5)
arrow(26, 48, 26, 43); arrow(47, 54, 55, 54)
arrow(26, 32, 26, 22); arrow(47, 37.5, 55, 37.5)
arrow(55, 14, 47, 14)
fig.savefig("figures/fig1_prisma.png", dpi=600, bbox_inches="tight")
fig.savefig("figures/fig1_prisma.svg", bbox_inches="tight")
print("wrote figures/fig1_prisma.png and .svg")

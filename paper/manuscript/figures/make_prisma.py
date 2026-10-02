"""PRISMA 2020 flow diagram from counts.json (written by paper/review/scripts/synthesis.py).
Writes fig1_prisma.png (Word) and fig1_prisma.svg (PDF).
Usage: python3 figures/make_prisma.py   (run from paper/manuscript)"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

c = json.load(open("figures/counts.json"))
f = lambda v: f"{v:,}"
LABEL = {"I1": "I1 outside scope", "I2": "I2 no paired ID/OOD values", "I3": "I3 no source-only OOD value",
         "E1": "E1 excluded domain", "E2": "E2 synthetic shift", "E3": "E3 random splits only",
         "E4": "E4 review article", "E5": "E5 disjoint label space"}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.6})
fig, ax = plt.subplots(figsize=(7.4, 7.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
GREY, BLUE, WHITE = "#F2F2F2", "#E8F1F8", "#FFFFFF"


def box(x, y, w, h, text, fc=GREY):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc=fc, ec="black", lw=0.6))
    ax.text(x + 1.0, y + h - 1.0, text, va="top", ha="left", linespacing=1.32)


def arrow(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=0.6, color="black", shrinkA=0, shrinkB=0))


def band(y, h, label):
    ax.add_patch(FancyBboxPatch((0, y), 2.8, h, boxstyle="square,pad=0", fc=BLUE, ec="black", lw=0.6))
    ax.text(1.4, y + h / 2, label, rotation=90, va="center", ha="center", fontweight="bold")


ident = c["openalex"] + c["s2"] + c["earlier"]
band(84, 15, "Identification"); band(16, 66, "Screening"); band(1, 14, "Included")
ax.text(22, 99.6, "Identification of studies via databases", ha="center", va="bottom", fontweight="bold")
ax.text(87, 99.6, "Via other methods", ha="center", va="bottom", fontweight="bold")

# identification
box(4, 85, 36, 13, f"Records identified (n = {f(ident)}):\n  OpenAlex (n = {f(c['openalex'])})\n"
    f"  Semantic Scholar (n = {f(c['s2'])})\n  Earlier OpenAlex iteration (n = {f(c['earlier'])})")
box(43, 88, 29, 7, f"Removed before screening:\n  duplicate records (n = {f(c['duplicates'])})")
box(75, 85, 24, 13, f"Pre-specified sentinel\nstudies not retrieved by\nthe database search\n(n = {c['other_sought']})")
arrow(40, 91.5, 43, 91.5)

# screening
box(4, 73, 36, 7, f"Records screened (title/abstract)\n(n = {f(c['screened'])})")
box(43, 73, 29, 7, f"Records excluded\n(n = {f(c['excluded_ta'])})")
arrow(22, 85, 22, 80); arrow(40, 76.5, 43, 76.5)

box(4, 60, 36, 9, f"Reports sought for retrieval\n(n = {f(c['sought'])}; {f(c['studies'])} studies after linking\n"
    f"{c['dup_reports']} duplicate reports)")
box(43, 60, 29, 9, f"Full text not retrieved\n(n = {f(c['not_retrieved'])}); assessed on\nabstract under rule E4")
arrow(22, 73, 22, 69); arrow(40, 64.5, 43, 64.5)

ABL = dict(LABEL, E4="E4 no paired values")
ab = "\n".join(f"  {ABL[k]} (n = {v})" for k, v in c["abs_excluded"].items())
box(43, 37, 29, 20, f"Abstract-level outcome:\n Excluded (n = {c['abs_excluded_total']}):\n{ab}\n"
    f" Included on abstract\n values (n = {c['abs_included']})")
arrow(57.5, 60, 57.5, 57)

box(4, 47, 36, 8, f"Reports assessed in full text\n(n = {f(c['retrieved'])})")
arrow(22, 60, 22, 55)
ft = "\n".join(f"  {LABEL[k]} (n = {v})" for k, v in c["ft_excluded"].items())
box(4, 16.5, 36, 28.5, f"Full-text outcome:\n Excluded (n = {c['ft_excluded_total']}):\n{ft}\n"
    f" Eligible, values only in figures\n (n = {c['ft_fig']}; not synthesised)")
arrow(22, 47, 22, 45)

box(75, 60, 24, 9, f"Reports sought\n(n = {c['other_sought']}); not\nretrieved (n = {c['other_not_retrieved']})")
box(75, 47, 24, 8, f"Assessed for eligibility\n(n = {c['other_assessed']})")
arrow(87, 85, 87, 69); arrow(87, 60, 87, 55)

# included
box(4, 2, 95, 12, f"Studies included in the quantitative synthesis (n = {c['included']}):\n"
    f"  from full text (n = {c['ft_included']}, of which {c['ft_include_o']} report a target-trained reference "
    f"but no in-distribution value)\n"
    f"  from abstracts of reports whose full text could not be retrieved (n = {c['abs_included']})\n"
    f"  from other methods (n = {c['other_included']})", fc=WHITE)
arrow(22, 16.5, 22, 14); arrow(57.5, 37, 57.5, 14); arrow(87, 47, 87, 14)

fig.savefig("figures/fig1_prisma.png", dpi=600, bbox_inches="tight")
fig.savefig("figures/fig1_prisma.svg", bbox_inches="tight")
print("wrote figures/fig1_prisma.png and .svg")

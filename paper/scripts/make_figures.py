#!/usr/bin/env python3
"""figures/src/*.py -> figures/out/*.pdf.  Vector only, fonts matched to the paper.

Palette: Okabe-Ito, validated colour-vision-deficiency safe in this order.
Always pair colour with line style AND marker shape — papers get printed in
grayscale and read by colour-blind reviewers.
"""
import glob, os, runpy, sys

PALETTE = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9"]
REFERENCE = "#000000"     # baseline / ground truth
LINESTYLES = ["-", "--", ":", "-."]
MARKERS = ["o", "s", "^", "D", "v", "P"]

RC = {                       # apply with matplotlib.rcParams.update(RC)
    "figure.figsize": (3.3, 2.4),      # one column; re-export, never \includegraphics-scale
    "savefig.format": "pdf", "savefig.bbox": "tight", "savefig.pad_inches": 0.01,
    "pdf.fonttype": 42, "ps.fonttype": 42,     # embed real fonts, not Type 3
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.4,
    "lines.linewidth": 1.4, "lines.markersize": 4,
    "legend.frameon": False, "figure.dpi": 200,
}

if __name__ == "__main__":
    os.makedirs("figures/out", exist_ok=True)
    srcs = sorted(glob.glob("figures/src/*.py"))
    if not srcs:
        print("no figures/src/*.py yet. Import PALETTE/RC from this module in each one.")
        sys.exit(0)
    for s in srcs:
        print(f"running {s}")
        runpy.run_path(s, run_name="__main__")

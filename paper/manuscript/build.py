"""Build the manuscript as Word (.docx) and PDF from review.md (single source).

review.md is a template: every {{ expression }} is replaced by a number from ../review/analysis/results.json or
figures/counts.json, and {{ include('file') }} inserts a generated table, so no number in the paper is typed by hand.
Usage (from paper/manuscript):  python3 build.py [--version v1.0]
Outputs: ../output/distribution_shift_review_<version>.docx and .pdf, and build/review_rendered.md"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile

import pypandoc

os.chdir(os.path.dirname(os.path.abspath(__file__)))
ver = sys.argv[sys.argv.index("--version") + 1] if "--version" in sys.argv else "v1.0"
out_dir = os.path.abspath("../output")
os.makedirs(out_dir, exist_ok=True)
os.makedirs("build", exist_ok=True)
name = f"distribution_shift_review_{ver}"
pandoc, py = pypandoc.get_pandoc_path(), sys.executable

# ---------------------------------------------------------------- regenerate figure 1 and the tables, then render
subprocess.run([py, "figures/make_prisma.py"], check=True)
subprocess.run([py, "make_tables.py"], check=True)
if not os.path.exists("reference.docx"):
    subprocess.run([py, "make_reference_docx.py"], check=True)

R = json.load(open("../review/analysis/results.json"))
C = json.load(open("figures/counts.json"))


def _get(d, path):
    """Walk nested keys separated by '>'; a key may itself contain '>' (longest matching key wins)."""
    while path:
        k = max((k for k in d if path == k or path.startswith(k + ">")), key=len)
        d, path = d[k], path[len(k) + 1:]
    return d


v = lambda p: _get(R, p)
c = lambda p: _get(C, p)
f1 = lambda x: f"{x:.1f}"
f2 = lambda x: f"{x:.2f}".replace("-", "−")
f3 = lambda x: f"{x:.3f}"
n = lambda x: f"{x:,}"
pc = lambda x: f"{round(100 * x)}".replace("-", "−")
pc_of = lambda a, b: f"{round(100 * a / b)}"
med = lambda p: f2(v(p)["median"])
iqr = lambda p: f"{f2(v(p)['q1'])}–{f2(v(p)['q3'])}"
ci = lambda p: f"{f2(v(p)['ci_lo'])}–{f2(v(p)['ci_hi'])}"
n_ = lambda p: v(p)["n"]
ch = lambda group, key: R["characteristics"][group].get(key, 0)
a = lambda q, level: R["appraisal"][q][level]
ap = lambda q, level: pc_of(R["appraisal"][q][level], R["n_appraised"])
wc = lambda name, field: R["within_study_contrasts"][name][field]
tx = lambda task, shift: f2(R["ret_by_task_shift"][f"{task}|{shift}"]["median"])
include = lambda path: open(path).read().strip()
NS = dict(v=v, c=c, f1=f1, f2=f2, f3=f3, n=n, pc=pc, pc_of=pc_of, med=med, iqr=iqr, ci=ci, n_=n_, ch=ch, a=a, ap=ap,
          wc=wc, tx=tx, include=include)


def render(text):
    return re.sub(r"\{\{(.+?)\}\}", lambda m: str(eval(m.group(1), {"__builtins__": {}}, NS)), text, flags=re.S)


rendered = render(open("review.md").read())
if "{{" in rendered:                      # LaTeX can contain "}}" but never "{{"
    sys.exit("unrendered template markers remain: " +
             " | ".join(m.group(0) for m in re.finditer(r".{0,40}\{\{.{0,40}", rendered)))
src = os.path.abspath("build/review_rendered.md")
open(src, "w").write(rendered)

common = [src, "--citeproc", "--bibliography=refs.bib", "--bibliography=generated/included.bib",
          "--csl=elsevier-harvard.csl", "--number-sections", "--resource-path=.:figures"]

docx = f"{out_dir}/{name}.docx"
subprocess.run([pandoc, *common, "--reference-doc=reference.docx", "-o", docx], check=True)
with zipfile.ZipFile(docx) as z:
    xml = z.read("word/document.xml").decode("utf-8")
print("docx:", docx, "| line numbers:", "lnNumType" in xml)

html = os.path.abspath(f"build/{name}.html")
subprocess.run([pandoc, *common, "-s", "--embed-resources", "--css=pdf.css", "--lua-filter=svg.lua", "--mathml",
                "--metadata=pagetitle:Distribution shift review", "-o", html], check=True)

CANDIDATES = ["/opt/pw-browsers/chromium", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              shutil.which("chromium") or "", shutil.which("google-chrome") or ""]
chrome = next((p for p in CANDIDATES if p and os.path.exists(p)), None)
if chrome is None:
    sys.exit("no Chrome or Chromium found for PDF printing")
pdf = f"{out_dir}/{name}.pdf"
if os.path.exists(pdf):
    os.remove(pdf)
profile = os.path.abspath("build/chrome-profile")
proc = subprocess.Popen([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-first-run",
                         "--disable-extensions", "--no-pdf-header-footer", f"--user-data-dir={profile}",
                         f"--print-to-pdf={pdf}", "file://" + html],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
last, stable = -1, 0
for _ in range(240):                      # Chrome writes the PDF, then may linger; stop it once the file is stable
    time.sleep(1)
    size = os.path.getsize(pdf) if os.path.exists(pdf) else -1
    stable = stable + 1 if size > 0 and size == last else 0
    last = size
    if stable >= 3 or proc.poll() is not None:
        break
proc.terminate()
try:
    proc.wait(timeout=10)
except subprocess.TimeoutExpired:
    proc.kill()
subprocess.run(["pkill", "-f", profile], capture_output=True)
print("pdf: ", pdf, f"({os.path.getsize(pdf) // 1024} KB)" if os.path.exists(pdf) else "(not written)")

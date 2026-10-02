"""Build the manuscript as Word (.docx) and PDF from review.md (single source).
Usage (from paper/manuscript):  ../.venv/bin/python build.py [--version v0.1]
Outputs: ../output/distribution_shift_review_<version>.docx and .pdf"""
import os
import subprocess
import sys
import time
import zipfile

import pypandoc

os.chdir(os.path.dirname(os.path.abspath(__file__)))
ver = sys.argv[sys.argv.index("--version") + 1] if "--version" in sys.argv else "v0.1"
out_dir = os.path.abspath("../output")
os.makedirs(out_dir, exist_ok=True)
os.makedirs("build", exist_ok=True)
name = f"distribution_shift_review_{ver}"
pandoc, py = pypandoc.get_pandoc_path(), sys.executable

subprocess.run([py, "figures/make_prisma.py"], check=True)
if not os.path.exists("reference.docx"):
    subprocess.run([py, "make_reference_docx.py"], check=True)

common = ["review.md", "--citeproc", "--bibliography=refs.bib", "--csl=elsevier-harvard.csl",
          "--number-sections", "--resource-path=.:figures"]

docx = f"{out_dir}/{name}.docx"
subprocess.run([pandoc, *common, "--reference-doc=reference.docx", "-o", docx], check=True)
with zipfile.ZipFile(docx) as z:
    xml = z.read("word/document.xml").decode("utf-8")
print("docx:", docx, "| line numbers:", "lnNumType" in xml)

html = os.path.abspath(f"build/{name}.html")
subprocess.run([pandoc, *common, "-s", "--embed-resources", "--css=pdf.css", "--lua-filter=svg.lua", "--mathml",
                "--metadata=pagetitle:Distribution shift review", "-o", html], check=True)
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
pdf = f"{out_dir}/{name}.pdf"
if os.path.exists(pdf):
    os.remove(pdf)
proc = subprocess.Popen([chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--disable-extensions",
                         "--no-pdf-header-footer", f"--user-data-dir={os.path.abspath('build/chrome-profile')}",
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
subprocess.run(["pkill", "-f", os.path.abspath("build/chrome-profile")], capture_output=True)
print("pdf: ", pdf)

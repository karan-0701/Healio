from pypdf import PdfReader # type: ignore
import json

try:
    reader = PdfReader("./data/karandeep_mlops.pdf")
    resume = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume += text
except FileNotFoundError:
    resume = "Resume not file not found"


with open("./data/summary.txt", "r") as f:
    summary = f.read()

with open("./data/style.txt", "r") as f:
    style = f.read()

with open("./data/facts.json", "r") as f:
    facts = json.load(f)

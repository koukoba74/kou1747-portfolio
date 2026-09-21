from pathlib import Path
import re, sys

OUT = Path(__file__).resolve().parent / "output"
errors = []
pages = list(OUT.glob("*.html"))
for page in pages:
    text = page.read_text(encoding="utf-8")
    if len(re.findall(r"<h1(?:\\s|>)", text, re.I)) != 1:
        errors.append(f"{page.name}: h1")
    if not re.search(r"<title>.+?</title>", text, re.I | re.S):
        errors.append(f"{page.name}: title")
    if "{{" in text or "}}" in text:
        errors.append(f"{page.name}: placeholder")
if errors:
    print("FAIL"); print("\n".join(errors)); sys.exit(1)
print(f"PASS: {len(pages)} pages")
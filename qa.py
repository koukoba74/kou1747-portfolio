from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parent
errors = []
PUBLIC_HTML = [
    ROOT / "index.html",
    ROOT / "pf01" / "index.html",
    ROOT / "pf02" / "index.html",
    ROOT / "pf03" / "index.html",
]

for page in PUBLIC_HTML:
    if not page.exists():
        errors.append(f"{page.relative_to(ROOT)}: missing")
        continue
    text = page.read_text(encoding="utf-8")
    if '<meta name="viewport"' not in text:
        errors.append(f"{page.relative_to(ROOT)}: viewport missing")
    if len(re.findall(r"<h1(?:\s|>)", text, re.I)) != 1:
        errors.append(f"{page.relative_to(ROOT)}: h1 count")
    if not re.search(r"<title>.+?</title>", text, re.I | re.S):
        errors.append(f"{page.relative_to(ROOT)}: title missing")
    for href in re.findall(r'href="([^"]+)"', text, re.I):
        if href.startswith(("http://","https://","#","mailto:","data:")):
            continue
        href_path = href.split("#")[0].split("?")[0]
        if not href_path:
            continue
        target = (page.parent / href_path).resolve()
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{page.relative_to(ROOT)}: broken link {href}")

print("PASS" if not errors else "FAIL")
if errors:
    print("\n".join(errors))
    sys.exit(1)

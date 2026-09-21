from pathlib import Path
import csv, html

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

TEMPLATE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title></head><body><main><p>自主制作</p><h1>{title}</h1>
<p><strong>{summary}</strong></p><div role="img" aria-label="{image_alt}">IMAGE PLACEHOLDER</div><p>{body}</p></main></body></html>"""

with (ROOT / "content.csv").open(encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    safe = {k: html.escape(v or "") for k, v in row.items()}
    (OUT / f"{safe['slug']}.html").write_text(TEMPLATE.format(**safe), encoding="utf-8")

print(f"generated: {len(rows)} pages")
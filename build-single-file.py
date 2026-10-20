"""Bundle index.html + images/ into one self-contained file: dist/index.html.

Every <img src="images/..."> is replaced with the image embedded as a
base64 data URI (each image once — the gallery reuses the card photos).
Run:  python3 build-single-file.py
"""
import base64, mimetypes, pathlib, re

root = pathlib.Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")
used = set()

def embed(m):
    path = root / m.group(1)
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    used.add(path.name)
    return 'src="data:%s;base64,%s"' % (mime, base64.b64encode(path.read_bytes()).decode("ascii"))

out = re.sub(r'src="(images/[^"]+)"', embed, html)
assert "images/" not in re.sub(r"/\*.*?\*/", "", out, flags=re.S), "an image path was left unembedded"
(root / "dist").mkdir(exist_ok=True)
(root / "dist" / "index.html").write_text(out, encoding="utf-8")
missing = {p.name for p in (root / "images").iterdir()} - used
print("dist/index.html: %d images embedded, %.2f MB" % (len(used), len(out.encode()) / 1e6))
if missing: print("note: not referenced by the page:", sorted(missing))

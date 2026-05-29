"""Bulk find/replace + page rename for Toowoomba Roof Repairs.

CONSERVATIVE — only boilerplate (URLs, brand, suburb names, postcode/coords, file renames).
All deep content hand-rewritten per page.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SELF_NAME = Path(__file__).name

REPLACEMENTS = [
    ("https://pakenhamdecking.com.au", "https://toowoombaroofrepairs.com.au"),
    ("https://pakenhamdecking.netlify.app", "https://toowoombaroofrepairs.netlify.app"),
    ("pakenhamdecking.netlify.app", "toowoombaroofrepairs.netlify.app"),
    ("pakenhamdecking.com.au", "toowoombaroofrepairs.com.au"),
    ("pakenhamdecking", "toowoombaroofrepairs"),
    ("Pakenham Decking &amp; Pergolas", "Toowoomba Roof Repairs"),
    ("Pakenham Decking & Pergolas", "Toowoomba Roof Repairs"),
    ("/officer/", "/glenvale/"),
    ("/beaconsfield/", "/wilsonton/"),
    ("/cockatoo/", "/highfields/"),
    ("/emerald/", "/rangeville/"),
    ("/pakenham-upper/", "/centenary-heights/"),
    ("/cardinia-shire/", "/toowoomba-region/"),
    ("/services/timber-decking/", "/services/roof-restoration/"),
    ("/services/composite-decking/", "/services/roof-repairs/"),
    ("/services/pergolas/", "/services/storm-hail-damage/"),
    ("/services/alfresco-outdoor-kitchens/", "/services/roof-replacement/"),
    ("/services/deck-restoration/", "/services/metal-roofing/"),
    ("VIC 3810", "QLD 4350"),
    ('"VIC"', '"QLD"'),
    ('"3810"', '"4350"'),
    ("Pakenham VIC 3810", "Toowoomba QLD 4350"),
    ("3810", "4350"),
    ("-38.0814", "-27.5598"),
    ("145.4842", "151.9507"),
    (">P</text>", ">T</text>"),  # favicon letter
]

EXTENSIONS = {".astro", ".md", ".toml", ".mjs", ".json", ".xml", ".txt", ".html", ".css", ".js"}

def patch_file(p):
    try:
        s = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    out = s
    for old, new in REPLACEMENTS:
        out = out.replace(old, new)
    if out != s:
        p.write_text(out, encoding="utf-8")
        return True
    return False

def main():
    PAGES = ROOT / "src" / "pages"
    for old, new in [
        ("officer.astro", "surfers-paradise.astro"),
        ("beaconsfield.astro", "southport.astro"),
        ("cockatoo.astro", "robina.astro"),
        ("emerald.astro", "coombabah.astro"),
        ("pakenham-upper.astro", "currumbin.astro"),
        ("cardinia-shire.astro", "toowoomba-region.astro"),
    ]:
        o, n = PAGES / old, PAGES / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed: {old} -> {new}")

    SVC = PAGES / "services"
    for old, new in [
        ("timber-decking.astro", "pre-purchase-inspection.astro"),
        ("composite-decking.astro", "annual-inspection.astro"),
        ("pergolas.astro", "chemical-soil-treatment.astro"),
        ("alfresco-outdoor-kitchens.astro", "baiting-systems.astro"),
        ("deck-restoration.astro", "post-construction-protection.astro"),
    ]:
        o, n = SVC / old, SVC / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed services/{old} -> {new}")

    changed = 0
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        if p.suffix not in EXTENSIONS: continue
        if "node_modules" in p.parts or "dist" in p.parts: continue
        if p.name == SELF_NAME: continue
        if patch_file(p):
            changed += 1

    pkg = ROOT / "package.json"
    if pkg.exists():
        s = pkg.read_text(encoding="utf-8")
        s = s.replace('"name": "pakenhamdecking"', '"name": "toowoombaroofrepairs"')
        pkg.write_text(s, encoding="utf-8")

    print(f"Done. {changed} files patched.")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Ponechá v katalógu len produkty, ktoré sú v exporte zo Shopify.

Použitie:  python3 tools/filter_catalog.py cesta/k/products_export.csv
Zálohu pôvodných dát nájdete v histórii gitu.
"""
import csv, json, re, sys, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "products.js")

CAT_ORDER = ["hood","flexible","rooftent","tonneau","rv","foldable",
             "blanket","controller","inverter","accessory","other"]

def load_handles(csv_path):
    """Vráti (aktívne, neaktívne) handle z exportu."""
    active, draft = [], []
    with open(csv_path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            h = (r.get("Handle") or "").strip()
            t = (r.get("Title") or "").strip()
            if not h or not t:
                continue                      # riadky s variantmi/fotkami
            st = (r.get("Status") or "").strip().lower()
            (draft if st and st != "active" else active).append(h)
    return list(dict.fromkeys(active)), list(dict.fromkeys(draft))

def main(csv_path):
    src = open(DATA, encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", src, re.S).group(1))
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});", src, re.S).group(1))
    cat_names = {c["k"]: c for c in meta["cats"]}

    active, draft = load_handles(csv_path)
    keep = set(active)
    kept = [p for p in P if p["id"] in keep]
    removed = [p for p in P if p["id"] not in keep]
    missing = [h for h in active if h not in {p["id"] for p in P}]

    # prepočítať počty kategórií a značiek
    cats = Counter(p["cat"] for p in kept)
    brands = Counter(p["b"] for p in kept if p["b"])
    new_meta = {
        "cats": [{"k": k, "sk": cat_names[k]["sk"], "cs": cat_names[k]["cs"], "n": cats[k]}
                 for k in CAT_ORDER if cats[k]],
        "brands": [{"k": b, "n": n} for b, n in sorted(brands.items(), key=lambda kv: (-kv[1], kv[0]))],
        "count": len(kept),
    }
    order = {c: i for i, c in enumerate(CAT_ORDER)}
    kept.sort(key=lambda x: (order.get(x["cat"], 99), x["b"] or "zzzz", -(x["w"] or 0), x["n"]["sk"]))

    with open(DATA, "w", encoding="utf-8") as f:
        f.write("/* Generované dáta katalógu — negenerujte ručne. */\n")
        f.write("window.CATALOG_META=" + json.dumps(new_meta, ensure_ascii=False, separators=(",", ":")) + ";\n")
        f.write("window.PRODUCTS=" + json.dumps(kept, ensure_ascii=False, separators=(",", ":")) + ";\n")

    print(f"ponechané:  {len(kept)}")
    print(f"odstránené: {len(removed)}")
    print(f"kategórie:  {dict(cats)}")
    print(f"značky:     {len(brands)}")
    nocat = [p for p in kept if p["cat"] == "other"]
    print(f"bez kategórie: {len(nocat)}" + ("" if not nocat else " -> " + ", ".join(p["id"] for p in nocat)))
    if draft:
        print("v exporte, ale neaktívne (nepridané):", ", ".join(draft))
    if missing:
        print("v exporte, ale chýbajú v dátach:", ", ".join(missing))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Downloads/products_export.csv"))

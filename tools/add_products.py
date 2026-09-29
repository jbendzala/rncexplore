# -*- coding: utf-8 -*-
"""Pridá do data/products.js nové produkty z ponuky Lensunu.

Zoznam, ktorý sa má pridať, je v NOVE nižšie: stačí handle z lensunsolar.com,
kategória, značka a slovenský aj český názov s popisom. Zvyšok — ceny,
prevedenia, fotografie, technické parametre, obsah balenia a video — si
skript stiahne priamo z Lensunu, aby sa ručne neprepisovalo nič, čo je
už raz niekde zapísané.

Spustenie:  python3 tools/add_products.py [--dry-run]
"""
import json
import os
import re
import sys
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enrich_products import SPEC_KEYS, parse_pack, strip_tags, tidy  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "products.js")
UA = {"User-Agent": "Mozilla/5.0"}

CAT_ORDER = ["hood", "flexible", "rooftent", "tonneau", "rv", "foldable",
             "blanket", "controller", "inverter", "accessory", "other"]

# Anglické názvy prevedení, ako ich píše Lensun, na naše. Kľúč sa hľadá
# v názve zmenšenom na malé písmená, prvá zhoda vyhráva — preto idú dlhšie
# a konkrétnejšie tvary skôr.
VARIANTS = [
    ("complete kit",        ("Kompletná sada (panel + MPPT regulátor + fólia)",
                             "Kompletní sada (panel + MPPT regulátor + fólie)")),
    ("mppt solar controller", ("Panel + MPPT regulátor", "Panel + MPPT regulátor")),
    ("mppt controller",     ("Panel + MPPT regulátor", "Panel + MPPT regulátor")),
    ("vinyl decal",         ("Panel + vinylová fólia", "Panel + vinylová fólie")),
    ("controller + y connectors", ("Panel + regulátor + predlžovací kábel",
                                   "Panel + regulátor + prodlužovací kabel")),
    ("controller + extend", ("Panel + regulátor + predlžovací kábel",
                             "Panel + regulátor + prodlužovací kabel")),
    ("y connectors",        ("Panel + predlžovací kábel", "Panel + prodlužovací kabel")),
    ("extend",              ("Panel + predlžovací kábel", "Panel + prodlužovací kabel")),
    ("controller",          ("Panel + regulátor", "Panel + regulátor")),
    ("panel only",          ("Samotný panel", "Samotný panel")),
    ("default title",       ("Základné prevedenie", "Základní provedení")),
]


def vlabel(title):
    """Názov prevedenia. Lensun ho píše zakaždým inak — „Solar Panel +
    Solar Controller", „Solar Panel + 20A Solar Controller + Extend
    16ft/5m Cable", „2pcs 80w solar panel" — a zoznam vzoriek na to
    nestačil: dve rôzne prevedenia vychádzali rovnako a zákazník potom
    v ponuke nevidel, čím sa líšia. Preto názov neprekladáme, ale
    skladáme z toho, čo v balení naozaj je."""
    t = (title or "").lower()

    # hotová sada má u Lensunu ustálené pomenovanie, to necháme
    if "complete kit" in t or "full kit" in t or "fullkit" in t:
        return ("Kompletná sada (panel + MPPT regulátor + fólia)",
                "Kompletní sada (panel + MPPT regulátor + fólie)")

    kusov = 1
    if "two solar panels" in t or "2pcs" in t or "2 pcs" in t:
        kusov = 2
    elif "three solar panels" in t or "3pcs" in t or "3 pcs" in t:
        kusov = 3

    mppt = "mppt" in t
    regulator = "controller" in t or "regulator" in t
    kabel = "cable" in t or "extend" in t or "connector" in t
    folia = "decal" in t

    pridane_sk, pridane_cs = [], []
    if regulator:
        pridane_sk.append("MPPT regulátor" if mppt else "regulátor")
        pridane_cs.append("MPPT regulátor" if mppt else "regulátor")
    if folia:
        pridane_sk.append("vinylová fólia"); pridane_cs.append("vinylová fólie")
    if kabel:
        pridane_sk.append("predlžovací kábel"); pridane_cs.append("prodlužovací kabel")

    if kusov == 1:
        zaklad_sk = zaklad_cs = "Panel" if pridane_sk else "Samotný panel"
    elif kusov == 2:
        zaklad_sk, zaklad_cs = "Dva panely", "Dva panely"
    else:
        zaklad_sk, zaklad_cs = "Tri panely", "Tři panely"

    return (" + ".join([zaklad_sk] + pridane_sk),
            " + ".join([zaklad_cs] + pridane_cs))


def fetch(handle):
    url = f"https://lensunsolar.com/products/{handle}.json"
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=30))["product"]


def build(item):
    """Z jedného riadka zoznamu a dát z Lensunu poskladá záznam katalógu."""
    d = fetch(item["h"])
    vs = sorted(d["variants"], key=lambda v: float(v["price"]))
    body = d.get("body_html") or ""
    text = strip_tags(body)

    specs = {}
    for line in text.split("\n"):
        line = line.strip()
        for label, key in SPEC_KEYS:
            if key in specs:
                continue
            m = re.match(re.escape(label) + r"\s*[:：]\s*(.+)$", line, re.I)
            if m:
                val = tidy(m.group(1), key)
                if val:
                    specs[key] = val

    rec = {
        "id": item["h"], "cat": item["cat"], "b": item.get("b"),
        "w": item.get("w"), "a": None, "v": None,
        "kg": round(float(vs[0].get("grams") or 0) / 1000.0, 1) or None,
        "usd": float(vs[0]["price"]),
        "was": float(vs[0]["compare_at_price"]) if vs[0].get("compare_at_price") else None,
        "img": [im["src"].split("?")[0] for im in d.get("images", [])][:8],
        "sku": vs[0].get("sku") or "",
        "n": {"sk": item["sk"], "cs": item["cs"]},
        "d": {"sk": item["dsk"], "cs": item["dcs"]},
        "var": [],
    }
    for v in vs:
        sk, cs = vlabel(v.get("title"))
        rec["var"].append({
            "sk": sk, "cs": cs, "p": float(v["price"]), "sku": v.get("sku") or "",
            "was": float(v["compare_at_price"]) if v.get("compare_at_price") else None,
        })
    # Pár produktov má parametre v popise rozsypané vo vetách, nie v riadkoch
    # „Peak power: …“. Tam sa dajú dopísať ručne cez kľúč spec v zozname.
    specs.update(item.get("spec") or {})
    if specs:
        rec["spec"] = specs
    pack = parse_pack(text)
    if pack:
        rec["pack"] = pack
    vid = re.search(r"(?:youtube\.com/embed/|youtu\.be/)([A-Za-z0-9_-]{8,})", body)
    if vid:
        rec["vid"] = vid.group(1)
    return rec


def write(P):
    """Prepíše katalóg aj s prepočítanými počtami kategórií a značiek."""
    src = open(DATA, encoding="utf-8").read()
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});", src, re.S).group(1))
    # Názvy kategórií berieme z menu, nie z katalógu — inak by prvý produkt
    # v dosiaľ prázdnej kategórii spadol na chýbajúcom preklade.
    from pages_shell import SUBCATS
    names = {k: {"sk": a, "cs": b} for k, a, b in SUBCATS}
    names.update({c["k"]: c for c in meta["cats"]})
    cats = Counter(p["cat"] for p in P)
    brands = Counter(p["b"] for p in P if p["b"])
    new_meta = {
        "cats": [{"k": k, "sk": names[k]["sk"], "cs": names[k]["cs"], "n": cats[k]}
                 for k in CAT_ORDER if cats[k]],
        "brands": [{"k": b, "n": n} for b, n in sorted(brands.items(), key=lambda kv: (-kv[1], kv[0]))],
        "count": len(P),
    }
    order = {c: i for i, c in enumerate(CAT_ORDER)}
    P.sort(key=lambda x: (order.get(x["cat"], 99), x["b"] or "zzzz", -(x["w"] or 0), x["n"]["sk"]))
    with open(DATA, "w", encoding="utf-8") as f:
        f.write("/* Generované dáta katalógu — negenerujte ručne. */\n")
        f.write("window.CATALOG_META=" + json.dumps(new_meta, ensure_ascii=False, separators=(",", ":")) + ";\n")
        f.write("window.PRODUCTS=" + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + ";\n")


def main():
    from new_products import NOVE, NAHRADY
    dry = "--dry-run" in sys.argv
    src = open(DATA, encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", src, re.S).group(1))
    have = {p["id"] for p in P}

    # 1. náhrady — Lensun produkt prepublikoval s iným výkonom aj odkazom
    for old, item in NAHRADY:
        if old not in have:
            print(f"  preskakujem, v katalógu nie je: {old}")
            continue
        P = [p for p in P if p["id"] != old]
        P.append(build(item))
        print(f"  nahradené  {old}\n          -> {item['h']}")

    # 2. novinky
    added = 0
    for item in NOVE:
        if item["h"] in have:
            print(f"  už máme:   {item['h']}")
            continue
        P.append(build(item))
        added += 1
        print(f"  pridané:   {item['h']}")

    print(f"\nnáhrad: {len(NAHRADY)}   noviniek: {added}   spolu v katalógu: {len(P)}")
    if dry:
        print("--dry-run: nič som nezapísal")
        return 0
    write(P)
    print("data/products.js prepísaný")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

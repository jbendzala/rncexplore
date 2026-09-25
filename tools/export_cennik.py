# -*- coding: utf-8 -*-
"""Vyexportuje katalóg do zošita Excelu pre cenník.

Názvy aj ceny berie z tých istých zdrojov ako web — data/products.js
a vzorec z tools/seo.py — takže v cenníku nemôže byť iné pomenovanie
ani iné číslo než na stránke.

Spustenie:
    python3 tools/export_cennik.py                 # do ~/Documents
    python3 tools/export_cennik.py /cesta/sub.xlsx
"""
import json
import os
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo  # noqa: E402  — rovnaký vzorec ceny ako na webe

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.rncexplore.com"

HEAD_BG = PatternFill("solid", fgColor="1F3A5F")
HEAD_FG = Font(bold=True, color="FFFFFF")


def catalog():
    s = open(os.path.join(ROOT, "data", "products.js"), encoding="utf-8").read()
    ps = json.loads(re.search(r"window\.PRODUCTS=(\[.*?\]);\s*\n", s, re.S).group(1))
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});\s*\n", s, re.S).group(1))
    cats = {c["k"]: c for c in meta["cats"]}
    return ps, cats


def variants(p):
    """Prevedenia produktu v poradí od najlacnejšieho, ako ich radí web."""
    vs = p.get("var") or [{"p": p["usd"], "sku": p.get("sku"), "sk": None, "cs": None}]
    return sorted(vs, key=lambda v: v["p"])


def sheet(wb, title, cols):
    ws = wb.create_sheet(title)
    ws.append([c[0] for c in cols])
    for i, (label, width, fmt) in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=i)
        cell.fill, cell.font = HEAD_BG, HEAD_FG
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"
    return ws


def finish(ws, cols, rows):
    """Dopíše riadky a nastaví formát čísel podľa hlavičky."""
    for r in rows:
        ws.append(r)
    for i, (_, _, fmt) in enumerate(cols, start=1):
        if not fmt:
            continue
        for c in range(2, ws.max_row + 1):
            ws.cell(row=c, column=i).number_format = fmt
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{ws.max_row}"


def build(out):
    ps, cats = catalog()
    # najprv panely podľa značky vozidla, univerzálne až za nimi
    ps = sorted(ps, key=lambda p: (0 if p.get("b") else 1, p.get("b") or "",
                                   -(p.get("w") or 0), p["n"]["sk"]))
    wb = Workbook()
    wb.remove(wb.active)

    # ---- prehľad produktov: to, čo zákazník vidí ako názov ----
    cols = [("#", 5, None), ("Názov produktu (web SK)", 62, None),
            ("Názov produktu (web CZ)", 62, None), ("Kategória", 20, None),
            ("Značka", 16, None), ("Výkon (W)", 11, "0"),
            ("Prevedení", 11, "0"), ("Odkaz", 58, None)]
    ws = sheet(wb, "Produkty", cols)
    rows = []
    for i, p in enumerate(ps, start=1):
        rows.append([i, p["n"]["sk"], p["n"]["cs"],
                     cats.get(p["cat"], {}).get("sk", p["cat"]),
                     p.get("b") or "univerzálny",
                     p.get("w") or "", len(variants(p)),
                     f"{SITE}/produkt/{p['id']}.html"])
    finish(ws, cols, rows)

    # ---- cenníky: riadok na každé prevedenie, cena presne ako na webe ----
    for lang, cur, tab in (("sk", "EUR", "Cenník SK"), ("cs", "CZK", "Cenník CZ")):
        money = '#,##0.00\\ "€"' if cur == "EUR" else '#,##0\\ "Kč"'
        cols = [("#", 5, None),
                ("Názov produktu (ako na webe)", 62, None),
                ("Prevedenie", 40, None), ("Kód (SKU)", 26, None),
                ("Cena bez DPH", 15, money), ("DPH 23 %", 14, money),
                ("Cena s DPH", 15, money), ("Odkaz", 58, None)]
        ws = sheet(wb, tab, cols)
        rows, i = [], 0
        for p in ps:
            for v in variants(p):
                i += 1
                gross = seo.price(v["p"], cur)
                # základ dopočítame z konečnej ceny, aby súčet na faktúre
                # dal presne to, čo zákazník vidí na stránke
                net = round(gross / (1 + seo.CFG["vat"]), 2)
                url = f"{SITE}/produkt/{p['id']}.html" if lang == "sk" \
                    else f"{SITE}/cz/produkt/{p['id']}.html"
                rows.append([i, p["n"][lang], v.get(lang) or "—",
                             v.get("sku") or p.get("sku") or "",
                             net, round(gross - net, 2), gross, url])
        finish(ws, cols, rows)

    # ---- nákupná strana; tento list pred posielaním von zmažte ----
    cols = [("#", 5, None), ("Názov produktu (web SK)", 62, None),
            ("Prevedenie", 40, None), ("Kód (SKU)", 26, None),
            ("Lensun (USD)", 14, '#,##0.00\\ "$"'),
            ("MO bez DPH (EUR)", 17, '#,##0.00\\ "€"'),
            ("MO s DPH (EUR)", 16, '#,##0.00\\ "€"'),
            ("MO s DPH (CZK)", 16, '#,##0\\ "Kč"')]
    ws = sheet(wb, "Interné – nákup", cols)
    rows, i = [], 0
    for p in ps:
        for v in variants(p):
            i += 1
            rows.append([i, p["n"]["sk"], v.get("sk") or "—",
                         v.get("sku") or p.get("sku") or "", v["p"], v["p"],
                         seo.price(v["p"], "EUR"), seo.price(v["p"], "CZK")])
    finish(ws, cols, rows)

    wb.save(out)
    return len(ps), i


if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/Documents/rncexplore-cennik.xlsx")
    n, v = build(dest)
    print(f"{n} produktov, {v} prevedení -> {dest}")

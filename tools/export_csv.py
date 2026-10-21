# -*- coding: utf-8 -*-
"""Vypíše celý katalóg do CSV — jeden riadok na prevedenie.

Súbor je v UTF-8 s BOM a stredníkom ako oddeľovačom, aby sa slovenský
Excel otvoril správne a nerozsypal diakritiku ani desatinné čiarky.
"""
import csv, json, os, re, sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo
import vystup

CIEL = vystup.kam(vystup.NASE, "produkty.csv")
WEB = "https://www.rncexplore.com"


def nacitaj():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});", s, re.S).group(1))
    prod = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))
    return {c["k"]: c["sk"] for c in meta["cats"]}, prod


def cislo(v):
    """Desatinná čiarka — inak to slovenský Excel berie ako text."""
    return f"{v:.2f}".replace(".", ",")


def main():
    kat, P = nacitaj()
    dph = seo.CFG.get("vat", 0.23)
    riadkov = 0
    with open(CIEL, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow([
            "Kód produktu", "Názov SK", "Názov CZ", "Kategória", "Značka",
            "Výkon (W)", "Prevedenie SK", "Prevedenie CZ",
            "Cena bez DPH (EUR)", "DPH (EUR)", "Cena s DPH (EUR)",
            "Cena s DPH (CZK)", "Odkaz",
        ])
        for p in P:
            for v in p["var"]:
                brutto = seo.price(v["p"], "EUR")
                netto = brutto / (1 + dph)
                w.writerow([
                    v.get("sku", ""),
                    p["n"]["sk"], p["n"]["cs"],
                    kat.get(p["cat"], p["cat"]),
                    p.get("b") or "univerzálny",
                    p.get("w") or "",
                    v["sk"], v["cs"],
                    cislo(netto), cislo(brutto - netto), cislo(brutto),
                    cislo(seo.price(v["p"], "CZK")),
                    f"{WEB}/produkt/{p['id']}.html",
                ])
                riadkov += 1
    print(f"{len(P)} produktov, {riadkov} prevedení -> {CIEL}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Vypíše katalóg Purelux do CSV vo formáte, aký Shoptet sám exportuje.

Rovnaký vzor ako tools/export_shoptet.py (odtiaľ je prevzaté kod()/pole()/
DAVKA), s jedným rozdielom: cena sa posiela priamo z p["eur"]/v["p"], bez
tools/seo.py's price(). Tá funkcia počíta z USD cez kurz/prirážku/dopravu/
DPH pre Lensun — Purelux ceny sú už hotové € s DPH priamo z valostore,
prehnanie cez ten istý prepočet by ich pokazilo.
"""
import hashlib
import json
import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup

CIEL = vystup.kam(vystup.IMPORT, "purelux-produkty-csv", "produkty.csv")

DAVKA = 40
PARAMETER = "Variant"
SKLAD = "0"


def kod(p, v):
    """Rovnaký dôvod ako pri Lensune — jedno SKU vie niesť viac produktov
    (napr. relay kit v inom bundle), značka za pomlčkou kolízii zabráni."""
    znacka = hashlib.sha1(p["id"].encode("utf-8")).hexdigest()[:4].upper()
    return f'{v.get("sku", "")}-{znacka}'


def pole(v, uvodzovky=True):
    if v == "" or v is None:
        return '""' if uvodzovky else ""
    return '"' + str(v).replace('"', '""') + '"'


def riadok(p, v, skupina, viac):
    cena = f'{v["p"]:.2f}'.replace(".", ",")
    return ";".join([
        pole(kod(p, v)),
        pole(skupina if viac else "", False),
        pole(p["n"]["sk"]),
        pole("", False),
        pole(cena),
        pole(""), pole(""), pole(""),
        pole("", False), pole("", False),
        pole(v["sk"] if viac else "", False),
        pole(SKLAD),
        pole("visible", False),
    ])


def main():
    s = open(os.path.join(KOREN, "data", "products-purelux.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PURELUX_PRODUCTS=(\[.*\]);", s, re.S).group(1))

    # productVisibility explicitne, nie spoliehanie sa na to, že ho
    # neskorší XML krok (s kategóriou) dorovná sám — pri paneloch sme
    # zistili, že nové produkty bez tohto poľa Shoptet založí ako
    # skryté a spoliehanie sa na "kategória to opraví" stálo pár dní
    # ladenia. Lacná poistka navyše.
    hlavicka = ("code;pairCode;name;guid;price;standardPrice;purchasePrice;"
                f'actionPrice;actionFrom;actionUntil;"variant:{PARAMETER}";stock;'
                "productVisibility;")
    riadky = [hlavicka]
    skupina = 0
    produktov = prevedeni = 0
    for p in P:
        viac = len(p["var"]) > 1
        if viac:
            skupina += 1
        for v in p["var"]:
            riadky.append(riadok(p, v, skupina, viac))
            prevedeni += 1
        produktov += 1

    with open(CIEL, "w", encoding="utf-8-sig", newline="") as f:
        f.write("\r\n".join(riadky) + "\r\n")
    print(f"{produktov} produktov, {prevedeni} prevedení -> {CIEL}")

    davky, teraz, kusov = [], [], 0
    for p in P:
        if kusov and kusov % DAVKA == 0:
            davky.append(teraz); teraz = []
        teraz.append(p); kusov += 1
    if teraz:
        davky.append(teraz)

    print(f"\npo dávkach (najviac {DAVKA} produktov na súbor):")
    skupina = 0
    for i, cast in enumerate(davky, 1):
        rr = [hlavicka]
        for p in cast:
            viac = len(p["var"]) > 1
            if viac:
                skupina += 1
            for v in p["var"]:
                rr.append(riadok(p, v, skupina, viac))
        c = vystup.kam(vystup.IMPORT, "purelux-produkty-csv",
                       f"davka-{i}-z-{len(davky)}.csv")
        with open(c, "w", encoding="utf-8-sig", newline="") as f:
            f.write("\r\n".join(rr) + "\r\n")
        print(f"  {os.path.basename(c):<34} {len(cast):>3} produktov · "
              f"{len(rr)-1:>3} riadkov")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Vypíše katalóg Adventure Design do CSV vo formáte, aký Shoptet exportuje.

Rovnaký vzor ako export_shoptet.py/export_purelux.py, dva rozdiely:
žiadne varianty (každá položka vo feede je samostatný produkt, nie
kombinácia) a stĺpec "currency" = CZK — cena ostáva v korunách, klient
chce overiť, či si ju "Cudzie meny" sám prepočíta na zobrazenie v EUR.
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

CIEL = vystup.kam(vystup.IMPORT, "adventure-design-csv", "produkty.csv")
SKLAD = "0"


def kod(p):
    znacka = hashlib.sha1(p["id"].encode("utf-8")).hexdigest()[:4].upper()
    return f'{p["sku"]}-{znacka}'


def pole(v, uvodzovky=True):
    if v == "" or v is None:
        return '""' if uvodzovky else ""
    return '"' + str(v).replace('"', '""') + '"'


def riadok(p):
    cena = f'{p["czk"]:.2f}'.replace(".", ",")
    return ";".join([
        pole(kod(p)), pole(p["n"]["sk"]), pole("", False),
        pole(cena), pole("CZK", False), pole(SKLAD), pole("visible", False),
    ])


def main():
    s = open(os.path.join(KOREN, "data", "products-adventure-design.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.AD_PRODUCTS=(\[.*\]);", s, re.S).group(1))

    hlavicka = "code;name;guid;price;currency;stock;productVisibility;"
    riadky = [hlavicka] + [riadok(p) for p in P]

    with open(CIEL, "w", encoding="utf-8-sig", newline="") as f:
        f.write("\r\n".join(riadky) + "\r\n")
    print(f"{len(P)} produktov -> {CIEL}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Doplní český text do exportu z Produkty → Export → "Jazyky".

Toto je správna cesta na jazykovú mutáciu v Shoptete — nie opakovaný
beh tools/export_purelux_xml.py s iným jazykom (ten zdvojil kategórie,
viď varovanie v tom súbore). Súbor z exportu má jeden riadok na
prevedenie, stĺpce name/shortDescription/description/metaDescription/
seoTitle v pároch ":sk"/":cs". Stĺpce ":sk" už sú správne (to je to, čo
je v obchode živé) — needitujú sa. Dopĺňajú sa len ":cs", a to iba na
riadkoch Purelux (podľa kódu — Lensun aj sady/komponenty majú iný tvar
kódu, tie riadky prejdú bez zmeny).

Obsah ":cs" sa skladá tými istými funkciami, čo XML krok
(kratky_popis/popis/seo_popis z export_purelux_xml.py), len s
JAZYK="cs" — rovnaká štruktúra HTML, len iný text, nech sa to nelíši
od toho, ako by to vyzeralo, keby jazyková mutácia fungovala cez XML.

Spustenie:
    python3 tools/purelux_preloz_jazyky.py ~/Downloads/products.xlsx
Výstup: ~/Downloads/products-doplnene-cs.xlsx — ten sa nahrá cez
Produkty → Import (tá istá obrazovka, záložka Import).
"""
import json
import os
import re
import sys

from openpyxl import load_workbook

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import export_purelux_xml as xml
from export_purelux import kod

HARO = "Export tovaru"
STLPCE_CS = ["name:cs", "shortDescription:cs", "description:cs",
             "metaDescription:cs", "seoTitle:cs"]


def obsah_produktu(p):
    """Český text pre jeden produkt — rovnaké funkcie ako XML export,
    len prepnuté na "cs"."""
    xml.JAZYK = "cs"
    return {
        "name:cs": p["n"]["cs"],
        "shortDescription:cs": xml.kratky_popis(p),
        "description:cs": xml.popis(p),
        "metaDescription:cs": xml.seo_popis(p["d"]["cs"]),
        "seoTitle:cs": p["n"]["cs"] + " | RnC Explore",
    }


def main():
    if len(sys.argv) < 2:
        sys.exit("použitie: python3 tools/purelux_preloz_jazyky.py <export z Produkty → Export → Jazyky>")
    vstup = os.path.expanduser(sys.argv[1])
    if not os.path.exists(vstup):
        sys.exit(f"súbor neexistuje: {vstup}")

    s = open(os.path.join(KOREN, "data", "products-purelux.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PURELUX_PRODUCTS=(\[.*\]);", s, re.S).group(1))

    # kód prevedenia -> obsah produktu, ktorému patrí (viac kódov na
    # jeden produkt pri viacvariantových)
    podla_kodu = {}
    for p in P:
        obsah = obsah_produktu(p)
        for v in p["var"]:
            podla_kodu[kod(p, v)] = obsah

    wb = load_workbook(vstup)
    if HARO not in wb.sheetnames:
        sys.exit(f"v súbore nie je hárok „{HARO}“; je tam: " + ", ".join(wb.sheetnames))
    ws = wb[HARO]

    hlavicka = {ws.cell(row=1, column=c).value: c for c in range(1, ws.max_column + 1)}
    chyba = [n for n in ["code"] + STLPCE_CS if n not in hlavicka]
    if chyba:
        sys.exit("v súbore chýbajú stĺpce: " + ", ".join(chyba))

    doplnene = nenajdene = 0
    for r in range(2, ws.max_row + 1):
        kod_riadku = ws.cell(row=r, column=hlavicka["code"]).value
        obsah = podla_kodu.get(kod_riadku)
        if obsah is None:
            continue  # nie je to Purelux riadok (Lensun/sady/komponenty) — nedotýkame sa
        for stlpec in STLPCE_CS:
            ws.cell(row=r, column=hlavicka[stlpec], value=obsah[stlpec])
        doplnene += 1

    vystup_cesta = os.path.join(os.path.dirname(vstup), "products-doplnene-cs.xlsx")
    wb.save(vystup_cesta)

    print(f"doplnených riadkov (Purelux): {doplnene}")
    print(f"zápisov v products-purelux.js: {len(podla_kodu)} kódov")
    if doplnene != len(podla_kodu):
        print(f"POZOR: počet sa nezhoduje — buď v exporte chýbajú niektoré Purelux "
              f"prevedenia, alebo je tam niečo navyše. Skontroluj pred nahratím.")
    print(f"-> {vystup_cesta}")
    print("nahraj cez Produkty → Import (tá istá obrazovka, záložka Import)")


if __name__ == "__main__":
    main()

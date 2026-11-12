# -*- coding: utf-8 -*-
"""Vyplní šablónu skladových kariet pre KROS Sklad.

Šablónu nevyrábame — berieme tú, ktorú KROS sám vyexportuje
(Zoznam_kariet.xlsx), a dopisujeme do nej. Názvy stĺpcov sa tak
nehádajú a formát zostane ich.

Karta je jedno prevedenie, nie produkt: sklad eviduje kusy, nie
karty v e-shope. Preto 533 riadkov a nie 157.

Kód musí ísť v tej podobe, v akej je v e-shope — s tou štvorznakovou
značkou, ktorú sme pridali kvôli tomu, že Lensun používa ten istý kód
na rôzne autá. Podľa neho sa sklad páruje s obchodom; bez nej by
KROS založil produkty znova.

Čo zámerne nevypĺňame:
  Zostatok            nevieme, dopĺňa sa pri naskladnení
  EAN kód             nemáme
  Nákupná cena        nevieme, to je práve to, na čo čakáme
  Popis               sklad ho nepotrebuje a je to HTML

„Posielať do eshopu“ dávame na Nie. Pri prvom importe chceme len
dostať karty do skladu a overiť, či sa kódy spárovali. Áno sa zapne
až potom — inak by KROS prepísal názvy produktov v e-shope týmito,
ktoré sú zložené z názvu a prevedenia.

Spustenie:
    python3 tools/karty_do_krosu.py ~/Downloads/Zoznam_kariet.xlsx
"""
import json
import os
import re
import shutil
import sys

from openpyxl import load_workbook

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo                                              # noqa: E402
from export_shoptet import kod                          # noqa: E402

DPH = 23
HARO = "Karty"

# Stĺpec v šablóne -> čo doň ide. Hľadáme podľa názvu, nie podľa
# poradia — keby KROS stĺpce prehodil, nájdu sa samy.
STLPCE = {
    "Kód karty": lambda p, v: v_obchode(kod(p, v)),
    "Názov": lambda p, v: f'{p["n"]["sk"]} – {v["sk"]}',
    "MJ": lambda p, v: "ks",
    "Hmotnosť [kg]": lambda p, v: round(float(p.get("kg") or 0), 2) or None,
    "DPH [%]": lambda p, v: DPH,
    "Posielať do eshopu": lambda p, v: "Nie",
    "Predajná cena ZC": lambda p, v: round(seo.price(v["p"], "EUR"), 2),
}


def v_obchode(k):
    """Kód tak, ako ho má Shoptet — veľké písmená, + a * ako pomlčka."""
    return re.sub(r"[+*]", "-", k.strip().upper())


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))


def main():
    if len(sys.argv) < 2:
        sys.exit("použitie: python3 tools/karty_do_krosu.py <šablóna z KROSu>")
    vzor = os.path.expanduser(sys.argv[1])
    if not os.path.exists(vzor):
        sys.exit(f"šablóna neexistuje: {vzor}")
    ciel = os.path.expanduser("~/Documents/rncexplore-karty-do-krosu.xlsx")
    shutil.copy(vzor, ciel)

    wb = load_workbook(ciel)
    if HARO not in wb.sheetnames:
        sys.exit(f"v šablóne nie je hárok „{HARO}“; je tam: "
                 + ", ".join(wb.sheetnames))
    ws = wb[HARO]

    hlavicka = {ws.cell(row=1, column=c).value: c
                for c in range(1, ws.max_column + 1)}
    chyba = [n for n in STLPCE if n not in hlavicka]
    if chyba:
        sys.exit("v šablóne chýbajú stĺpce: " + ", ".join(chyba)
                 + "\nje tam: " + ", ".join(str(x) for x in hlavicka))

    P = katalog()
    r = 2
    dlhe = 0
    for p in sorted(P, key=lambda x: x["n"]["sk"]):
        for v in p["var"]:
            if not v.get("sku"):
                continue
            for nazov, fn in STLPCE.items():
                ws.cell(row=r, column=hlavicka[nazov], value=fn(p, v))
            if len(ws.cell(row=r, column=hlavicka["Názov"]).value) > 80:
                dlhe += 1
            r += 1
    wb.save(ciel)

    print(f"{r - 2} kariet -> {ciel}")
    print("  nevyplnené zámerne: Zostatok, EAN kód, Nákupná cena, Popis")
    print(f"  „Posielať do eshopu“ = Nie pri všetkých")
    if dlhe:
        print(f"  POZOR: {dlhe} názvov je dlhších než 80 znakov — ak ich "
              "KROS odmietne, treba ich skrátiť")


if __name__ == "__main__":
    main()

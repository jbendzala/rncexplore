# -*- coding: utf-8 -*-
"""Vyplní šablónu skladových kariet pre KROS Sklad — Adventure Design.

Rovnaký vzor ako tools/karty_do_krosu.py, len bez variant — každá
položka feedu je samostatný produkt, teda aj samostatná karta (45).

Cena: p["czk"] je dohodnutá ako "bez DPH" (klientovo rozhodnutie —
Shoptet si DPH dopočíta sám). "Predajná cena ZC" pri ostatných
katalógoch nesie finálnu maloobchodnú cenu s DPH v EUR, tak isto aj tu
— NIE cez tools/seo.py's price() (ten počíta Lensunovu prirážku z EUR
základu, na CZK vstup by sa netrafil), ale priamo kurzom a sadzbou DPH
z config.js: (czk / rates.CZK) * (1 + vat).

Hmotnosť nemáme (feed výrobcu ju neuvádza vôbec), stĺpec zostáva
prázdny — rovnaký stav ako pri produktoch, kde ju ešte nevieme.

Spustenie:
    python3 tools/adventure_design_karty_do_krosu.py ~/Downloads/Zoznam_kariet.xlsx
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
from export_adventure_design import kod                 # noqa: E402

DPH = 23
HARO = "Karty"


def cena_eur_s_dph(czk):
    return czk / seo.CFG["rates"]["CZK"] * (1 + seo.CFG["vat"])


STLPCE = {
    "Kód karty": lambda p: v_obchode(kod(p)),
    "Názov": lambda p: p["n"]["sk"],
    "MJ": lambda p: "ks",
    "Hmotnosť [kg]": lambda p: None,
    "DPH [%]": lambda p: DPH,
    "Posielať do eshopu": lambda p: "Nie",
    "Predajná cena ZC": lambda p: round(cena_eur_s_dph(p["czk"]), 2),
}


def v_obchode(k):
    return re.sub(r"[+*]", "-", k.strip().upper())


def katalog():
    s = open(os.path.join(KOREN, "data", "products-adventure-design.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.AD_PRODUCTS=(\[.*\]);", s, re.S).group(1))


def main():
    if len(sys.argv) < 2:
        sys.exit("použitie: python3 tools/adventure_design_karty_do_krosu.py <šablóna z KROSu>")
    vzor = os.path.expanduser(sys.argv[1])
    if not os.path.exists(vzor):
        sys.exit(f"šablóna neexistuje: {vzor}")
    ciel = os.path.expanduser("~/Documents/rncexplore-adventure-design-karty-do-krosu.xlsx")
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
        for nazov, fn in STLPCE.items():
            ws.cell(row=r, column=hlavicka[nazov], value=fn(p))
        if len(ws.cell(row=r, column=hlavicka["Názov"]).value) > 80:
            dlhe += 1
        r += 1
    wb.save(ciel)

    print(f"{r - 2} kariet -> {ciel}")
    print("  nevyplnené zámerne: Zostatok, EAN kód, Nákupná cena, Popis, Hmotnosť (feed ju nemá)")
    print("  „Posielať do eshopu“ = Nie pri všetkých")
    if dlhe:
        print(f"  POZOR: {dlhe} názvov je dlhších než 80 znakov — ak ich "
              "KROS odmietne, treba ich skrátiť")


if __name__ == "__main__":
    main()

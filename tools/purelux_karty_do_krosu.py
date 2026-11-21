# -*- coding: utf-8 -*-
"""Vyplní šablónu skladových kariet pre KROS Sklad — Purelux.

Rovnaký vzor ako tools/karty_do_krosu.py (Lensun), dva rozdiely:

- Cena ide priamo z v["p"] (už hotové € s DPH z valostore), nie cez
  tools/seo.py's price() — tá je kalibrovaná na Lensunov prepočet z USD
  a Purelux by prepočítala druhýkrát.
- Hmotnosť berieme z KAŽDEJ variante (v["kg"]), nie z produktu — Purelux
  sa predáva v baleniach od 1 do 8 kusov s rozdielom v desiatkach kíl,
  spoločná hmotnosť na produkte by bola pri väčších baleniach zavádzajúca
  (rovnaký dôvod ako v tools/export_purelux_xml.py).

Karty aj tu idú ako "Posielať do eshopu" = Nie, pri prvom importe len na
overenie, že sa kódy spárovali.

Spustenie:
    python3 tools/purelux_karty_do_krosu.py ~/Downloads/Zoznam_kariet.xlsx
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
from export_purelux import kod                          # noqa: E402

DPH = 23
HARO = "Karty"

STLPCE = {
    "Kód karty": lambda p, v: v_obchode(kod(p, v)),
    "Názov": lambda p, v: f'{p["n"]["sk"]} – {v["sk"]}',
    "MJ": lambda p, v: "ks",
    "Hmotnosť [kg]": lambda p, v: round(float(v.get("kg") or 0), 2) or None,
    "DPH [%]": lambda p, v: DPH,
    "Posielať do eshopu": lambda p, v: "Nie",
    "Predajná cena ZC": lambda p, v: round(float(v["p"]), 2),
}


def v_obchode(k):
    return re.sub(r"[+*]", "-", k.strip().upper())


def katalog():
    s = open(os.path.join(KOREN, "data", "products-purelux.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PURELUX_PRODUCTS=(\[.*\]);", s, re.S).group(1))


def main():
    if len(sys.argv) < 2:
        sys.exit("použitie: python3 tools/purelux_karty_do_krosu.py <šablóna z KROSu>")
    vzor = os.path.expanduser(sys.argv[1])
    if not os.path.exists(vzor):
        sys.exit(f"šablóna neexistuje: {vzor}")
    ciel = os.path.expanduser("~/Documents/rncexplore-purelux-karty-do-krosu.xlsx")
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
    print("  „Posielať do eshopu“ = Nie pri všetkých")
    if dlhe:
        print(f"  POZOR: {dlhe} názvov je dlhších než 80 znakov — ak ich "
              "KROS odmietne, treba ich skrátiť")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Zošit na kontrolu úplnosti katalógu — jeden riadok na produkt.

Shoptetov vlastný export sa na toto nehodí: dáva riadok na každé
prevedenie (533 namiesto 157), popisy v ňom sú HTML a stĺpcov má
niekoľko desiatok. Hľadať v tom, čo chýba, je horšie než to nehľadať.

Tento zošit má jeden riadok na produkt, stĺpce len tie, ktoré sa dajú
skontrolovať okom, a posledný stĺpec povie, čo pri produkte chýba.
Prázdne bunky sú zvýraznené, nech ich vidno pri rolovaní.

Ceny sa berú z toho istého vzorca ako web, takže v zošite nemôže byť
iné číslo než v obchode.

Spustenie:
    python3 tools/prehlad_produktov.py                # do ~/Documents
    python3 tools/prehlad_produktov.py /cesta/sub.xlsx
"""
import json
import os
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo                                              # noqa: E402
from export_shoptet import kod                          # noqa: E402

# Stĺpce zošita: nadpis, šírka, ako sa hodnota získa.
# Tretia položka vracia hodnotu, štvrtá hovorí, či je pole povinné —
# nepovinné sa do „čo chýba“ nerátajú.
KATEGORIE = {
    "hood": "Panely na kapotu", "flexible": "Flexibilné panely",
    "rooftent": "Pre strešné stany", "foldable": "Skladacie panely",
    "blanket": "Solárne deky", "rv": "Karavany a prívesy",
    "tonneau": "Na kryty korby",
}

CHYBA = PatternFill("solid", fgColor="FFF2CC")      # jemná žltá
NADPIS = PatternFill("solid", fgColor="1B2420")


def cena_od(p):
    return round(min(seo.price(v["p"], "EUR") for v in p["var"]), 2)


def kody(p):
    return ", ".join(kod(p, v) for v in p["var"] if v.get("sku"))


STLPCE = [
    ("Kód prvého prevedenia", 26, lambda p: kody(p).split(", ")[0], True),
    ("Názov (SK)", 52, lambda p: p["n"]["sk"], True),
    ("Názov (CZ)", 52, lambda p: p["n"]["cs"], True),
    ("Kategória", 20, lambda p: KATEGORIE.get(p["cat"], p["cat"]), True),
    ("Značka vozidla", 16, lambda p: p.get("b") or "", False),
    ("Výkon (W)", 10, lambda p: p.get("w") or "", True),
    ("Rozmer", 22, lambda p: (p.get("spec") or {}).get("dim") or "", True),
    ("Hmotnosť balíka (kg)", 18, lambda p: p.get("kg") or "", True),
    ("Čistá hmotnosť (kg)", 18, lambda p: (p.get("spec") or {}).get("kg") or "", False),
    ("Pripojovacia skrinka", 20, lambda p: (p.get("spec") or {}).get("jbox") or "", False),
    ("Účinnosť", 12, lambda p: (p.get("spec") or {}).get("eff") or "", False),
    ("Prevedení", 10, lambda p: len(p["var"]), True),
    ("Cena od (€ s DPH)", 16, cena_od, True),
    ("Fotografií", 10, lambda p: len(p.get("img") or []), True),
    ("Obsah balenia", 14, lambda p: len(p.get("pack") or []) or "", False),
    ("Video", 10, lambda p: p.get("video") or "", False),
    ("Popis (SK) znakov", 16, lambda p: len(p["d"].get("sk") or ""), True),
    ("Popis (CZ) znakov", 16, lambda p: len(p["d"].get("cs") or ""), True),
]


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))


def main():
    ciel = (sys.argv[1] if len(sys.argv) > 1
            else os.path.expanduser("~/Documents/rncexplore-prehlad-produktov.xlsx"))
    P = katalog()

    wb = Workbook()
    ws = wb.active
    ws.title = "Produkty"

    hlavicka = [n for n, _, _, _ in STLPCE] + ["Čo chýba"]
    ws.append(hlavicka)
    for i, n in enumerate(hlavicka, 1):
        b = ws.cell(row=1, column=i)
        b.font = Font(bold=True, color="FFFFFF")
        b.fill = NADPIS
        b.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 30

    suhrn = {n: 0 for n, _, _, povinne in STLPCE if povinne}
    for p in sorted(P, key=lambda x: (x["cat"], x["n"]["sk"])):
        riadok, chyba = [], []
        for nazov, _, fn, povinne in STLPCE:
            v = fn(p)
            riadok.append(v)
            if povinne and (v == "" or v is None):
                chyba.append(nazov)
                suhrn[nazov] += 1
        riadok.append(", ".join(chyba))
        ws.append(riadok)
        r = ws.max_row
        for i, (nazov, _, _, povinne) in enumerate(STLPCE, 1):
            if povinne and nazov in chyba:
                ws.cell(row=r, column=i).fill = CHYBA
        if chyba:
            ws.cell(row=r, column=len(hlavicka)).fill = CHYBA

    for i, (_, sirka, _, _) in enumerate(STLPCE, 1):
        ws.column_dimensions[get_column_letter(i)].width = sirka
    ws.column_dimensions[get_column_letter(len(hlavicka))].width = 34
    ws.freeze_panes = "C2"

    # Druhý hárok: čo a koľkokrát chýba, nech sa to nemusí rátať ručne.
    s2 = wb.create_sheet("Čo chýba")
    s2.append(["Údaj", "Chýba pri koľkých produktoch", "Z celkového počtu"])
    for i in range(1, 4):
        b = s2.cell(row=1, column=i)
        b.font = Font(bold=True, color="FFFFFF")
        b.fill = NADPIS
    for nazov, kolko in sorted(suhrn.items(), key=lambda x: -x[1]):
        s2.append([nazov, kolko, len(P)])
        if kolko:
            s2.cell(row=s2.max_row, column=2).fill = CHYBA
    for i, w in enumerate((30, 28, 18), 1):
        s2.column_dimensions[get_column_letter(i)].width = w

    wb.save(ciel)
    print(f"{len(P)} produktov -> {ciel}")
    print("\nchýbajúce povinné údaje:")
    for nazov, kolko in sorted(suhrn.items(), key=lambda x: -x[1]):
        if kolko:
            print(f"  {nazov:<24} {kolko:>3} z {len(P)}")
    if not any(suhrn.values()):
        print("  žiadne")


if __name__ == "__main__":
    main()

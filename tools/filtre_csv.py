#!/usr/bin/env python3
"""CSV s hodnotami filtrov pre Shoptet.

Obsahový XML vie poslať len informačné parametre a tie sa zobrazujú
v tabuľke. Hodnoty, podľa ktorých sa dá filtrovať, berie Shoptet zo
stĺpca „filteringProperty:<názov>“ v importe produktov — v schéme XML
preň element nie je. Preto tento druhý, malý súbor: nič neprepisuje,
len dopĺňa dva filtre.

Výkon ide v pásmach, nie v číslach. Rôznych wattáží je v katalógu 38
a Shoptet filtruje podľa presných hodnôt, takže v jednej kategórii
z toho bol zoznam 25 políčok v náhodnom poradí.

Názvy stĺpcov musia sedieť na písmeno s tým, čo je v administrácii
v Parametroch pre filtrovanie. Keby sa líšili, Shoptet založí ďalší
parameter a v paneli budú oba.

Spustenie:  python3 tools/filtre_csv.py
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vystup                                           # noqa: E402
from export_shoptet_xml import shoptet_kod              # noqa: E402

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VYKON = "Výkon"
MONTAZ = "Montáž"

# Pásma z návrhu. Hranice sú vrchné a vrátane, aby 50 W padlo do
# prvého pásma a 100 W do druhého — tak to číta zákazník.
PASMA = [(50, "do 50 W"), (100, "50 – 100 W"), (200, "100 – 200 W"),
         (10 ** 9, "nad 200 W")]

# Montáž má jednu hodnotu na produkt, nie dve.
#
# Návrh má v tej skupine dve políčka, „Montáž bez vŕtania“ a „Na mieru
# podľa vozidla“, a produkt by pokojne mohol mať obe. Lenže
# dokumentácia Shoptetu nikde nepíše, ako sa viac hodnôt jedného
# filtra zapisuje do bunky — či bodkočiarkou, zvislou čiarou, alebo
# vôbec. Tipovať to by znamenalo založiť v obchode hodnotu
# „Bez vŕtania|Na mieru podľa vozidla“ a potom ju ručne čistiť.
#
# Delenie je preto na to, čo zákazník naozaj rieši: či je panel
# tvarovaný na jeho auto, alebo univerzálny. Lepí sa aj tak oboje.
# Prenosné panely a deky montáž nemajú, tie zostávajú bez hodnoty
# a pri filtrovaní podľa montáže medzi výsledky nepatria.
PRILEPENE = {"hood", "flexible", "rooftent", "tonneau", "rv"}


def pasmo(w):
    for strop, nazov in PASMA:
        if w <= strop:
            return nazov


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))


def main():
    P = katalog()
    riadky = [f'code;"filteringProperty:{VYKON}";"filteringProperty:{MONTAZ}"']
    pocty = {"vykon": 0, "montaz": 0, "prevedeni": 0}

    for p in P:
        v = pasmo(p["w"]) if p.get("w") else ""
        if p.get("b"):
            m = "Na mieru podľa vozidla"
        elif p["cat"] in PRILEPENE:
            m = "Univerzálny panel"
        else:
            m = ""
        if v:
            pocty["vykon"] += 1
        if m:
            pocty["montaz"] += 1
        # Riadok na každé prevedenie: import páruje podľa kódu a kód má
        # prevedenie, nie produkt. Hodnota je pri všetkých rovnaká —
        # filtre sú vlastnosťou produktu, nie prevedenia.
        for var in p["var"]:
            pocty["prevedeni"] += 1
            riadky.append(f'{shoptet_kod(p, var)};"{v}";"{m}"')

    cesta = vystup.kam(vystup.IMPORT, "obsah-xml", "filtre.csv")
    with open(cesta, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write("\n".join(riadky) + "\n")

    print(f"{len(riadky) - 1} riadkov -> {cesta}")
    print(f"   produktov s výkonom: {pocty['vykon']} · s montážou: {pocty['montaz']}"
          f" · prevedení: {pocty['prevedeni']}")
    import collections
    pv = collections.Counter(pasmo(p["w"]) for p in P if p.get("w"))
    print("   pásma:", " · ".join(f"{k} ({v})" for _, k in PASMA for kk, v in pv.items() if kk == k))
    pm = collections.Counter(
        "Na mieru podľa vozidla" if p.get("b")
        else "Univerzálny panel" if p["cat"] in PRILEPENE else "(bez hodnoty)"
        for p in P)
    print("   montáž:", " · ".join(f"{k} ({v})" for k, v in pm.most_common()))


if __name__ == "__main__":
    main()

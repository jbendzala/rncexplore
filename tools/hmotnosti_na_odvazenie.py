#!/usr/bin/env python3
"""Zoznam produktov, ktoré treba odvážiť.

Hmotnosti sme z cenníkov Lensunu vytiahli presne pri 66 produktoch,
zvyšok je odhad z mediánu rovnako výkonných panelov. Krížová skúška na
tých, kde skutočnosť poznáme, ukázala medián chyby 0,41 kg (13 %) —
pri paneloch na kapotu to do ceny dopravy nezasiahne.

Vážiť teda netreba všetko. Tento zoznam vyberá tie, kde sa to oplatí:

  * odhad padne blízko hranice pásma DPD — pár desatín kila tam mení
    cenu dopravy o celé euro aj viac,
  * odhad presahuje 31,5 kg, čo je strop balíka DPD; taký kus sa
    kuriérom neodošle vôbec a treba o tom vedieť skôr než si ho
    niekto objedná,
  * ide o zostavu z viacerých panelov, ktorá sa balí inak a odhad pre
    ňu nemá zmysel.

Spustenie:  python3 tools/hmotnosti_na_odvazenie.py
"""

import json
import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup                                           # noqa: E402
from hmotnosti_z_pdf import z_pdf, norm, viac_panelov    # noqa: E402

# Pásma z cenovej ponuky DPD pre Safiri (2026-10-07), vnútroštátna
# preprava. Nad 31,5 kg DPD balík neberie.
PASMA = [(1, "2,80"), (3, "3,00"), (6, "3,10"), (10, "3,35"),
         (20, "5,50"), (31.5, "7,95")]
STROP = 31.5

# Koľko kíl od hranice pásma ešte považujeme za „tesne“. Pri chybe
# odhadu s mediánom 0,41 kg je pol kila rozumná hranica.
TESNO = 0.8

NAZVY = {"hood": "Panel na kapotu", "flexible": "Flexibilný panel",
         "foldable": "Skladací panel", "rooftent": "Na strešný stan",
         "blanket": "Solárna deka", "rv": "Karavan a príves",
         "tonneau": "Na kryt korby"}


def pasmo(kg):
    for strop, cena in PASMA:
        if kg <= strop:
            return strop, cena
    return None, None


def main():
    riadky = z_pdf()
    presne = {norm(k): kg for k, _, kg in riadky}

    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))

    vyber = []
    for p in P:
        kod = norm(p.get("sku", ""))
        kg = p.get("kg") or 0
        if kod in presne:
            continue                      # hmotnosť máme z cenníka
        if viac_panelov(p):
            duvod = "zostava z viacerých panelov"
        elif kg > STROP:
            duvod = f"nad {STROP} kg — DPD balík neberie"
        else:
            strop, _ = pasmo(kg)
            if strop is None or strop - kg > TESNO:
                continue                  # odhad je od hranice ďaleko
            duvod = f"tesne pod hranicou {strop} kg"
        strop, cena = pasmo(kg)
        vyber.append((p, kg, duvod,
                      f"do {strop} kg" if strop else "mimo pásiem",
                      cena or "—"))

    vyber.sort(key=lambda x: -x[1])

    cesta = vystup.kam(vystup.NASE, "hmotnosti-na-odvazenie.csv")
    with open(cesta, "w", encoding="utf-8-sig", newline="") as f:
        f.write("Kód;Kategória;Výkon (W);Odhad (kg);Pásmo DPD;"
                "Cena dopravy bez DPH;Prečo;SKUTOČNÁ HMOTNOSŤ (kg)\n")
        for p, kg, duvod, pas, cena in vyber:
            f.write(f'{p.get("sku","")};{NAZVY.get(p["cat"], p["cat"])};'
                    f'{p["w"] or ""};{str(kg).replace(".", ",")};{pas};'
                    f'{cena};{duvod};\n')

    print(f"{len(vyber)} produktov na odváženie -> {cesta}\n")
    for p, kg, duvod, pas, cena in vyber:
        print(f"   {kg:>6.2f} kg  {pas:<14} {duvod:<32} {p['n']['sk'][:40]}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Odreže prázdny okraj z loga.

Logo má plátno 2400 × 800, ale kresba v ňom sedí od x = 80 po x = 1626.
Vľavo tak zostáva 80 jednotiek prázdna a vpravo 774, teda **tretina
šírky**. V hlavičke sa logo roztiahne na výšku, takže ten prázdny pás
vľavo posunul kresbu o pár pixelov doprava od všetkého ostatného na
stránke — pri výške 62 px to bolo 6 px — a prázdny pás vpravo robil
medzeru medzi logom a menu, ktorá tam nemala čo robiť.

Dá sa to zaplátať aj v CSS záporným okrajom, ale ten by platil len pre
jednu veľkosť. Toto je oprava v súbore: pomer ostáva, kresba sa
nemení, len plátno ide tesne okolo nej.

Výška sa zámerne nemení. Keby sme orezali aj zhora a zdola, logo by
pri tej istej výške hlavičky zrazu narástlo a zmenil by sa vzhľad.

Spustenie:  python3 tools/oreze_logo.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vystup                                           # noqa: E402

# Namerané vykreslením loga do rastra a hľadaním prvého a posledného
# neprázdneho stĺpca; prepočítané do jednotiek viewBoxu.
VLAVO = 80
VPRAVO = 1626


def main():
    priecinok = vystup.kam(vystup.IMPORT, "vzhlad", "logo")
    sirka = VPRAVO - VLAVO
    hotovo = []

    for meno in ("logo-na-tmave.svg", "logo-na-svetle.svg"):
        cesta = os.path.join(priecinok, meno)
        if not os.path.exists(cesta):
            sys.exit(f"chýba {cesta}")
        s = open(cesta, encoding="utf-8").read()

        novy, n = re.subn(
            r'(<svg[^>]*?)width="2400"(\s+)height="800"(\s+)viewBox="0 0 2400 800"',
            rf'\1width="{sirka}"\2height="800"\3viewBox="{VLAVO} 0 {sirka} 800"',
            s, count=1)
        if n != 1:
            sys.exit(f"{meno}: hlavičku svg sa nepodarilo nájsť — "
                     "súbor asi nie je ten, pre ktorý bol skript písaný")

        ciel = os.path.join(priecinok, meno.replace(".svg", "-orezane.svg"))
        with open(ciel, "w", encoding="utf-8") as f:
            f.write(novy)
        hotovo.append((os.path.basename(ciel), os.path.getsize(ciel)))

    print(f"plátno 2400 × 800  ->  {sirka} × 800   (odrezané "
          f"{VLAVO} px vľavo a {2400 - VPRAVO} px vpravo)")
    for meno, b in hotovo:
        print(f"   {meno:<34} {b // 1024} kB")
    print(f"\n{priecinok}")
    print("nahrať v Nastavenia → Vzhľad → Logo (tmavé aj svetlé)")


if __name__ == "__main__":
    main()

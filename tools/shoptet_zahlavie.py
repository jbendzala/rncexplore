# -*- coding: utf-8 -*-
"""Pripraví vzhľad na nasadenie do Shoptetu.

Samostatné pole „Vlastné CSS“ Shoptet nemá — to som si vymyslel a stálo
to zbytočné hľadanie. Kód sa vkladá do HTML editora:

    Vzhľad a obsah → Editor → záložka „HTML kód“ → sekcia „Záhlavie“

Lenže záhlavie berie najviac 8192 znakov a náš vzhľad má dvakrát tolko.
Preto sa CSS nahrá ako samostatný súbor a do záhlavia ide len odkaz naň.
Vznikajú teda dva súbory:

    rnc-vzhlad.css      nahrať do Vzhľad a obsah → Správca súborov
    do-zahlavia.html    vložiť do záhlavia (zmestí sa, je krátke)

Na odkaz používame relatívnu adresu /user/documents/…, nie celú s
doménou — po prepnutí na www.rncexplore.com bude fungovať bez úpravy.

Za adresou je ?v= s odtlačkom obsahu. Keď sa CSS zmení, zmení sa aj
adresa a prehliadače si stiahnu nové. Bez toho by návštevník videl starý
vzhľad, kým mu nevyprší cache.

Jeden zdroj, žiadne prepisovanie: oboje sa vyrába zo
shoptet/vlastne-css.css.

Spustenie:  python3 tools/shoptet_zahlavie.py
"""
import hashlib
import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup

ZDROJ = os.path.join(KOREN, "shoptet", "vlastne-css.css")
SUBOR = "rnc-vzhlad.css"            # ako sa bude volať v Správcovi súborov
STROP = 8192                        # koľko znakov znesie záhlavie


def main():
    css = open(ZDROJ, encoding="utf-8").read()

    # Písma načíta záhlavie samo cez <link> — ten prehliadač začne sťahovať
    # hneď, kým @import až keď dočíta štýl.
    pisma = re.search(r'@import url\("([^"]+)"\);\s*', css)
    if pisma:
        css = css.replace(pisma.group(0), "")
    css = css.strip() + "\n"

    cesta_css = vystup.kam(vystup.IMPORT, "vzhlad", SUBOR)
    with open(cesta_css, "w", encoding="utf-8") as f:
        f.write(css)

    odtlacok = hashlib.sha1(css.encode("utf-8")).hexdigest()[:8]
    r = ["<!-- rncexplore.com — vzhľad podľa návrhu.",
         "",
         f"     1. {SUBOR} nahraj do Vzhľad a obsah → Správca súborov",
         "     2. toto vlož do Vzhľad a obsah → Editor → HTML kód → Záhlavie",
         "",
         "     Zdroj je shoptet/vlastne-css.css v repozitári. Needituj tu ani",
         "     v nahranom súbore — uprav zdroj a spusti",
         "     tools/shoptet_zahlavie.py. -->"]
    if pisma:
        r.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
        r.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
        r.append(f'<link rel="stylesheet" href="{pisma.group(1)}">')
    r.append(f'<link rel="stylesheet" href="/user/documents/{SUBOR}?v={odtlacok}">')
    zahlavie = "\n".join(r) + "\n"

    cesta_z = vystup.kam(vystup.IMPORT, "vzhlad", "do-zahlavia.html")
    with open(cesta_z, "w", encoding="utf-8") as f:
        f.write(zahlavie)

    print(f"1. nahrať do Správcu súborov")
    print(f"   {cesta_css}")
    print(f"   {len(css):>6} znakov · {css.count('{')} pravidiel")
    print(f"2. vložiť do záhlavia")
    print(f"   {cesta_z}")
    zvysok = STROP - len(zahlavie)
    print(f"   {len(zahlavie):>6} znakov · strop {STROP} · "
          f"{'zmestí sa, zostáva ' + str(zvysok) if zvysok >= 0 else 'NEZMESTÍ SA'}")


if __name__ == "__main__":
    main()

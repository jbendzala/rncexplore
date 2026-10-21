# -*- coding: utf-8 -*-
"""Zabalí vzhľad do podoby, ktorú Shoptet prijme.

Samostatné pole „Vlastné CSS“ Shoptet nemá — to som si vymyslel a stálo
to zbytočné hľadanie. CSS sa vkladá do HTML editora:

    Vzhľad a obsah → Editor → záložka „HTML kód“ → sekcia „Záhlavie“

Tam patria meta značky, odkazy na CSS a skripty. Preto sa CSS musí
zabaliť do <style> a písma sa načítajú cez <link>, nie cez @import —
prehliadač <link> začne sťahovať hneď, @import až keď dočíta štýl.

Jeden zdroj, žiadne prepisovanie: súbor sa vyrába zo shoptet/vlastne-css.css.

Spustenie:  python3 tools/shoptet_zahlavie.py
"""
import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup

ZDROJ = os.path.join(KOREN, "shoptet", "vlastne-css.css")


def main():
    css = open(ZDROJ, encoding="utf-8").read()

    # @import vyberieme a spravíme z neho <link>
    pisma = re.search(r'@import url\("([^"]+)"\);\s*', css)
    css = css.replace(pisma.group(0), "") if pisma else css

    r = ["<!-- rncexplore.com — vzhľad podľa návrhu. Vložiť celé do:",
         "     Vzhľad a obsah → Editor → HTML kód → Záhlavie",
         f"     Zdroj: shoptet/vlastne-css.css v repozitári. Needituj tu,",
         "     uprav zdroj a spusti tools/shoptet_zahlavie.py. -->"]
    if pisma:
        r.append(f'<link rel="preconnect" href="https://fonts.googleapis.com">')
        r.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
        r.append(f'<link rel="stylesheet" href="{pisma.group(1)}">')
    r.append("<style>")
    r.append(css.strip())
    r.append("</style>")

    ciel = vystup.kam(vystup.IMPORT, "vzhlad", "do-zahlavia.html")
    with open(ciel, "w", encoding="utf-8") as f:
        f.write("\n".join(r) + "\n")

    print(f"{len(''.join(r))//1024} kB -> {ciel}")
    print(f"  písma ako <link>: {'áno' if pisma else 'nie'}")
    print(f"  CSS pravidiel:    {css.count('{')}")


if __name__ == "__main__":
    main()

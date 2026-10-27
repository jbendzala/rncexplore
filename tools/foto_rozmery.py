#!/usr/bin/env python3
"""Zistí šírku hlavnej fotky každého produktu.

Shoptet na detaile vykresľuje fotku do rámu 1024 × 1024 a menšie
nezväčšuje — doplní ich bielou. Z našich 157 fotiek je 145 menších,
takže biela obruba je pri každom produkte iná: od 1,2 % pri zdroji
1000 px po 21 % pri 599 px. Jedno pravidlo v CSS to neodstráni, lebo
by buď nechalo bielu, alebo odrezalo kus panela.

Tento súbor dáva skriptu v zápätí údaj, o koľko má ktorú fotku
priblížiť. Meria sa raz a výsledok sa ukladá, aby generátor zápätia
nemusel pri každom behu sťahovať stopäťdesiat obrázkov.

Sťahuje sa len prvých pár kilobajtov — rozmery sú v hlavičke súboru.

Spustenie:  python3 tools/foto_rozmery.py
"""

import io
import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIEL = os.path.join(KOREN, "data", "foto-rozmery.json")

# Koľko bajtov stačí na hlavičku s rozmermi. JPEG ich má v značke SOF0,
# ktorá býva do pár kilobajtov; 16 kB je s rezervou.
KUS = 16384


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))


def sirka(url):
    from PIL import Image
    try:
        r = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0", "Range": f"bytes=0-{KUS - 1}"})
        with urllib.request.urlopen(r, timeout=30) as o:
            return Image.open(io.BytesIO(o.read())).size[0]
    except Exception:
        return None


def main():
    try:
        import PIL  # noqa: F401
    except ImportError:
        sys.exit("chýba Pillow:  python3 -m pip install Pillow")

    P = [p for p in katalog() if p.get("img")]
    with ThreadPoolExecutor(max_workers=12) as ex:
        sirky = list(ex.map(lambda p: sirka(p["img"][0]), P))

    t = {p["id"]: w for p, w in zip(P, sirky) if w}
    chyba = [p["id"] for p, w in zip(P, sirky) if not w]

    with open(CIEL, "w", encoding="utf-8") as f:
        json.dump(t, f, ensure_ascii=False, indent=0, sort_keys=True)

    print(f"{len(t)} fotiek -> {CIEL}")
    import collections
    c = collections.Counter(t.values())
    for k in sorted(c):
        pas = max(0, (1024 - k) / 2)
        print(f"   {k:>5} px  ×{c[k]:<4} biely pás {pas:.0f} px na stranu")
    if chyba:
        print(f"\n   nepodarilo sa zmerať {len(chyba)}: " + ", ".join(chyba[:5]))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Stiahne fotografie pre dlaždice kategórií na domovskej.

Dlaždice doteraz ukazovali prvý obrázok prvého produktu v kategórii,
načítaný priamo z cdn.shopify.com. Dve veci na tom boli zlé. Prvá:
je to stránka dodávateľa, a keď tam obrázok zmení alebo zmaže,
rozpadne sa nám domovská a nikto si toho hneď nevšimne — rovnaká úvaha
ako pri hero fotke. Druhá: poradie v katalógu nie je výber. Pri
skladacích paneloch z neho vyšla marketingová grafika s textom „500W
Foldable Solar Panel“ cez pol obrázka, čo ako dlaždica vyzerá zle.

Fotky sú preto vybrané po jednej a uložené u nás. Výber je na
produkte, nie na poradí — keď sa katalóg preusporiada, nič sa
nezmení. Keď sa produkt z katalógu stratí, skript spadne a povie
ktorý, namiesto aby ticho stiahol niečo iné.

Spustenie:  python3 tools/fotky_kategorii.py
"""

import io
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vystup                                           # noqa: E402

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Kategória -> produkt, z ktorého berieme prvú fotku, a názov súboru.
# Vyberané podľa toho, ako obrázok vyzerá v dlaždici 4:3: najprv
# fotografia na vozidle, studiový záber až keď lepší nie je.
VYBER = {
    "hood": ("dacia-duster-lensun-67w-hood-bonnet-solar-panel",
             "panely-na-kapotu"),
    "flexible": ("vw-grand-california-600-front-over-cab-lensun-130w-solar-panel",
                 "flexibilne-panely"),
    "rooftent": ("alu-cab-modcap-camper-roof-tent-lensun-400w-flexible-solar-panel",
                 "pre-stresne-stany"),
    "foldable": ("lensun-innovative-waterproof-300w-foldable-solar-panel",
                 "skladacie-panely"),
    "blanket": ("lensunsolar-300w-12v-solar-blanket-for-power-station-12v-battery",
                "solarne-deky"),
    "rv": ("turtleback-expedition-trailers-lensun-66w-flexible-solar-panel",
           "karavany-a-privesy"),
    "tonneau": ("gmc-sierra-1500-bakflip-mx4-tonneau-cover-lensun-80w-solar-panel",
                "na-kryty-korby"),
}

# Dlaždica má na najširšej obrazovke okolo 345 px; 900 px stačí aj na
# obrazovky s dvojnásobnou hustotou a nenúti návštevníka sťahovať
# trojmegový originál.
SIRKA = 900
KVALITA = 82


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))


def stiahni(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=60) as o:
        return o.read()


def main():
    try:
        from PIL import Image
    except ImportError:
        sys.exit("chýba Pillow:  python3 -m pip install Pillow")

    by = {p["id"]: p for p in katalog()}
    chyba = [i for i, _ in VYBER.values() if i not in by]
    if chyba:
        sys.exit("v katalógu nie sú tieto produkty:\n  " + "\n  ".join(chyba))

    priecinok = vystup.kam(vystup.IMPORT, "vzhlad", "fotky")
    hotovo = []
    for kat, (pid, slug) in VYBER.items():
        url = (by[pid].get("img") or [""])[0]
        if not url:
            sys.exit(f"produkt {pid} nemá žiadnu fotku")
        im = Image.open(io.BytesIO(stiahni(url)))
        if im.mode in ("RGBA", "LA", "P"):
            # Priehľadnosť na bielu — dlaždice stoja na bielej karte.
            podklad = Image.new("RGB", im.size, "white")
            im = im.convert("RGBA")
            podklad.paste(im, mask=im.split()[-1])
            im = podklad
        else:
            im = im.convert("RGB")
        povodna = im.size
        if im.width > SIRKA:
            im = im.resize((SIRKA, round(im.height * SIRKA / im.width)),
                           Image.LANCZOS)
        meno = f"kategoria-{slug}.jpg"
        cesta = os.path.join(priecinok, meno)
        im.save(cesta, "JPEG", quality=KVALITA, optimize=True)
        hotovo.append((meno, povodna, im.size, os.path.getsize(cesta)))

    print(f"{len(hotovo)} fotiek -> {priecinok}")
    for meno, p, n, b in hotovo:
        print(f"   {meno:<38} {p[0]}×{p[1]} -> {n[0]}×{n[1]}  {b // 1024} kB")
    print("\nnahrať do Vzhľad a obsah → Správca súborov")


if __name__ == "__main__":
    main()

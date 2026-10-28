#!/usr/bin/env python3
"""Fotografie k článkom, pripravené na nahratie do Shoptetu.

V pokynoch bola pri každom článku uvedená adresa obrázka, lenže
Shoptet k článku prijíma nahratý súbor, nie odkaz. Preto nemá fotku
ani jeden článok — ani vo výpise, ani na domovskej.

Perex sa dopĺňať nemusí: samostatné pole preň Shoptet nemá a do
náhľadu berie text po značku „<!-- pagebreak -->“. Tú aj s perexom
dáva na začiatok tela tools/export_blog.py, takže stačí znova vložiť
obsah článku.

Spustenie:  python3 tools/blog_doplnky.py
"""

import io
import os
import sys
import urllib.request

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup                                           # noqa: E402
from blog_content import POSTS                          # noqa: E402

# Článok sa vo výpise aj na domovskej ukazuje v malom náhľade, do
# detailu sa nedostane vôbec. Tisíc pixelov je na to s rezervou a
# nemá zmysel ťahať do obchodu štvormegové originály.
SIRKA = 1000
KVALITA = 82


def stiahni(url):
    # Jeden článok má fotku z našej starej stránky, teda cestu bez
    # domény. Tá je v repozitári, netreba ju sťahovať.
    if url.startswith("/"):
        return open(os.path.join(KOREN, url.lstrip("/")), "rb").read()
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=60) as o:
        return o.read()


def main():
    try:
        from PIL import Image
    except ImportError:
        sys.exit("chýba Pillow:  python3 -m pip install Pillow")

    priecinok = vystup.kam(vystup.VLOZIT, "blog", "fotky")
    riadky = [
        "FOTOGRAFIE A PEREXY K ČLÁNKOM",
        "=" * 70,
        "",
        "Vzhľad a obsah → Články → otvor článok. Pri každom dve veci:",
        "",
        "  Obsah     cez Nástroje → Zdrojový kód vlož nanovo obsah zo",
        "            súboru <adresa>.html. Začína perexom a značkou",
        "            konca stránky — práve po ňu berie Shoptet text do",
        "            náhľadu vo výpise rubriky.",
        "  Obrázok   tlačidlom Nahrať pod editorom nahraj súbor",
        "            z priečinka fotky/ (Shoptet berie súbor, nie odkaz)",
        "",
        "Samostatné pole pre perex v Shoptete nie je — preto je perex",
        "prvým odsekom článku a hneď za ním stojí tá značka.",
        "",
    ]
    hotovo = chyba = 0

    for p in POSTS:
        adresa = p["slug"] if isinstance(p, dict) else p.slug
        nazov = p["title"][0] if isinstance(p, dict) else p.title[0]
        lead = p["lead"][0] if isinstance(p, dict) else p.lead[0]
        hero = p["hero"] if isinstance(p, dict) else p.hero

        meno = f"{adresa}.jpg"
        cesta = os.path.join(priecinok, meno)
        stav = "už stiahnuté"
        if not os.path.exists(cesta):
            try:
                im = Image.open(io.BytesIO(stiahni(hero)))
                if im.mode in ("RGBA", "LA", "P"):
                    podklad = Image.new("RGB", im.size, "white")
                    im = im.convert("RGBA")
                    podklad.paste(im, mask=im.split()[-1])
                    im = podklad
                else:
                    im = im.convert("RGB")
                if im.width > SIRKA:
                    im = im.resize((SIRKA, round(im.height * SIRKA / im.width)),
                                   Image.LANCZOS)
                im.save(cesta, "JPEG", quality=KVALITA, optimize=True)
                stav = f"{im.width}×{im.height}"
                hotovo += 1
            except Exception as e:
                stav = f"NEPODARILO SA — {e}"
                chyba += 1
                meno = "(chýba)"

        riadky += [
            "-" * 70,
            nazov,
            f"  adresa    {adresa}",
            f"  obrázok   fotky/{meno}",
            f"  obsah     {adresa}.html",
            "  náhľad    " + lead,
            "",
        ]
        print(f"   {adresa:<42} {stav}")

    cesta_txt = vystup.kam(vystup.VLOZIT, "blog", "_FOTKY-A-PEREXY.txt")
    with open(cesta_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(riadky) + "\n")

    print(f"\n{len(POSTS)} článkov · stiahnutých {hotovo}"
          + (f" · chýb {chyba}" if chyba else ""))
    print(f"   {priecinok}")
    print(f"   {cesta_txt}")


if __name__ == "__main__":
    main()

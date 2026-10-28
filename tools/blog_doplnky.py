#!/usr/bin/env python3
"""Perexy a fotografie k článkom, pripravené na doplnenie v Shoptete.

Články sú v obchode vložené, ale chýbajú im dve veci a obe sú vidieť
na prvý pohľad.

Perex: v Shoptete zostalo pole „Popis“ prázdne, takže si ho dopočítal
sám z tela článku — a keďže telá začínajú nadpisom <h2>, zobral z neho
len prvé slovo a oreže ho. Vo výpise rubriky tak pod každým názvom
svieti „Preč…“, „Para…“, „Podk…“. Perexy pritom napísané máme, len sa
do obchodu nedostali.

Fotografia: v pokynoch bola uvedená adresa obrázka, lenže Shoptet
k článku prijíma nahratý súbor, nie odkaz. Preto nemá fotku ani jeden
článok — ani vo výpise, ani na domovskej.

Tento nástroj teda stiahne obrázky a vypíše perexy tak, aby sa dali
kopírovať pole po poli.

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
        "PEREXY A FOTOGRAFIE K ČLÁNKOM",
        "=" * 70,
        "",
        "Vzhľad a obsah → Články → otvor článok.",
        "",
        "  Popis     vlož perex odtiaľto (je to pole nad obsahom)",
        "  Obrázok   nahraj súbor z priečinka fotky/",
        "",
        "Perex nie je ozdoba: bez neho si ho Shoptet dopočíta z tela",
        "článku a keďže telá začínajú nadpisom, vyjde z toho „Preč…“.",
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
            "  perex     " + lead,
            "",
        ]
        print(f"   {adresa:<42} {stav}")

    cesta_txt = vystup.kam(vystup.VLOZIT, "blog", "_PEREXY-A-FOTKY.txt")
    with open(cesta_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(riadky) + "\n")

    print(f"\n{len(POSTS)} článkov · stiahnutých {hotovo}"
          + (f" · chýb {chyba}" if chyba else ""))
    print(f"   {priecinok}")
    print(f"   {cesta_txt}")


if __name__ == "__main__":
    main()

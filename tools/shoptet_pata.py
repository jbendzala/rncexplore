#!/usr/bin/env python3
"""Pätička e-shopu podľa návrhu.

Shoptet má v Classic šablóne pätičku prakticky prázdnu — zostane v nej
len riadok s copyrightom a podpisom „Vytvoril Shoptet“. Štyri stĺpce
z návrhu tam cez administráciu nijak nedostaneme: jediné pole, ktoré
vie vložiť vlastné HTML na každú stránku, je Vzhľad a obsah → Editor →
HTML kód → Zápätie, a to sa vykreslí až pred </body>, teda pod
pätičkou. Preto je na konci štyri riadky skriptu, ktoré blok presunú
dovnútra <footer> nad riadok s copyrightom. Bez toho by stĺpce viseli
pod ním.

Podpis Shoptetu zostáva — má v sebe natvrdo
„display:inline-block !important; visibility:visible !important“ a na
skúšobnej verzii sa vypnúť nedá.

Výstup: pata.html — jeden blok na vloženie do Zápätia.
"""

import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vystup                                          # noqa: E402

# Adresy sú overené proti živému obchodu, nie odhadnuté. Dve sa od
# predpokladu líšia: články sú na /blog/ (nie /nase-spravy/) a kontakt
# na /kontakty/ (nie /kontakt/).
PRODUKTY = [
    ("Panely na kapotu",   "/panely-na-kapotu/"),
    ("Flexibilné panely",  "/flexibilne-panely/"),
    ("Pre strešné stany",  "/pre-stresne-stany/"),
    ("Na kryty korby",     "/na-kryty-korby/"),
    ("Karavany a prívesy", "/karavany-a-privesy/"),
    ("Skladacie panely",   "/skladacie-panely/"),
    ("Solárne deky",       "/solarne-deky/"),
]

INFORMACIE = [
    ("Veľkoobchod", "/velkoobchod/"),
    ("Na mieru",    "/na-mieru/"),
    ("Montáž",      "/montaz/"),
    ("O nás",       "/o-nas/"),
    ("Blog",        "/blog/"),
    ("FAQ",         "/faq/"),
    ("Kontakt",     "/kontakty/"),
]

PEREX = ("Solárna energia pre vozidlá a karavany. Panely, regulátory "
         "a vybavenie pre cestovateľov.")


def e(x):
    return html.escape(str(x), quote=True)


def stlpec(nadpis, odkazy):
    polozky = "".join(f'<li><a href="{e(u)}">{e(n)}</a></li>'
                      for n, u in odkazy)
    return (f'<div class="rnc-pata-st"><h3>{e(nadpis)}</h3>'
            f'<ul>{polozky}</ul></div>')


def blok():
    return f'''<div id="rnc-pata" class="rnc-pata">
  <div class="container rnc-pata-in">
    <div class="rnc-pata-st rnc-pata-znacka">
      <h3>RNC EXPLORE</h3>
      <p>{e(PEREX)}</p>
    </div>
    {stlpec("Produkty", PRODUKTY)}
    {stlpec("Informácie", INFORMACIE)}
    <div class="rnc-pata-st">
      <h3>Pre partnerov a kontakt</h3>
      <p><a class="rnc-btn-ghost-amber" href="/velkoobchod/">Veľkoobchod (B2B) →</a></p>
      <p class="rnc-pata-jazyk"><strong>SK</strong><span>|</span>CZ</p>
    </div>
  </div>
  <div class="container rnc-pata-spodok">
    <a href="/obchodne-podmienky/">Obchodné podmienky</a>
  </div>
</div>
<script>
/* Zápätie sa vkladá pred </body>, teda pod pätičku. Presunieme blok
   dovnútra <footer> nad riadok s copyrightom. */
(function () {{
  var p = document.getElementById("rnc-pata"),
      f = document.getElementById("footer");
  if (p && f) {{ f.insertBefore(p, f.firstChild); }}
}})();
</script>'''


def main():
    kod = blok()
    cesta = vystup.kam(vystup.IMPORT, "vzhlad", "pata.html")
    with open(cesta, "w", encoding="utf-8") as f:
        f.write(kod)
    print("vložiť do Vzhľad a obsah → Editor → HTML kód → Zápätie")
    print(f"   {cesta}")
    znakov = len(kod)
    print(f"   {znakov:>6} znakov · strop 8192 · "
          + ("zmestí sa, zostáva %d" % (8192 - znakov) if znakov <= 8192
             else "PRESAHUJE, treba skrátiť"))
    print(f"   odkazov: {len(PRODUKTY) + len(INFORMACIE) + 2}")
    if znakov > 8192:
        sys.exit(1)


if __name__ == "__main__":
    main()

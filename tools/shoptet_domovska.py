# -*- coding: utf-8 -*-
"""Postaví domovskú stránku podľa návrhu grafika.

Shoptet má na domovskej vlastné bloky — karusel, bannery, blok produktov
— ale návrh ich poskladanie nekopíruje a dva prvky (články a recenzie)
Classic vôbec nemá. Preto sa celá domovská stavia ako naše HTML a vkladá
sa do úvodnej stránky, kde máme plnú kontrolu:

    Vzhľad a obsah → Stránky → úvodná stránka → HTML režim

Vyhľadávanie vozidla sa vkladá hotové z tools/shoptet_vyhladavanie.py —
ten si musí stiahnuť adresy produktov z mapy stránok obchodu, takže je to
jediná časť stavby, ktorá potrebuje sieť. Spusti ho pred týmto skriptom.

Nie sú tu stany a kempingové vybavenie, ktoré návrh ukazuje
medzi kategóriami — tie v katalógu nie sú.

Spustenie:  python3 tools/shoptet_domovska.py
"""
import html
import json
import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo
import vystup
import blog_content as B
from pages_content import REVIEWS
from shoptet_vyhladavanie import adresy, bez_diakritiky

# Adresy kategórií v Shoptete. Vznikli z názvov pri importe — overené
# v mape stránky obchodu.
KATEGORIE = [
    ("hood",     "Panely na kapotu",   "panely-na-kapotu"),
    ("flexible", "Flexibilné panely",  "flexibilne-panely"),
    ("rooftent", "Pre strešné stany",  "pre-stresne-stany"),
    ("foldable", "Skladacie panely",   "skladacie-panely"),
    ("blanket",  "Solárne deky",       "solarne-deky"),
    ("rv",       "Karavany a prívesy", "karavany-a-privesy"),
    ("tonneau",  "Na kryty korby",     "na-kryty-korby"),
]

# Štyri do veľkých kachličiek — tie, ktoré majú najviac produktov.
VELKE = ["hood", "flexible", "foldable", "rooftent"]

# Odporúčané produkty. Prvé tri sú z návrhu — a zhodou okolností sú to
# práve tie, ku ktorým máme recenzie. Štvrtý mal byť regulátor MPPT 20 A,
# ktorý samostatne nepredávame; najbližšie má deka v sade s MPPT
# regulátorom, a zároveň ukáže aj iný druh tovaru než panel na kapotu.
ODPORUCAME = [
    "dacia-duster-lensun-40w-hood-bonnet-solar-panel",
    "toyota-land-cruiser-100-series-lensun-100w-hood-flexible-solar-panel",
    "lensun-400w-200w-flexible-solar-panel",
    "lensunsolar-300w-solar-panel-blanket-with-controller",
]

VYHODY = [
    ("Energia bez motora",
     "Panel nabíja batériu počas státia aj jazdy. Chladnička či fotoaparát "
     "fungujú bez štartovania auta."),
    ("Tvarované na konkrétne vozidlo",
     "Kapotové panely sú vyrobené na tvar konkrétneho modelu a generácie. "
     "Nelepíte univerzálny obdĺžnik."),
    ("Montáž bez vŕtania",
     "Flexibilné panely sú hrubé pár milimetrov a prilepia sa na povrch, "
     "bez dier, rámov a odporu vzduchu."),
    ("Stavané na drsné použitie",
     "Navrhnuté pre vietor, dážď, prach a vibrácie, na trvalé používanie vonku."),
]

BLOG_ZAKLAD = "/nase-spravy"       # kde Shoptet drží články
ADRESY = {}                        # id produktu -> adresa v obchode

# Fotografie, ktoré si do návrhu vybral grafik. Nahrávajú sa do Správcu
# súborov a odkazujeme na vlastnú kópiu, nie na pôvodný zdroj: hero bola
# na lensunsolar.com, čo je stránka dodávateľa. Keby ju tam zmenili,
# zmizol by najväčší obrázok na domovskej a nikto by si toho hneď
# nevšimol. Súbory sú v shoptet-import/vzhlad/fotky.
FOTO = {
    "hero": "/user/documents/upload/hero-tacoma.jpg",
    "life": "/user/documents/upload/lifestyle-montaz.jpg",
}


def e(x):
    return html.escape(str(x), quote=True)


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});", s, re.S).group(1))
    return P, meta


def od_ceny(p):
    return min(seo.price(v["p"], "EUR") for v in p["var"])


def cena(x):
    return f"{x:,.2f}".replace(",", " ").replace(".", ",") + " €"


def hero():
    """Hero na celú šírku okna.

    V návrhu má 1440 × 560 px, teda siaha od okraja po okraj, a štyri
    výhody sú dole v jednom rade s jantárovými bodkami. Obsah Shoptetu je
    pritom obmedzený na šírku stránky, takže sa z nej musíme vymaniť —
    na to je ten výpočet so 100vw v CSS.
    """
    body = "".join(f"<li>{e(n)}</li>" for n, _ in VYHODY)
    return f'''
<section class="rnc-hero" style="background-image:url('{e(FOTO["hero"])}')">
  <div class="rnc-wrap rnc-hero-in">
    <p class="rnc-eyebrow">RNC EXPLORE</p>
    <h2>Solárna energia<br>pre vozidlá a karavany</h2>
    <p class="rnc-lead">Vyberte produkt a prevedenie, vložte do košíka a
       objednajte. Faktúru s QR kódom pošleme e-mailom, tovar odošleme
       po úhrade.</p>
    <p class="rnc-cta">
      <a class="rnc-btn" href="/panely-na-kapotu/">Zobraziť celý katalóg →</a>
      <a class="rnc-link-light" href="/na-mieru/">Panely na mieru</a>
    </p>
    <ul class="rnc-hero-body">{body}</ul>
  </div>
</section>'''


def vyhladavanie():
    """Vyhľadávanie vozidla. Vyrába ho tools/shoptet_vyhladavanie.py, lebo
    si musí stiahnuť adresy produktov z mapy stránok obchodu — a to je
    jediné miesto v celej stavbe, ktoré potrebuje sieť. Tu sa len vloží."""
    cesta = vystup.kam(vystup.IMPORT, "vzhlad", "vyhladavanie-vozidla.html")
    if not os.path.exists(cesta):
        sys.exit("chýba vyhľadávanie vozidla — spusti najprv:\n"
                 "  python3 tools/shoptet_vyhladavanie.py")
    return open(cesta, encoding="utf-8").read()


def kategorie(P, meta):
    pocty = {c["k"]: c["n"] for c in meta["cats"]}
    foto = {}
    for p in P:
        foto.setdefault(p["cat"], (p.get("img") or [""])[0])

    velke = "".join(f'''
    <a class="rnc-cat" href="/{slug}/">
      <span class="rnc-cat-img" style="background-image:url('{e(foto.get(k, ""))}')"></span>
      <span class="rnc-cat-txt"><strong>{e(nazov)}</strong>
        <span>{pocty.get(k, 0)} produktov</span></span>
      <span class="rnc-cat-sip">→</span>
    </a>''' for k, nazov, slug in KATEGORIE if k in VELKE)

    stitky = "".join(
        f'<a href="/{slug}/">{e(nazov)} <span>{pocty.get(k, 0)}</span></a>'
        for k, nazov, slug in KATEGORIE)

    return f'''
<section class="rnc-sec">
  <div class="rnc-sec-head">
    <div>
      <p class="rnc-eyebrow">KATEGÓRIE</p>
      <h2>Vyberte, čo hľadáte</h2>
    </div>
    <a class="rnc-more" href="/panely-na-kapotu/">Zobraziť celý katalóg →</a>
  </div>
  <div class="rnc-cats">{velke}
  </div>
  <p class="rnc-eyebrow rnc-eyebrow-sm">SOLÁRNE PANELY PODĽA TYPU</p>
  <div class="rnc-chips">{stitky}</div>
</section>'''


def odporucame(P):
    """Vypíše odporúčané produkty.

    Keď niektorý v katalógu nie je, skript spadne. Je to zámer: tichý
    preskok by znamenal domovskú s tromi kachličkami namiesto štyroch a
    nikto by si toho nevšimol, kým to neuvidí zákazník.
    """
    by = {p["id"]: p for p in P}
    chyba = [x for x in ODPORUCAME if x not in by]
    if chyba:
        sys.exit("v katalógu nie sú tieto odporúčané produkty:\n  "
                 + "\n  ".join(chyba))
    karty = []
    for pid in ODPORUCAME:
        p = by[pid]
        kat = dict((k, n) for k, n, _ in KATEGORIE).get(p["cat"], "")
        karty.append(f'''
    <a class="rnc-prod" href="{e(ADRESY[p["id"]])}">
      <span class="rnc-prod-img" style="background-image:url('{e((p.get("img") or [""])[0])}')"></span>
      <h3>{e(p["n"]["sk"])}</h3>
      <p class="rnc-prod-kat">{e(kat)}</p>
      <p class="rnc-prod-cena">od <strong>{cena(od_ceny(p))}</strong>
         <span>s DPH</span></p>
      <p class="rnc-more">Zobraziť detail →</p>
    </a>''')
    return f'''
<section class="rnc-sec rnc-sec-alt">
  <div class="rnc-sec-head">
    <div>
      <p class="rnc-eyebrow">ODPORÚČAME</p>
      <h2>Odporúčame</h2>
    </div>
    <a class="rnc-more" href="/panely-na-kapotu/">Zobraziť celý katalóg →</a>
  </div>
  <p class="rnc-sub">Vyberte produkt a prevedenie, vložte do košíka a objednajte.</p>
  <div class="rnc-prods">{"".join(karty)}
  </div>
</section>'''


def benefity():
    polozky = "".join(f'<div><strong>{e(n)}</strong><p>{e(t)}</p></div>'
                      for n, t in VYHODY)
    return f'''
<section class="rnc-sec rnc-life">
  <div class="rnc-life-foto" style="background-image:url('{e(FOTO["life"])}')"></div>
  <div class="rnc-life-txt">
    <h2>Energia, ktorá vám dáva slobodu</h2>
    <p class="rnc-sub">Pre dlhšie cesty, vzdialenejšie miesta a väčšiu
       nezávislosť.</p>
    <div class="rnc-benefits">{polozky}</div>
  </div>
</section>'''


def recenzie():
    karty = "".join(f'''
    <figure class="rnc-rev">
      <span class="rnc-rev-img" style="background-image:url('{e(r["img"])}')"></span>
      <blockquote>{e(r["sk"])}</blockquote>
      <figcaption><strong>{e(r["who"])}</strong><span>{e(r["car"])}</span></figcaption>
    </figure>''' for r in REVIEWS)
    return f'''
<section class="rnc-sec rnc-sec-alt">
  <p class="rnc-eyebrow">RECENZIE</p>
  <h2>Skúsenosti zákazníkov</h2>
  <p class="rnc-sub">Zostavy na reálnych vozidlách. Recenzie z lensunsolar.com,
     preložené a skrátené.</p>
  <div class="rnc-revs">{karty}</div>
</section>'''


def clanky():
    def datum(d):
        r, m, den = d.split("-")
        return f"{int(den)}. {int(m)}. {r}"
    karty = "".join(f'''
    <article class="rnc-post">
      <a class="rnc-post-img" href="{BLOG_ZAKLAD}/{e(a["slug"])}/"
         style="background-image:url('{e(a.get("hero") or "")}')"></a>
      <p class="rnc-post-meta"><span class="rnc-tag">{e(B.CAT[a["cat"]][0])}</span>
         {datum(a["date"])}</p>
      <h3><a href="{BLOG_ZAKLAD}/{e(a["slug"])}/">{e(a["title"][0])}</a></h3>
      <p>{e(a["lead"][0][:130])}…</p>
      <p><a class="rnc-more" href="{BLOG_ZAKLAD}/{e(a["slug"])}/">Čítať viac →</a></p>
    </article>''' for a in B.newest(3))
    return f'''
<section class="rnc-sec">
  <div class="rnc-sec-head">
    <div>
      <p class="rnc-eyebrow">BLOG</p>
      <h2>Tipy, montáž a inšpirácia</h2>
    </div>
    <a class="rnc-more" href="{BLOG_ZAKLAD}/">Všetky články →</a>
  </div>
  <p class="rnc-sub">Návody a nápady, vďaka ktorým z techniky vyťažíte maximum.</p>
  <div class="rnc-posts">{karty}</div>
</section>'''


def b2b():
    return '''
<section class="rnc-b2b">
  <div>
    <h2>Ste predajca alebo montážny servis?</h2>
    <p>Partnerské ceny a nákupné funkcie uvidíte po prihlásení do B2B.</p>
  </div>
  <p class="rnc-cta">
    <a class="rnc-btn" href="/velkoobchod/">Registrácia partnera</a>
    <a class="rnc-btn rnc-btn-ghost" href="/login/">Prihlásiť sa do B2B →</a>
  </p>
</section>'''


def main():
    P, meta = katalog()
    # Odkazy na produkty berieme z mapy stránok obchodu, nie z odhadu —
    # rovnako ako vo vyhľadávaní vozidla.
    mapa = adresy()
    global ADRESY
    ADRESY = {p["id"]: "/" + mapa[bez_diakritiky(p["n"]["sk"])] + "/"
              for p in P if bez_diakritiky(p["n"]["sk"]) in mapa}
    casti = [
        "<!-- Domovská stránka rncexplore.com podľa návrhu grafika.",
        "     Vyrába tools/shoptet_domovska.py — needituj tu, uprav zdroj.",
        "     Vkladá sa do: Vzhľad a obsah → Stránky → úvodná stránka,",
        "     v editore prepni na HTML režim. -->",
        hero(), vyhladavanie(), kategorie(P, meta), odporucame(P),
        benefity(), recenzie(), clanky(), b2b(),
    ]
    h = "\n".join(casti) + "\n"
    ciel = vystup.kam(vystup.IMPORT, "vzhlad", "uvodna-stranka.html")
    with open(ciel, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"{len(h):>6} znakov -> {ciel}")
    print(f"  sekcií: {len(casti) - 4}")
    print(f"  kategórií: {len(KATEGORIE)} · značiek: {len(meta['brands'])} · "
          f"produktov: {len(ODPORUCAME)} · recenzií: {len(REVIEWS)} · článkov: 3")
    print("  vyhľadávanie vozidla: vložené")


if __name__ == "__main__":
    main()

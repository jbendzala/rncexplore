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

BLOG_ZAKLAD = "/blog"              # overené proti živému obchodu;
                                   # /nase-spravy vracia 404
ADRESY = {}                        # id produktu -> adresa v obchode

# Fotografie, ktoré si do návrhu vybral grafik. Nahrávajú sa do Správcu
# súborov a odkazujeme na vlastnú kópiu, nie na pôvodný zdroj: hero bola
# na lensunsolar.com, čo je stránka dodávateľa. Keby ju tam zmenili,
# zmizol by najväčší obrázok na domovskej a nikto by si toho hneď
# nevšimol. Súbory sú v shoptet-import/vzhlad/fotky.
FOTO = {
    "hero": "/user/documents/upload/hero-tacoma.jpg",
    # Lifestyle pás zámerne bez fotky. V návrhu je na tomto mieste
    # prázdne okno s popisom „LIFESTYLE FOTO — dvojklik = nahrať“ a ten
    # tmavo-oranžový prechod je jeho výplň, nie fotografia. Čo sme tam
    # mali predtým (lifestyle-montaz.jpg) je detail dverí vysoký 864 px;
    # v páse širokom cez celú obrazovku z neho zostal červený pruh.
    # Sem patrí široký záber vozidla v teréne — keď príde, stačí ho
    # doplniť a prekryje prechod.
    "life": "",
}

# Video pod tlačidlom „Pozrieť video“ v lifestyle páse. Návrh je obrázok,
# odkaz v ňom nie je, tak sem ide to z katalógu, ktoré je najvšeobecnejšie
# — montáž flexibilného panela, visí pri štyroch produktoch. Keď klient
# natočí vlastné, stačí vymeniť adresu tu.
VIDEO = "https://www.youtube.com/watch?v=k20-KXD_x_k"


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
  <div class="container rnc-hero-in">
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
    """Štyri veľké dlaždice a pod nimi štítky so všetkými kategóriami.

    Fotky v dlaždiciach sú naše vlastné kópie, nie odkazy na
    cdn.shopify.com — prečo, je v tools/fotky_kategorii.py. Keď niektorá
    chýba, dlaždica by zostala prázdna a nebolo by to na prvý pohľad
    vidieť, tak to radšej povieme hneď.
    """
    pocty = {c["k"]: c["n"] for c in meta["cats"]}
    fotky = os.path.join(vystup.IMPORT, "vzhlad", "fotky")
    chyba = [s for _, _, s in KATEGORIE
             if not os.path.exists(os.path.join(fotky, f"kategoria-{s}.jpg"))]
    if chyba:
        sys.exit("chýbajú fotky kategórií — spusti najprv:\n"
                 "  python3 tools/fotky_kategorii.py\n  "
                 + "\n  ".join(f"kategoria-{x}.jpg" for x in chyba))
    foto = {s: f"/user/documents/upload/kategoria-{s}.jpg"
            for _, _, s in KATEGORIE}

    velke = "".join(f'''
    <a class="rnc-cat" href="/{slug}/">
      <span class="rnc-cat-img" style="background-image:url('{e(foto[slug])}')"></span>
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
            # Vnútri odkazu sú zámerne len <span>, žiadne <h3> a <p>.
        # Editor Shoptetu si z vloženého HTML robí svoje: keď v <a>
        # nájde blokový prvok, odkaz okolo neho rozdelí a prázdny
        # zvyšok zahodí. Na ostrej stránke tak zo štyroch kariet
        # zostali holé texty bez fotky a bez prekliku. Dlaždice
        # kategórií to prežili práve preto, že majú len spany.
        karty.append(f'''
    <a class="rnc-prod" href="{e(ADRESY[p["id"]])}">
      <span class="rnc-prod-img" style="background-image:url('{e((p.get("img") or [""])[0])}')"></span>
      <span class="rnc-prod-n">{e(p["n"]["sk"])}</span>
      <span class="rnc-prod-kat">{e(kat)}</span>
      <span class="rnc-prod-cena">od <strong>{cena(od_ceny(p))}</strong>
         <span>s DPH</span></span>
      <span class="rnc-more">Zobraziť detail →</span>
    </a>''')
    return f'''
<section class="rnc-sec">
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
    """Lifestyle pás podľa návrhu.

    V návrhu ide cez celú šírku okna: vľavo fotka stmavená prechodom,
    v nej nadpis, veta a odkaz na video, vpravo tmavý panel so štyrmi
    výhodami pod sebou, oddelenými tenkou linkou. Fotka je na pozadí
    celého pásu a panel ju vpravo prekrýva — vďaka tomu sa predel medzi
    nimi trafí presne tam, kde končí obsah stránky, a výhody sú
    zarovnané s ostatnými sekciami.
    """
    polozky = "".join(
        f'<div class="rnc-ben"><span class="rnc-ben-ico"></span>'
        f'<strong>{e(n)}</strong><p>{e(t)}</p></div>' for n, t in VYHODY)
    foto = (f' style="background-image:url(\'{e(FOTO["life"])}\')"'
            if FOTO["life"] else "")
    return f'''
<section class="rnc-life">
  <div class="rnc-life-foto"{foto}></div>
  <div class="container rnc-life-in">
    <div class="rnc-life-txt">
      <h2>Energia, ktorá vám dáva slobodu.</h2>
      <p>Pre dlhšie cesty, vzdialenejšie miesta a väčšiu nezávislosť.</p>
      <a class="rnc-play" href="{e(VIDEO)}" target="_blank" rel="noopener">
        <span class="rnc-play-ico">▶</span><span>Pozrieť video</span></a>
    </div>
    <div class="rnc-life-panel">{polozky}</div>
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
<section class="rnc-sec">
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
<section class="rnc-sec rnc-band rnc-band-biely">
  <div class="container">
  <div class="rnc-sec-head">
    <div>
      <p class="rnc-eyebrow">BLOG</p>
      <h2>Tipy, montáž a inšpirácia</h2>
    </div>
    <a class="rnc-more" href="{BLOG_ZAKLAD}/">Všetky články →</a>
  </div>
  <p class="rnc-sub">Návody a nápady, vďaka ktorým z techniky vyťažíte maximum.</p>
  <div class="rnc-posts">{karty}</div>
  </div>
</section>'''


def b2b():
    return '''
<section class="rnc-band rnc-b2b">
  <div class="container rnc-b2b-in">
    <div>
      <h2>Ste predajca alebo montážny servis?</h2>
      <p>Partnerské ceny a nákupné funkcie uvidíte po prihlásení do B2B.</p>
    </div>
    <p class="rnc-cta">
      <a class="rnc-btn" href="/velkoobchod/">Registrácia partnera</a>
      <a class="rnc-btn rnc-btn-ghost" href="/login/">Prihlásiť sa do B2B →</a>
    </p>
  </div>
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

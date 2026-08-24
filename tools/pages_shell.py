# -*- coding: utf-8 -*-
"""Spoločné časti stránok: hlavička, navigácia, pätička."""

# (súbor, SK názov, CZ názov)  — poradie v hlavnom menu
NAV = [
    ("index",       "Domov",        "Domů"),
    ("produkty",    "Produkty",     "Produkty"),
    ("velkoobchod", "Veľkoobchod",  "Velkoobchod"),
    ("na-mieru",    "Na mieru",     "Na míru"),
    ("montaz",      "Montáž",       "Montáž"),
    ("o-nas",       "O nás",        "O nás"),
    ("faq",         "FAQ",          "FAQ"),
    ("kontakt",     "Kontakt",      "Kontakt"),
]

# kategórie do rozbaľovacieho menu pod "Produkty"
SUBCATS = [
    ("hood",       "Panely na kapotu",     "Panely na kapotu"),
    ("flexible",   "Flexibilné panely",    "Flexibilní panely"),
    ("rooftent",   "Pre strešné stany",    "Pro střešní stany"),
    ("tonneau",    "Na kryty korby",       "Na kryty korby"),
    ("rv",         "Karavany a prívesy",   "Karavany a přívěsy"),
    ("foldable",   "Skladacie panely",     "Skládací panely"),
    ("blanket",    "Solárne deky",         "Solární deky"),
    ("controller", "Regulátory nabíjania", "Regulátory nabíjení"),
    ("inverter",   "Meniče napätia",       "Měniče napětí"),
    ("accessory",  "Príslušenstvo",        "Příslušenství"),
]

LOGO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="#141310" stroke-width="2.4" '
            'stroke-linecap="round"><circle cx="12" cy="12" r="4" fill="#141310" stroke="none"/>'
            '<path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1'
            'M19.1 4.9L17 7M7 17l-2.1 2.1"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' fill='%23ffd300'/%3E%3Cpath d='M16 6v3M16 23v3M6 16h3"
           "M23 16h3M9 9l2 2M21 21l2 2M23 9l-2 2M11 21l-2 2' stroke='%23141310' stroke-width='2.2'"
           " stroke-linecap='round'/%3E%3Ccircle cx='16' cy='16' r='4.5' fill='%23141310'/%3E%3C/svg%3E")


def head(lang, base, slug, title, desc):
    other = "cz/" if lang == "sk" else "../"
    return f"""<!doctype html>
<html lang="{'sk' if lang=='sk' else 'cs'}" data-theme="">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://www.rncexplore.com/{'' if lang=='sk' else 'cz/'}{'' if slug=='index' else slug+'.html'}">
<link rel="alternate" hreflang="sk" href="https://www.rncexplore.com/{'' if slug=='index' else slug+'.html'}">
<link rel="alternate" hreflang="cs" href="https://www.rncexplore.com/cz/{'' if slug=='index' else slug+'.html'}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{base}assets/styles.css">
</head>
<body>
"""


def header(lang, base, slug, page=""):
    i = 1 if lang == "sk" else 2
    items = []
    for s, sk, cs in NAV:
        label = sk if lang == "sk" else cs
        href = page + ("index.html" if s == "index" else s + ".html")
        cur = ' aria-current="page"' if s == slug else ""
        if s == "produkty":
            subs = "".join(
                f'<li><a href="{page}produkty.html?cat={k}">{(a if lang=="sk" else b)}</a></li>'
                for k, a, b in SUBCATS)
            items.append(
                f'<li class="has-sub"><button type="button" aria-expanded="false">{label}'
                f'<svg class="caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" '
                f'stroke-width="2"><path d="M2 4l4 4 4-4"/></svg></button>'
                f'<ul class="sub"><li><a href="{page}produkty.html"><strong>{"Celý katalóg" if lang=="sk" else "Celý katalog"}</strong></a></li>{subs}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    nav = "".join(items)

    f = "index.html" if slug == "index" else slug + ".html"
    if lang == "sk":
        to_sk, to_cs = f, "cz/" + f
    else:
        to_sk, to_cs = "../" + f, f

    util = "Solárne panely pre vozidlá, karavany a outdoor" if lang == "sk" else "Solární panely pro vozidla, karavany a outdoor"
    search_ph = "Hľadať produkt…" if lang == "sk" else "Hledat produkt…"
    menu = "Menu"
    return f"""<div class="util"><div class="util-in">
  <span>{util}</span><span class="sp"></span>
  <a class="js-phone" href="#"></a><a class="js-mail" href="#"></a>
</div></div>

<header class="hdr"><div class="wrap hdr-in">
  <a class="brand" href="{page}index.html">
    <span class="brand-mark" aria-hidden="true">{LOGO_SVG}</span>
    <span class="js-company"></span>
  </a>
  <span class="hdr-sp"></span>
  <ul class="nav" id="nav">{nav}</ul>
  <button class="icon-btn" id="themeBtn" data-t-theme>
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
      <path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z"/></svg>
  </button>
  <nav class="langs" aria-label="Jazyk">
    <a href="{to_sk}"{' aria-current="true"' if lang=='sk' else ''}>SK</a>
    <a href="{to_cs}"{' aria-current="true"' if lang=='cs' else ''}>CZ</a>
  </nav>
  <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="{menu}">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
      <path d="M3 6h18M3 12h18M3 18h18"/></svg>
  </button>
</div></header>
"""


def footer(lang, base, page=""):
    sk = lang == "sk"
    nav_links = "".join(
        f'<li><a href="{base}{"index.html" if s=="index" else s+".html"}">{(a if sk else b)}</a></li>'
        for s, a, b in NAV)
    h_nav  = "Navigácia" if sk else "Navigace"
    h_con  = "Kontakt"
    h_inf  = "Informácie" if sk else "Informace"
    terms  = "Obchodné podmienky" if sk else "Obchodní podmínky"
    info   = ("Katalóg slúži na prezeranie sortimentu. Objednávky vybavujeme "
              "individuálne e-mailom." if sk else
              "Katalog slouží k prohlížení sortimentu. Objednávky vyřizujeme "
              "individuálně e-mailem.")
    return f"""
<footer class="ftr">
  <div class="wrap ftr-in">
    <div>
      <h4>{h_con}</h4>
      <p><strong class="js-company"></strong></p>
      <ul>
        <li><a class="js-mail" href="#"></a></li>
        <li><a class="js-phone" href="#"></a></li>
        <li class="js-web"></li>
      </ul>
    </div>
    <div>
      <h4>{h_nav}</h4>
      <ul>{nav_links}</ul>
    </div>
    <div>
      <h4>{h_inf}</h4>
      <p>{info}</p>
      <ul><li><a href="{page}podmienky.html">{terms}</a></li></ul>
    </div>
  </div>
  <div class="wrap ftr-btm"><span class="js-rights"></span></div>
</footer>

<script src="{base}config.js"></script>
<script>window.LANG="{'sk' if sk else 'cs'}";</script>
<script src="{base}assets/site.js"></script>
"""


def catalog_scripts(base):
    return (f'<script src="{base}data/products.js"></script>\n'
            f'<script src="{base}assets/app.js"></script>\n')


def close():
    return "</body>\n</html>\n"

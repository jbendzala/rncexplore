#!/usr/bin/env python3
"""Horná lišta a pätička podľa návrhu.

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

To isté pole berie aj hornú lištu. Shoptet do nej dáva telefón
z nastavení, položky Horného menu a prihlásenie; návrh tam má vľavo
dva sľuby o objednávke a vpravo jazyk, veľkoobchod a kontakt. Vlastný
blok sa vloží na začiatok lišty a Shoptetove dva sa skryjú v CSS.
Nástroje vpravo (prihlásenie a na mobile hamburger) zostávajú — sú to
jediné miesta, kadiaľ sa dá na desktope prihlásiť.

Odkazy, ktoré doteraz viseli v hornom menu — ako nakupovať, obchodné
podmienky a ochrana osobných údajov — sú preto v spodnom riadku
pätičky. Zmiznúť nesmú.

Vznikajú dva súbory, rovnako ako pri vzhľade:

    rnc-skript.js      nahrať do Vzhľad a obsah → Správca súborov
    do-zapatia.html    vložiť do Zápätia (značky a odkaz na skript)

Prečo oddelene: pole Zápätia berie najviac 8192 znakov a samotný skript
sa doň prestal zmestať, keď k nemu pribudla tabuľka s údajmi pre karty
produktov. Značky tam zostávajú — pätička má šestnásť odkazov a tie
majú byť v zdroji stránky, nie dorábané skriptom.

Za adresou skriptu je ?v= s odtlačkom obsahu, nech si prehliadače
stiahnu novú verziu hneď po zmene.
"""

import hashlib
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jazyk
import vystup                                          # noqa: E402
from shoptet_vyhladavanie import adresy, bez_diakritiky  # noqa: E402

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SUBOR = "rnc-skript.js"             # ako sa bude volať v Správcovi súborov
CESTA = "/user/documents/upload"    # kam ukladá Správca súborov
STROP = 8192                        # koľko znakov znesie pole Zápätia

# Názvy kategórií tak, ako ich má vidieť zákazník na karte. Kľúče sú
# naše vnútorné kódy z data/products.js.
KATEGORIE = {
    "hood":     "Panely na kapotu",
    "flexible": "Flexibilné panely",
    "rooftent": "Pre strešné stany",
    "foldable": "Skladacie panely",
    "blanket":  "Solárne deky",
    "rv":       "Karavany a prívesy",
    "tonneau":  "Na kryty korby",
}

# Čo sa lepí na povrch — tie dostanú štítok „Bez vŕtania“. Skladacie
# panely a deky sa nemontujú vôbec.
PRILEPENE = {"hood", "flexible", "rooftent", "tonneau", "rv"}

# Rám, do ktorého Shoptet vykresľuje hlavnú fotku na detaile. Menšie
# fotky nezväčšuje, len ich doplní bielou — odtiaľ tá obruba.
RAM_DETAILU = 1024

# Rubrika blogu -> jej adresa v obchode. Kľúče sú naše vnútorné kódy
# z tools/blog_content.py.
RUBRIKY = {
    "kapota":   "solarny-panel-na-kapotu",
    "montaz":   "skusenosti-z-montaze",
    "prenosne": "prenosne-panely",
    "technika": "technika",
}

# Koľko najnovších článkov ukázať na stránke Blog. Rubrika Blog
# vlastné články nemá — všetky sú v jej štyroch podrubrikách a Shoptet
# ich do nadradenej rubriky nepreberá.
CLANKOV_NA_BLOGU = 9

# Adresy sú overené proti živému obchodu, nie odhadnuté. Dve sa od
# predpokladu líšia: články sú na /blog/ (nie /nase-spravy/) a kontakt
# na /kontakty/ (nie /kontakt/).
# Stĺpec Produkty má podľa návrhu to isté, čo dlaždice na domovskej,
# plus panely na mieru. Adresy sú overené proti živému obchodu —
# kempovanie aj strešné stany už existujú, zatiaľ bez tovaru.
PRODUKTY = [
    ("Solárne panely na kapotu a strešné stany", "/panely-na-kapotu/"),
    ("Flexibilné solárne panely",                "/flexibilne-panely/"),
    ("Strešné stany a markízy",                  "/stresne-stany-a-markizy/"),
    ("Kempovanie a outdoor",                     "/kempovanie-a-outdoor-vybavenie/"),
    ("Panely na mieru",                          "/na-mieru/"),
]

SERVIS = [
    ("Doprava a platba", "/doprava-a-platba/"),
    ("Montáž",           "/montaz/"),
    ("Blog",             "/blog/"),
    ("FAQ",              "/faq/"),
]

VELKOOBCHOD = [
    ("Informácie",  "/velkoobchod/"),
    ("Registrácia", "/registracia/"),
]

SLOVA = {
    "sk": {
        "kategorie": {"hood": "Panely na kapotu",
                      "flexible": "Flexibilné panely",
                      "rooftent": "Pre strešné stany",
                      "foldable": "Skladacie panely",
                      "blanket": "Solárne deky",
                      "rv": "Karavany a prívesy",
                      "tonneau": "Na kryty korby"},
        "produkty": ["Solárne panely na kapotu a strešné stany",
                     "Flexibilné solárne panely", "Strešné stany a markízy",
                     "Kempovanie a outdoor", "Panely na mieru"],
        "servis": ["Doprava a platba", "Montáž", "Blog", "FAQ"],
        "velkoobchod": ["Informácie", "Registrácia"],
        "pravne": ["Obchodné podmienky", "Reklamácie",
                   "Ochrana osobných údajov", "Cookies",
                   "Identifikácia prevádzkovateľa"],
        "perex": "Solárne riešenia, kempingové a outdoor vybavenie pre "
                 "cestovateľov, dobrodruhov aj profesionálov.",
        "istoty": ["Faktúru s QR kódom pošleme e-mailom po objednaní.",
                   "Tovar odošleme po úhrade.",
                   "Montáž bez vŕtania, návod ku každému produktu."],
        "h_produkty": "Produkty", "h_servis": "Zákaznícky servis",
        "h_velkoobchod": "Veľkoobchod", "kontakt": "Kontakt",
        "b2b": "Veľkoobchod (B2B)",
        "bez_vrtania": "Bez vŕtania", "na_mieru": "Na mieru",
        "katalog": "Katalóg", "vsetko": "Všetko", "s_dph": "s DPH",
        "pd_b2b": "Ste predajca alebo montážny servis? ",
        "ucet": "Môj účet", "odhlasit": "Odhlásiť sa",
        "cela_recenzia": "Zobraziť celú recenziu", "skryt": "Skryť",
    },
    "cs": {
        "kategorie": {"hood": "Panely na kapotu",
                      "flexible": "Flexibilní panely",
                      "rooftent": "Pro střešní stany",
                      "foldable": "Skládací panely",
                      "blanket": "Solární deky",
                      "rv": "Karavany a přívěsy",
                      "tonneau": "Na kryty korby"},
        "produkty": ["Solární panely na kapotu a střešní stany",
                     "Flexibilní solární panely", "Střešní stany a markýzy",
                     "Kempování a outdoor", "Panely na míru"],
        "servis": ["Doprava a platba", "Montáž", "Blog", "FAQ"],
        "velkoobchod": ["Informace", "Registrace"],
        "pravne": ["Obchodní podmínky", "Reklamace",
                   "Ochrana osobních údajů", "Cookies",
                   "Identifikace provozovatele"],
        "perex": "Solární řešení, kempingové a outdoor vybavení pro "
                 "cestovatele, dobrodruhy i profesionály.",
        "istoty": ["Fakturu s QR kódem pošleme e-mailem po objednání.",
                   "Zboží odešleme po úhradě.",
                   "Montáž bez vrtání, návod ke každému produktu."],
        "h_produkty": "Produkty", "h_servis": "Zákaznický servis",
        "h_velkoobchod": "Velkoobchod", "kontakt": "Kontakt",
        "b2b": "Velkoobchod (B2B)",
        "bez_vrtania": "Bez vrtání", "na_mieru": "Na míru",
        "katalog": "Katalog", "vsetko": "Vše", "s_dph": "s DPH",
        "pd_b2b": "Jste prodejce nebo montážní servis? ",
        "ucet": "Můj účet", "odhlasit": "Odhlásit se",
        "cela_recenzia": "Zobrazit celou recenzi", "skryt": "Skrýt",
    },
}


PREDPONY = {"sk": "", "cs": "/cs"}


def sl():
    return jazyk.t(SLOVA)


PEREX = ("Solárne riešenia, kempingové a outdoor vybavenie pre "
         "cestovateľov, dobrodruhov aj profesionálov.")

# Istoty pod tlačidlom na detaile produktu. Sú to naše skutočné
# podmienky, nie sľuby navyše — tie isté vety sú na domovskej aj
# v obchodných podmienkach.
ISTOTY = [
    "Faktúru s QR kódom pošleme e-mailom po objednaní.",
    "Tovar odošleme po úhrade.",
    "Montáž bez vŕtania, návod ku každému produktu.",
]

# Horná lišta. Vľavo dva sľuby o objednávke, vpravo jazyk a dva odkazy.
# Horná lišta má podľa klienta len jazyk, veľkoobchod a kontakt,
# zarovnané doprava. Sľuby o objednávke z nej odišli — tie isté vety
# sú v hero aj v istotách na detaile produktu.
SLUBY = []

# Spodný riadok pätičky. Prvý je z návrhu, ďalšie dva sem presúvame
# z horného menu, aby sa na ne dalo dostať aj po prerobení lišty.
# „Ako nakupovať“ tu bývalo tiež, ale tú stránku sme zrušili — jej
# obsah pokrývajú obchodné podmienky. Odkaz by viedol na 404.
# Cookies nemajú vlastnú stránku — Shoptet na ne otvára svoje okno
# cez triedu js-cookies-settings. /cookies/ je 404, overené.
PRAVNE = [
    ("Obchodné podmienky", "/obchodne-podmienky/"),
    ("Reklamácie", "/reklamacie/"),
    ("Ochrana osobných údajov", "/podmienky-ochrany-osobnych-udajov/"),
    ("Cookies", None),
    ("Identifikácia prevádzkovateľa", "/identifikacia-prevadzkovatela/"),
]


def e(x):
    return html.escape(str(x), quote=True)


def udaje_kariet():
    """Tabuľka adresa produktu -> kategória a štítky.

    Karta vo výpise nenesie ani kategóriu, ani parametre — má len
    názov, cenu, dostupnosť, kód, popis a fotku. Overené na značke
    stránky, slovo „param“ v nej nie je. Jediné, čím sa karta dá
    spoľahlivo priradiť k produktu, je adresa v odkaze; kód sa ukazuje
    tiež, ale len pre jedno prevedenie a dá sa v nastaveniach vypnúť.

    Tabuľka sa prepočítava pri každom behu z data/products.js, takže
    sa neudržiava ručne — rovnako ako vyhľadávanie vozidla.
    """
    zdroj = os.path.join(KOREN, "data", "products.js")
    s = open(zdroj, encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))

    kam = adresy_produktov(P)
    rozmery = foto_rozmery()
    t = {}
    for p in P:
        a = kam.get(p["id"])
        if not a:
            continue
        # Ukladáme kľúče, nie hotové texty — tabuľka je spoločná pre
        # obe mutácie a jazyk sa vyberá až v prehliadači.
        stitky = []
        if p.get("w"):
            stitky.append(f'{p["w"]} W')
        if p["cat"] in PRILEPENE:
            stitky.append("@bez_vrtania")
        if p.get("b"):
            stitky.append("@na_mieru")
        riadok = [p["cat"], stitky]
        # Tretia položka je priblíženie hlavnej fotky, a to len keď ho
        # fotka naozaj potrebuje. Číslo je presné: rám delený šírkou
        # zdroja presne pokryje bielu obrubu a nič neoreže.
        w = rozmery.get(p["id"])
        if w and w < RAM_DETAILU:
            riadok.append(round(RAM_DETAILU / w, 3))
        t[a] = riadok
    return t


def foto_rozmery():
    """Šírky hlavných fotiek, zmerané tools/foto_rozmery.py.

    Keď súbor chýba, priblíženie sa jednoducho nedoplní — fotky budú
    mať bielu obrubu ako doteraz, ale nič sa nerozbije.
    """
    cesta = os.path.join(KOREN, "data", "foto-rozmery.json")
    if not os.path.exists(cesta):
        print("   pozor: chýba data/foto-rozmery.json, fotky zostanú "
              "s bielou obrubou (spusti tools/foto_rozmery.py)")
        return {}
    return json.load(open(cesta, encoding="utf-8"))


def clanky(kod):
    """Najnovšie články pre stránku Blog.

    Obrázky článkov sedia v obchode pod adresou odvodenou od adresy
    článku, lebo tak sa volajú súbory, ktoré pripravuje
    tools/blog_doplnky.py. Keby ich niekto nahral pod iným názvom,
    karta sa vykreslí bez fotky — nerozbije sa.
    """
    from blog_content import POSTS, CAT
    I = 0 if kod == "sk" else 1
    zoz = sorted(POSTS, key=lambda p: p["date"], reverse=True)
    r = []
    for p in zoz[:CLANKOV_NA_BLOGU]:
        rub = RUBRIKY.get(p["cat"])
        if not rub:
            continue
        r.append([
            PREDPONY[kod] + f'/{rub}/{p["slug"]}/',
            p["title"][I],
            p["lead"][I],
            f'/user/articles/images/{p["slug"]}.jpg',
            CAT[p["cat"]][I],
        ])
    return r


def adresy_produktov(P):
    """Adresy produktov v obchode, z mapy stránok obchodu.

    Rovnaký zdroj ako pri vyhľadávaní vozidla a domovskej stránke —
    nie odhad, ako si Shoptet preloží názov do adresy. Keď produkt
    v mape nie je, kartu proste nedoplníme; spadnúť kvôli tomu by
    bolo prehnané, vzhľad zostane funkčný aj bez štítkov.
    """
    mapa = adresy()
    # Kľúč je bez predpony mutácie. Záhlavie a zápätie sú v Shoptete
    # spoločné pre všetky jazyky — overené na živom obchode, /cs/ aj /
    # ťahajú ten istý rnc-skript.js — takže tabuľka musí poslúžiť
    # obom. Skript si pri hľadaní predponu odreže.
    return {p["id"]: "/" + mapa[bez_diakritiky(p["n"]["sk"])] + "/"
            for p in P if bez_diakritiky(p["n"]["sk"]) in mapa}


def stlpec(nadpis, odkazy, nazvy):
    polozky = "".join(
        f'<li><a href="{e(jazyk.odkaz(u))}">{e(nz)}</a></li>'
        for (n, u), nz in zip(odkazy, nazvy))
    return (f'<div class="rnc-pata-st"><h3>{e(nadpis)}</h3>'
            f'<ul>{polozky}</ul></div>')


def prepinac_jazyka():
    """SK | CZ ako skutočné odkazy.

    Shoptet má vlastný prepínač s vlajkami v .languagesMenu; ten CSS
    skrýva, lebo návrh má na jeho mieste tieto dve skratky. Adresy sú
    jeho — mutáciu prepína cez action, nie cez cestu, takže si zapamätá,
    na ktorej stránke si bol.
    """
    akt = jazyk.aktualny()
    kusy = []
    for kod, popis in (("sk", "SK"), ("cs", "CZ")):
        if kod == akt:
            kusy.append(f"<strong>{popis}</strong>")
        else:
            kusy.append(
                f'<a href="/action/Language/changeLanguage/?language={kod}"'
                f' rel="nofollow">{popis}</a>')
    return ('<span class="rnc-top-jazyk">'
            + '<span class="rnc-top-jazyk-del">|</span>'.join(kusy)
            + "</span>")


def blok_oboch():
    """Horná lišta a pätička pre obe mutácie v jednom súbore.

    Shoptet má pole Zápätie spoločné pre celý obchod — overené na
    živom obchode, / aj /cs/ ťahajú ten istý rnc-skript.js. Vkladáme
    preto oba bloky a skript ten cudzí hneď zmaže.
    """
    kusy = []
    povodny = jazyk.aktualny()
    try:
        for kod in SLOVA:
            jazyk.nastav(kod)
            kusy.append(f'<div data-rnc-jazyk="{kod}">' + blok() + "</div>")
    finally:
        jazyk.nastav(povodny)
    return "\n".join(kusy)


def blok():
    # Oddeľovač je samostatný prvok, nie ::before vnútri odkazu —
    # tam by sa bodka stala súčasťou klikateľnej plochy.
    pravne = '<span class="rnc-pata-bod">·</span>'.join(
        f'<a href="{e(jazyk.odkaz(u))}">{e(nz)}</a>' if u
        else f'<a href="#" class="js-cookies-settings">{e(nz)}</a>'
        for (n, u), nz in zip(PRAVNE, sl()["pravne"]))
    sluby = "".join(f'<span>{e(x)}</span>' for x in SLUBY)
    return f'''<div id="rnc-top" class="rnc-top">
  <div class="rnc-top-sluby">{sluby}</div>
  <div class="rnc-top-odkazy">
    {prepinac_jazyka()}
    <a class="rnc-top-b2b" href="{jazyk.odkaz("/velkoobchod/")}">{e(sl()["b2b"])}</a>
    <a href="{jazyk.odkaz("/kontakty/")}">{e(sl()["kontakt"])}</a>
  </div>
</div>
<div id="rnc-pata" class="rnc-pata">
  <div class="container rnc-pata-in">
    <div class="rnc-pata-st rnc-pata-znacka">
      <h3>RNC EXPLORE</h3>
      <p>{e(sl()["perex"])}</p>
      <p class="rnc-pata-kontakt"><a href="{jazyk.odkaz("/kontakty/")}">{e(sl()["kontakt"])}</a></p>
    </div>
    {stlpec(sl()["h_produkty"], PRODUKTY, sl()["produkty"])}
    {stlpec(sl()["h_servis"], SERVIS, sl()["servis"])}
    {stlpec(sl()["h_velkoobchod"], VELKOOBCHOD, sl()["velkoobchod"])}
  </div>
  <div class="container rnc-pata-spodok">
    {pravne}
  </div>
</div>'''


def skript():
    """Telo rnc-skript.js.

    To isté, čo doteraz sedelo v Zápätí, plus doplnenie kariet. Do
    poľa sa to prestalo zmestať, keď k tomu pribudla tabuľka údajov.
    """
    # Záhlavie a zápätie sú v Shoptete spoločné pre všetky mutácie,
    # takže jazyk nevyberáme pri generovaní, ale až v prehliadači
    # podľa cesty. Do skriptu preto ide tabuľka oboch jazykov.
    def pre(kod):
        z = SLOVA[kod]
        return {
            "istoty": ('<ul class="rnc-istoty">'
                       + "".join(f"<li>{e(x)}</li>" for x in z["istoty"])
                       + "</ul>"),
            "katalog": z["katalog"], "vsetko": z["vsetko"],
            "s_dph": z["s_dph"], "pd_b2b": z["pd_b2b"], "b2b": z["b2b"],
            "ucet": z["ucet"], "odhlasit": z["odhlasit"],
            "cela_recenzia": z["cela_recenzia"], "skryt": z["skryt"],
            "bez_vrtania": z["bez_vrtania"], "na_mieru": z["na_mieru"],
            "kategorie": z["kategorie"],
            "b2b_odkaz": PREDPONY[kod] + "/velkoobchod/",
            "klient": PREDPONY[kod] + "/klient/",
            "odhlasenie": PREDPONY[kod] + "/logout/",
        }
    texty = json.dumps({k: pre(k) for k in SLOVA}, ensure_ascii=False,
                       separators=(",", ":"))
    udaje = json.dumps(udaje_kariet(), ensure_ascii=False,
                       separators=(",", ":"))
    posty = json.dumps({k: clanky(k) for k in SLOVA}, ensure_ascii=False,
                       separators=(",", ":"))
    return f'''
/* Zápätie sa vkladá pred </body>, teda až pod celou stránkou. Oba
   bloky preto presunieme tam, kam patria. Skript beží hneď, nie na
   DOMContentLoaded — oba ciele sú v stránke dávno pred ním. */
(function () {{
  /* Poistka proti dvojitému behu. Keby sa pole zápätia vykreslilo
     dvakrát, mali by sme na stránke dve pätičky a na detaile dva
     nadpisy — a nebolo by hneď jasné prečo. */
  if (document.documentElement.dataset.rncZapatie) {{ return; }}
  document.documentElement.dataset.rncZapatie = "1";

  /* Záhlavie a zápätie má Shoptet spoločné pre všetky mutácie, takže
     jazyk nevyberáme pri generovaní, ale tu — podľa cesty. */
  var JAZ = location.pathname.indexOf("/cs/") === 0 ? "cs" : "sk";
  var T = {texty}[JAZ];

  /* Z dvoch pripravených blokov necháme ten, ktorý patrí k jazyku. */
  var bloky = document.querySelectorAll("[data-rnc-jazyk]");
  for (var bi = 0; bi < bloky.length; bi++) {{
    if (bloky[bi].getAttribute("data-rnc-jazyk") !== JAZ) {{
      bloky[bi].parentNode.removeChild(bloky[bi]);
    }}
  }}

  var f = document.getElementById("footer"),
      p = document.getElementById("rnc-pata"),
      t = document.getElementById("rnc-top"),
      l = document.querySelector(".top-navigation-bar .container");
  if (f && p) {{ f.insertBefore(p, f.firstChild); }}
  if (l && t) {{ l.insertBefore(t, l.firstChild); }}

  /* Prihlásenie z hornej lišty medzi ikony v hlavičke. Tlačidlo
     presúvame, nerobíme nové — visí na ňom Shoptetov obsluhovač,
     ktorý otvára prihlasovacie okno. */
  var u = document.querySelector(".top-nav-button-login"),
      ik = document.querySelector("#header .navigation-buttons");
  if (u && ik) {{
    u.className += " rnc-ucet";
    ik.insertBefore(u, ik.firstChild);
  }}

  /* Menu sa pri posúvaní nadol skryje a pri posúvaní nahor vráti.
     Prah 120 px, nech sa hlavička nestráca hneď pri prvom pohybe;
     pri otvorenom mobilnom menu alebo hľadaní sa neskrýva vôbec. */
  (function () {{
    var kde = window.pageYOffset || 0, prah = 120, caka = false;
    function prepocitaj() {{
      caka = false;
      var n = window.pageYOffset || 0, b = document.body;
      if (b.classList.contains("navigation-window-visible")
          || b.classList.contains("search-window-visible")) {{
        b.classList.remove("rnc-skryte-menu");
      }} else if (n > prah && n > kde + 4) {{
        b.classList.add("rnc-skryte-menu");
      }} else if (n < kde - 4 || n <= prah) {{
        b.classList.remove("rnc-skryte-menu");
      }}
      kde = n;
    }}
    window.addEventListener("scroll", function () {{
      if (!caka) {{ caka = true; window.requestAnimationFrame(prepocitaj); }}
    }}, {{passive: true}});
  }})();

  /* Výpis kategórie. Návrh má nad nadpisom riadok so zaradením.
     Berieme ho z omrvinkovej navigácie — predposledná položka, teda
     nadradená kategória. Na nej samej by bol ten istý text ako
     v nadpise, čo nemá zmysel, tak ho vtedy vynechávame. */
  var n = document.querySelectorAll(".breadcrumbs a");
  var t = document.querySelector(".category-title");
  if (t && !t.previousElementSibling) {{
    /* Posledný odkaz v omrvinkách býva samotná kategória, teda to isté,
       čo je v nadpise. Berieme preto posledný, ktorý sa od nadpisu
       líši — nadradenú kategóriu. */
    var nadpis = t.textContent.trim(), r = "";
    for (var x = 0; x < n.length; x++) {{
      var v = n[x].textContent.trim();
      /* Domov preskakujeme. Na koreni katalógu je to jediný odkaz,
         ktorý sa od nadpisu líši, a nad nadpisom potom svietilo
         „Domov“ namiesto zaradenia. */
      if (v && v !== nadpis && n[x].getAttribute("href") !== "/") {{ r = v; }}
    }}
    if (!r) {{ r = T.katalog; }}
    if (r) {{
      var u = document.createElement("p");
      u.className = "rnc-eyebrow";
      u.textContent = r;
      t.parentNode.insertBefore(u, t);
    }}
  }}

  /* Typy panelov ako štítky nad výpisom. Návrh ich má nad všetkým,
     nie v bočnom stĺpci — vľavo zostávajú len filtre. Skladáme ich
     zo stromu kategórií, ktorý Shoptet aj tak vykresľuje, takže keď
     klient kategóriu pridá alebo premenuje, štítky idú s ním. */
  var strom = document.querySelector("#categories .categories");
  if (strom && t) {{
    var rad = document.createElement("div");
    rad.className = "rnc-typy";
    var cesta = location.pathname;

    function stitok(odkaz, text, aktivny) {{
      var a = document.createElement("a");
      a.href = odkaz;
      a.textContent = text;
      if (aktivny) {{ a.className = "aktivny"; }}
      rad.appendChild(a);
    }}

    var koren = strom.querySelector(".topic a");
    if (koren) {{
      stitok(koren.getAttribute("href"), T.vsetko,
             koren.getAttribute("href") === cesta);
    }}
    var polozky = strom.querySelectorAll(":scope > ul > li");
    for (var y = 0; y < polozky.length; y++) {{
      var o = polozky[y].querySelector("a");
      if (!o) {{ continue; }}
      /* Aktívny je aj vtedy, keď sme o úroveň nižšie — napríklad na
         značke Dacia pod Panelmi na kapotu. Netrafiť sa na triedu je
         ľahké: Shoptet dá „active“ až tej značke a nadradenej vetve
         len „expandable“. Preto hľadáme adresu medzi všetkými
         odkazmi v položke, nie v triedach. */
      var je = false, vn = polozky[y].querySelectorAll("a");
      for (var z = 0; z < vn.length; z++) {{
        if (vn[z].getAttribute("href") === cesta) {{ je = true; break; }}
      }}
      stitok(o.getAttribute("href"),
             o.textContent.replace(/\s+/g, " ").trim(), je);
    }}
    /* Horný popis kategórie vykresľuje Shoptet až za podkategóriami,
       teda pod štítky. V návrhu je veta nad nimi, tak sa vešiame za
       ňu, nie za nadpis. */
    var za = t.parentNode.querySelector(".category-perex") || t;
    if (rad.children.length > 1) {{ za.parentNode.insertBefore(rad, za.nextSibling); }}
  }}

  /* Detail produktu. Návrh má v pravom stĺpci najprv zaradenie,
     nadpis a štítok, až potom popis a cenu; Shoptet dáva nadpis nad
     oba stĺpce. Poradie zvyšku vyrieši CSS cez order, ale nadpis
     treba preniesť — cez stĺpce to CSS nevie. */
  var i = document.querySelector(".p-info-wrapper");
  if (!i) {{ return; }}

  var hlava = document.createElement("div");
  hlava.className = "rnc-pd-hlava";

  /* Zaradenie berieme z omrvinkovej navigácie, z prvej kategórie za
     Produktmi — teda „Panely na kapotu“, nie „Dacia“. Keby sa
     omrvinky zmenili, riadok proste nebude, nič sa nerozbije. */
  var k = document.querySelector("#navigation-2 a [itemprop=name]");
  if (k && k.textContent.trim()) {{
    var e = document.createElement("p");
    e.className = "rnc-eyebrow";
    e.textContent = k.textContent.trim();
    hlava.appendChild(e);
  }}
  var h = document.querySelector(".p-detail-inner-header h1");
  if (h) {{ hlava.appendChild(h); }}
  var d = document.querySelector(".p-detail-info");
  if (d) {{ hlava.appendChild(d); }}
  if (hlava.children.length) {{ i.insertBefore(hlava, i.firstChild); }}

  /* Cena je bez poznámky o dani. Dopĺňame ju do značky, nie cez CSS,
     nech sa dá označiť aj preložiť. */
  var c = i.querySelector(".price-final");
  if (c && !c.querySelector(".rnc-dph")) {{
    var s = document.createElement("span");
    s.className = "rnc-dph";
    s.textContent = T.s_dph;
    c.appendChild(s);
  }}

  var z = document.createElement("div");
  z.className = "rnc-pd-pata";
  z.innerHTML = T.istoty
    + '<p class="rnc-pd-b2b">' + T.pd_b2b
    + '<a href="' + T.b2b_odkaz + '">' + T.b2b + '</a></p>';
  i.appendChild(z);
}})();

/* Radenie ako rozbaľovací zoznam.

   Shoptet ho vykresľuje ako štyri tlačidlá vedľa seba; návrh má
   jeden zoznam s popisom „Zoradiť“. Tlačidlá nemažeme, len ich
   v CSS skryjeme — keby skript nezbehol, zostane funkčné radenie
   namiesto prázdneho miesta. */
(function () {{
  var r = document.querySelector(".listSorting");
  if (!r || r.querySelector(".rnc-zoradit")) {{ return; }}
  var t = r.querySelectorAll(".listSorting__control");
  if (t.length < 2) {{ return; }}

  var obal = document.createElement("label");
  obal.className = "rnc-zoradit";
  obal.appendChild(document.createTextNode("Zoradiť"));

  var v = document.createElement("select");
  for (var n = 0; n < t.length; n++) {{
    var o = document.createElement("option");
    o.value = t[n].getAttribute("data-url") || "";
    o.textContent = t[n].textContent.replace(/\s+/g, " ").trim();
    if (/--current/.test(t[n].className)) {{ o.selected = true; }}
    v.appendChild(o);
  }}
  v.addEventListener("change", function () {{
    if (this.value) {{ location.href = this.value; }}
  }});
  obal.appendChild(v);
  r.appendChild(obal);
  r.className += " rnc-ma-zoradit";
}})();

/* Najnovšie články na stránke Blog.

   Rubrika Blog vlastné články nemá — všetky sú v jej štyroch
   podrubrikách a Shoptet ich do nadradenej rubriky nepreberá, takže
   stránka hlásila „Záznamy neboli nájdené“. Vypisujeme ich teda sami,
   v tej istej podobe ako výpis rubriky. */
(function () {{
  var o = document.querySelector(".type-posts-listing .content-inner");
  if (!o || o.querySelector(".news-wrapper") || o.querySelector(".rnc-clanky")) {{ return; }}

  var C = {posty}[JAZ];
  if (!C.length) {{ return; }}

  var h = document.createElement("h2");
  h.className = "rnc-clanky-nadpis";
  h.textContent = "Najnovšie články";

  var r = document.createElement("div");
  r.className = "news-wrapper rnc-clanky";
  for (var n = 0; n < C.length; n++) {{
    var c = C[n];
    var k = document.createElement("div");
    k.className = "news-item";
    k.innerHTML =
      '<div class="image"><a href="' + c[0] + '"><img src="' + c[3]
        + '" alt="" loading="lazy"></a></div>'
      + '<div class="text">'
      + '<a class="title" href="' + c[0] + '"></a>'
      + '<p class="rnc-clanok-rubrika"></p>'
      + '<div class="description"><p></p></div>'
      + '</div>';
    /* Texty cez textContent, nie do innerHTML — názvy a perexy sú
       naše, ale aj tak sa to tak má robiť. */
    k.querySelector(".title").textContent = c[1];
    k.querySelector(".rnc-clanok-rubrika").textContent = c[4];
    k.querySelector(".description p").textContent = c[2];
    /* Keď fotka nie je nahraná, dlaždica by zostala prázdna a biela. */
    var i = k.querySelector("img");
    i.onerror = function () {{
      var d = this.closest(".image");
      if (d) {{ d.parentNode.removeChild(d); }}
    }};
    r.appendChild(k);
  }}
  o.appendChild(h);
  o.appendChild(r);
}})();

/* Varianty ako prepínače, nie rozbaľovací zoznam.

   Zoznam nemažeme a ani neobchádzame — prepínač len nastaví jeho
   hodnotu a vyvolá na ňom zmenu, takže všetko ostatné (cena,
   dostupnosť, odomknutie tlačidla do košíka) si ďalej rieši Shoptet
   svojím kódom. Keby sme to prepisovali sami, rozišlo by sa to s ním
   pri prvej zmene na ich strane. */
(function () {{
  var v = document.querySelector("#simple-variants-select");
  if (!v || document.querySelector(".rnc-varianty")) {{ return; }}

  var r = document.createElement("div");
  r.className = "rnc-varianty";

  /* Zoradené od najlacnejšieho. Shoptet ich dáva v poradí, v akom
     prišli z importu, čo zákazníkovi nič nehovorí. */
  var zoz = [];
  for (var q = 0; q < v.options.length; q++) {{
    if (v.options[q].value) {{ zoz.push(v.options[q]); }}
  }}
  zoz.sort(function (a, b) {{
    return (parseFloat(a.getAttribute("data-customerprice")) || 0)
         - (parseFloat(b.getAttribute("data-customerprice")) || 0);
  }});

  for (var n = 0; n < zoz.length; n++) {{
    var o = zoz[n];

    var t = o.textContent.replace(/\s+/g, " ").trim();
    var cena = "";
    /* Cena je v poslednej zátvorke s číslicou; názvy prevedení majú
       zátvorky tiež, preto odzadu. */
    var m = t.match(/\(([^()]*\d[^()]*)\)\s*$/);
    if (m) {{ cena = m[1]; t = t.slice(0, m.index); }}
    t = t.replace(/[-\u2013\u2014]\s*(Momentálne nedostupné|Momentálně nedostupné)\s*$/i, "");
    t = t.replace(/^(Prevedenie|Provedení):\s*/i, "").replace(/[\s\u00b7-]+$/, "").trim();

    var l = document.createElement("label");
    l.className = "rnc-variant";
    var i = document.createElement("input");
    i.type = "radio";
    i.name = "rnc-variant";
    i.value = o.value;
    if (n === 0) {{ i.checked = true; }}   /* predvolený je najlacnejší */
    l.appendChild(i);
    var b = document.createElement("b");
    b.textContent = t;
    l.appendChild(b);
    if (cena) {{
      var c = document.createElement("span");
      c.className = "rnc-variant-cena";
      c.textContent = cena;
      l.appendChild(c);
    }}
    r.appendChild(l);
  }}
  if (!r.children.length) {{ return; }}

  r.addEventListener("change", function (e) {{
    if (!e.target.value) {{ return; }}
    v.value = e.target.value;
    v.dispatchEvent(new Event("change", {{bubbles: true}}));
  }});
  v.parentNode.insertBefore(r, v);
  v.parentNode.className += " rnc-ma-varianty";

  /* Predvolenú voľbu musí dostať aj pôvodný zoznam, inak by na nej
     stál prepínač, ale cena a tlačidlo do košíka by čakali na výber. */
  if (zoz.length) {{
    v.value = zoz[0].value;
    v.dispatchEvent(new Event("change", {{bubbles: true}}));
  }}
}})();

/* Karty vo výpise: kategória pod názvom a štítky pod ňou.

   Shoptet do výpisu posiela len názov, cenu, dostupnosť, kód, popis
   a fotku — žiadne kategórie ani parametre, hoci ich v databáze má.
   Údaje preto nesieme so sebou a kartu k produktu priraďujeme podľa
   adresy v odkaze. Tabuľku prepočítava tools/shoptet_zapatie.py pri
   každom behu z data/products.js, needituje sa ručne. */
(function () {{
  var U = {udaje};

  function dopln() {{
  var karty = document.querySelectorAll(".products-block .p");
  for (var n = 0; n < karty.length; n++) {{
    var k = karty[n], o = k.querySelector("a.name") || k.querySelector("a.image");
    if (!o) {{ continue; }}
    var u = U[(o.getAttribute("href") || "").replace(/^\/cs/, "")];
    if (!u || k.querySelector(".rnc-karta-kat")) {{ continue; }}

    var meno = k.querySelector("a.name");
    if (!meno) {{ continue; }}
    var po = meno;

    if (u[0] && T.kategorie[u[0]]) {{
      var kat = document.createElement("p");
      kat.className = "rnc-karta-kat";
      kat.textContent = T.kategorie[u[0]] || "";
      po.parentNode.insertBefore(kat, po.nextSibling);
      po = kat;
    }}
    if (u[1] && u[1].length) {{
      var r = document.createElement("div");
      r.className = "rnc-karta-stitky";
      for (var m = 0; m < u[1].length; m++) {{
        var x = document.createElement("span");
        var st = u[1][m];
        x.textContent = st.charAt(0) === "@" ? T[st.slice(1)] : st;
        r.appendChild(x);
      }}
      po.parentNode.insertBefore(r, po.nextSibling);
    }}
  }}
  }}

  dopln();
  /* Po filtrovaní Shoptet výpis prekreslí a naše doplnky by zmizli.
     Sledujeme preto obal výpisu a dopĺňame znova; poistka proti
     opakovaniu je v samotnej funkcii, pozerá sa, či karta doplnok
     už nemá. */
  /* Hlavná fotka na detaile. Shoptet ju vykresľuje do rámu 1024 px
     a menšie nezväčšuje, len doplní bielou — obruba je preto pri
     každom produkte iná. Priblíženie je presne rám delený šírkou
     zdroja, takže bielu pokryje a z fotky neodreže nič. */
  var d = U[location.pathname.replace(/^\/cs/, "")];
  if (d && d[2]) {{
    var f = document.querySelector(".p-main-image img");
    if (f) {{
      f.style.transform = "scale(" + d[2] + ")";
      var o = f.closest(".p-image");
      if (o) {{ o.style.overflow = "hidden"; }}
    }}
  }}

  /* Odhlásenie do hornej lišty. Shoptet ho má len v okne pod ikonou
     účtu a v bočnom menu zákazníka — teda tam, kde ho zákazník
     nehľadá. Prihlásenie poznáme podľa toho, že na stránke vôbec je
     odkaz na odhlásenie; pri neprihlásenom tam nie je žiadny. */
  var odhl = document.querySelector('[data-testid="headerSignout"]');
  var top = document.querySelector("#rnc-top .rnc-top-odkazy");
  if (odhl && top && !top.querySelector(".rnc-top-odhlasit")) {{
    var ucet = document.createElement("a");
    ucet.className = "rnc-top-ucet";
    ucet.href = T.klient;
    ucet.textContent = T.ucet;
    var von = document.createElement("a");
    von.className = "rnc-top-odhlasit";
    von.href = odhl.getAttribute("href") || T.odhlasenie;
    von.setAttribute("rel", "nofollow");
    von.textContent = T.odhlasit;
    top.appendChild(ucet);
    top.appendChild(von);
  }}

  /* Recenzie na domovskej: dva riadky a zvyšok na rozkliknutie.
     Orez zapíname až odtiaľto, nie priamo v CSS — keby skript
     nedobehol, zostal by text natrvalo useknutý bez tlačidla, ktorým
     sa dá rozbaliť. Tlačidlo dávame len tam, kde sa text naozaj
     nezmestil; pri krátkej recenzii by inak nerobilo nič. */
  document.querySelectorAll(".rnc-rev").forEach(function (k) {{
    var t = k.querySelector("blockquote");
    if (!t || k.querySelector(".rnc-rev-viac")) {{ return; }}
    k.classList.add("rnc-rev-orez");
    if (t.scrollHeight <= t.clientHeight + 1) {{
      k.classList.remove("rnc-rev-orez");
      return;
    }}
    var b = document.createElement("button");
    b.type = "button";
    b.className = "rnc-rev-viac";
    b.textContent = T.cela_recenzia;
    b.addEventListener("click", function () {{
      var cele = k.classList.toggle("rnc-rev-cele");
      b.textContent = cele ? T.skryt : T.cela_recenzia;
    }});
    k.appendChild(b);
  }});

  var obal = document.querySelector(".products-block");
  if (obal && window.MutationObserver) {{
    new MutationObserver(dopln).observe(obal.parentNode || obal,
                                        {{childList: true, subtree: true}});
  }}
}})();
'''


def main():
    jazyk.z_argumentov()
    js = skript().strip() + "\n"
    cesta_js = vystup.kam(vystup.IMPORT, "vzhlad", SUBOR)
    with open(cesta_js, "w", encoding="utf-8") as f:
        f.write(js)
    odtlacok = hashlib.sha1(js.encode("utf-8")).hexdigest()[:8]

    kod = (
        "<!-- rncexplore.com — horná lišta a pätička podľa návrhu.\n"
        "\n"
        f"     1. {SUBOR} nahraj do Vzhľad a obsah → Správca súborov\n"
        "     2. toto vlož do Vzhľad a obsah → Editor → HTML kód → Zápätie\n"
        "\n"
        "     Zdroj je tools/shoptet_zapatie.py v repozitári. Needituj tu\n"
        "     ani v nahranom súbore — uprav zdroj a spusti ten skript. -->\n"
        + blok_oboch().strip() + "\n"
        f'<script src="{CESTA}/{SUBOR}?v={odtlacok}"></script>\n')

    cesta_z = vystup.kam(vystup.IMPORT, "vzhlad", "do-zapatia.html")
    with open(cesta_z, "w", encoding="utf-8") as f:
        f.write(kod)

    print("1. nahrať do Správcu súborov")
    print(f"   {cesta_js}")
    print(f"   {len(js):>6} znakov · {len(udaje_kariet())} produktov v tabuľke")
    print("2. vložiť do Vzhľad a obsah → Editor → HTML kód → Zápätie")
    print(f"   {cesta_z}")
    znakov = len(kod)
    print(f"   {znakov:>6} znakov · strop {STROP} · "
          + (f"zmestí sa, zostáva {STROP - znakov}" if znakov <= STROP
             else "PRESAHUJE, treba skrátiť"))
    print(f"   odkazov: {len(PRODUKTY) + len(SERVIS) + len(VELKOOBCHOD) + len(PRAVNE) + 1}")
    if znakov > STROP:
        sys.exit(1)


if __name__ == "__main__":
    main()

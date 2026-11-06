# -*- coding: utf-8 -*-
"""Vyhľadávanie panela podľa vozidla — značka, model, rok.

Shoptet takú vec nemá a dáta na ňu v katalógu nie sú ako údaje, sú
schované v názve produktu: „Dacia Duster 1. generácia (2010–2017) –
100W solárny panel na kapotu“. Tento skript ich odtiaľ vytiahne a
postaví z nich hotový prvok — zoznam, trochu JavaScriptu a nič viac.
Beží v prehliadači, nepotrebuje server ani žiadny doplnok Shoptetu.

Tri rozhodnutia, ktoré stoja za vysvetlenie:

  * Modely sa zlučujú do rodín. Katalóg pozná „Land Cruiser 70 Series
    GRJ78“, ale zákazník vie, že má Land Cruiser. Preto sa v rozbaľovači
    ponúka rodina a presné označenie je až pri výsledku. Bez toho by mala
    Toyota v zozname dvadsaťšesť položiek.

  * Produkt bez rokov v názve sa nezahadzuje, ale ani nemieša medzi tie,
    ktoré rok naozaj sedia. Tridsaťjeden panelov rozsah neuvádza — pri
    Land Cruiseri je to trinásť z osemnástich — a keby sa zobrazovali ako
    rovnocenné, filter podľa roku by stratil zmysel. Sú preto pod
    výsledkami, oddelene a s vysvetlením. Až keď sa roky doplnia do
    katalógu, tá druhá skupina zmizne sama.

  * Adresy produktov sa neodvodzujú, berú sa z mapy stránok obchodu.
    Shoptet si ich tvorí sám a odhadovať ich by znamenalo odkazy, ktoré
    raz prestanú fungovať.

Spustenie:  python3 tools/shoptet_vyhladavanie.py
"""
import gzip
import html
import json
import os
import re
import sys
import unicodedata
import urllib.request

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo
import jazyk
import vystup

OBCHOD = "https://822969.myshoptet.com"
TERAZ = 2026          # čím sa nahrádza „súčasnosť“ v rozsahu rokov

# Model, ako ho pozná zákazník. Vľavo je to, čím sa označenie z katalógu
# začína, vpravo rodina do rozbaľovača. Poradie rozhoduje — konkrétnejšie
# musí byť vyššie, inak „Range Rover Sport“ spadne pod „Range Rover“.
RODINY = [
    (r"^Land Cruiser Prado|^Prado", "Land Cruiser Prado"),
    (r"^Land Cruiser",              "Land Cruiser"),
    (r"^Hilux",                     "Hilux"),
    (r"^RAV4",                      "RAV4"),
    (r"^Range Rover Sport",         "Range Rover Sport"),
    (r"^Range Rover|^Ranger Rover", "Range Rover"),
    (r"^Discovery Sport",           "Discovery Sport"),
    (r"^Discovery",                 "Discovery"),
    (r"^Defender",                  "Defender"),
    (r"^Freelander",                "Freelander"),
    (r"^Patrol",                    "Patrol"),
    (r"^Pathfinder",                "Pathfinder"),
    (r"^Navara",                    "Navara"),
    (r"^X-Trail",                   "X-Trail"),
    (r"^Ranger",                    "Ranger"),
    (r"^Transit Custom",            "Transit Custom"),
    (r"^Transit Connect",           "Transit Connect"),
    (r"^Transit",                   "Transit"),
    (r"^Amarok",                    "Amarok"),
    (r"^Caddy",                     "Caddy"),
    (r"^Crafter",                   "Crafter"),
    (r"^Grand California",          "Grand California"),
    (r"^T4$|^T5|^T6",               "Transporter T4–T6"),
    (r"^Tiguan",                    "Tiguan"),
    (r"^Sprinter",                  "Sprinter"),
    (r"^Vito",                      "Vito"),
    (r"^G-Wagen|^G-Class",          "G-Class"),
    (r"^X-Class",                   "X-Class"),
    (r"^D-Max",                     "D-Max"),
    (r"^Duster",                    "Duster"),
    (r"^Wrangler",                  "Wrangler"),
    (r"^Jimny",                     "Jimny"),
    (r"^Ducato",                    "Ducato"),
    (r"^Cayenne",                   "Cayenne"),
    (r"^Grenadier",                 "Grenadier"),
]
GENERACIA = re.compile(r"\s*\d+\.\s*gener[áa]cia\b", re.I)


def bez_diakritiky(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", t.lower())


def adresy():
    """Adresy produktov z mapy stránok obchodu, kľúčované názvom.

    Česká mutácia beží v podadresári, takže jej adresy majú o jeden
    segment viac. Shoptet si navyše názov prevádza na adresu v každej
    mutácii zvlášť — české adresy teda nevzniknú predponovaním
    slovenských a treba ich brať z mapy stránok tak, ako sú."""
    url = OBCHOD + "/sitemaps/sitemap0.xml.gz"
    with urllib.request.urlopen(url, timeout=30) as r:
        xml = gzip.decompress(r.read()).decode("utf-8")
    cesty = [x.replace(OBCHOD + "/", "").strip("/")
             for x in re.findall(r"<loc>([^<]+)</loc>", xml)]
    predpona = jazyk.odkaz("/").strip("/")      # "" alebo "cs"
    if not predpona:
        return {bez_diakritiky(c): c for c in cesty if "/" not in c}
    zac = predpona + "/"
    return {bez_diakritiky(c[len(zac):]): c
            for c in cesty if c.startswith(zac) and c.count("/") == 1}


def rozbor(p):
    """Zo (značky a) názvu vytiahne rodinu, presné označenie a roky."""
    vozidlo = p["n"]["sk"].split(" – ")[0].strip()
    r = re.search(r"\((\d{4})\s*[–-]\s*(\d{4}|súčasnosť)\)", vozidlo)
    od = int(r.group(1)) if r else None
    do = (TERAZ if r.group(2) == "súčasnosť" else int(r.group(2))) if r else None

    t = re.sub(r"\([^)]*\)", "", vozidlo).strip()
    if t.lower().startswith(p["b"].lower()):
        t = t[len(p["b"]):].strip()
    t = re.sub(r"\s{2,}", " ", GENERACIA.sub("", t).strip(" -–,"))
    for vzor, rodina in RODINY:
        if re.search(vzor, t, re.I):
            return rodina, t, od, do
    return t, t, od, do


def main():
    jazyk.z_argumentov()
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))

    mapa = adresy()
    j = jazyk.aktualny()
    chyba = [p["n"][j] for p in P if bez_diakritiky(p["n"][j]) not in mapa]
    if chyba:
        sys.exit("v mape stránok obchodu nie sú tieto produkty:\n  "
                 + "\n  ".join(chyba[:10]))

    polozky, rokov = [], []
    for p in P:
        if not p.get("b"):
            continue
        rodina, presne, od, do = rozbor(p)
        polozky.append({
            "b": p["b"], "m": rodina, "p": presne,
            "od": od, "do": do,
            "n": p["n"][j],
            "w": p["w"],
            "c": round(min(seo.price(v["p"], "EUR") for v in p["var"]), 2),
            "i": (p.get("img") or [""])[0],
            "u": "/" + mapa[bez_diakritiky(p["n"][j])] + "/",
        })
        if od:
            rokov += [od, do]

    data = json.dumps(polozky, ensure_ascii=False, separators=(",", ":"))
    najstarsi = min(rokov)
    h = prelož(SABLONA).replace("__DATA__", data) \
               .replace("__OD__", str(najstarsi)) \
               .replace("__DO__", str(TERAZ))

    ciel = vystup.kam(vystup.IMPORT, jazyk.priecinok("vzhlad"),
                      "vyhladavanie-vozidla.html")
    with open(ciel, "w", encoding="utf-8") as f:
        f.write(h)

    # To isté ako samostatná stránka. V menu má byť položka „Podľa
    # vozidla“ a tá musí niekam viesť — domovská na to nestačí, lebo
    # vyhľadávanie je na nej až pod hero. Stránka sa vkladá cez
    # Vzhľad a obsah → Stránky, preto ide do iného priečinka než
    # vzhľad a bez hlavičkového komentára pre úvodnú stránku.
    uvod = "<p>" + jazyk.t(SLOVA)["uvod"] + "</p>\n"
    bez = re.sub(r"^<!--.*?-->\s*", "", h, flags=re.S)
    cesta = vystup.kam(vystup.VLOZIT, jazyk.priecinok("stranky"),
                       "podla-vozidla.html")
    with open(cesta, "w", encoding="utf-8") as f:
        f.write(uvod + bez)
    print(f"{len(uvod) + len(bez):>6} znakov -> {cesta}")

    znacky = sorted({x["b"] for x in polozky})
    print(f"{len(h):>6} znakov -> {ciel}")
    print(f"  vozidiel: {len(polozky)} · značiek: {len(znacky)} · "
          f"roky {najstarsi}–{TERAZ}")
    print(f"  bez rokov v názve: {sum(1 for x in polozky if not x['od'])} "
          f"(zobrazia sa pri každom roku)")


SLOVA = {
    "sk": {
        "nadpis": "Nájdi produkt pre svoje vozidlo",
        "znacka": "Značka", "model": "Model", "rok": "Rok výroby",
        "najprv_znacku": "Najskôr vyber značku",
        "najprv_model": "Najskôr vyber model",
        "tlacidlo": "Zobraziť kompatibilné produkty",
        "s_dph": "s DPH", "od": "od",
        "jeden": " panel", "par": " panely", "viac": " panelov",
        "pre_rok": " pre rok ", "pre_model": " pre tento model",
        "nic": "Pre toto vozidlo zatiaľ panel nemáme. ",
        "nic_rok_a": "Pre rok ", "nic_rok_b": " nemáme panel s overeným rozsahom. ",
        "na_mieru": "Vyrobíme ho na mieru →",
        "dalsie": "Ďalšie panely pre tento model. Pri týchto neuvádzame "
                  "roky výroby, tak overte rozmer alebo nám napíšte.",
        "uvod": "Vyberte značku, model a rok výroby. Zobrazíme panely, "
                "ktoré sú tvarované presne na vaše vozidlo — a pod nimi "
                "aj tie, pri ktorých výrobca roky neuvádza.",
    },
    "cs": {
        "nadpis": "Najdi produkt pro své vozidlo",
        "znacka": "Značka", "model": "Model", "rok": "Rok výroby",
        "najprv_znacku": "Nejprve vyber značku",
        "najprv_model": "Nejprve vyber model",
        "tlacidlo": "Zobrazit kompatibilní produkty",
        "s_dph": "s DPH", "od": "od",
        "jeden": " panel", "par": " panely", "viac": " panelů",
        "pre_rok": " pro rok ", "pre_model": " pro tento model",
        "nic": "Pro toto vozidlo zatím panel nemáme. ",
        "nic_rok_a": "Pro rok ", "nic_rok_b": " nemáme panel s ověřeným rozsahem. ",
        "na_mieru": "Vyrobíme ho na míru →",
        "dalsie": "Další panely pro tento model. U těchto neuvádíme "
                  "roky výroby, tak ověřte rozměr nebo nám napište.",
        "uvod": "Vyberte značku, model a rok výroby. Zobrazíme panely, "
                "které jsou tvarované přesně na vaše vozidlo — a pod nimi "
                "i ty, u kterých výrobce roky neuvádí.",
    },
}


def prelož(sablona):
    """Doplní do šablóny texty v aktuálnom jazyku a predponu mutácie.
    Tokeny sú @@kluc@@, nie formátovacie zátvorky — v šablóne je
    JavaScript a ten je zátvoriek plný."""
    v = jazyk.t(SLOVA)
    out = sablona
    for k, text in v.items():
        out = out.replace(f"@@{k}@@", text)
    return out.replace("@@na-mieru@@", jazyk.odkaz("/na-mieru/"))


SABLONA = '''<!-- Vyhľadávanie panela podľa vozidla.
     Vyrába tools/shoptet_vyhladavanie.py — needituj tu, uprav zdroj.
     Patrí do úvodnej stránky, na miesto pásu so značkami. -->
<section class="rnc-finder" id="rnc-finder">

    <div class="rnc-find-karta">
      <div class="rnc-find-nadpis">
        <strong>@@nadpis@@</strong>
      </div>
      <select id="rnc-b" aria-label="@@znacka@@"><option value="">@@znacka@@</option></select>
      <select id="rnc-m" aria-label="@@model@@" disabled><option value="">@@najprv_znacku@@</option></select>
      <select id="rnc-r" aria-label="@@rok@@" disabled><option value="">@@najprv_model@@</option></select>
      <a class="rnc-btn" href="#rnc-vysledok" id="rnc-go">@@tlacidlo@@</a>
    </div>

    <div id="rnc-vysledok" class="rnc-find-out" aria-live="polite"></div>
</section>

<script>
(function () {
  "use strict";
  var V = __DATA__, OD = __OD__, DO = __DO__;
  var zb = document.getElementById("rnc-b"),
      zm = document.getElementById("rnc-m"),
      zr = document.getElementById("rnc-r"),
      out = document.getElementById("rnc-vysledok");
  if (!zb) return;

  function naplň(sel, zoznam, prvy) {
    sel.innerHTML = "";
    sel.appendChild(new Option(prvy, ""));
    zoznam.forEach(function (x) { sel.appendChild(new Option(x, x)); });
    sel.disabled = !zoznam.length;
  }
  function jedinečné(pole) {
    return pole.filter(function (x, i, a) { return a.indexOf(x) === i; }).sort();
  }
  function cena(x) {
    return x.toFixed(2).replace(".", ",") + " €";
  }
  function poč(n) {
    return n + (n === 1 ? "@@jeden@@" : (n < 5 ? "@@par@@" : "@@viac@@"));
  }
  function mriežka(zoznam) {
    return '<div class="rnc-prods">' + zoznam.map(function (x) {
      return '<a class="rnc-prod" href="' + x.u + '">' +
        '<span class="rnc-prod-img" style="background-image:url(\\'' + x.i + '\\')"></span>' +
        '<span class="rnc-prod-hlava">' + x.n + '</span>' +
        '<span class="rnc-prod-cena">@@od@@ <strong>' + cena(x.c) + '</strong> <span>@@s_dph@@</span></span>' +
        '</a>';
    }).join("") + "</div>";
  }

  naplň(zb, jedinečné(V.map(function (x) { return x.b; })), "@@znacka@@");

  zb.addEventListener("change", function () {
    var b = zb.value;
    naplň(zm, b ? jedinečné(V.filter(function (x) { return x.b === b; })
                             .map(function (x) { return x.m; })) : [],
          b ? "@@model@@" : "@@najprv_znacku@@");
    naplň(zr, [], "@@najprv_model@@");
    ukáž();
  });

  zm.addEventListener("change", function () {
    /* Ponúkame len roky, ktoré model naozaj pokrýva. Zoznam od 1967 po
       2026 pri každom modeli je síce jednoduchší na výrobu, ale núti
       zákazníka hľadať svoj rok medzi šesťdesiatimi položkami, z ktorých
       väčšina nikdy nič nenájde. */
    var roky = [], m = zm.value;
    if (m) {
      var p = V.filter(function (x) { return x.b === zb.value && x.m === m && x.od; });
      var a = p.length ? Math.min.apply(null, p.map(function (x) { return x.od; })) : OD;
      var b = p.length ? Math.max.apply(null, p.map(function (x) { return x.do; })) : DO;
      for (var r = b; r >= a; r--) roky.push(String(r));
    }
    naplň(zr, roky, m ? "@@rok@@" : "@@najprv_model@@");
    zr.disabled = !m;
    ukáž();
  });

  zr.addEventListener("change", ukáž);

  /* Výsledky sa prepočítavajú hneď pri výbere, tlačidlo z návrhu teda nič
     nespúšťa — len posunie stránku k nim. Keby niekto klikol skôr, než si
     vybral, pripomenie mu to. */
  var go = document.getElementById("rnc-go");
  if (go) go.addEventListener("click", function (ev) {
    if (!zb.value || !zm.value) { ev.preventDefault(); zb.focus(); }
  });

  function ukáž() {
    var b = zb.value, m = zm.value, r = zr.value ? +zr.value : null;
    if (!b || !m) { out.innerHTML = ""; return; }

    var pre = V.filter(function (x) { return x.b === b && x.m === m; });
    var sedia = [], mozno = [];
    pre.forEach(function (x) {
      if (!r) { sedia.push(x); return; }             /* rok nevybraný */
      if (!x.od) { mozno.push(x); return; }          /* rok neuvádzame */
      if (r >= x.od && r <= x.do) sedia.push(x);
    });

    if (!sedia.length && !mozno.length) {
      out.innerHTML = '<p class="rnc-find-nic">@@nic@@' +
        '<a href="@@na-mieru@@">@@na_mieru@@</a></p>';
      return;
    }

    var h = "";
    if (sedia.length) {
      h += '<p class="rnc-find-pocet">' + poč(sedia.length) +
           (r ? "@@pre_rok@@" + r : "@@pre_model@@") + "</p>" + mriežka(sedia);
    } else {
      h += '<p class="rnc-find-nic">@@nic_rok_a@@' + r + '@@nic_rok_b@@' +
           '<a href="@@na-mieru@@">@@na_mieru@@</a></p>';
    }
    if (mozno.length) {
      h += '<p class="rnc-find-dalsie">@@dalsie@@</p>' + mriežka(mozno);
    }
    out.innerHTML = h;
  }
})();
</script>
'''

if __name__ == "__main__":
    main()

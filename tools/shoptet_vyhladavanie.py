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
    """Adresy produktov z mapy stránok obchodu, kľúčované názvom."""
    url = OBCHOD + "/sitemaps/sitemap0.xml.gz"
    with urllib.request.urlopen(url, timeout=30) as r:
        xml = gzip.decompress(r.read()).decode("utf-8")
    cesty = [x.replace(OBCHOD + "/", "").strip("/")
             for x in re.findall(r"<loc>([^<]+)</loc>", xml)]
    return {bez_diakritiky(c): c for c in cesty if "/" not in c}


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
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))

    mapa = adresy()
    chyba = [p["n"]["sk"] for p in P if bez_diakritiky(p["n"]["sk"]) not in mapa]
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
            "n": p["n"]["sk"],
            "w": p["w"],
            "c": round(min(seo.price(v["p"], "EUR") for v in p["var"]), 2),
            "i": (p.get("img") or [""])[0],
            "u": "/" + mapa[bez_diakritiky(p["n"]["sk"])] + "/",
        })
        if od:
            rokov += [od, do]

    data = json.dumps(polozky, ensure_ascii=False, separators=(",", ":"))
    najstarsi = min(rokov)
    h = SABLONA.replace("__DATA__", data) \
               .replace("__OD__", str(najstarsi)) \
               .replace("__DO__", str(TERAZ))

    ciel = vystup.kam(vystup.IMPORT, "vzhlad", "vyhladavanie-vozidla.html")
    with open(ciel, "w", encoding="utf-8") as f:
        f.write(h)

    znacky = sorted({x["b"] for x in polozky})
    print(f"{len(h):>6} znakov -> {ciel}")
    print(f"  vozidiel: {len(polozky)} · značiek: {len(znacky)} · "
          f"roky {najstarsi}–{TERAZ}")
    print(f"  bez rokov v názve: {sum(1 for x in polozky if not x['od'])} "
          f"(zobrazia sa pri každom roku)")


SABLONA = '''<!-- Vyhľadávanie panela podľa vozidla.
     Vyrába tools/shoptet_vyhladavanie.py — needituj tu, uprav zdroj.
     Patrí do úvodnej stránky, na miesto pásu so značkami. -->
<section class="rnc-finder" id="rnc-finder">
  <div class="rnc-wrap">

    <div class="rnc-find-karta">
      <div class="rnc-find-nadpis">
        <strong>Nájdi panel pre svoje vozidlo</strong>
        <span>Vyber značku, model a rok a zobrazíme ti kompatibilné produkty.</span>
      </div>
      <label>Značka
        <select id="rnc-b"><option value="">Vyberte značku</option></select>
      </label>
      <label>Model
        <select id="rnc-m" disabled><option value="">Najprv značku</option></select>
      </label>
      <label>Rok výroby
        <select id="rnc-r" disabled><option value="">Najprv model</option></select>
      </label>
      <a class="rnc-btn" href="#rnc-vysledok" id="rnc-go">Zobraziť kompatibilné produkty →</a>
    </div>

    <div class="rnc-find-pod">
      <p class="rnc-find-rec">Z recenzií zákazníkov: Dacia Duster 3 ·
         Toyota Land Cruiser 100 · Jeep</p>
      <p class="rnc-find-mieru"><a href="/na-mieru/">Nenašli ste vozidlo?
         Panel na mieru</a></p>
    </div>

    <ul class="rnc-find-istoty">
      <li>Slovensko a Česko (SK / CZ)</li>
      <li>Faktúra s QR kódom e-mailom</li>
      <li>Odoslanie po úhrade</li>
      <li>Montáž a poradenstvo</li>
    </ul>

    <div id="rnc-vysledok" class="rnc-find-out" aria-live="polite"></div>
  </div>
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
    return n + (n === 1 ? " panel" : (n < 5 ? " panely" : " panelov"));
  }
  function mriežka(zoznam) {
    return '<div class="rnc-prods">' + zoznam.map(function (x) {
      return '<a class="rnc-prod" href="' + x.u + '">' +
        '<span class="rnc-prod-img" style="background-image:url(\\'' + x.i + '\\')"></span>' +
        '<h3>' + x.n + '</h3>' +
        '<p class="rnc-prod-cena">od <strong>' + cena(x.c) + '</strong> <span>s DPH</span></p>' +
        '</a>';
    }).join("") + "</div>";
  }

  naplň(zb, jedinečné(V.map(function (x) { return x.b; })), "Vyberte značku");

  zb.addEventListener("change", function () {
    var b = zb.value;
    naplň(zm, b ? jedinečné(V.filter(function (x) { return x.b === b; })
                             .map(function (x) { return x.m; })) : [],
          b ? "Vyberte model" : "Najprv značku");
    naplň(zr, [], "Najprv model");
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
    naplň(zr, roky, m ? "Vyberte rok" : "Najprv model");
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
      out.innerHTML = '<p class="rnc-find-nic">Pre toto vozidlo zatiaľ panel ' +
        'nemáme. <a href="/na-mieru/">Vyrobíme ho na mieru →</a></p>';
      return;
    }

    var h = "";
    if (sedia.length) {
      h += '<p class="rnc-find-pocet">' + poč(sedia.length) +
           (r ? " pre rok " + r : " pre tento model") + "</p>" + mriežka(sedia);
    } else {
      h += '<p class="rnc-find-nic">Pre rok ' + r + ' nemáme panel s overeným ' +
           'rozsahom. <a href="/na-mieru/">Vyrobíme ho na mieru →</a></p>';
    }
    if (mozno.length) {
      h += '<p class="rnc-find-dalsie">Ďalšie panely pre tento model. Pri ' +
           'týchto neuvádzame roky výroby, tak overte rozmer alebo nám ' +
           'napíšte.</p>' + mriežka(mozno);
    }
    out.innerHTML = h;
  }
})();
</script>
'''

if __name__ == "__main__":
    main()

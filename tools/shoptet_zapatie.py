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

Výstup: do-zapatia.html — jeden blok na vloženie do Zápätia.
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

# Istoty pod tlačidlom na detaile produktu. Sú to naše skutočné
# podmienky, nie sľuby navyše — tie isté vety sú na domovskej aj
# v obchodných podmienkach.
ISTOTY = [
    "Faktúru s QR kódom pošleme e-mailom po objednaní.",
    "Tovar odošleme po úhrade.",
    "Montáž bez vŕtania, návod ku každému produktu.",
]

# Horná lišta. Vľavo dva sľuby o objednávke, vpravo jazyk a dva odkazy.
SLUBY = ["Faktúra s QR kódom e-mailom", "Odoslanie po úhrade"]

# Spodný riadok pätičky. Prvý je z návrhu, ďalšie dva sem presúvame
# z horného menu, aby sa na ne dalo dostať aj po prerobení lišty.
PRAVNE = [
    ("Obchodné podmienky", "/obchodne-podmienky/"),
    ("Ako nakupovať", "/ako-nakupovat/"),
    ("Ochrana osobných údajov", "/podmienky-ochrany-osobnych-udajov/"),
]


def e(x):
    return html.escape(str(x), quote=True)


def stlpec(nadpis, odkazy):
    polozky = "".join(f'<li><a href="{e(u)}">{e(n)}</a></li>'
                      for n, u in odkazy)
    return (f'<div class="rnc-pata-st"><h3>{e(nadpis)}</h3>'
            f'<ul>{polozky}</ul></div>')


def blok():
    istoty = ('<ul class="rnc-istoty">'
              + "".join(f"<li>{e(x)}</li>" for x in ISTOTY) + "</ul>")
    pravne = "".join(f'<a href="{e(u)}">{e(n)}</a>' for n, u in PRAVNE)
    sluby = "".join(f'<span>{e(x)}</span>' for x in SLUBY)
    return f'''<div id="rnc-top" class="rnc-top">
  <div class="rnc-top-sluby">{sluby}</div>
  <div class="rnc-top-odkazy">
    <span class="rnc-top-jazyk"><strong>SK</strong><span>|</span>CZ</span>
    <a class="rnc-top-b2b" href="/velkoobchod/">Veľkoobchod (B2B)</a>
    <a href="/kontakty/">Kontakt</a>
  </div>
</div>
<div id="rnc-pata" class="rnc-pata">
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
    {pravne}
  </div>
</div>
<script>
/* Zápätie sa vkladá pred </body>, teda až pod celou stránkou. Oba
   bloky preto presunieme tam, kam patria. Skript beží hneď, nie na
   DOMContentLoaded — oba ciele sú v stránke dávno pred ním. */
(function () {{
  /* Poistka proti dvojitému behu. Keby sa pole zápätia vykreslilo
     dvakrát, mali by sme na stránke dve pätičky a na detaile dva
     nadpisy — a nebolo by hneď jasné prečo. */
  if (document.documentElement.dataset.rncZapatie) {{ return; }}
  document.documentElement.dataset.rncZapatie = "1";

  var f = document.getElementById("footer"),
      p = document.getElementById("rnc-pata"),
      t = document.getElementById("rnc-top"),
      l = document.querySelector(".top-navigation-bar .container");
  if (f && p) {{ f.insertBefore(p, f.firstChild); }}
  if (l && t) {{ l.insertBefore(t, l.firstChild); }}

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
      if (v && v !== nadpis) {{ r = v; }}
    }}
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
      stitok(koren.getAttribute("href"), "Všetko",
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
    if (rad.children.length > 1) {{ t.parentNode.insertBefore(rad, t.nextSibling); }}
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
    s.textContent = "s DPH";
    c.appendChild(s);
  }}

  var z = document.createElement("div");
  z.className = "rnc-pd-pata";
  z.innerHTML = {istoty!r}
    + '<p class="rnc-pd-b2b">Ste predajca alebo montážny servis? '
    + '<a href="/velkoobchod/">Veľkoobchod (B2B)</a></p>';
  i.appendChild(z);
}})();
</script>'''


def main():
    kod = blok()
    cesta = vystup.kam(vystup.IMPORT, "vzhlad", "do-zapatia.html")
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

#!/usr/bin/env python3
"""Stránky, ktoré existujú len v Shoptete.

Doprava a platba, Reklamácie a Identifikácia prevádzkovateľa na starom
webe neboli — vznikli až z pripomienok k pätičke. Nejdú preto cez
export_stranky.py, ktorý prerába obsah statickej stránky; píšu sa tu.

Obsah nie je vymyslený: firemné údaje sú z config.js a reklamačná časť
hovorí to isté, čo oddiel 10 obchodných podmienok, len zrozumiteľne.

Ceny dopravy sú NÁVRH. Vychádzajú z cenovej ponuky DPD pre Safiri zo
7. 10. 2026, lenže tá je bez DPH a bez palivového, mýtneho a
bezpečnostného príplatku, ktoré sa menia mesačne. Preto je k nim
pripočítaná DPH a rezerva — a musia sedieť s tým, čo je nastavené
v Shoptete, inak bude stránka klamať.

Čo sa nedá odvodiť, je v texte označené ako [DOPLNIŤ: …] a skript to
na konci vypíše. Bez doplnenia sa stránka vkladať nemá.

Spustenie:  python3 tools/stranky_shoptet.py
"""

import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup                                           # noqa: E402

# Pásma DPD: hmotnosť, cena bez DPH z ponuky, navrhnutá cena s DPH.
# Rezerva nad DPH kryje palivový, mýtny a bezpečnostný príplatok.
DPD = [("do 1 kg", "2,80", "4,20"), ("do 3 kg", "3,00", "4,50"),
       ("do 6 kg", "3,10", "4,60"), ("do 10 kg", "3,35", "4,90"),
       ("do 20 kg", "5,50", "7,90"), ("do 31,5 kg", "7,95", "11,50")]
DOBIERKA = "1,00"
STROP = "31,5 kg"

LEHOTA_SKLADOM = "[DOPLNIŤ: koľko pracovných dní, keď je tovar skladom]"
LEHOTA_OBJEDNAVKA = "[DOPLNIŤ: koľko dní, keď sa tovar objednáva od výrobcu]"
REKLAMACNA_ADRESA = "[DOPLNIŤ: adresa, kam sa posiela reklamovaný tovar]"


def firma():
    """Údaje firmy z config.js — jeden zdroj pre web aj pre Shoptet."""
    s = open(os.path.join(KOREN, "config.js"), encoding="utf-8").read()
    u = {}
    for k in ("company", "street", "city", "ico", "dic", "icDph",
              "orderEmail", "infoEmail", "phone", "hours"):
        m = re.search(rf'{k}\s*:\s*"([^"]*)"', s)
        if not m:
            sys.exit(f"v config.js chýba {k}")
        u[k] = m.group(1)
    return u


def doprava(f):
    riadky = "".join(
        f"<tr><td>{p}</td><td>{s}&nbsp;€</td></tr>" for p, _, s in DPD)
    return f"""<h2>Ako tovar doručujeme</h2>
<p>Zásielky posielame kuriérom DPD po celom Slovensku. Cena sa počíta
podľa hmotnosti zabaleného balíka.</p>
<table><thead><tr><th>Hmotnosť</th><th>Cena s DPH</th></tr></thead>
<tbody>{riadky}</tbody></table>
<p>Zásielky nad {STROP} kuriér neprepravuje. Pri takom tovare sa
ozveme a dohodneme individuálnu prepravu alebo osobný odber.</p>

<h2>Kedy tovar odošleme</h2>
<p>Tovar odosielame <strong>po pripísaní platby</strong> na účet, pri
dobierke hneď po potvrdení objednávky.</p>
<ul>
  <li>Tovar skladom: {LEHOTA_SKLADOM}</li>
  <li>Tovar na objednávku: {LEHOTA_OBJEDNAVKA}</li>
</ul>
<p>O odoslaní vás upozorníme e-mailom spolu s číslom zásielky, ktoré si
môžete sledovať na stránke dopravcu.</p>

<h2>Ako sa dá platiť</h2>
<h3>Prevodom na účet</h3>
<p>Po objednaní vám pošleme e-mailom faktúru s QR kódom. Stačí ho
naskenovať v mobilnej aplikácii banky a platba sa vyplní sama —
nemusíte nič prepisovať.</p>
<h3>Dobierkou</h3>
<p>Zaplatíte kuriérovi pri prevzatí. K cene dopravy sa pripočíta
{DOBIERKA}&nbsp;€.</p>

<h2>Ceny a DPH</h2>
<p>Všetky ceny v obchode aj v tejto tabuľke sú <strong>s DPH</strong>.
{f["company"]} je platiteľom DPH, IČ DPH {f["icDph"]}.</p>
<p>Podrobnosti o dodaní a platbe upravujú oddiely 8 a 9
<a href="/obchodne-podmienky/">obchodných podmienok</a>.</p>"""


def reklamacie(f):
    return f"""<h2>Na čo máte nárok</h2>
<p>Na tovar sa vzťahuje záruka <strong>24 mesiacov</strong> od
prevzatia. Záruka sa nevzťahuje na opotrebenie bežným používaním ani na
poškodenie spôsobené nesprávnou montážou alebo zásahom do výrobku.</p>

<h2>Ako reklamáciu uplatniť</h2>
<ol>
  <li>Napíšte nám na <a href="mailto:{f["infoEmail"]}">{f["infoEmail"]}</a>
      alebo zavolajte na {f["phone"]}. Uveďte číslo objednávky a čo sa
      stalo; fotografia závady nám prácu veľmi uľahčí.</li>
  <li>Ozveme sa vám a dohodneme ďalší postup. Niektoré veci sa dajú
      vyriešiť na diaľku a tovar nikam posielať netreba.</li>
  <li>Ak je potrebné tovar zaslať, pošlite ho na adresu
      {REKLAMACNA_ADRESA}. Priložte doklad o kúpe a popis závady.</li>
</ol>
<p>Tovar neposielajte na dobierku — takú zásielku nemôžeme prevziať.</p>

<h2>Dokedy to vybavíme</h2>
<p>Prijatie reklamácie potvrdíme bez zbytočného odkladu. Reklamáciu
vybavíme <strong>najneskôr do 30 dní</strong> od jej uplatnenia a
o výsledku vás budeme informovať.</p>

<h2>Odstúpenie od zmluvy</h2>
<p>Ak ste spotrebiteľ, môžete od zmluvy odstúpiť <strong>do 14 dní</strong>
od prevzatia tovaru aj bez udania dôvodu. Postup a podmienky nájdete
v oddiele 6 <a href="/obchodne-podmienky/">obchodných podmienok</a>.</p>

<h2>Keď sa nedohodneme</h2>
<p>Ak nie ste s vybavením reklamácie spokojní, máte právo obrátiť sa na
nás so žiadosťou o nápravu. Ak ju zamietneme alebo na ňu neodpovieme do
30 dní, môžete podať návrh na alternatívne riešenie sporu — orgánom
dozoru je Slovenská obchodná inšpekcia.</p>"""


def identifikacia(f):
    return f"""<h2>Prevádzkovateľ internetového obchodu</h2>
<table><tbody>
<tr><th>Obchodné meno</th><td>{f["company"]}</td></tr>
<tr><th>Sídlo</th><td>{f["street"]}, {f["city"]}</td></tr>
<tr><th>IČO</th><td>{f["ico"]}</td></tr>
<tr><th>DIČ</th><td>{f["dic"]}</td></tr>
<tr><th>IČ DPH</th><td>{f["icDph"]}</td></tr>
<tr><th>Zápis</th><td>Obchodný register Okresného súdu Žilina,
    oddiel Sro, vložka č. 84177/L</td></tr>
</tbody></table>

<h2>Kontakt</h2>
<table><tbody>
<tr><th>Objednávky</th><td><a href="mailto:{f["orderEmail"]}">{f["orderEmail"]}</a></td></tr>
<tr><th>Otázky a poradenstvo</th><td><a href="mailto:{f["infoEmail"]}">{f["infoEmail"]}</a></td></tr>
<tr><th>Telefón</th><td>{f["phone"]}</td></tr>
<tr><th>Dostupnosť</th><td>pracovné dni {f["hours"]}</td></tr>
</tbody></table>

<h2>Orgán dozoru</h2>
<p>Slovenská obchodná inšpekcia, Inšpektorát SOI pre Žilinský kraj,
Predmestská 71, 011 79 Žilina.</p>
<p>Podmienky predaja upravujú
<a href="/obchodne-podmienky/">obchodné podmienky</a>, nakladanie
s údajmi <a href="/podmienky-ochrany-osobnych-udajov/">ochrana osobných
údajov</a>.</p>"""


STRANKY = [
    ("doprava-a-platba", "Doprava a platba", doprava),
    ("reklamacie", "Reklamácie", reklamacie),
    ("identifikacia-prevadzkovatela", "Identifikácia prevádzkovateľa",
     identifikacia),
]


def main():
    f = firma()
    priecinok = vystup.kam(vystup.VLOZIT, "stranky")
    chyba = []
    for adresa, nazov, tvor in STRANKY:
        t = tvor(f)
        cesta = os.path.join(priecinok, f"{adresa}.html")
        with open(cesta, "w", encoding="utf-8") as s:
            s.write(t.strip() + "\n")
        n = re.findall(r"\[DOPLNIŤ:[^\]]*\]", t)
        chyba += [(nazov, x) for x in n]
        print(f"   {adresa + '.html':<36} {nazov}"
              + (f"   · {len(n)} miest na doplnenie" if n else ""))

    print(f"\n{priecinok}")
    print("vkladať cez Vzhľad a obsah → Stránky → Pridať stránku,"
          " obsah cez Nástroje → Zdrojový kód")
    if chyba:
        print("\nPOZOR, bez tohto stránky nevkladaj:")
        for nazov, x in chyba:
            print(f"   {nazov:<34} {x}")


if __name__ == "__main__":
    main()

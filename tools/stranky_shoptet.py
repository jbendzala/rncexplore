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

# Odberné miesta Pickup majú v ponuke vlastný, lacnejší cenník, ale
# končia na 20 kg. Pri 20 kg je nákup rovnaký ako pri kuriérovi (5,50),
# takže tam výhoda mizne — to nie je chyba prepočtu, tak to DPD má.
PICKUP = [("do 1 kg", "2,10", "3,20"), ("do 3 kg", "2,20", "3,40"),
          ("do 6 kg", "2,45", "3,70"), ("do 10 kg", "2,90", "4,30"),
          ("do 20 kg", "5,50", "7,90")]
PICKUP_STROP = "20 kg"
PICKUP_DOBIERKA = "1 000 €"

# Osobný odber je u partnera, nie v sídle firmy — adresa aj hodiny sú
# teda jeho a treba ich držať podľa neho, nie podľa config.js.
ODBER = {
    "miesto": "Auto123",
    "ulica": "Hlinická cesta 1319",
    "mesto": "014 01 Bytča",
    "hodiny": [("Pondelok – piatok", "8:00 – 18:00"),
               ("Sobota", "8:00 – 15:00"),
               ("Nedeľa", "zatvorené")],
}

LEHOTA_SKLADOM = "do 2 pracovných dní"
# Lensun je zatiaľ jediný dodávateľ v katalógu. Keď pribudnú ďalší,
# pridá sa im sem vlastný riadok s ich lehotou.
LEHOTA_OBJEDNAVKA = "do 10 pracovných dní"


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


def tabulka(pasma):
    riadky = "".join(
        f"<tr><td>{p}</td><td>{s}&nbsp;€</td></tr>" for p, _, s in pasma)
    return ("<table><thead><tr><th>Hmotnosť</th><th>Cena s DPH</th></tr>"
            f"</thead><tbody>{riadky}</tbody></table>")


def doprava(f):
    hodiny = "".join(f"<tr><td>{d}</td><td>{h}</td></tr>"
                     for d, h in ODBER["hodiny"])
    o = ODBER
    return f"""<h2>Ako si tovar prevezmete</h2>
<p>Na výber sú tri spôsoby. Cena dopravy sa pri všetkých počíta podľa
hmotnosti zabaleného balíka.</p>

<h3>Kuriérom DPD</h3>
<p>Doručenie na adresu po celom Slovensku, zvyčajne nasledujúci pracovný
deň po odoslaní. Pred doručením vám príde SMS alebo e-mail a čas
doručenia si môžete zmeniť.</p>
{tabulka(DPD)}
<p>Zásielky nad {STROP} kuriér neprepravuje. Pri takom tovare sa
ozveme a dohodneme individuálnu prepravu alebo osobný odber.</p>

<h3>Na odberné miesto DPD Pickup</h3>
<p>Zásielku si vyzdvihnete na ktoromkoľvek výdajnom mieste DPD v čase,
ktorý vám vyhovuje — nemusíte čakať na kuriéra. Je to aj lacnejšie.</p>
{tabulka(PICKUP)}
<p>Na odberné miesto sa dajú poslať zásielky do {PICKUP_STROP}.
Ťažší tovar, teda väčšina panelov s rámom, chodí kuriérom.
Dobierka na odbernom mieste je možná do {PICKUP_DOBIERKA}.</p>

<h3>Osobný odber v Bytči</h3>
<p>Tovar si môžete vyzdvihnúť osobne, <strong>zadarmo</strong>, na
adrese:</p>
<p><strong>{o["miesto"]}</strong><br>
{o["ulica"]}<br>
{o["mesto"]}</p>
<table><thead><tr><th>Deň</th><th>Otvorené</th></tr></thead>
<tbody>{hodiny}</tbody></table>
<p>Ozveme sa vám hneď, ako bude tovar na mieste pripravený. Príďte až
potom — bez nášho e-mailu alebo SMS tam zásielka ešte nemusí byť.</p>

<h2>Kedy tovar odošleme</h2>
<p>Tovar odosielame <strong>po pripísaní platby</strong> na účet, pri
dobierke hneď po potvrdení objednávky.</p>
<ul>
  <li>Tovar skladom: <strong>{LEHOTA_SKLADOM}</strong></li>
  <li>Tovar na objednávku: <strong>{LEHOTA_OBJEDNAVKA}</strong></li>
</ul>
<p>Pri každom produkte je napísané, či je skladom. Keď skladom nie je,
objednávame ho u výrobcu a platí druhá lehota.</p>
<p>O odoslaní vás upozorníme e-mailom spolu s číslom zásielky, ktoré si
môžete sledovať na stránke dopravcu.</p>

<h2>Ako sa dá platiť</h2>
<h3>Prevodom na účet</h3>
<p>Po objednaní vám pošleme e-mailom faktúru s QR kódom. Stačí ho
naskenovať v mobilnej aplikácii banky a platba sa vyplní sama —
nemusíte nič prepisovať.</p>
<h3>Dobierkou</h3>
<p>Zaplatíte pri prevzatí — kuriérovi alebo na odbernom mieste. K cene
dopravy sa pripočíta {DOBIERKA}&nbsp;€.</p>
<h3>Pri osobnom odbere</h3>
<p>Pri osobnom odbere platíte vopred prevodom. Tovar vám na mieste
odovzdáme až po pripísaní platby.</p>

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
  <li>Ak je potrebné tovar zaslať, pošlite ho na adresu sídla:
      <strong>{f["company"]}, {f["street"]}, {f["city"]}</strong>.
      Priložte doklad o kúpe a popis závady.</li>
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

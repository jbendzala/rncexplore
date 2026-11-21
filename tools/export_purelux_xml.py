# -*- coding: utf-8 -*-
"""Vypíše obsah katalógu Purelux do XML vo formáte, aký Shoptet sám exportuje.

Rovnaký dvojkrokový vzor ako pri Lensune (tools/export_shoptet_xml.py):
CSV (tools/export_purelux.py) založí produkty/ceny/prevedenia, toto doplní
popisy, fotky, zaradenie do kategórií a hmotnosť — a produkty znova
nezakladá, páruje ich podľa toho istého kódu.

Rozdiely oproti Lensunu, a prečo nejde o jeden spoločný skript:

- Cena sa neposiela vôbec (rovnaký dôvod ako pri Lensune — je v obchode
  správna, prepisovať ju by bolo riskantné), ale aj tak je tento súbor
  nezávislý od tools/seo.py, lebo Purelux nemá vozidlovú os, výrobcu ani
  recenzie, ktoré by zdieľal s Lensunom.
- Hmotnosť berieme z KAŽDEJ varianty zvlášť (v["kg"]), nie z produktu
  (p["kg"]) ako pri Lensune. Pri paneloch sa varianty líšia o pár gramov
  (regulátor, fólia) a spoločná hmotnosť na produkte stačila; pri Purelux
  sa tá istá karta predáva v baleniach od 1 do 8 kusov a hmotnosť sa líši
  o desiatky kíl — baliť všetky varianty na váhu toho najľahšieho by bolo
  vyslovene zlé pre dopravcu.
- Žiadna tabuľka technických parametrov zatiaľ — list „Technické údaje“ z
  klientovho xlsx má parametre viazané na konkrétne varianty (nie každá
  hodnota platí pre celý produkt) a to chce vlastné spracovanie. Prvá
  verzia ide bez nej, text popisu a obsah balenia stačia na spustenie.

POZOR — argument "cs" už nepoužívaj na český obsah. Tento súbor zakladá
kategórie priamo cez <CATEGORIES>, a Shoptet pri behu s iným jazykom
vytvoril úplne novú, samostatnú kategóriu "LED osvětlení" namiesto
toho, aby len doplnil český názov tej istej "LED osvetlenie" — zdvojilo
to kategórie a prepísalo defaultCategory aj meno produktu naprieč
celým katalógom (zistené priamo v exporte, opravené zmazaním duplicitnej
kategórie). Jazyk JAZYK="cs" tu zostáva len kvôli zdieľaným funkciám
(kratky_popis/popis/seo_popis), ktoré používa tools/purelux_preloz_jazyky.py
— ten vyplní český text správnou cestou (Produkty → Export → Jazyky),
bez toho, aby sa čohokoľvek dotkol na úrovni kategórií.
"""
import html
import json
import os
import re
import subprocess
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup
from export_purelux import kod as shoptet_kod_base

VYROBCA = "Purelux"
PARAMETER = "Variant"

# Jazyk exportu — "sk" alebo "cs", nastavuje sa prvým argumentom, rovnaký
# vzor ako v export_shoptet_xml.py. Dáta nesú "sk" aj "cs" pri každom
# texte (p["n"]["sk"/"cs"], v["sk"/"cs"], položky p["pack"] sú teraz
# {"sk":..., "cs":...} namiesto obyčajného reťazca).
JAZYK = "sk"

KOREN_KATEGORIE = {"sk": "LED osvetlenie", "cs": "LED osvětlení"}

NAZVY = {
    "sk": {
        "led-rampy": "LED rampy",
        "led-privesvetla": "Prídavné svetlá",
        "led-pracovne": "Pracovné svetlá",
        "led-vystrazne": "Výstražné svetlá",
        "led-hmlovky": "Hmlové a polohové svetlá",
        "ziarovky": "Žiarovky",
        "elektroinstalacia": "Elektroinštalácia a relé",
        "montaz-prislusenstvo": "Montáž a príslušenstvo",
    },
    "cs": {
        "led-rampy": "LED rampy",
        "led-privesvetla": "Přídavná světla",
        "led-pracovne": "Pracovní světla",
        "led-vystrazne": "Výstražná světla",
        "led-hmlovky": "Mlhová a polohová světla",
        "ziarovky": "Žárovky",
        "elektroinstalacia": "Elektroinstalace a relé",
        "montaz-prislusenstvo": "Montáž a příslušenství",
    },
}

SLOVA = {
    "sk": {"balenie": "Obsah balenia (základná varianta)"},
    "cs": {"balenie": "Obsah balení (základní varianta)"},
}


def e(x):
    return html.escape(str(x), quote=True)


def shoptet_kod(p, v):
    """Rovnaká úprava, akú Shoptet sám spraví s kódom pri CSV importe —
    veľké písmená, + a * na pomlčku (viď export_shoptet_xml.py)."""
    k = shoptet_kod_base(p, v).upper()
    for znak in "+*":
        k = k.replace(znak, "-")
    return k


def prvá_veta(txt):
    txt = (txt or "").strip()
    m = re.search(r"(?<!\d)[.!?](?=\s+[A-ZÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ])", txt)
    return txt[:m.end()].strip() if m else txt


def seo_popis(txt):
    txt = txt or ""
    if len(txt) <= 155:
        return txt
    kus = txt[:155]
    return kus[:kus.rfind(" ")].rstrip(" ,;–-") + "…"


def kratky_popis(p):
    return f"<p>{e(prvá_veta(p['d'][JAZYK]))}</p>"


def rozbal(nadpis, telo_html):
    return f"<details><summary>{e(nadpis)}</summary>{telo_html}</details>"


def popis(p):
    c = [f"<p>{e(p['d'][JAZYK])}</p>"]
    if p.get("pack"):
        polozky = "".join(f"<li>{e(riadok[JAZYK])}</li>" for riadok in p["pack"])
        c.append(rozbal(SLOVA[JAZYK]["balenie"], f"<ul>{polozky}</ul>"))
    return "".join(c)


def cesty(kategoria):
    """Vlastný strom, nie pod „Produkty" (Lensun) — klient chcel Purelux
    ako samostatnú vetvu v navigácii, nie podkategóriu panelov."""
    koren = KOREN_KATEGORIE[JAZYK]
    hlavna = f"{koren} > {kategoria}"
    return [koren, hlavna], hlavna


def prevedenie(p, v, odsadenie, s_parametrom):
    r, o = [], " " * odsadenie
    r.append(f"{o}<CODE>{e(shoptet_kod(p, v))}</CODE>")
    r.append(f"{o}<UNIT>ks</UNIT>")
    if v.get("kg"):
        r.append(f"{o}<LOGISTIC><WEIGHT>{v['kg']}</WEIGHT></LOGISTIC>")
    if s_parametrom:
        r.append(f"{o}<PARAMETERS><PARAMETER>")
        r.append(f"{o}  <NAME>{e(PARAMETER)}</NAME>")
        r.append(f"{o}  <VALUE>{e(v[JAZYK])}</VALUE>")
        r.append(f"{o}</PARAMETER></PARAMETERS>")
    return r


def shopitem(p):
    viac = len(p["var"]) > 1
    r = ["  <SHOPITEM>"]
    r.append(f"    <NAME>{e(p['n'][JAZYK])}</NAME>")
    r.append(f"    <SHORT_DESCRIPTION>{e(kratky_popis(p))}</SHORT_DESCRIPTION>")
    r.append(f"    <DESCRIPTION>{e(popis(p))}</DESCRIPTION>")
    r.append(f"    <MANUFACTURER>{e(VYROBCA)}</MANUFACTURER>")
    r.append(f"    <SEO_TITLE>{e(p['n'][JAZYK] + ' | RnC Explore')}</SEO_TITLE>")
    r.append(f"    <META_DESCRIPTION>{e(seo_popis(p['d'][JAZYK]))}</META_DESCRIPTION>")

    zoznam, hlavna = cesty(NAZVY[JAZYK][p["cat"]])
    r.append("    <CATEGORIES>")
    r += [f"      <CATEGORY>{e(k)}</CATEGORY>" for k in zoznam]
    r.append(f"      <DEFAULT_CATEGORY>{e(hlavna)}</DEFAULT_CATEGORY>")
    r.append("    </CATEGORIES>")

    obrazky = p.get("img") or []
    if obrazky:
        r.append("    <IMAGES>")
        r += [f"      <IMAGE>{e(u)}</IMAGE>" for u in obrazky]
        r.append("    </IMAGES>")

    if viac:
        r.append("    <VARIANTS>")
        for v in p["var"]:
            r.append("      <VARIANT>")
            r += prevedenie(p, v, 8, True)
            r.append("      </VARIANT>")
        r.append("    </VARIANTS>")
    else:
        r += prevedenie(p, p["var"][0], 4, False)

    r.append("  </SHOPITEM>")
    return r


SCHEMA = os.path.join(TU, "shoptet-schema", "products-complete-v10.rng")


def over(cesta):
    try:
        v = subprocess.run(["xmllint", "--noout", "--relaxng", SCHEMA, cesta],
                           capture_output=True, text=True)
    except FileNotFoundError:
        return "xmllint nie je k dispozícii, neoverené"
    if v.returncode == 0:
        return "schéma v poriadku"
    chyby = [r for r in v.stderr.splitlines() if "validity error" in r]
    for r in chyby[:5]:
        print("   " + r.strip())
    return f"NEPREJDE — {len(chyby)} chýb"


def zapis(cesta, produkty):
    r = ['<?xml version="1.0" encoding="UTF-8"?>', "<SHOP>"]
    for p in produkty:
        r += shopitem(p)
    r.append("</SHOP>")
    with open(cesta, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(r) + "\n")


DAVKA = 40


def main():
    global JAZYK
    if len(sys.argv) > 1:
        if sys.argv[1] not in NAZVY:
            sys.exit(f"neznámy jazyk {sys.argv[1]!r}; poznám sk, cs")
        JAZYK = sys.argv[1]
    priecinok = "purelux-obsah-xml" if JAZYK == "sk" else f"purelux-obsah-xml-{JAZYK}"

    s = open(os.path.join(KOREN, "data", "products-purelux.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PURELUX_PRODUCTS=(\[.*\]);", s, re.S).group(1))

    ciel = vystup.kam(vystup.IMPORT, priecinok, "obsah.xml")
    zapis(ciel, P)
    fotiek = sum(len(p.get("img") or []) for p in P)
    prevedeni = sum(len(p["var"]) for p in P)
    print(f"jazyk: {JAZYK}")
    print(f"{len(P)} produktov, {prevedeni} prevedení, {fotiek} fotografií -> {ciel}")
    print(f"   {over(ciel)}")

    skuska = max(P, key=lambda p: (len(p["var"]), len(p.get("img") or [])))
    c = vystup.kam(vystup.IMPORT, priecinok, "skuska-jeden-produkt.xml")
    zapis(c, [skuska])
    print(f"\nna skúšku jeden produkt ({skuska['n'][JAZYK]}, "
          f"{len(skuska['var'])} variant) -> {c}\n   {over(c)}")

    davky = [P[i:i + DAVKA] for i in range(0, len(P), DAVKA)]
    print(f"\npo dávkach (najviac {DAVKA} produktov na súbor):")
    for i, cast in enumerate(davky, 1):
        c = vystup.kam(vystup.IMPORT, priecinok,
                       f"davka-{i}-z-{len(davky)}.xml")
        zapis(c, cast)
        print(f"  {os.path.basename(c):<40} {len(cast):>3} produktov · "
              f"{over(c)}")


if __name__ == "__main__":
    main()

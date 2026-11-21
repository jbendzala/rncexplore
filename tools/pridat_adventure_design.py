# -*- coding: utf-8 -*-
"""Postaví data/products-adventure-design.js z feedu výrobcu.

Zdroj: https://adventure-design.cz/feed/produkty.xml?znacka=adventure-design
(Heureka-podobný formát, nie Shoptet). Samostatný súbor, rovnaký dôvod
ako pri Purelux — iná mena (CZK), iné kategórie, žiadna väzba na starý
statický web.

Berieme len 3 kategórie, čo určil klient (rovnaké členenie, aké má
výrobca na vlastnom webe): "Střešní nosiče" → strešné-nosiče,
"Bedracky" → bedrack, "Montážní příslušenství a MOLLE" →
montážne-príslušenstvo. Zvyšných ~17 položiek (zákazkové prestavby,
nárazníky/kryty, odpruženie, hardtopy, merch...) je mimo rozsahu —
nemajú jasné zaradenie do týchto troch a veľa z nich beztak nemá cenu.

Cena: "Cena bez DPH" (párovaná aj z voľného textu "Cena na webu", keď
štruktúrované pole chýba) ide do CSV ako základ v CZK — Shoptet DPH
dopočíta sám (klientovo rozhodnutie). Pozor: tých pár cien dotiahnutých
z voľného textu (nie je pri nich "bez DPH" explicitne) môže byť v
skutočnosti s DPH — nevieme to s istotou, flagnuté v `pack`-type pozn.

Položky bez akejkoľvek ceny (8 z 45) dostanú cenu 0 — vlastné "Cena na
vyžiadanie" bez plateného doplnku, rieši ho CSS/JS v
tools/shoptet_zapatie.py (trieda rnc-na-dopyt). Pôvodne sme na to
používali 99 999 999 (rovnaká hodnota ako interne platený doplnok),
ale to v natívnom cenovom filtri kategórie vytiahlo hornú hranicu na
absurdné číslo a zbytočný rozsah (1998 – 99 999 670) zoškrtil reálne
ceny na nepoužiteľný kúsok slidera. Nula robí presne opačnú, oveľa
menej rušivú vec — posunie len dolnú hranicu na "0 Kč", reálne ceny
ostanú na slideri v rozumnom rozsahu.

Spustenie:  python3 tools/pridat_adventure_design.py [--dry-run]
"""
import json
import os
import re
import sys
import unicodedata
import urllib.request
from collections import Counter

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
CIEL = os.path.join(KOREN, "data", "products-adventure-design.js")
ZDROJ = "https://adventure-design.cz/feed/produkty.xml?znacka=adventure-design"

CENA_NA_DOPYT = 0

MAPA_KATEGORII = {
    "Střešní nosiče": "strešné-nosiče",
    "Bedracky": "bedrack",
    "Montážní příslušenství a MOLLE": "montážne-príslušenstvo",
}
NAZVY = {
    "strešné-nosiče": "Strešné nosiče",
    "bedrack": "Bedrack",
    "montážne-príslušenstvo": "Montážne príslušenstvo",
}
CAT_ORDER = ["strešné-nosiče", "bedrack", "montážne-príslušenstvo"]

# Feed nenesie hmotnosť vôbec — dotiahnuté ručne z popisov na
# adventure-design.cz (len tie produkty, kde je "hmotnost"/"váha"
# skutočne uvedená; väčšina MOLLE panelov, rebríkov a drobností ju
# na webe nemá, tak ostávajú bez hmotnosti).
HMOTNOSTI = {
    "stresni-nosic-zahradka-ford-custom-ad56": 25,
    "stresni-nosic-zahradka-ford-transit-tourneo-custom-vw-transporter-ad26": 20,
    "stresni-nosic-zahradka-ineos-grenadier-ad57": 20,
    "stresni-nosic-zahradka-jeep-wrangler-rubicon-jl-jk-ad31": 20,
    "stresni-nosic-zahradka-land-rover-discovery-3-4-ad50": 20,
    "stresni-nosic-zahradka-mercedes-benz-sprinter-ad53": 30,
    "stresni-nosic-zahradka-mercedes-benz-vito-viano-homologace-ad73": 23,
    "stresni-nosic-zahradka-range-rover-sport-ad45": 20,
    "stresni-nosic-zahradka-toyota-hilux-ad59": 15,
    "stresni-nosic-zahradka-toyota-land-cruiser-150-ad46": 20,
    "stresni-nosic-zahradka-toyota-land-cruiser-250-ad58": 20,
    "stresni-nosic-zahradka-toyota-land-cruiser-78-ad55": 20,
    "stresni-nosic-zahradka-vw-crafter-man-tge-sprinter-ad64": 30,
    "stresni-nosic-zahradka-vw-t5-t6-t6-1-transporter-caravelle-multivan-ad65": 20,
    "stresni-nosic-zahradka-vw-t5-t6-t6-1-long-ad54": 24,
    "stresni-nosic-vw-t7-multivan-ad578": 15,
}


def pole_text(it, tag):
    m = re.search(rf"<{tag}>(.*?)</{tag}>", it, re.S)
    return m.group(1).strip() if m else None


def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return re.sub(r"-{2,}", "-", t)


def cena_z_textu(text):
    """'35 000 Kč' -> 35000; vráti None, keď tam číslo nie je
    ('Dohodou', 'na dotaz')."""
    if not text:
        return None
    cislice = re.sub(r"[^0-9]", "", text)
    return int(cislice) if cislice else None


def main():
    dry = "--dry-run" in sys.argv
    req = urllib.request.Request(ZDROJ, headers={"User-Agent": "Mozilla/5.0"})
    xml = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    polozky = re.findall(r"<SHOPITEM>.*?</SHOPITEM>", xml, re.S)
    print(f"feed: {len(polozky)} položiek spolu")

    produkty = []
    bez_ceny = 0
    for it in polozky:
        cat_text = pole_text(it, "CATEGORYTEXT") or ""
        podkat = cat_text.split("|")[-1].strip()
        cat = MAPA_KATEGORII.get(podkat)
        if cat is None:
            continue

        nazov = pole_text(it, "PRODUCTNAME") or pole_text(it, "PRODUCT")
        params = dict(re.findall(r"<PARAM_NAME>(.*?)</PARAM_NAME><VAL>(.*?)</VAL>", it))

        cena = cena_z_textu(params.get("Cena bez DPH"))
        z_textu = False
        if cena is None:
            cena = cena_z_textu(params.get("Cena na webu"))
            z_textu = cena is not None
        if cena is None:
            cena = CENA_NA_DOPYT
            bez_ceny += 1

        obrazky = [pole_text(it, "IMGURL")] if "<IMGURL>" in it else []
        obrazky += re.findall(r"<IMGURL_ALTERNATIVE>(.*?)</IMGURL_ALTERNATIVE>", it)
        obrazky = [u for u in obrazky if u]

        popis = pole_text(it, "DESCRIPTION") or ""

        id_ = f'{slug(nazov)[:70]}-ad{pole_text(it, "ITEM_ID")}'
        produkt = {
            "id": id_,
            "cat": cat,
            "sku": f'AD-{pole_text(it, "ITEM_ID")}',
            "n": {"sk": nazov},
            "d": {"sk": popis},
            "czk": cena,
            "cena_z_volneho_textu": z_textu,
            "img": obrazky,
            "url_vyrobca": pole_text(it, "URL"),
        }
        if id_ in HMOTNOSTI:
            produkt["kg"] = HMOTNOSTI[id_]
        produkty.append(produkt)

    cats = Counter(p["cat"] for p in produkty)
    meta = {
        "cats": [{"k": k, "sk": NAZVY[k], "n": cats[k]} for k in CAT_ORDER if cats.get(k)],
        "count": len(produkty),
    }
    produkty.sort(key=lambda p: (CAT_ORDER.index(p["cat"]), p["n"]["sk"]))

    print(f"zaradených do 3 kategórií: {len(produkty)}")
    for k in CAT_ORDER:
        if cats.get(k):
            print(f"  {k:24s} {cats[k]:4d}  {NAZVY[k]}")
    print(f"z toho bez akejkoľvek ceny (0, cena na vyžiadanie): {bez_ceny}")

    s_hmotnostou = sum(1 for p in produkty if "kg" in p)
    print(f"hmotnosť dotiahnutá z webu výrobcu: {s_hmotnostou}/{len(produkty)} "
          f"(zvyšok ju na webe nemá uvedenú)")

    z_textu_zoznam = [p["n"]["sk"] for p in produkty if p["cena_z_volneho_textu"]]
    if z_textu_zoznam:
        print(f"\npozor, {len(z_textu_zoznam)} cien je dotiahnutých z voľného textu "
              f"(nie je pri nich explicitne \"bez DPH\" — môžu už byť s DPH, overiť):")
        for n in z_textu_zoznam:
            print("  -", n)

    for p in produkty:
        del p["cena_z_volneho_textu"]

    if dry:
        print("\n--dry-run: nič som nezapísal")
        return 0

    with open(CIEL, "w", encoding="utf-8") as f:
        f.write("/* Generované dáta katalógu Adventure Design — negenerujte ručne. */\n")
        f.write("window.AD_META=" + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + ";\n")
        f.write("window.AD_PRODUCTS=" + json.dumps(produkty, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(f"\nzapísané: {CIEL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Vypíše obsah katalógu Adventure Design do XML (popis, fotky, kategórie).

Druhý krok po CSV (export_adventure_design.py), rovnaký vzor ako pri
Purelux. Bez variant — každá položka feedu je samostatný produkt.

Popis vo feede je čistý text s "•" odrážkami a prázdnymi riadkami medzi
odsekmi, nie HTML — prevod_popisu() ho zmení na <p>/<ul><li> podľa
tvaru riadku, nech to na karte nevyzerá ako jeden nečlenený blok textu.
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
from export_adventure_design import kod

VYROBCA = "Adventure Design"
KOREN_KATEGORIE = "Strešné nosiče a výbava"

NAZVY = {
    "strešné-nosiče": "Strešné nosiče",
    "bedrack": "Bedrack",
    "montážne-príslušenstvo": "Montážne príslušenstvo",
}


def e(x):
    return html.escape(str(x), quote=True)


def prvá_veta(txt):
    txt = (txt or "").strip()
    m = re.search(r"(?<!\d)[.!?](?=\s+[A-ZÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ])", txt)
    return txt[:m.end()].strip() if m else txt


def seo_popis(txt):
    txt = re.sub(r"\s+", " ", (txt or "")).strip()
    if len(txt) <= 155:
        return txt
    kus = txt[:155]
    return kus[:kus.rfind(" ")].rstrip(" ,;–-•") + "…"


def prevod_popisu(txt):
    """Čistý text s "•" odrážkami a prázdnymi riadkami medzi odsekmi ->
    <p>/<ul><li>. Odrážkový blok sa uzavrie, keď príde riadok, čo
    nezačína "•", alebo keď text skončí."""
    bloky, odrazky = [], []

    def zavri_odrazky():
        if odrazky:
            bloky.append("<ul>" + "".join(f"<li>{e(o)}</li>" for o in odrazky) + "</ul>")
            odrazky.clear()

    for odsek in (txt or "").split("\n\n"):
        odsek = odsek.strip()
        if not odsek:
            continue
        riadky = [r.strip() for r in odsek.split("\n") if r.strip()]
        for r in riadky:
            if r.startswith("•"):
                odrazky.append(r.lstrip("•").strip())
            else:
                zavri_odrazky()
                bloky.append(f"<p>{e(r)}</p>")
        zavri_odrazky()
    return "".join(bloky)


def kratky_popis(p):
    return f"<p>{e(prvá_veta(p['d']['sk']))}</p>"


def cesty(kategoria):
    hlavna = f"{KOREN_KATEGORIE} > {kategoria}"
    return [KOREN_KATEGORIE, hlavna], hlavna


def shopitem(p):
    r = ["  <SHOPITEM>"]
    r.append(f"    <NAME>{e(p['n']['sk'])}</NAME>")
    r.append(f"    <SHORT_DESCRIPTION>{e(kratky_popis(p))}</SHORT_DESCRIPTION>")
    r.append(f"    <DESCRIPTION>{e(prevod_popisu(p['d']['sk']))}</DESCRIPTION>")
    r.append(f"    <MANUFACTURER>{e(VYROBCA)}</MANUFACTURER>")
    r.append(f"    <SEO_TITLE>{e(p['n']['sk'] + ' | RnC Explore')}</SEO_TITLE>")
    r.append(f"    <META_DESCRIPTION>{e(seo_popis(p['d']['sk']))}</META_DESCRIPTION>")

    zoznam, hlavna = cesty(NAZVY[p["cat"]])
    r.append("    <CATEGORIES>")
    r += [f"      <CATEGORY>{e(k)}</CATEGORY>" for k in zoznam]
    r.append(f"      <DEFAULT_CATEGORY>{e(hlavna)}</DEFAULT_CATEGORY>")
    r.append("    </CATEGORIES>")

    obrazky = p.get("img") or []
    if obrazky:
        r.append("    <IMAGES>")
        r += [f"      <IMAGE>{e(u)}</IMAGE>" for u in obrazky]
        r.append("    </IMAGES>")

    r.append(f"    <CODE>{e(kod(p))}</CODE>")
    r.append("    <UNIT>ks</UNIT>")
    if "kg" in p:
        r.append(f"    <LOGISTIC><WEIGHT>{p['kg']}</WEIGHT></LOGISTIC>")
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


def main():
    s = open(os.path.join(KOREN, "data", "products-adventure-design.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.AD_PRODUCTS=(\[.*\]);", s, re.S).group(1))

    r = ['<?xml version="1.0" encoding="UTF-8"?>', "<SHOP>"]
    for p in P:
        r += shopitem(p)
    r.append("</SHOP>")

    ciel = vystup.kam(vystup.IMPORT, "adventure-design-xml", "obsah.xml")
    with open(ciel, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(r) + "\n")
    fotiek = sum(len(p.get("img") or []) for p in P)
    print(f"{len(P)} produktov, {fotiek} fotografií -> {ciel}")
    print(f"   {over(ciel)}")


if __name__ == "__main__":
    main()

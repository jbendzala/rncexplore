# -*- coding: utf-8 -*-
"""Fotky (a krátky obsah) pre sady panelov, čo sady_panelov.py zakladá
len cez CSV.

nove-sady.csv nesie meno, cenu a prepojenie — nie obsah. Tri nové
produkty na panel ("Panel + vinylová fólia", "Panel + MPPT regulátor",
"Kompletná sada") preto naživo nemali ani jednu fotku, ani popis.
Komponenty (fólia, regulátor) fotku nepotrebujú — sú skryté v kategórii
"Skryté – sady a komponenty" a zákazník ich nikdy neuvidí priamo.

Fotky aj text preberajú z pôvodného panela — fyzicky ide o ten istý
box, len s iným príslušenstvom v balení. Kategóriu zámerne neposielame
(tú už správne nastavilo CSV cez defaultCategory) — tento súbor dopĺňa
len to, čo v CSV chýbalo.

Spustenie:  python3 tools/sady_panelov_xml.py
"""
import html
import os
import re
import subprocess
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup
import sady_panelov as sp

VYROBCA = "LensunSolar"

DOPLNOK = {
    sp.FOLIA: "Sada obsahuje aj vinylovú fóliu na ochranu laku pod panelom.",
    sp.MPPT: "Sada obsahuje aj MPPT regulátor nabíjania.",
    sp.KOMPLETNA: "Sada obsahuje aj vinylovú fóliu na ochranu laku pod panelom a MPPT regulátor nabíjania.",
}


def e(x):
    return html.escape(str(x), quote=True)


def prvá_veta(t):
    t = (t or "").strip()
    m = re.search(r"(?<!\d)[.!?](?=\s+[A-ZÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ])", t)
    return t[:m.end()].strip() if m else t


def seo_popis(t):
    t = re.sub(r"\s+", " ", (t or "")).strip()
    if len(t) <= 155:
        return t
    kus = t[:155]
    return kus[:kus.rfind(" ")].rstrip(" ,;–-") + "…"


def shopitem(code, name, popis_panela, doplnok, obrazky, kg):
    # Vnútorný text sa escapuje raz (nech "&"/"<" v ňom nerozbijú HTML
    # úryvok) a celý ten úryvok ešte raz (nech jeho vlastné <p> tagy
    # nerozbijú XML dokument) — rovnaký dvojkrokový vzor ako v
    # export_shoptet_xml.py/export_purelux_xml.py.
    kratky_html = f"<p>{e(prvá_veta(popis_panela))}</p>"
    dlhy_html = f"<p>{e(popis_panela)}</p><p>{e(doplnok)}</p>"
    r = ["  <SHOPITEM>"]
    r.append(f"    <NAME>{e(name)}</NAME>")
    r.append(f"    <SHORT_DESCRIPTION>{e(kratky_html)}</SHORT_DESCRIPTION>")
    r.append(f"    <DESCRIPTION>{e(dlhy_html)}</DESCRIPTION>")
    r.append(f"    <MANUFACTURER>{e(VYROBCA)}</MANUFACTURER>")
    r.append(f"    <SEO_TITLE>{e(name + ' | RnC Explore')}</SEO_TITLE>")
    r.append(f"    <META_DESCRIPTION>{e(seo_popis(popis_panela))}</META_DESCRIPTION>")
    if obrazky:
        r.append("    <IMAGES>")
        r += [f"      <IMAGE>{e(u)}</IMAGE>" for u in obrazky]
        r.append("    </IMAGES>")
    r.append(f"    <CODE>{e(code)}</CODE>")
    r.append("    <UNIT>ks</UNIT>")
    r.append(f"    <LOGISTIC><WEIGHT>{kg}</WEIGHT></LOGISTIC>")
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
    P = sp.katalog()
    riadky = ['<?xml version="1.0" encoding="UTF-8"?>', "<SHOP>"]
    pocet = 0
    for p in P:
        if not sp.kvalifikuje(p):
            continue
        k = sp.kody_produktu(p)
        obrazky = p.get("img") or []
        kg = p.get("kg") or 0
        popis_panela = p["d"]["sk"]
        for kluc, label in ((k["sada_folia"], sp.FOLIA),
                            (k["sada_mppt"], sp.MPPT),
                            (k["sada_kompletna"], sp.KOMPLETNA)):
            riadky += shopitem(kluc, f'{p["n"]["sk"]} – {label}',
                               popis_panela, DOPLNOK[label], obrazky, kg)
            pocet += 1
    riadky.append("</SHOP>")

    ciel = vystup.kam(vystup.IMPORT, "sady-panelov", "fotky-sad.xml")
    with open(ciel, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(riadky) + "\n")
    print(f"{pocet} sady (fotky z pôvodného panela) -> {ciel}")
    print(f"   {over(ciel)}")


if __name__ == "__main__":
    main()

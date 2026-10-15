# -*- coding: utf-8 -*-
"""Vypíše oddelenia katalógu do CSV vo formáte Shopify.

Formát je ten istý, aký posiela Lensun — dá sa teda nahrať rovnakým
importom. Prvý riadok produktu nesie údaje o produkte, ďalšie riadky
len prevedenia, a za nimi riadky s ostatnými fotografiami.

Navyše sú v súbore štyri stĺpce s cenami, ktoré Shopify nepozná a pri
importe ich preskočí — sú tam pre nás a pre veľkoobchodných partnerov.
"""
import csv, html, json, os, re, sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo

CIEL = os.path.expanduser("~/Documents")
VENDOR = "LensunSolar"
KATEGORIA_G = "Hardware > Power & Electrical Supplies > Solar Energy Kits"

# Ktoré oddelenia vyviezť, ako sa bude volať súbor a aká je veľkoobchodná
# zľava z maloobchodnej ceny BEZ DPH.
ODDELENIA = [
    ("hood",     "panely-na-kapotu",   0.30),
    ("flexible", "flexibilne-panely",  0.25),
    ("rooftent", "stresne-stany",      0.25),
]

STLPCE = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type",
    "Tags", "Published", "Option1 Name", "Option1 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker",
    "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
    "Variant Requires Shipping", "Variant Taxable", "Variant Weight Unit",
    "Image Src", "Image Position", "Image Alt Text",
    "SEO Title", "SEO Description", "Status",
    # vlastné stĺpce — Shopify ich pri importe ignoruje
    "Cena bez DPH (EUR)", "Veľkoobchodná zľava (%)",
    "Veľkoobchodná cena bez DPH (EUR)", "Veľkoobchodná cena s DPH (EUR)",
]

POPISKY = {
    "w": "Výkon", "eff": "Účinnosť článkov", "vmp": "Napätie pri max. výkone",
    "imp": "Prúd pri max. výkone", "voc": "Napätie naprázdno",
    "isc": "Skratový prúd", "vsys": "Max. napätie sústavy",
    "dim": "Rozmer", "kg": "Hmotnosť", "jbox": "Pripojovacia skrinka",
}
PORADIE = ["w", "eff", "vmp", "imp", "voc", "isc", "vsys", "dim", "kg", "jbox"]


def e(x):
    return html.escape(str(x), quote=False)


def telo(p):
    """Popis produktu v HTML — veta, tabuľka parametrov, obsah balenia."""
    c = ["<p>" + e(p["d"]["sk"]) + "</p>"]
    spec = p.get("spec") or {}
    riadky = [(POPISKY[k], spec[k]) for k in PORADIE if spec.get(k)]
    if p.get("b"):
        riadky.append(("Značka vozidla", p["b"]))
    if riadky:
        c.append("<h3>Technické parametre</h3><table>")
        c += [f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in riadky]
        c.append("</table>")
    if p.get("pack"):
        c.append("<h3>Obsah balenia</h3><ul>")
        c += ["<li>" + e(r["sk"]) + "</li>" for r in p["pack"]]
        c.append("</ul>")
    return "".join(c)


def ciarka(v):
    """Desatinná čiarka — slovenský Excel inak číslo berie ako text."""
    return f"{v:.2f}".replace(".", ",")


def main():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});", s, re.S).group(1))
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))
    nazvy = {c["k"]: c["sk"] for c in meta["cats"]}
    dph = seo.CFG.get("vat", 0.23)

    for kat, subor, zlava in ODDELENIA:
        polozky = [p for p in P if p["cat"] == kat]
        cesta = os.path.join(CIEL, f"rncexplore-{subor}.csv")
        prevedeni = fotiek = 0
        riadky = []
        if True:
            for p in polozky:
                obrazky = p.get("img") or []
                for i, v in enumerate(p["var"]):
                    brutto = seo.price(v["p"], "EUR")
                    netto = brutto / (1 + dph)
                    vo_netto = netto * (1 - zlava)
                    r = {k: "" for k in STLPCE}
                    r.update({
                        "Handle": p["id"],
                        "Option1 Value": v["sk"],
                        "Variant SKU": v.get("sku", ""),
                        "Variant Grams": int(round((p.get("kg") or 0) * 1000)),
                        "Variant Inventory Policy": "continue",
                        "Variant Fulfillment Service": "manual",
                        "Variant Price": ciarka(brutto),
                        "Variant Requires Shipping": "TRUE",
                        "Variant Taxable": "TRUE",
                        "Variant Weight Unit": "kg",
                        "Cena bez DPH (EUR)": ciarka(netto),
                        "Veľkoobchodná zľava (%)": int(zlava * 100),
                        "Veľkoobchodná cena bez DPH (EUR)": ciarka(vo_netto),
                        "Veľkoobchodná cena s DPH (EUR)": ciarka(vo_netto * (1 + dph)),
                    })
                    if i == 0:          # prvý riadok nesie údaje o produkte
                        r.update({
                            "Title": p["n"]["sk"],
                            "Body (HTML)": telo(p),
                            "Vendor": VENDOR,
                            "Product Category": KATEGORIA_G,
                            "Type": nazvy.get(kat, kat),
                            "Tags": ", ".join(x for x in (p.get("b"), nazvy.get(kat)) if x),
                            "Published": "TRUE",
                            "Option1 Name": "Prevedenie",
                            "Status": "active",
                            "SEO Title": p["n"]["sk"][:70],
                            "SEO Description": p["d"]["sk"][:320],
                        })
                        if obrazky:
                            r.update({"Image Src": obrazky[0], "Image Position": 1,
                                      "Image Alt Text": p["n"]["sk"]})
                            fotiek += 1
                    riadky.append(r)
                    prevedeni += 1
                # ostatné fotografie vlastnými riadkami
                for k, u in enumerate(obrazky[1:], start=2):
                    r = {x: "" for x in STLPCE}
                    r.update({"Handle": p["id"], "Image Src": u, "Image Position": k,
                              "Image Alt Text": f'{p["n"]["sk"]} — fotografia {k}'})
                    riadky.append(r)
                    fotiek += 1
        # Stĺpec, ktorý zostal prázdny v každom riadku, do súboru nepatrí —
        # Shopify si chýbajúce doplní sám a tabuľka je o dosť čitateľnejšia.
        pouzite = [k for k in STLPCE if any(str(r.get(k, "")) != "" for r in riadky)]
        vyhodene = [k for k in STLPCE if k not in pouzite]
        with open(cesta, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=pouzite, delimiter=",",
                               extrasaction="ignore")
            w.writeheader()
            w.writerows(riadky)

        if vyhodene:
            print(f"     vynechané prázdne stĺpce: {', '.join(vyhodene)}")
        print(f"  {nazvy.get(kat, kat):<22} {len(polozky):>3} produktov · "
              f"{prevedeni:>3} prevedení · {fotiek:>3} fotografií · "
              f"zľava {int(zlava*100)} %  ->  {os.path.basename(cesta)}")


if __name__ == "__main__":
    main()

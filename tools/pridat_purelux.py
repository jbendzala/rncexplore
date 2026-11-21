# -*- coding: utf-8 -*-
"""Postaví data/products-purelux.js z klientovho xlsx (valostore.com, značka Purelux).

Zdroj: ~/Downloads/purelux_valostore_detail.xlsx, listy „Produkty",
„Varianty" a „Obrázky". Je to samostatný súbor, nie rozšírenie
data/products.js — Purelux ceny sú už hotové € s DPH priamo z valostore,
kým tools/seo.py's price() počíta z USD cez kurz/prirážku/dopravu/DPH pre
Lensun. Zmiešanie by cenu prepočítalo druhýkrát. Aj build.py/sitemap.py/
product_pages.py čítajú data/products.js pre starý statický web — Purelux
tam zatiaľ nepatrí, nemá vozidlovú os ani český preklad.

Berieme len varianty, ktoré vieme nakúpiť veľkoobchodne (stĺpec „V Hárok1"
= Áno, alebo jedno z dvoch potvrdených premenovaní — viď list „Rozdiely"
v tom istom zošite), bez merchu (tričká, mikiny, čiapky...) a bez
produktov, ktorým po filtri neostala ani jedna varianta (to sú vyradené
modely, čo valostore už nepredáva, a 3 informačné stránky bez predaja).

Spustenie:  python3 tools/pridat_purelux.py [--dry-run]
"""
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

import openpyxl

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
CIEL = os.path.join(KOREN, "data", "products-purelux.js")
ZDROJ = os.path.expanduser("~/Downloads/purelux_valostore_detail.xlsx")
PREKLADY = os.path.join(TU, "purelux_preklady.json")

MERCH = ("t-shirt", "hoodie", "cap", "beanie", "keychain", "sticker",
         "air freshener", "fur hat", "pom pom", "trucker")

# Dve potvrdené premenovania — staré číslo z Hárok1 na webe nie je, nové
# je, ide o ten istý produkt (list „Rozdiely", typ „Chýba v Hárok1"/„Nie
# je na webe").
PREMENOVANE_NA = {"HS18701-20759", "HS23184-20753"}

CAT_ORDER = ["led-rampy", "led-privesvetla", "led-pracovne", "led-vystrazne",
             "led-hmlovky", "ziarovky", "elektroinstalacia",
             "montaz-prislusenstvo"]

NAZVY = {
    "led-rampy": "LED rampy",
    "led-privesvetla": "Prídavné svetlá",
    "led-pracovne": "Pracovné svetlá",
    "led-vystrazne": "Výstražné svetlá",
    "led-hmlovky": "Hmlové a polohové svetlá",
    "ziarovky": "Žiarovky",
    "elektroinstalacia": "Elektroinštalácia a relé",
    "montaz-prislusenstvo": "Montáž a príslušenstvo",
}

# Podľa „Zaradenie (celá cesta)" z valostore — prvá zhoda vyhráva, preto
# idú konkrétnejšie reťazce pred všeobecnejšími.
PRAVIDLA = [
    ("led bars", "led-rampy"),
    ("worklight", "led-pracovne"),
    ("work lights", "led-pracovne"),
    ("round lights", "led-privesvetla"),
    ("extralight kits", "led-privesvetla"),
    ("by brand and model", "led-privesvetla"),
    ("driving lights", "led-privesvetla"),
    ("warning", "led-vystrazne"),
    ("position", "led-hmlovky"),
    ("reversing", "led-hmlovky"),
    ("tail lights", "led-hmlovky"),
    ("fog lights", "led-hmlovky"),
    ("bulbs", "ziarovky"),
    ("wiring", "elektroinstalacia"),
    ("switches and relays", "elektroinstalacia"),
    ("connectors", "elektroinstalacia"),
    ("batteries", "elektroinstalacia"),
    ("brackets", "montaz-prislusenstvo"),
    ("stands", "montaz-prislusenstvo"),
    ("stone shields", "montaz-prislusenstvo"),
    ("supports and mounts", "montaz-prislusenstvo"),
    ("mounts", "montaz-prislusenstvo"),
    ("accessories", "elektroinstalacia"),
]
VYCHODZIA = "montaz-prislusenstvo"

OBSAH_RIADOK = re.compile(r"(\d+)\s*[×x]\s*\[SKU\s*(\d+)\]\s*([^\n]+)")


def kategoria(cesta):
    """Vráti (kód, zhodlo_sa_pravidlo) — druhé len na diagnostiku, nech sa
    nehlási ako podozrivé aj to, čo do východzej kategórie trafilo
    pravidlom (napr. „mounts"), nie len jej skutočným neúspechom."""
    c = (cesta or "").lower()
    for kluc, kod in PRAVIDLA:
        if kluc in c:
            return kod, True
    return VYCHODZIA, False


def je_merch(nazov):
    n = (nazov or "").lower()
    return any(k in n for k in MERCH)


def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return re.sub(r"-{2,}", "-", t)


def rozober_obsah(text):
    """'2× [SKU 123] Názov\\n1× [SKU 456] Iný názov' -> [(2,'123','Názov'), ...]."""
    if not text:
        return []
    return [(int(ks), kod, nazov.strip().rstrip(","))
            for ks, kod, nazov in OBSAH_RIADOK.findall(text)]


def nacitaj_obrazky(wb):
    """Product number (základ) -> zoznam URL galérie, podľa poradia."""
    ws = wb["Obrázky"]
    rows = list(ws.iter_rows(values_only=True))
    idx = {h: i for i, h in enumerate(rows[0])}
    podla_produktu = defaultdict(list)
    for r in rows[1:]:
        if r[idx["Typ"]] != "galéria produktu":
            continue
        podla_produktu[r[idx["Product number"]]].append(
            (r[idx["Poradie v galérii"]] or 0, r[idx["Link"]]))
    return {k: [u for _, u in sorted(v) if u] for k, v in podla_produktu.items()}


def preloz(produkty):
    """Nahradí anglický text (z valostore) slovenským a doplní český,
    podľa slovníka vytvoreného jedným veľkým prekladateľským behom
    (389 produktov, 1104 unikátnych reťazcov). Slovník je v repozitári
    (tools/purelux_preklady.json), nie generovaný nanovo pri každom
    behu — preklad cez LLM stojí čas aj peniaze, netreba ho opakovať
    pri texte, čo sa nezmenil.

    Keď klient dodá nový xlsx s novými produktmi, ich text v slovníku
    chýba — necháme ho po anglicky (nie prázdny, nie pád skriptu) a
    vypíšeme ho, nech sa dá doplniť. Vracia zoznam nepreložených."""
    if not os.path.exists(PREKLADY):
        return []
    slovnik = json.load(open(PREKLADY, encoding="utf-8"))
    chybajuce = []

    def t(text):
        preklad = slovnik.get(text)
        if preklad is None:
            if text and text not in chybajuce:
                chybajuce.append(text)
            return {"sk": text, "cs": text}
        return preklad

    for p in produkty:
        preklad = t(p["n"]["sk"])
        p["n"] = {"sk": preklad["sk"], "cs": preklad["cs"]}
        preklad = t(p["d"]["sk"])
        p["d"] = {"sk": preklad["sk"], "cs": preklad["cs"]}
        for v in p.get("var", []):
            preklad = t(v["sk"])
            v["sk"], v["cs"] = preklad["sk"], preklad["cs"]
        p["pack"] = [{"sk": t(item)["sk"], "cs": t(item)["cs"]}
                     for item in p.get("pack", [])]
    return chybajuce


def main():
    dry = "--dry-run" in sys.argv
    wb = openpyxl.load_workbook(ZDROJ, data_only=True)
    obrazky = nacitaj_obrazky(wb)

    p_rows = list(wb["Produkty"].iter_rows(values_only=True))
    p_idx = {h: i for i, h in enumerate(p_rows[0])}
    v_rows = list(wb["Varianty"].iter_rows(values_only=True))
    v_idx = {h: i for i, h in enumerate(v_rows[0])}

    podla_zakladu = defaultdict(list)
    preskocene_merch = 0
    for r in v_rows[1:]:
        cislo = r[v_idx["Product number variantu"]]
        vie_sa_nakupit = (r[v_idx["V Hárok1"]] == "Áno"
                           or cislo in PREMENOVANE_NA)
        if not vie_sa_nakupit:
            continue
        if je_merch(r[v_idx["Celý názov variantu"]]):
            preskocene_merch += 1
            continue
        podla_zakladu[r[v_idx["Product number (základ)"]]].append(r)

    produkty = []
    preskocene_prazdne = 0
    for pr in p_rows[1:]:
        zaklad = pr[p_idx["Product number"]]
        varianty = podla_zakladu.get(zaklad, [])
        if not varianty or je_merch(pr[p_idx["Názov produktu"]]):
            preskocene_prazdne += 1
            continue

        var_zaznamy = []
        for v in varianty:
            cena = v[v_idx["Akciová cena (€)"]] or v[v_idx["Bežná cena (€)"]]
            je_sada = v[v_idx["Sada (bundle)"]] == "Áno"
            obsah = rozober_obsah(v[v_idx["Obsah variantu (množstvo × položka)"]])
            var_zaznamy.append({
                "sk": v[v_idx["Variant"]] or v[v_idx["Celý názov variantu"]],
                "p": round(float(cena), 2),
                "sku": str(v[v_idx["Product number variantu"]]),
                "kg": v[v_idx["Hmotnosť (kg)"]],
                "_pack": [f"{ks}× {nazov}" for ks, _, nazov in obsah] if je_sada else [],
            })
        var_zaznamy.sort(key=lambda v: v["p"])

        zakladna = var_zaznamy[0]
        cat, zhoda = kategoria(pr[p_idx["Zaradenie (celá cesta)"]])
        produkty.append({
            "id": f'{slug(pr[p_idx["Názov produktu"]])[:70]}-{zaklad.lower()}',
            "cat": cat,
            "_bez_zhody": not zhoda,
            "sku": str(zaklad),
            "n": {"sk": pr[p_idx["Názov produktu"]]},
            "d": {"sk": (pr[p_idx["Úvodný text"]] or "").strip()},
            "eur": zakladna["p"],
            "kg": zakladna["kg"],
            "img": obrazky.get(zaklad, []),
            "pack": zakladna["_pack"],
            # Vždy aspoň jeden záznam, aj pri jedinej variante — presne ako
            # pri Lensune (export_shoptet.py ide rovno cez "for v in
            # p['var']", prázdny zoznam by mlčky nevypísal nič).
            "var": [{k: v2 for k, v2 in v.items() if k != "_pack"}
                    for v in var_zaznamy],
        })

    cats = Counter(p["cat"] for p in produkty)
    meta = {
        "cats": [{"k": k, "sk": NAZVY[k], "n": cats[k]} for k in CAT_ORDER if cats.get(k)],
        "count": len(produkty),
    }
    produkty.sort(key=lambda p: (CAT_ORDER.index(p["cat"]), p["n"]["sk"]))

    print(f"produktov: {len(produkty)}   "
          f"variant spolu: {sum(max(1, len(p['var'])) for p in produkty)}")
    print(f"vynechané produktové stránky (prázdne po filtri/merch): {preskocene_prazdne}")
    print(f"vynechané varianty (merch): {preskocene_merch}")
    for k in CAT_ORDER:
        if cats.get(k):
            print(f"  {k:24s} {cats[k]:4d}  {NAZVY[k]}")

    bez_zhody = [p["n"]["sk"] for p in produkty if p["_bez_zhody"]]
    if bez_zhody:
        print(f"\npozor, {len(bez_zhody)} produktov nezachytilo žiadne pravidlo "
              f"a padlo do východzej kategórie „{VYCHODZIA}“, skontroluj ručne:")
        for n in bez_zhody:
            print("  -", n)

    for p in produkty:
        del p["_bez_zhody"]

    chybajuce = preloz(produkty)
    if chybajuce:
        print(f"\npozor, {len(chybajuce)} nových anglických textov nemá preklad "
              f"v tools/purelux_preklady.json (ostali po anglicky, treba doplniť):")
        for t in chybajuce[:20]:
            print("  -", t)

    if dry:
        print("\n--dry-run: nič som nezapísal")
        return 0

    with open(CIEL, "w", encoding="utf-8") as f:
        f.write("/* Generované dáta katalógu Purelux — negenerujte ručne. */\n")
        f.write("window.PURELUX_META=" + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + ";\n")
        f.write("window.PURELUX_PRODUCTS=" + json.dumps(produkty, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(f"\nzapísané: {CIEL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

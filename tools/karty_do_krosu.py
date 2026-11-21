# -*- coding: utf-8 -*-
"""Vyplní šablónu skladových kariet pre KROS Sklad.

Šablónu nevyrábame — berieme tú, ktorú KROS sám vyexportuje
(Zoznam_kariet.xlsx), a dopisujeme do nej. Názvy stĺpcov sa tak
nehádajú a formát zostane ich.

Karta je jedno prevedenie, nie produkt: sklad eviduje kusy, nie
karty v e-shope.

108 produktov (presná štandardná štvorica, pozri sady_panelov.py)
dnes v e-shope nemá tie 4 prevedenia ako natívne varianty — boli
rozložené na sady a komponenty (Sady produktov + Varianty ako
samostatné produkty). Fyzicky sa skladujú len TRI veci: panel, fólia,
MPPT regulátor — sady samotné sklad nemajú, ich dostupnosť si Shoptet
dopočíta z týchto troch sám. Tým produktom preto dávame 3 karty
(panel + 2 komponenty), nie 4 ako predtým. Zvyšných ~49 produktov s
inými kombináciami (iný regulátor, predlžovací kábel, viacpanelové
sady) touto zmenou prejdené nebolo — tie idú po starom, karta na
natívne prevedenie.

Kód musí ísť v tej podobe, v akej je v e-shope — s tou štvorznakovou
značkou, ktorú sme pridali kvôli tomu, že Lensun používa ten istý kód
na rôzne autá. Podľa neho sa sklad páruje s obchodom; bez nej by
KROS založil produkty znova. Kódy komponentov fólia/MPPT sú nové
(RNC-FOLIA-…/RNC-MPPT-…, pozri sady_panelov.py) — v KROSe predtým
neexistovali, lebo dovtedy neboli samostatne skladovanou položkou.

Čo zámerne nevypĺňame:
  Zostatok            nevieme, dopĺňa sa pri naskladnení
  EAN kód             nemáme
  Nákupná cena        nevieme, to je práve to, na čo čakáme
  Popis               sklad ho nepotrebuje a je to HTML

„Posielať do eshopu“ dávame na Nie. Pri prvom importe chceme len
dostať karty do skladu a overiť, či sa kódy spárovali. Áno sa zapne
až potom — inak by KROS prepísal názvy produktov v e-shope týmito,
ktoré sú zložené z názvu a prevedenia.

Spustenie:
    python3 tools/karty_do_krosu.py ~/Downloads/Zoznam_kariet.xlsx
"""
import json
import os
import re
import shutil
import sys

from openpyxl import load_workbook

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo                                              # noqa: E402
import sady_panelov as sp                               # noqa: E402
from export_shoptet import kod                          # noqa: E402

DPH = 23
HARO = "Karty"
STLPCE = ["Kód karty", "Názov", "MJ", "Hmotnosť [kg]", "DPH [%]",
          "Posielať do eshopu", "Predajná cena ZC"]


def v_obchode(k):
    """Kód tak, ako ho má Shoptet — veľké písmená, + a * ako pomlčka."""
    return re.sub(r"[+*]", "-", k.strip().upper())


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))


def riadok(kod_karty, nazov, hmotnost, cena_eur):
    return {
        "Kód karty": kod_karty, "Názov": nazov, "MJ": "ks",
        "Hmotnosť [kg]": round(float(hmotnost or 0), 2) or None,
        "DPH [%]": DPH, "Posielať do eshopu": "Nie",
        "Predajná cena ZC": round(cena_eur, 2),
    }


def riadky_sady(p):
    """Panel + 2 komponenty (fólia, MPPT) — sady samotné kartu nemajú,
    ich dostupnosť si Shoptet dopočíta z týchto troch sám."""
    k = sp.kody_produktu(p)
    panel_v = sp.najdi(p, sp.SAMOTNY)
    ck = sp.cena_komponentov(p)
    hmotnost = p.get("kg") or 0
    return [
        riadok(k["panel"], f'{p["n"]["sk"]} – {sp.SAMOTNY}',
               hmotnost, seo.price(panel_v["p"], "EUR")),
        riadok(k["folia_komponent"], f'{p["n"]["sk"]} – Vinylová fólia (komponent)',
               0, seo.price(ck["folia"], "EUR")),
        riadok(k["mppt_komponent"], f'{p["n"]["sk"]} – MPPT regulátor (komponent)',
               0, seo.price(ck["mppt"], "EUR")),
    ]


def riadky_varianty(p):
    """Pôvodný vzor — jedna karta na natívne prevedenie. Platí pre tých
    ~49 produktov, čo cez sady_panelov.py neprešli."""
    riadky = []
    for v in p["var"]:
        if not v.get("sku"):
            continue
        riadky.append(riadok(v_obchode(kod(p, v)), f'{p["n"]["sk"]} – {v["sk"]}',
                             p.get("kg") or 0, seo.price(v["p"], "EUR")))
    return riadky


def vsetky_riadky(P):
    riadky = []
    for p in sorted(P, key=lambda x: x["n"]["sk"]):
        riadky += riadky_sady(p) if sp.kvalifikuje(p) else riadky_varianty(p)
    return riadky


def main():
    if len(sys.argv) < 2:
        sys.exit("použitie: python3 tools/karty_do_krosu.py <šablóna z KROSu>")
    vzor = os.path.expanduser(sys.argv[1])
    if not os.path.exists(vzor):
        sys.exit(f"šablóna neexistuje: {vzor}")
    ciel = os.path.expanduser("~/Documents/rncexplore-karty-do-krosu.xlsx")
    shutil.copy(vzor, ciel)

    wb = load_workbook(ciel)
    if HARO not in wb.sheetnames:
        sys.exit(f"v šablóne nie je hárok „{HARO}“; je tam: "
                 + ", ".join(wb.sheetnames))
    ws = wb[HARO]

    hlavicka = {ws.cell(row=1, column=c).value: c
                for c in range(1, ws.max_column + 1)}
    chyba = [n for n in STLPCE if n not in hlavicka]
    if chyba:
        sys.exit("v šablóne chýbajú stĺpce: " + ", ".join(chyba)
                 + "\nje tam: " + ", ".join(str(x) for x in hlavicka))

    P = katalog()
    riadky = vsetky_riadky(P)
    r = 2
    dlhe = 0
    for riadok_dat in riadky:
        for nazov in STLPCE:
            ws.cell(row=r, column=hlavicka[nazov], value=riadok_dat[nazov])
        if len(riadok_dat["Názov"]) > 80:
            dlhe += 1
        r += 1
    wb.save(ciel)

    pocet_sady = sum(1 for p in P if sp.kvalifikuje(p))
    print(f"{len(riadky)} kariet -> {ciel}")
    print(f"  z toho {pocet_sady * 3} kariet (panel + 2 komponenty) "
          f"za {pocet_sady} produktov v sadách")
    print("  nevyplnené zámerne: Zostatok, EAN kód, Nákupná cena, Popis")
    print("  „Posielať do eshopu“ = Nie pri všetkých")
    if dlhe:
        print(f"  POZOR: {dlhe} názvov je dlhších než 80 znakov — ak ich "
              "KROS odmietne, treba ich skrátiť")


if __name__ == "__main__":
    main()

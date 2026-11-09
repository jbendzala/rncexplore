# -*- coding: utf-8 -*-
"""Doplní české preklady do Shoptetovej šablóny „Jazyky“.

Importný XML feed jazyky nepozná — v schéme nie je ani jeden jazykový
atribút a v importnom okne nie je prepínač. Preklady sa do Shoptetu
dostanú inak: cez Produkty → Export → systémový export „Jazyky“, ktorý
vypíše stĺpce typu „name:cs“. Ten súbor sa vyplní a naimportuje späť.

Stĺpce s jazykovou verziou vedia existujúce produkty len upraviť, nové
nezakladajú. Nám to vyhovuje — katalóg v obchode už je.

Zámerne nevyrábame šablónu sami a nehádame názvy stĺpcov. Berieme súbor
tak, ako ho Shoptet vyexportoval, dopíšeme do neho a hlavičku necháme
nedotknutú — vrátane poradia a prípadných stĺpcov, o ktorých nevieme.

Použitie:
    python3 tools/jazyky_csv.py ~/Downloads/export-jazyky.csv
"""
import csv
import json
import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import jazyk as jaz                                     # noqa: E402
import vystup                                           # noqa: E402
from export_shoptet import kod                          # noqa: E402
import export_shoptet_xml as X                          # noqa: E402

JAZYK = "cs"

# Popisy staviame tými istými funkciami ako slovenský import, len
# s prepnutým jazykom. Inak by česká karta mala inú stavbu než
# slovenská — iné nadpisy, inú tabuľku, chýbajúce rozbaľovače.
X.JAZYK = JAZYK
jaz.nastav(JAZYK)


def ako_v_obchode(k):
    """Kód v tej podobe, v akej ho má Shoptet.

    Pri importe si ho prepísal: veľké písmená a znaky, ktoré do adresy
    nepustí, nahradil pomlčkou. Z „LS-100FX2-Max+DC“ je tak
    „LS-100FX2-MAX-DC“ a z „2*LS-200FX2-N+FullKit“ zasa
    „2-LS-200FX2-N-FULLKIT“. Bez tejto úpravy sa spáruje 158 riadkov
    z 533 a zvyšok by zostal po slovensky.
    """
    return re.sub(r"[+*]", "-", k.strip().upper())


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))


def kluce(hlavicka):
    """Z hlavičky vytiahne stĺpce, ktoré vieme naplniť.

    Shoptet ich pomenúva „pole:jazyk“. Hľadáme teda koncovku a nie
    konkrétne názvy — keby pribudol ďalší preložiteľný stĺpec, nájde
    sa sám a nebudeme ho musieť dopisovať.
    """
    kon = ":" + JAZYK
    return [h for h in hlavicka if h and h.endswith(kon)]


# Ktoré naše pole patrí do ktorého stĺpca. Kľúč je názov stĺpca bez
# jazykovej koncovky, malými písmenami.
ZDROJE = {
    "name": lambda p: p["n"][JAZYK],
    "shortdescription": X.kratky_popis,
    "description": X.popis,
    "metadescription": X.seo_popis,
    "seotitle": lambda p: p["n"][JAZYK] + " | RnC Explore",
}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip().splitlines()[-1])
    zdroj = os.path.expanduser(sys.argv[1])
    if not os.path.exists(zdroj):
        sys.exit(f"súbor neexistuje: {zdroj}")

    P = katalog()
    # Shoptet páruje riadky podľa kódu prevedenia; názov a popis sú
    # pritom vlastnosťou produktu, takže ich dopĺňame všetkým jeho
    # prevedeniam rovnako.
    #
    # Kľúčom musí byť kód tak, ako je v obchode — teda z kod(), nie
    # holé sku. Lensun ten istý kód používa na rôzne autá; LS-100FX2-Max
    # nesie deväť panelov. Pri párovaní podľa sku si teda produkty
    # posadajú na seba a český názov sadne cudziemu autu. Pri skúške sa
    # presne to stalo: Dacia Duster dostala názov Volkswagenu Tiguan.
    podla_kodu = {}
    kolizie = 0
    for p in P:
        for v in p["var"]:
            if not v.get("sku"):
                continue
            k = ako_v_obchode(kod(p, v))
            if k in podla_kodu and podla_kodu[k] is not p:
                kolizie += 1
            podla_kodu[k] = p
    if kolizie:
        sys.exit(f"kódy sa opakujú ({kolizie}×) aj po odlíšení značkou — "
                 "párovanie by produkty pomiešalo")

    with open(zdroj, encoding="utf-8-sig", newline="") as f:
        vzorka = f.read(4096)
        f.seek(0)
        try:
            oddel = csv.Sniffer().sniff(vzorka, delimiters=";,\t").delimiter
        except csv.Error:
            oddel = ";"
        citac = csv.DictReader(f, delimiter=oddel)
        hlavicka = citac.fieldnames or []
        riadky = list(citac)

    stlpce = kluce(hlavicka)
    if not stlpce:
        sys.exit("v hlavičke nie je ani jeden stĺpec s koncovkou "
                 f"„:{JAZYK}“. Je to naozaj export „Jazyky“?\n"
                 "hlavička: " + ", ".join(hlavicka[:12]))

    kod_stlpec = next((h for h in hlavicka if h.lower() == "code"), None)
    if not kod_stlpec:
        sys.exit("v hlavičke nie je stĺpec „code“, podľa ktorého sa páruje")

    doplnene, bez_zdroja, nezname = 0, set(), 0
    for r in riadky:
        kluc = ako_v_obchode(r.get(kod_stlpec) or "")
        p = podla_kodu.get(kluc)
        if not p:
            nezname += 1
            continue
        for h in stlpce:
            pole = h[:-len(JAZYK) - 1].lower()
            fn = ZDROJE.get(pole)
            if not fn:
                bez_zdroja.add(h)
                continue
            r[h] = fn(p)
            doplnene += 1

    ciel = vystup.kam(vystup.VLOZIT, "jazyky", f"preklady-{JAZYK}.csv")
    with open(ciel, "w", encoding="utf-8-sig", newline="") as f:
        zapis = csv.DictWriter(f, fieldnames=hlavicka, delimiter=oddel)
        zapis.writeheader()
        zapis.writerows(riadky)

    print(f"{len(riadky)} riadkov -> {ciel}")
    print(f"  vyplnených buniek: {doplnene}")
    plnene = [h for h in stlpce if h not in bez_zdroja]
    print(f"  stĺpce, ktoré sme plnili: {', '.join(plnene)}")
    if bez_zdroja:
        print("  stĺpce, ku ktorým nemáme zdroj (nechali sme ich tak):")
        for h in sorted(bez_zdroja):
            print(f"    {h}")
    if nezname:
        print(f"  riadkov s kódom, ktorý v našich dátach nie je: {nezname}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Rozbije štandardnú štvoricu kombinácií (Samotný panel / Panel +
vinylová fólia / Panel + MPPT regulátor / Kompletná sada) na komponenty
a sady podľa dvoch Shoptet doplnkov, overených na pilote jedného panela
(D-Max V-Cross 100W): "Sady produktov" (dostupnosť sady sa počíta
naživo z komponentov) a "Varianty ako samostatné produkty" (zobrazí
prepojené produkty ako riadky s menom a cenou na karte).

Nie všetkých 157 produktov má túto štvoricu — len tie, ktorých zoznam
kombinácií sa presne zhoduje so štandardnými štyrmi názvami (zisťuje sa
podľa textu, nie podľa kategórie ani podľa poradia: var[0] nie je
spoľahlivo "Samotný panel" u 38 zo 157 produktov). Zvyšné produkty
(iný regulátor, predlžovací kábel, viacpanelové sady) majú iné
komponenty a nechávajú sa na samostatné posúdenie.

data/products.js sa needituje — zostáva zdrojom pre starý statický web
presne v dnešnom tvare. Všetko sa odvodí z neho tu.

Tri výstupné súbory, v tomto poradí a s týmto nastavením importu:

  1. orezanie.csv   — po jednom riadku na produkt, varianta "Samotný
                       panel". Import s nastavením "Zmeniť len produkty
                       obsiahnuté v importe a zmazať ich chýbajúce
                       varianty" — tým zmiznú zvyšné 3 natívne
                       prevedenia LEN pri týchto produktoch, nič iné
                       v obchode sa nedotkne.
  2. nove-sady.csv  — nové komponenty (fólia, regulátor — skryté,
                       špecifické pre dané auto) a nové produkty typu
                       sada (itemType=set + setItem). Import "Nemeniť
                       produkty a varianty, ktoré nie sú v súbore" —
                       len pridáva nové produkty.
  3. prepojenie.csv — až keď 1. a 2. doběhli a všetky kódy existujú:
                       doplní "Súvisiace produkty" (relatedProduct) pri
                       paneli aj pri všetkých troch sadách, aby ich
                       doplnok zobrazil pohromade. Zámerne samostatný
                       krok, nie súčasť súboru 2 — vtedy by niektoré
                       kódy, na ktoré odkazuje, ešte neexistovali.

Spustenie:  python3 tools/sady_panelov.py
"""
import hashlib
import json
import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup
from export_shoptet import kod

# Komponenty aj sady musia byť "visible" (viď riadky_nove_sady nižšie),
# takže by sa bez tohto zaradenia zdvojovali v bežnej kategórii panela.
# Založí sa ako nová kategória — v administrácii jej treba raz ručne
# vypnúť "Zobraziť v menu kategórií" aj "Viditeľnosť", aby sa
# neukazovala pri prehliadaní (sama osebe vzniknúť môže, Shoptet si ju
# pri prvom importe s neznámou cestou v defaultCategory založí sám).
SKRYTA_KATEGORIA = "Skryté – sady a komponenty"


def shoptet_kod(p, v):
    """Kód tak, ako ho má Shoptet po (pôvodnom) importe uložený — veľké
    písmená, + a * na pomlčku (rovnaký prepočet ako v
    export_shoptet_xml.py). Existujúce panely majú v kod() plus (napr.
    LS-100FX2-Max+DC), lenže ten pri CSV importe Shoptet sám premenil.
    setItem aj relatedProduct musia mieriť na TÚTO, už uloženú podobu —
    inak sa prepojenie na existujúci panel netrafí."""
    k = kod(p, v).upper()
    for znak in "+*":
        k = k.replace(znak, "-")
    return k


SAMOTNY = "Samotný panel"
FOLIA = "Panel + vinylová fólia"
MPPT = "Panel + MPPT regulátor"
KOMPLETNA = "Kompletná sada (panel + MPPT regulátor + fólia)"
STANDARD = {SAMOTNY, FOLIA, MPPT, KOMPLETNA}

DAVKA = 40
SKLAD = "0"


def pole(v, uvodzovky=True):
    if v == "" or v is None:
        return '""' if uvodzovky else ""
    return '"' + str(v).replace('"', '""') + '"'


def kod_komponentu(p, znacka):
    """Kód pre komponent, ktorý predtým ako samostatný produkt
    neexistoval (fólia/regulátor boli dosiaľ len súčasťou kombinovanej
    ceny, nie vlastným kódom) — rovnaký SHA1 vzor ako kod() v
    export_shoptet.py, aby nekolidoval so zvyškom katalógu."""
    h = hashlib.sha1(f'{p["id"]}-{znacka}'.encode("utf-8")).hexdigest()[:8].upper()
    return f"RNC-{znacka}-{h}"


def katalog():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))


def najdi(p, label):
    for v in p["var"]:
        if v["sk"] == label:
            return v
    return None


def kvalifikuje(p):
    return {v["sk"] for v in p["var"]} == STANDARD


def zapis(cesta, hlavicka, riadky):
    with open(cesta, "w", encoding="utf-8-sig", newline="") as f:
        f.write("\r\n".join([hlavicka] + riadky) + "\r\n")


def zapis_davkovane(priecinok, nazov, hlavicka, produkty, riadky_na_produkt):
    """Rovnaký dôvod ako DAVKA v export_shoptet.py — Shoptet veľký súbor
    odmietol. Dávkuje sa po produktoch (riadky_na_produkt na jeden), nie
    po riadkoch, nech sa súrodenci neroztrhnú medzi súbory."""
    davky = [produkty[i:i + DAVKA] for i in range(0, len(produkty), DAVKA)]
    for i, cast in enumerate(davky, 1):
        riadky = []
        for p in cast:
            riadky += riadky_na_produkt(p)
        c = vystup.kam(vystup.IMPORT, priecinok,
                       f"{nazov}-davka-{i}-z-{len(davky)}.csv")
        zapis(c, hlavicka, riadky)
        print(f"   {os.path.basename(c):<40} {len(cast):>3} produktov · {len(riadky):>4} riadkov")


def cena_komponentov(p):
    """Cena fólie a regulátora ako samostatných komponentov — rozdiel
    medzi cenou kombinácie a cenou samotného panela. Komponent sám
    o sebe cenovku nemá (zákazník ho nikdy nekupuje zvlášť), toto je
    len interná hodnota pre sklad/KROS."""
    panel = najdi(p, SAMOTNY)
    folia_v, mppt_v = najdi(p, FOLIA), najdi(p, MPPT)
    return {
        "folia": round(folia_v["p"] - panel["p"], 2),
        "mppt": round(mppt_v["p"] - panel["p"], 2),
    }


def kody_produktu(p):
    panel, folia_v, mppt_v, kompletna_v = (
        najdi(p, SAMOTNY), najdi(p, FOLIA), najdi(p, MPPT), najdi(p, KOMPLETNA))
    return {
        "panel": shoptet_kod(p, panel),
        "folia_komponent": kod_komponentu(p, "FOLIA"),
        "mppt_komponent": kod_komponentu(p, "MPPT"),
        "sada_folia": shoptet_kod(p, folia_v),
        "sada_mppt": shoptet_kod(p, mppt_v),
        "sada_kompletna": shoptet_kod(p, kompletna_v),
    }


HLAVICKA_1 = ('code;pairCode;name;guid;price;standardPrice;purchasePrice;'
              'actionPrice;actionFrom;actionUntil;"variant:Prevedenie";stock;')
HLAVICKA_2 = ('code;name;guid;price;standardPrice;purchasePrice;'
              'actionPrice;actionFrom;actionUntil;stock;weight;productVisibility;'
              'defaultCategory;itemType;setItem;setItem2;setItem3;')
HLAVICKA_3 = "code;relatedProduct;relatedProduct2;relatedProduct3;"
HLAVICKA_OPRAVA = "code;weight;productVisibility;defaultCategory;"


def riadky_orezanie(p):
    k = kody_produktu(p)
    v = najdi(p, SAMOTNY)
    cena = f'{v["p"]:.2f}'.replace(".", ",")
    return [";".join([
        pole(k["panel"]), pole("", False), pole(p["n"]["sk"]),
        pole("", False), pole(cena), pole(""), pole(""), pole(""),
        pole("", False), pole("", False), pole("", False), pole(SKLAD), "",
    ])]


def riadky_nove_sady(p):
    """Shoptet vyžaduje, aby VŠETKY položky sady (aj samotný panel) mali
    úplne rovnakú viditeľnosť ako sada sama — potvrdené chybovou
    hláškou pri ručnom ukladaní ("Viditeľnosť všetkých položiek musí
    byť v súlade s viditeľnosťou sady"), nie je to voľba, dá sa to
    obísť jedine takto. Keďže panel musí zostať "Viditeľný" (je to
    hlavný produkt v kategórii), musia byť "Viditeľné" aj fólia,
    regulátor a všetky 3 sady — inak sa sada nedá zviditeľniť vôbec,
    ani cez import, ani ručne.

    Aby fólia/regulátor/sady nezdvojovali ponuku pri prehliadaní
    kategórie panela, idú do vlastnej SKRYTEJ kategórie namiesto tej
    panelovej — vo vyhľadávaní na webe sa teoreticky objaviť môžu
    (viditeľný produkt je viditeľný produkt), to sa pri tomto obmedzení
    Shoptetu úplne vylúčiť nedá.

    Hmotnosť komponentov nemáme rozpísanú zvlášť (Lensun ju vedie len
    na celý balík), necháme 0. Sady majú hmotnosť tú istú, čo balík
    panela — fyzicky ide o ten istý box."""
    k = kody_produktu(p)
    panel, folia_v, mppt_v = najdi(p, SAMOTNY), najdi(p, FOLIA), najdi(p, MPPT)
    kompletna_v = najdi(p, KOMPLETNA)
    ck = cena_komponentov(p)
    cena_folia_komp, cena_mppt_komp = ck["folia"], ck["mppt"]
    hmotnost = p.get("kg") or 0
    kat = SKRYTA_KATEGORIA

    def riadok(code, name, price, viditelnost, vaha=0, set_items=()):
        # "kód;1.00" — kód položky a počet kusov v jednej bunke, oddelené
        # bodkočiarkou (zistené z reálneho príkladu, oficiálna dokumentácia
        # formát nepíše). Keďže bodkočiarka je zároveň oddeľovač stĺpcov
        # CSV, MUSÍ to ísť v úvodzovkách (pole() s predvoleným True) —
        # predtým to bolo bez úvodzoviek aj bez množstva, Shoptet si
        # množstvo dosadil na 0 a sadu to urobilo neuložiteľnou.
        si = [f"{c};1.00" for c in set_items] + [""] * (3 - len(set_items))
        cena = f'{price:.2f}'.replace(".", ",")
        return ";".join([
            pole(code), pole(name), pole("", False), pole(cena),
            pole(""), pole(""), pole(""), pole("", False), pole("", False),
            pole(SKLAD), pole(vaha, False), pole(viditelnost, False), pole(kat),
            pole("set" if set_items else "", False),
            pole(si[0]) if si[0] else pole("", False),
            pole(si[1]) if si[1] else pole("", False),
            pole(si[2]) if si[2] else pole("", False),
        ])

    # Komponenty NESMÚ byť "hidden" — Shoptet skryje aj celú sadu, ak
    # obsahuje čo i len jeden skrytý produkt (zdokumentované správanie
    return [
        riadok(k["folia_komponent"], f'{p["n"]["sk"]} – Vinylová fólia (komponent)',
               cena_folia_komp, "visible"),
        riadok(k["mppt_komponent"], f'{p["n"]["sk"]} – MPPT regulátor (komponent)',
               cena_mppt_komp, "visible"),
        riadok(k["sada_folia"], f'{p["n"]["sk"]} – {FOLIA}',
               folia_v["p"], "visible", hmotnost, [k["panel"], k["folia_komponent"]]),
        riadok(k["sada_mppt"], f'{p["n"]["sk"]} – {MPPT}',
               mppt_v["p"], "visible", hmotnost, [k["panel"], k["mppt_komponent"]]),
        riadok(k["sada_kompletna"], f'{p["n"]["sk"]} – {KOMPLETNA}',
               kompletna_v["p"], "visible", hmotnost,
               [k["panel"], k["folia_komponent"], k["mppt_komponent"]]),
    ]


def riadky_oprava(p):
    """Malý dodatočný krok pre tých 540 položiek, čo už boli nahraté
    predošlými behmi nove-sady.csv — aktualizuje len hmotnosť,
    viditeľnosť a kategóriu, nič iné sa nemení."""
    k = kody_produktu(p)
    hmotnost = p.get("kg") or 0
    riadky = [
        ";".join([pole(k["folia_komponent"]), pole(0, False), pole("visible", False), pole(SKRYTA_KATEGORIA)]),
        ";".join([pole(k["mppt_komponent"]), pole(0, False), pole("visible", False), pole(SKRYTA_KATEGORIA)]),
    ]
    for kluc in ("sada_folia", "sada_mppt", "sada_kompletna"):
        riadky.append(";".join([pole(k[kluc]), pole(hmotnost, False), pole("visible", False), pole(SKRYTA_KATEGORIA)]))
    return riadky


def riadky_prepojenie(p):
    k = kody_produktu(p)
    sady = [k["sada_folia"], k["sada_mppt"], k["sada_kompletna"]]
    riadky = [";".join([pole(k["panel"])] + [pole(x, False) for x in sady])]
    for i, vlastny in enumerate(sady):
        ostatne = [k["panel"]] + [s for j, s in enumerate(sady) if j != i]
        riadky.append(";".join([pole(vlastny)] + [pole(x, False) for x in ostatne]))
    return riadky


def main():
    P = katalog()
    produkty = [p for p in P if kvalifikuje(p)]
    print(f"{len(produkty)} z {len(P)} produktov má presne štandardnú "
          f"štvoricu kombinácií — len tie sa menia.\n")

    c1 = vystup.kam(vystup.IMPORT, "sady-panelov", "orezanie.csv")
    zapis(c1, HLAVICKA_1, [r for p in produkty for r in riadky_orezanie(p)])
    print(f"1. orezanie na 1 prevedenie -> {c1}")
    print('   import s nastavením "Zmeniť len produkty obsiahnuté v importe a '
          'zmazať ich chýbajúce varianty":')
    zapis_davkovane("sady-panelov", "orezanie", HLAVICKA_1, produkty, riadky_orezanie)

    c2 = vystup.kam(vystup.IMPORT, "sady-panelov", "nove-sady.csv")
    zapis(c2, HLAVICKA_2, [r for p in produkty for r in riadky_nove_sady(p)])
    print(f"\n2. nové komponenty a sady (5 na produkt) -> {c2}")
    print('   import s nastavením "Nemeniť produkty a varianty, ktoré nie sú '
          'v súbore" — len pridáva:')
    zapis_davkovane("sady-panelov", "nove-sady", HLAVICKA_2, produkty, riadky_nove_sady)

    c3 = vystup.kam(vystup.IMPORT, "sady-panelov", "prepojenie.csv")
    zapis(c3, HLAVICKA_3, [r for p in produkty for r in riadky_prepojenie(p)])
    print(f"\n3. prepojenie súvisiacich produktov (4 na produkt) -> {c3}")
    print('   import "Nemeniť produkty a varianty, ktoré nie sú v súbore" — '
          "spustiť AŽ po tom, čo 1. a 2. doběhli:")
    zapis_davkovane("sady-panelov", "prepojenie", HLAVICKA_3, produkty, riadky_prepojenie)

    c4 = vystup.kam(vystup.IMPORT, "sady-panelov", "oprava-hmotnost-viditelnost.csv")
    zapis(c4, HLAVICKA_OPRAVA, [r for p in produkty for r in riadky_oprava(p)])
    print(f"\n4. oprava pre už nahraté položky z predošlého behu nove-sady.csv "
          f"(chýbala im hmotnosť a viditeľnosť) -> {c4}")
    print('   import "Nemeniť produkty a varianty, ktoré nie sú v súbore" — '
          "len doplní tieto dve polia na existujúcich 540 položkách")

    print(f"\nspolu: {len(produkty)} orezaných produktov, "
          f"{5 * len(produkty)} nových (komponenty + sady)")


if __name__ == "__main__":
    main()

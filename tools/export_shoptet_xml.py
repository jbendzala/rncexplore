# -*- coding: utf-8 -*-
"""Vypíše obsah produktov do XML vo formáte, aký Shoptet sám exportuje.

CSV import založil produkty, ceny a prevedenia — ale popisy, fotografie,
zaradenie do kategórií ani parametre neprenáša. Toto je druhý krok:
doplní presne to, čo v obchode chýba.

Hmotnosť posielame z poľa kg, nie z technického listu. Lensun uvádza
čistú hmotnosť panela (1 až 3,5 kg pri paneloch na kapotu), ale prepravca
účtuje zásielku — a tá je tvrdý obal veľkosti 1,4 × 0,5 m. Pole kg je
odhad prepravnej hmotnosti a je trojnásobok až desaťnásobok čistej, čo
tomu zodpovedá. Čistú hmotnosť zákazník vidí v tabuľke parametrov.

Sú to odhady, nie vážené čísla. Keď klient zváži jednu skutočnú zásielku
od každej veľkosti, prepočítame ich.

Produkty sa nezakladajú znova. Shoptet páruje podľa kódu prevedenia, a
kódy už v obchode sú — len ich pri importe premenil na veľké písmená a
plus nahradil pomlčkou. Preto ich tu vypisujeme v tej istej podobe, inak
by sa katalóg založil druhý raz.

Súbory si pred odovzdaním sami overíme proti schéme Shoptetu, ktorá je
v tools/shoptet-schema. Import totiž odmietne celý feed jednou vetou,
bez riadka a bez názvu prvku — hľadať chybu až v obchode je drahé.

Cenu zámerne neposielame. V obchode je správna (maloobchodná s DPH) a
pri opakovanom zápise by sa dala pokaziť, keby import číslo pochopil ako
cenu bez DPH. Tento súbor nesie iba obsah.
"""
import html, json, os, re, subprocess, sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo
from export_shopify import telo          # popis v HTML — rovnaký ako pre Shopify
from export_shoptet import kod, PARAMETER, DAVKA

CIEL = os.path.expanduser("~/Documents/rncexplore-shoptet-obsah.xml")
VYROBCA = "LensunSolar"

# Či import pochopí popisy, fotografie a kategórie tak, ako čakáme, sa
# z exportu obchodu vyčítať nedá — tie polia sú tam prázdne, tak ich
# Shoptet nevypísal. Preto píšeme aj súbor s jediným produktom: skúška
# na ňom nič nestojí a ukáže, čo import naozaj spraví. Vybraný je
# Discovery Sport, ktorý má štyri prevedenia, osem fotografií a opravené
# štítky prevedení — na ňom je teda vidieť aj to, že sa párovanie trafilo.
SKUSKA = "land-rover-discovery-sport-lensun-100w-bonnet-solar-panel"


def shoptet_kod(p, v):
    """Kód v podobe, akú z neho urobil Shoptet pri importe CSV.

    Odpozerané z exportu obchodu: veľké písmená, plus aj zvieračka na
    pomlčku, medzery zostávajú (LS-75FX2-RG - 60FX2-RG-D185 je v obchode
    s medzerami). Zvieračka je v katalógu jediná — 2*LS-200FX2-N+FullKit —
    a práve na nej sa párovanie prvý raz netrafilo.
    """
    k = kod(p, v).upper()
    for znak in "+*":
        k = k.replace(znak, "-")
    return k


def e(x):
    return html.escape(str(x), quote=True)


def prvá_veta(t):
    """Krátky popis — prvá veta dlhého. Shoptet ho dáva nad fotografiu."""
    m = re.match(r"(.+?[.!?])(\s|$)", t.strip(), re.S)
    return (m.group(1) if m else t).strip()


def prevedenie(p, v, odsadenie, s_parametrom):
    r, o = [], " " * odsadenie
    r.append(f"{o}<CODE>{e(shoptet_kod(p, v))}</CODE>")
    r.append(f"{o}<UNIT>ks</UNIT>")
    r.append(f"{o}<LOGISTIC><WEIGHT>{p['kg']}</WEIGHT></LOGISTIC>")
    if s_parametrom:
        r.append(f"{o}<PARAMETERS><PARAMETER>")
        r.append(f"{o}  <NAME>{e(PARAMETER)}</NAME>")
        r.append(f"{o}  <VALUE>{e(v['sk'])}</VALUE>")
        r.append(f"{o}</PARAMETER></PARAMETERS>")
    return r


# Značku vozidla nemožno dať do MANUFACTURER — tam patrí LensunSolar a
# potrebujeme ho tak pre Heureku a Google. Preto je značka podkategóriou.
# Delíme len panely na kapotu: tých je 103 a každý patrí ku konkrétnemu
# autu. Flexibilné panely a panely pre strešné stany sú univerzálne, tam
# by podkategória podľa značky nemala čo znamenať.
DELIT = {"hood"}


def cesty(p, kategoria):
    """Kategórie produktu. Shoptet vnorenie zapisuje cez „>“ a strom si
    vytvorí sám. Rodiča vypisujeme zvlášť, aby sa produkt objavil aj v ňom
    bez ohľadu na to, či je v obchode zapnuté dedenie z podkategórií."""
    if p["cat"] in DELIT and p.get("b"):
        podkat = f'{kategoria} > {p["b"]}'
        return [kategoria, podkat], podkat
    return [kategoria], kategoria


def seo_popis(p):
    """Popis do výsledkov vyhľadávania. Google ukáže asi 155 znakov, zvyšok
    odreže — tak ho režeme sami, a na hranici slova, nie v polovici."""
    t = p["d"]["sk"]
    if len(t) <= 155:
        return t
    kus = t[:155]
    return kus[:kus.rfind(" ")].rstrip(" ,;–-") + "…"


def shopitem(p, kategoria):
    viac = len(p["var"]) > 1
    r = ["  <SHOPITEM>"]
    r.append(f"    <NAME>{e(p['n']['sk'])}</NAME>")
    r.append(f"    <SHORT_DESCRIPTION>{e(prvá_veta(p['d']['sk']))}</SHORT_DESCRIPTION>")
    r.append(f"    <DESCRIPTION>{e(telo(p))}</DESCRIPTION>")
    r.append(f"    <MANUFACTURER>{e(VYROBCA)}</MANUFACTURER>")
    # Titulok a popis pre vyhľadávače. Bez nich dá Shoptet každému produktu
    # predvolený titulok a Google si popis vyberie sám z čohokoľvek na
    # stránke. Titulok dopĺňame firmou, aby bol v zoznamoch rozpoznateľný.
    r.append(f"    <SEO_TITLE>{e(p['n']['sk'] + ' | RnC Explore')}</SEO_TITLE>")
    r.append(f"    <META_DESCRIPTION>{e(seo_popis(p))}</META_DESCRIPTION>")
    if p.get("v"):
        r.append("    <RELATED_VIDEOS><RELATED_VIDEO>"
                 f"<YOUTUBE_VIDEO_CODE>{e(p['v'])}</YOUTUBE_VIDEO_CODE>"
                 "</RELATED_VIDEO></RELATED_VIDEOS>")
    zoznam, hlavna = cesty(p, kategoria)
    r.append("    <CATEGORIES>")
    r += [f"      <CATEGORY>{e(k)}</CATEGORY>" for k in zoznam]
    r.append(f"      <DEFAULT_CATEGORY>{e(hlavna)}</DEFAULT_CATEGORY>")
    r.append("    </CATEGORIES>")

    obrazky = p.get("img") or []
    if obrazky:
        r.append("    <IMAGES>")
        r += [f"      <IMAGE>{e(u)}</IMAGE>" for u in obrazky]
        r.append("    </IMAGES>")

    # Parametre na úrovni produktu. PARAMETERS tu nesmie byť — schéma ho
    # pripúšťa len vnútri prevedenia, kde určuje jeho kombináciu. Pre údaje
    # o celom produkte má Shoptet INFORMATION_PARAMETERS.
    par = [("Výkon", f"{p['w']} W")] if p.get("w") else []
    if p.get("b"):
        par.append(("Značka vozidla", p["b"]))
    if par:
        r.append("    <INFORMATION_PARAMETERS>")
        for a, b in par:
            r.append(f"      <INFORMATION_PARAMETER><NAME>{e(a)}</NAME>"
                     f"<VALUE>{e(b)}</VALUE></INFORMATION_PARAMETER>")
        r.append("    </INFORMATION_PARAMETERS>")

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


# Validujeme proti complete, nie supplier: SEO_TITLE, META_DESCRIPTION a
# RELATED_VIDEOS supplier nepozná. Complete je nadmnožina, takže nič
# nestrácame.
SCHEMA = os.path.join(TU, "shoptet-schema", "products-complete-v10.rng")


def over(cesta):
    """Nechá súbor skontrolovať tou istou schémou, akou ho kontroluje Shoptet.

    Import odmietne celý feed jednou vetou, bez riadka a bez názvu prvku.
    xmllint povie presne, čo je zle — preto to robíme tu a nie až v obchode.
    """
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


def zapis(cesta, produkty, nazvy):
    r = ['<?xml version="1.0" encoding="UTF-8"?>', "<SHOP>"]
    for p in produkty:
        r += shopitem(p, nazvy[p["cat"]])
    r.append("</SHOP>")
    with open(cesta, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(r) + "\n")


def main():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});", s, re.S).group(1))
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))
    nazvy = {c["k"]: c["sk"] for c in meta["cats"]}

    zapis(CIEL, P, nazvy)
    fotiek = sum(len(p.get("img") or []) for p in P)
    prevedeni = sum(len(p["var"]) for p in P)
    print(f"{len(P)} produktov, {prevedeni} prevedení, {fotiek} fotografií "
          f"-> {CIEL}\n   {over(CIEL)}")

    skus = [p for p in P if p["id"] == SKUSKA]
    c = os.path.expanduser("~/Documents/rncexplore-shoptet-obsah-skuska.xml")
    zapis(c, skus, nazvy)
    print(f"\nna skúšku jeden produkt -> {c}\n   {over(c)}")

    # Po dávkach, z tej istej opatrnosti ako pri CSV — a tu navyše preto,
    # že 857 fotografií si Shoptet musí sám stiahnuť.
    davky = [P[i:i + DAVKA] for i in range(0, len(P), DAVKA)]
    print(f"\npo dávkach (najviac {DAVKA} produktov na súbor):")
    for i, cast in enumerate(davky, 1):
        c = os.path.expanduser(f"~/Documents/rncexplore-shoptet-obsah-{i}-z-{len(davky)}.xml")
        zapis(c, cast, nazvy)
        print(f"  {os.path.basename(c):<40} {len(cast):>3} produktov · "
              f"{sum(len(p.get('img') or []) for p in cast):>3} fotografií · "
              f"{over(c)}")


if __name__ == "__main__":
    main()

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
import vystup
from export_shopify import PORADIE   # popisky máme vlastné, po jazykoch
from export_shoptet import kod, DAVKA
from pages_content import REVIEWS

CIEL = vystup.kam(vystup.IMPORT, "obsah-xml", "obsah.xml")
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
    """Prvá veta popisu.

    Bodka sama o sebe vetu nekončí: „Dacia Duster 3. generácia“ má bodku
    v poradovej číslovke a naivné delenie z toho urobí „…vozidla Dacia
    Duster 3.“ Vetu preto končíme len tam, kde za bodkou nasleduje medzera
    a veľké písmeno, a kde pred ňou nie je číslica.
    """
    t = t.strip()
    m = re.search(r"(?<!\d)[.!?](?=\s+[A-ZÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ])", t)
    return t[:m.end()].strip() if m else t


def prevedenie(p, v, odsadenie, s_parametrom):
    r, o = [], " " * odsadenie
    r.append(f"{o}<CODE>{e(shoptet_kod(p, v))}</CODE>")
    r.append(f"{o}<UNIT>ks</UNIT>")
    r.append(f"{o}<LOGISTIC><WEIGHT>{p['kg']}</WEIGHT></LOGISTIC>")
    if s_parametrom:
        r.append(f"{o}<PARAMETERS><PARAMETER>")
        r.append(f"{o}  <NAME>{e(t('parameter'))}</NAME>")
        r.append(f"{o}  <VALUE>{e(v[JAZYK])}</VALUE>")
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
    podľa toho vytvorí — a aj prestaví, takže cesta musí byť úplná,
    vrátane koreňa. Rodiča vypisujeme zvlášť, aby sa produkt objavil aj
    v ňom bez ohľadu na to, či je zapnuté dedenie z podkategórií."""
    koren = t("koren")
    k = f"{koren} > {kategoria}" if koren else kategoria
    if p["cat"] in DELIT and p.get("b"):
        podkat = f'{k} > {p["b"]}'
        return [k, podkat], podkat
    return [k], k


# Recenzie zákazníkov podľa adresy produktu. Máme ich tri zo 157, takže
# sekciu „Skúsenosť zákazníka“ z návrhu dostanú len tie tri — prázdny rám
# na zvyšných 154 kartách by vyzeral horšie než žiadny.
RECENZIE = {r["pid"]: r for r in REVIEWS}

# Jazyk exportu. Dáta produktov nesú „sk“ aj „cs“ pri názve, popise,
# obsahu balenia aj prevedení — prepne sa teda celý obsah, nielen
# nadpisy. Nastavuje sa prvým argumentom: „python3 … cs“.
JAZYK = "sk"

# Texty, ktoré sú v návrhu rovnaké pri každom produkte, a nadpisy
# rozbaľovačov. Adresy odkazov nechávame rovnaké — česká mutácia má
# vlastné stránky, ale ak im klient nechá tie isté adresy, sadnú.
SLOVA = {
    "sk": {
        "montaz": "Priemerne zručný človek panel nalepí za jednu až dve "
                  "hodiny a nepotrebuje špeciálne náradie.",
        "zapojenie": "Panel, regulátor aj káble nájdete pokope. Pri otázkach "
                     "vám poradí náš odborný tím.",
        "objednavka": "Vyberiete produkt a prevedenie, vložíte ho do košíka "
                      "a objednáte. Faktúru pošleme e-mailom a tovar "
                      "odošleme po úhrade.",
        "na_mieru": "Ak v ponuke nenájdete svoje vozidlo, panel vyrobíme "
                    "na mieru.",
        "h_montaz": "Montáž",
        "h_zapojenie": "Čo potrebujete k zapojeniu",
        "h_balenie": "Obsah balenia",
        "h_objednavka": "Objednávka a platba",
        "h_na_mieru": "Iné vozidlo alebo rozmer",
        "h_detaily": "Detaily produktu",
        "h_technicke": "Technické údaje",
        "h_recenzia": "Skúsenosť zákazníka",
        "znacka": "Značka vozidla",
        "odkaz_montaz": "Postup montáže krok za krokom →",
        "odkaz_na_mieru": "Panely na mieru →",
        "tvarovany": "Tvarovaný na",
        "ine_vozidlo": "Iné vozidlo? Na mieru",
        "zdroj_recenzie": "recenzia z lensunsolar.com, preložená a skrátená",
        "parameter": "Prevedenie",
        "koren": "Produkty",
        "popisky": {"w": "Výkon", "eff": "Účinnosť článkov",
                    "vmp": "Napätie pri max. výkone",
                    "imp": "Prúd pri max. výkone", "voc": "Napätie naprázdno",
                    "isc": "Skratový prúd", "vsys": "Max. napätie sústavy",
                    "dim": "Rozmer", "kg": "Hmotnosť",
                    "jbox": "Pripojovacia skrinka"},
    },
    "cs": {
        "montaz": "Průměrně zručný člověk panel nalepí za jednu až dvě "
                  "hodiny a nepotřebuje speciální nářadí.",
        "zapojenie": "Panel, regulátor i kabely najdete pohromadě. "
                     "Při dotazech vám poradí náš odborný tým.",
        "objednavka": "Vyberete produkt a provedení, vložíte ho do košíku "
                      "a objednáte. Fakturu pošleme e-mailem a zboží "
                      "odešleme po úhradě.",
        "na_mieru": "Pokud v nabídce nenajdete své vozidlo, panel vyrobíme "
                    "na míru.",
        "h_montaz": "Montáž",
        "h_zapojenie": "Co potřebujete k zapojení",
        "h_balenie": "Obsah balení",
        "h_objednavka": "Objednávka a platba",
        "h_na_mieru": "Jiné vozidlo nebo rozměr",
        "h_detaily": "Detaily produktu",
        "h_technicke": "Technické údaje",
        "h_recenzia": "Zkušenost zákazníka",
        "znacka": "Značka vozidla",
        "odkaz_montaz": "Postup montáže krok za krokem →",
        "odkaz_na_mieru": "Panely na míru →",
        "tvarovany": "Tvarovaný na",
        "ine_vozidlo": "Jiné vozidlo? Na míru",
        "zdroj_recenzie": "recenze z lensunsolar.com, přeložená a zkrácená",
        "parameter": "Provedení",
        "koren": "Produkty",
        "popisky": {"w": "Výkon", "eff": "Účinnost článků",
                    "vmp": "Napětí při max. výkonu",
                    "imp": "Proud při max. výkonu", "voc": "Napětí naprázdno",
                    "isc": "Zkratový proud", "vsys": "Max. napětí soustavy",
                    "dim": "Rozměr", "kg": "Hmotnost",
                    "jbox": "Připojovací skříňka"},
    },
}


def t(kluc):
    """Text v jazyku exportu."""
    return SLOVA[JAZYK][kluc]


def vozidlo(p):
    """Z názvu vytiahne vozidlo — časť pred pomlčkou.

    „Dacia Duster 1. generácia (2010–2017) – 100W solárny panel na kapotu“
    dá „Dacia Duster 1. generácia (2010–2017)“. Univerzálne panely bez auta
    v názve pomlčku nemajú a vrátia nič.
    """
    if not p.get("b"):
        return ""
    casti = p["n"][JAZYK].split(" – ")
    return casti[0].strip() if len(casti) > 1 else ""


def kratky_popis(p):
    """Krátky popis. CSS ho na karte posúva nad cenu, takže je to prvé, čo
    zákazník prečíta — návrh tam má vetu o produkte a riadok s vozidlom."""
    r = [f"<p>{e(prvá_veta(p['d'][JAZYK]))}</p>"]
    auto = vozidlo(p)
    if auto:
        r.append(f'<p class="rnc-fit">{e(t("tvarovany"))} '
                 f'<strong>{e(auto)}</strong> · '
                 f'<a href="/na-mieru/">{e(t("ine_vozidlo"))}</a></p>')
    return "".join(r)


def rozbal(nadpis, telo_html):
    return (f"<details><summary>{e(nadpis)}</summary>{telo_html}</details>")


def popis(p):
    """Popis produktu v podobe, akú má návrh: veta, tabuľka parametrov a
    rozbaľovače. Shoptet to zobrazí v záložke, CSS zo záložky urobí sekciu.

    Štyri výhody („Prečo panel na kapotu“) tu nie sú zámerne — tie Shoptet
    vykresľuje sám cez benefitBanner a nastavujú sa v administrácii.
    """
    c = [f"<p>{e(p['d'][JAZYK])}</p>"]

    spec = p.get("spec") or {}
    riadky = [(t('popisky')[k], spec[k]) for k in PORADIE if spec.get(k)]
    if p.get("b"):
        riadky.append((t("znacka"), p["b"]))
    c.append(f'<h2>{e(t("h_detaily"))}</h2>')
    if riadky:
        c.append(f"<h3>{e(t('h_technicke'))}</h3><table>")
        c += [f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in riadky]
        c.append("</table>")

    c.append(rozbal(t("h_montaz"), f"<p>{t('montaz')}</p>"
                    f'<p><a href="/montaz/">{e(t("odkaz_montaz"))}</a></p>'))
    c.append(rozbal(t("h_zapojenie"), f"<p>{t('zapojenie')}</p>"))
    if p.get("pack"):
        polozky = "".join(f"<li>{e(r[JAZYK])}</li>" for r in p["pack"])
        c.append(rozbal(t("h_balenie"), f"<ul>{polozky}</ul>"))
    c.append(rozbal(t("h_objednavka"), f"<p>{t('objednavka')}</p>"))
    c.append(rozbal(t("h_na_mieru"), f"<p>{t('na_mieru')}</p>"
                    f'<p><a href="/na-mieru/">{e(t("odkaz_na_mieru"))}</a></p>'))

    rec = RECENZIE.get(p["id"])
    if rec:
        c.append(f'<h2>{e(t("h_recenzia"))}</h2>'
                 f'<blockquote class="rnc-review"><p>{e(rec[JAZYK])}</p>'
                 f'<footer><strong>{e(rec["who"])}</strong> · {e(rec["car"])} · '
                 f'{e(t("zdroj_recenzie"))}</footer>'
                 '</blockquote>')
    return "".join(c)


def seo_popis(p):
    """Popis do výsledkov vyhľadávania. Google ukáže asi 155 znakov, zvyšok
    odreže — tak ho režeme sami, a na hranici slova, nie v polovici."""
    t = p["d"][JAZYK]
    if len(t) <= 155:
        return t
    kus = t[:155]
    return kus[:kus.rfind(" ")].rstrip(" ,;–-") + "…"


def shopitem(p, kategoria):
    viac = len(p["var"]) > 1
    r = ["  <SHOPITEM>"]
    r.append(f"    <NAME>{e(p['n'][JAZYK])}</NAME>")
    r.append(f"    <SHORT_DESCRIPTION>{e(kratky_popis(p))}</SHORT_DESCRIPTION>")
    r.append(f"    <DESCRIPTION>{e(popis(p))}</DESCRIPTION>")
    r.append(f"    <MANUFACTURER>{e(VYROBCA)}</MANUFACTURER>")
    # Štítok „Z recenzie“ na kachličke. Shoptet má šesť voľných príznakov,
    # custom1 je prvý — jeho názov sa nastavuje v administrácii.
    if p["id"] in RECENZIE:
        r.append("    <FLAGS><FLAG><CODE>custom1</CODE>"
                 "<ACTIVE>1</ACTIVE></FLAG></FLAGS>")
    # Titulok a popis pre vyhľadávače. Bez nich dá Shoptet každému produktu
    # predvolený titulok a Google si popis vyberie sám z čohokoľvek na
    # stránke. Titulok dopĺňame firmou, aby bol v zoznamoch rozpoznateľný.
    r.append(f"    <SEO_TITLE>{e(p['n'][JAZYK] + ' | RnC Explore')}</SEO_TITLE>")
    r.append(f"    <META_DESCRIPTION>{e(seo_popis(p))}</META_DESCRIPTION>")
    # Video je v poli vid, nie v. Pole v je napätie panela (12 V, 36 V) —
    # to tu nemá čo robiť a raz sa tak už stalo.
    if p.get("vid"):
        r.append("    <RELATED_VIDEOS><RELATED_VIDEO>"
                 f"<YOUTUBE_VIDEO_CODE>{e(p['vid'])}</YOUTUBE_VIDEO_CODE>"
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
    # Výkon tu zámerne nie je, hoci by sa sem hodil.
    #
    # Shoptet si z informačných parametrov založí hodnoty filtra. Pri
    # výkone to znamenalo 38 hodnôt — 36 W, 40 W, 45 W, 46 W… — a vo
    # výpise z toho bol zoznam 25 políčok v náhodnom poradí, v ktorom
    # sa nedá nič nájsť. Výkon preto do filtra ide osobitne v pásmach
    # (tools/filtre_csv.py) a presné wattáže zostávajú v tabuľke
    # technických údajov v popise, kam patria.
    par = []
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
    global JAZYK
    if len(sys.argv) > 1:
        if sys.argv[1] not in SLOVA:
            sys.exit(f"neznámy jazyk {sys.argv[1]!r}; poznám "
                     + ", ".join(SLOVA))
        JAZYK = sys.argv[1]
    # Slovenčina ide do pôvodného priečinka, aby staré postupy sedeli;
    # čeština vedľa, nech sa súbory nezamiešajú.
    priecinok = "obsah-xml" if JAZYK == "sk" else f"obsah-xml-{JAZYK}"

    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});", s, re.S).group(1))
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))
    nazvy = {c["k"]: c[JAZYK] for c in meta["cats"]}

    ciel = vystup.kam(vystup.IMPORT, priecinok, "obsah.xml")
    zapis(ciel, P, nazvy)
    fotiek = sum(len(p.get("img") or []) for p in P)
    prevedeni = sum(len(p["var"]) for p in P)
    print(f"jazyk: {JAZYK}")
    print(f"{len(P)} produktov, {prevedeni} prevedení, {fotiek} fotografií "
          f"-> {ciel}\n   {over(ciel)}")

    skus = [p for p in P if p["id"] == SKUSKA]
    c = vystup.kam(vystup.IMPORT, priecinok, "skuska-jeden-produkt.xml")
    zapis(c, skus, nazvy)
    print(f"\nna skúšku jeden produkt -> {c}\n   {over(c)}")

    # Po dávkach, z tej istej opatrnosti ako pri CSV — a tu navyše preto,
    # že 857 fotografií si Shoptet musí sám stiahnuť.
    davky = [P[i:i + DAVKA] for i in range(0, len(P), DAVKA)]
    print(f"\npo dávkach (najviac {DAVKA} produktov na súbor):")
    for i, cast in enumerate(davky, 1):
        c = vystup.kam(vystup.IMPORT, priecinok,
                       f"davka-{i}-z-{len(davky)}.xml")
        zapis(c, cast, nazvy)
        print(f"  {os.path.basename(c):<40} {len(cast):>3} produktov · "
              f"{sum(len(p.get('img') or []) for p in cast):>3} fotografií · "
              f"{over(c)}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Vypíše stránky webu do čistého HTML na vloženie do Shoptetu.

Stránky na našom webe sú napísané s našimi CSS triedami, formulármi a
ikonami. Vložiť ich do Shoptetu tak, ako sú, by nefungovalo: triedy tam
neexistujú a formuláre posielajú poštu na náš Cloudflare Worker, ktorý
po prechode nebude mať dôvod bežať. Shoptet má navyše vlastný kontaktný
formulár aj vlastnú registráciu veľkoobchodu.

Preto z každej stránky zostane len obsah — nadpisy, odseky, zoznamy,
odkazy — a to v značke, ktorú redakčný systém zvládne.

Jedna vec, ktorú treba spraviť a nie je vidieť: firemné údaje na webe
dopĺňa JavaScript do prázdnych <span class="js-ico"> a podobne. Tu ten
skript nebeží, takže ich dosadíme z config.js. Inak by v obchodných
podmienkach boli prázdne miesta namiesto IČO a adresy.

Spustenie:  python3 tools/export_stranky.py
"""
import html, os, re, sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo
import pages_content as pc
from build import catalog_counts

CIEL = os.path.expanduser("~/Documents/rncexplore-shoptet-stranky")

# Ktoré stránky vyviezť a ako sa budú volať súbory. Košík, katalóg ani
# domovskú stránku nevyvážame — tie si Shoptet robí sám.
STRANKY = [
    ("o_nas",       "o-nas",               "O nás",               "O nás"),
    ("montaz",      "montaz",              "Montáž",              "Montáž"),
    ("faq",         "faq",                 "Časté otázky",        "Časté otázky"),
    ("velkoobchod", "velkoobchod",         "Veľkoobchod",         "Velkoobchod"),
    ("na_mieru",    "na-mieru",            "Na mieru",            "Na míru"),
    ("kontakt",     "kontakt",             "Kontakt",             "Kontakt"),
    ("podmienky",   "obchodne-podmienky",  "Obchodné podmienky",  "Obchodní podmínky"),
]

# Značky, ktoré si obsah nesie: nadpisy, text, zoznamy, tabuľky, odkazy.
# Všetko ostatné je naša úprava stránky alebo ovládací prvok a ide von.
NECHAT = {"h2", "h3", "h4", "p", "ul", "ol", "li", "table", "thead", "tbody",
          "tr", "th", "td", "strong", "em", "b", "i", "br", "a", "img", "blockquote"}

# Celé bloky, ktoré sa vyhadzujú s obsahom — formuláre a ikony.
VON_S_OBSAHOM = ["form", "button", "svg", "select", "textarea", "label",
                 "script", "style", "noscript"]

# Prázdne <span>, do ktorých na webe JavaScript dopĺňa údaje firmy.
UDAJE = {
    "js-company": "company", "js-street": "street", "js-city": "city",
    "js-ico": "ico", "js-dic": "dic", "js-icdph": "icDph",
    "js-hours": "hours", "js-phone": "phone", "js-web": "web",
    "js-mail": "mail", "js-info": "infoEmail",
}


# Odkazy na stránky nášho webu. V Shoptete majú iné adresy, a tie, pre
# ktoré tam náhrada nie je, sa zo značky vypustia a zostane len text.
ODKAZY = {
    "produkty.html": "/panely-na-kapotu/",
    "index.html": "/",
    "kontakt.html": "/kontakt/",
    "montaz.html": "/montaz/",
    "faq.html": "/faq/",
    "velkoobchod.html": "/velkoobchod/",
    "na-mieru.html": "/na-mieru/",
    "o-nas.html": "/o-nas/",
    "obchodne-podmienky.html": "/obchodne-podmienky/",
}


def dosad_udaje(h):
    """Vyplní prázdne značky firemnými údajmi z config.js.

    Trieda môže byť na čomkoľvek — js-company je na <strong>, js-info na
    <a>. Preto nehľadáme konkrétnu značku, ale ľubovoľnú s tou triedou.
    """
    adresa = html.escape(f'{seo.CFG["street"]}, {seo.CFG["city"]}')
    h = re.sub(r'<([a-z]+) class="js-address"[^>]*></\1>', adresa, h)
    for trieda, kluc in UDAJE.items():
        hodnota = html.escape(str(seo.CFG.get(kluc) or ""))
        if "@" in hodnota:
            hodnota = f'<a href="mailto:{hodnota}">{hodnota}</a>'
        h = re.sub(rf'<([a-z]+) class="{trieda}"[^>]*></\1>', hodnota, h)
    return h


def faq_html(lang):
    """FAQ skladáme z dvojíc otázka–odpoveď, nie z vykreslenej stránky.

    Na webe je otázka tlačidlom rozbaľovača a tie sa pri očiste vyhadzujú
    s obsahom — zostali by len odpovede bez otázok.
    """
    uvod = ("Najčastejšie otázky k výberu, montáži a objednávaniu."
            if lang == "sk" else
            "Nejčastější otázky k výběru, montáži a objednávání.")
    out = [f"<p>{uvod}</p>"]
    for otazka, odpoved in pc.faq_pairs(lang):
        out.append(f"<h3>{html.escape(otazka)}</h3>")
        out.append(odpoved)
    return "".join(out)


# Vety, ktoré na našom webe odkazovali na formulár. Shoptet má vlastný
# kontaktný formulár aj vlastnú registráciu veľkoobchodu, takže formuláre
# sa vyhodili — a text, ktorý ich sľubuje, by zostal visieť.
PREPISY = [
    ("Vyplňte formulár a pošleme vám cenník aj podmienky. Alebo nám napíšte priamo na",
     "Napíšte nám a pošleme vám cenník aj podmienky:"),
    ("Vyplňte formulář a pošleme vám ceník i podmínky. Nebo nám napište přímo na",
     "Napište nám a pošleme vám ceník i podmínky:"),
    ("Žltou farbou sú označené údaje, ktoré ešte dopĺňame.", ""),
    ("Žlutou barvou jsou označené údaje, které ještě doplňujeme.", ""),
]


def prepisy(h, kde):
    for stara, nova in PREPISY:
        if stara in h:
            h = h.replace(stara, nova)
            ZMENENE.append((kde, stara[:46]))
    return h


ZMENENE = []


def dosad_odkazy(h):
    """Prepíše odkazy na starý web na adresy v Shoptete."""
    for stara, nova in ODKAZY.items():
        h = h.replace(f'href="{stara}"', f'href="{nova}"')
    # čo zostalo z nášho webu, radšej nech nie je odkaz než zlý odkaz
    return re.sub(r'<a href="(?!/|https?:|mailto:)[^"]*"[^>]*>(.*?)</a>',
                  r"\1", h, flags=re.S)


def ocisti(h):
    """Nechá z HTML len obsah: vyhodí ovládacie prvky, obaly a triedy."""
    for t in VON_S_OBSAHOM:
        h = re.sub(rf"<{t}\b.*?</{t}>", "", h, flags=re.S)
        h = re.sub(rf"<{t}\b[^>]*/?>", "", h)
    # obaly bez obsahu vlastného významu
    h = re.sub(r"</?(section|div|span|figure|header|footer|nav)\b[^>]*>", "\n", h)
    # atribúty, ktoré v cudzom systéme nič neznamenajú
    h = re.sub(r'\s(class|id|data-[\w-]+|aria-[\w-]+|role|style)="[^"]*"', "", h)
    h = re.sub(r"\s(hidden|aria-hidden)(?=[\s>])", "", h)
    # čo zostalo z nepovolených značiek
    h = re.sub(r"</?([a-zA-Z][\w-]*)\b[^>]*>",
               lambda m: m.group(0) if m.group(1).lower() in NECHAT else "", h)
    # prázdne značky, ktoré zostali po vyhodených tlačidlách
    for _ in range(3):
        h = re.sub(r"<(a|p|strong|em|h[234])\b[^>]*>\s*</\1>", "", h)
    # zbytočné prázdne miesta
    h = re.sub(r"<p>\s*</p>", "", h)
    h = re.sub(r"\n{2,}", "\n", h)
    h = re.sub(r"[ \t]{2,}", " ", h)
    return h.strip()


def zarovnaj(h):
    """Jedna značka na riadok — aby sa to dalo prečítať aj v okne Shoptetu.

    Zároveň premení <strong> stojaci samostatne na nadpis. Na webe to bol
    štítok v mriežke („E-mail“, „Telefón“), ktorej obal sme vyhodili —
    v plynulom texte je to nadpis a má ním aj byť.
    """
    h = re.sub(r">\s*<", ">\n<", h)
    riadky, odsadenie = [], 0
    for r in h.split("\n"):
        r = r.strip()
        if not r:
            continue
        m = re.fullmatch(r"<strong>([^<]{2,60})</strong>", r)
        if m:
            r = f"<h3>{m.group(1)}</h3>"
        if re.match(r"</(ul|ol|table|thead|tbody|tr)", r):
            odsadenie = max(0, odsadenie - 1)
        riadky.append("  " * odsadenie + r)
        if re.match(r"<(ul|ol|table|thead|tbody|tr)\b", r):
            odsadenie += 1
    return "\n".join(riadky)


def main():
    # Počty produktov a značiek si stránky berú z premenných, ktoré
    # normálne nastaví build.py. Bez nich by v texte boli nuly.
    pc.N_PRODUCTS, pc.N_BRANDS = catalog_counts()
    os.makedirs(CIEL, exist_ok=True)
    print(f"{CIEL}\n")
    for fn, slug, nazov_sk, nazov_cs in STRANKY:
        for lang, nazov, pr in (("sk", nazov_sk, ""), ("cs", nazov_cs, "cz-")):
            h = faq_html(lang) if fn == "faq" else getattr(pc, fn)(lang, "")
            h = prepisy(h, f"{slug} {lang}")
            h = zarovnaj(ocisti(dosad_odkazy(dosad_udaje(h))))
            cesta = os.path.join(CIEL, f"{pr}{slug}.html")
            with open(cesta, "w", encoding="utf-8") as f:
                f.write(h + "\n")
            zvysok = sorted(set(re.findall(r"js-[a-z-]+", h)))
            print(f"  {os.path.basename(cesta):<28} {nazov:<20} "
                  f"{len(h):>6} znakov"
                  + (f"   NEDOSADENÉ: {zvysok}" if zvysok else ""))
    if ZMENENE:
        print("\nupravený text (formuláre má Shoptet vlastné):")
        for kde, veta in ZMENENE:
            print(f"  {kde:<26} „{veta}…“")


if __name__ == "__main__":
    main()

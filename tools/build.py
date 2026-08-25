# -*- coding: utf-8 -*-
"""Vygeneruje všetky stránky webu v SK a CZ.  Spustenie:  python3 tools/build.py"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages_shell as sh
import pages_content as c

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def catalog_counts():
    """Skutočné počty z data/products.js, aby texty nezostarli."""
    import json, re
    src = open(os.path.join(ROOT, "data", "products.js"), encoding="utf-8").read()
    meta = json.loads(re.search(r"window\.CATALOG_META=(\{.*?\});", src, re.S).group(1))
    return meta["count"], len(meta["brands"])

N_PRODUCTS, N_BRANDS = catalog_counts()
c.N_PRODUCTS, c.N_BRANDS = N_PRODUCTS, N_BRANDS

# slug -> (builder, SK titulok, CZ titulok, SK popis, CZ popis, potrebuje katalóg?)
PAGES = {
 "index": (c.home,
   "Solárne panely pre vozidlá a karavany",
   "Solární panely pro vozidla a karavany",
   "Solárne panely tvarované na kapotu vozidla, flexibilné a skladacie panely, panely pre strešné stany a solárne deky.",
   "Solární panely tvarované na kapotu vozidla, flexibilní a skládací panely, panely pro střešní stany a solární deky.", True),
 "produkty": (c.produkty,
   "Katalóg produktov", "Katalog produktů",
   f"{N_PRODUCTS} solárnych panelov pre {N_BRANDS} značiek vozidiel. Filtrujte podľa kategórie, značky a výkonu.",
   f"{N_PRODUCTS} solárních panelů pro {N_BRANDS} značek vozidel. Filtrujte podle kategorie, značky a výkonu.", True),
 "velkoobchod": (c.velkoobchod,
   "Veľkoobchod a partnerský predaj", "Velkoobchod a partnerský prodej",
   "Veľkoobchodné dodávky solárnych panelov pre predajcov, stavitelov obytných vozidiel a autoservisy.",
   "Velkoobchodní dodávky solárních panelů pro prodejce, stavitele obytných vozidel a autoservisy.", False),
 "na-mieru": (c.na_mieru,
   "Solárne panely na mieru", "Solární panely na míru",
   "Vaše vozidlo nie je v katalógu? Tvarovaný solárny panel vyrobíme na mieru podľa rozmerov.",
   "Vaše vozidlo není v katalogu? Tvarovaný solární panel vyrobíme na míru podle rozměrů.", False),
 "montaz": (c.montaz,
   "Montáž solárneho panela", "Montáž solárního panelu",
   "Postup lepenia flexibilného panela bez vŕtania, zapojenie regulátora a na čo si dať pozor.",
   "Postup lepení flexibilního panelu bez vrtání, zapojení regulátoru a na co si dát pozor.", False),
 "o-nas": (c.o_nas, "O nás", "O nás",
   "Dodávame solárne panely a príslušenstvo pre vozidlá, karavany a outdoor na Slovensku a v Česku.",
   "Dodáváme solární panely a příslušenství pro vozidla, karavany a outdoor na Slovensku a v Česku.", False),
 "faq": (c.faq, "Časté otázky", "Časté dotazy",
   "Výber panela k vozidlu, regulátor nabíjania, montáž bez vŕtania a priebeh objednávky.",
   "Výběr panelu k vozidlu, regulátor nabíjení, montáž bez vrtání a průběh objednávky.", False),
 "kontakt": (c.kontakt, "Kontakt", "Kontakt",
   "Napíšte nám značku a model vozidla — poradíme s výberom panela aj regulátora.",
   "Napište nám značku a model vozidla — poradíme s výběrem panelu i regulátoru.", False),
 "podmienky": (c.podmienky, "Obchodné podmienky", "Obchodní podmínky",
   "Objednávka, ceny, dodanie, záruka, odstúpenie od zmluvy a ochrana osobných údajov.",
   "Objednávka, ceny, dodání, záruka, odstoupení od smlouvy a ochrana osobních údajů.", False),
}

# nadpis stránky (page-head) — index má vlastný hero
HEADS = {
 "produkty":    ("Katalóg", "Katalog"),
 "velkoobchod": ("Veľkoobchod", "Velkoobchod"),
 "na-mieru":    ("Panely na mieru", "Panely na míru"),
 "montaz":      ("Montáž", "Montáž"),
 "o-nas":       ("O nás", "O nás"),
 "faq":         ("Časté otázky", "Časté dotazy"),
 "kontakt":     ("Kontakt", "Kontakt"),
 "podmienky":   ("Obchodné podmienky", "Obchodní podmínky"),
}

def page_head(lang, slug, title):
    sk = lang == "sk"
    home = "Domov" if sk else "Domů"
    desc = PAGES[slug][3 if sk else 4]
    return (f'<section class="page-head"><div class="wrap">'
            f'<p class="crumb"><a href="index.html">{home}</a> / {title}</p>'
            f'<h1>{title}</h1><p>{desc}</p></div></section>\n')

def build():
    made = []
    for lang in ("sk", "cs"):
        outdir = ROOT if lang == "sk" else os.path.join(ROOT, "cz")
        os.makedirs(outdir, exist_ok=True)
        abase = "" if lang == "sk" else "../"     # cesta k assets/config/data
        pbase = ""                                 # susedné stránky sú v tom istom priečinku
        for slug, (fn, tsk, tcs, dsk, dcs, needs_catalog) in PAGES.items():
            title = (tsk if lang == "sk" else tcs)
            desc  = (dsk if lang == "sk" else dcs)
            out = [sh.head(lang, abase, slug, title, desc)]
            out.append(sh.header(lang, abase, slug, pbase))
            if slug != "index":
                out.append(page_head(lang, slug, HEADS[slug][0 if lang == "sk" else 1]))
            out.append(fn(lang, pbase))
            if needs_catalog:
                out.append(c.MODALS % {"close": "Zavrieť" if lang == "sk" else "Zavřít"})
            out.append(sh.footer(lang, abase, pbase))
            if needs_catalog:
                out.append(sh.catalog_scripts(abase))
            out.append(sh.close())
            path = os.path.join(outdir, ("index.html" if slug == "index" else slug + ".html"))
            open(path, "w", encoding="utf-8").write("".join(out))
            made.append(os.path.relpath(path, ROOT))
    return made

if __name__ == "__main__":
    files = build()
    print("vygenerované stránky:", len(files))
    for f in sorted(files): print("  ", f)

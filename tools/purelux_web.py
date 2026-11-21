# -*- coding: utf-8 -*-
"""Purelux v tvare, aký čaká starý statický web (produkty.html,
stránky jednotlivých produktov) — rovnaká štruktúra ako Lensun produkt
v data/products.js, len "cat" vždy "led" (jedna položka v menu
"Produkty", nie Shoptetovských 8 podkategórií).

data/products-purelux.js sa needituje — merguje sa až tu, za behu
generovania webu, rovnako ako sa data/products.js needituje kvôli
sadám (sady_panelov.py) a Purelux CSV/XML exportu (export_purelux.py).

Cena: data/products-purelux.js nesie hotovú cenu s DPH priamo v EUR
(pole "eur"). Starý web ale všade počíta cenu cez tools/seo.py's
price() / assets/app.js's convert() — vzorec "usd × markup × kurz ×
(1+DPH)", ktorý očakáva SUROVÚ cenu PRED prirážkou aj DPH (Lensunov
nákup v USD). Namiesto prepisovania tohto vzorca na dvoch miestach
(Python aj JS, s rizikom, že sa časom rozídu) sa Purelux cena prevedie
OPAČNÝM smerom na takú hodnotu, ktorú ten istý, nezmenený vzorec vráti
presne na hotovú cenu späť — pseudo_usd(). Platí to presne vtedy, keď
je v config.js markup 1.0 a kurz EUR 1.0 (dnes áno) — nie je to vynútené,
len zhoda okolností. Ak sa tieto dve hodnoty niekedy zmenia (napr. sa
zavedie skutočná prirážka na Lensun), treba si dať pozor, že by to
potichu pokazilo aj zobrazenú cenu Purelux produktov.
"""
import json
import os
import re
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo                                              # noqa: E402

CAT = "led"
VYROBCA = "Purelux"


def pseudo_usd(eur):
    return eur / (1 + seo.CFG["vat"])


def katalog():
    cesta = os.path.join(KOREN, "data", "products-purelux.js")
    s = open(cesta, encoding="utf-8").read()
    return json.loads(re.search(r"window\.PURELUX_PRODUCTS=(\[.*\]);", s, re.S).group(1))


def na_web():
    """Purelux produkty v tvare Lensun produktu z data/products.js —
    pripravené na product_pages.py's render()/tools/seo.py's product()
    aj na vloženie do window.PRODUCTS."""
    vystup = []
    for p in katalog():
        var = [{"sk": v["sk"], "cs": v["cs"], "p": pseudo_usd(v["p"]),
                "sku": v.get("sku"), "kg": v.get("kg")} for v in p["var"]]
        vystup.append({
            "id": p["id"], "cat": CAT, "b": None, "w": None, "a": None, "v": None,
            "kg": p.get("kg") or (var[0]["kg"] if var else 0),
            "usd": pseudo_usd(p["eur"]),
            "img": p.get("img") or [],
            "sku": (p["var"][0].get("sku") if p.get("var") else None),
            "n": p["n"], "d": p["d"],
            "var": var, "spec": None, "pack": p.get("pack") or [],
            "vyrobca": VYROBCA,
        })
    return vystup

# -*- coding: utf-8 -*-
"""Štruktúrované dáta (JSON-LD) pre vyhľadávače a jazykové modely.

Vyhľadávače z nich skladajú rozšírené výsledky — cena, dostupnosť,
hodnotenie. Jazykové modely, ktoré dnes odpovedajú na otázky typu
„solárny panel na kapotu Land Roveru“, čítajú to isté: keď sú fakty
v strojovo čitateľnej podobe, citujú ich presnejšie než z bežného textu.

Ceny sa počítajú rovnakým vzorcom ako v assets/app.js, aby v dátach
nebolo iné číslo než na stránke.
"""
import json
import os
import re

SITE = "https://www.rncexplore.com"


def _cfg():
    """Prečíta config.js — jediný zdroj cien, meny a údajov firmy."""
    s = open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "config.js"), encoding="utf-8").read()

    def num(key, default=0.0):
        m = re.search(key + r":\s*([\d.]+)", s)
        return float(m.group(1)) if m else default

    def txt(key, default=""):
        m = re.search(key + r':\s*"([^"]*)"', s)
        return m.group(1) if m else default

    def flag(key):
        m = re.search(key + r":\s*(true|false)", s)
        return bool(m) and m.group(1) == "true"

    m = re.search(r"rates:\s*\{\s*EUR:\s*([\d.]+)\s*,\s*CZK:\s*([\d.]+)", s)
    rates = {"EUR": float(m.group(1)), "CZK": float(m.group(2))} if m else {"EUR": 1, "CZK": 1}
    m = re.search(r"shippingGross:\s*\{\s*EUR:\s*([\d.]+)\s*,\s*CZK:\s*([\d.]+)", s)
    ship = {"EUR": float(m.group(1)), "CZK": float(m.group(2))} if m else {"EUR": 0, "CZK": 0}
    return {
        "company": txt("company"), "street": txt("street"), "city": txt("city"),
        "ico": txt("ico"), "phone": txt("phone"), "mail": txt("orderEmail"),
        "markup": num("markup", 1.0), "vat": num("vat", 0.0),
        "rates": rates, "ship": ship, "shipInPrice": flag("shippingInPrice"),
        "rounding": txt("rounding"),
    }


CFG = _cfg()


def price(usd, cur):
    """Rovnaký vzorec ako convert() v assets/app.js."""
    import math
    v = usd * CFG["markup"] * CFG["rates"][cur]
    if CFG["shipInPrice"]:
        v += CFG["ship"][cur]
    v = v * (1 + CFG["vat"])
    if CFG["rounding"] == "half":
        return math.floor(v) + (0 if cur == "CZK" else 0.5)
    v = max(0, round(v))
    if CFG["rounding"] == "9" and v >= 100:
        v = (v // 10) * 10 + 9
    return v


def _shipping(lang, cur):
    """Doprava nie je v cene, tak ju uvedieme zvlášť — inak by vyhľadávač
    ukazoval cenu, ktorú zákazník v košíku nezaplatí."""
    return {
        "@type": "OfferShippingDetails",
        "shippingRate": {"@type": "MonetaryAmount",
                         "value": 0 if CFG["shipInPrice"] else CFG["ship"][cur],
                         "currency": cur},
        "shippingDestination": {"@type": "DefinedRegion",
                                "addressCountry": "SK" if lang == "sk" else "CZ"},
        "deliveryTime": {"@type": "ShippingDeliveryTime",
                         "handlingTime": {"@type": "QuantitativeValue",
                                          "minValue": 1, "maxValue": 2,
                                          "unitCode": "DAY"},
                         "transitTime": {"@type": "QuantitativeValue",
                                         "minValue": 2, "maxValue": 5,
                                         "unitCode": "DAY"}},
    }


def _address():
    city = CFG["city"]
    m = re.match(r"([\d\s]+)\s+(.+)", city)
    zipc, town = (m.group(1).strip(), m.group(2)) if m else ("", city)
    return {"@type": "PostalAddress", "streetAddress": CFG["street"],
            "addressLocality": town, "postalCode": zipc, "addressCountry": "SK"}


def organization():
    return {
        "@context": "https://schema.org", "@type": "OnlineStore",
        "@id": SITE + "/#organizacia", "name": CFG["company"], "url": SITE,
        "email": CFG["mail"], "telephone": CFG["phone"],
        "address": _address(),
        "identifier": [{"@type": "PropertyValue", "name": "IČO", "value": CFG["ico"]}],
        "areaServed": [{"@type": "Country", "name": "Slovensko"},
                       {"@type": "Country", "name": "Česko"}],
        "currenciesAccepted": "EUR, CZK",
        "paymentAccepted": "Bankový prevod",
    }


def breadcrumbs(items):
    """items — dvojice (názov, absolútna adresa)."""
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": u}
            for i, (n, u) in enumerate(items, 1)],
    }


def product(p, lang, url):
    """Produkt aj s cenou a dostupnosťou — základ rozšíreného výsledku."""
    cur = "EUR" if lang == "sk" else "CZK"
    name = p["n"]["sk" if lang == "sk" else "cs"]
    desc = p["d"]["sk" if lang == "sk" else "cs"]
    offers = []
    for v in (p.get("var") or [{"p": p["usd"], "sku": p.get("sku")}]):
        label = v.get("sk" if lang == "sk" else "cs") or name
        offers.append({
            "@type": "Offer",
            "name": label,
            "sku": v.get("sku") or p.get("sku") or "",
            "price": price(v["p"], cur),
            "priceCurrency": cur,
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
            "url": url,
            "seller": {"@id": SITE + "/#organizacia"},
            "shippingDetails": _shipping(lang, cur),
        })
    out = {
        "@context": "https://schema.org", "@type": "Product",
        "name": name, "description": desc, "url": url,
        "sku": p.get("sku") or "",
        "image": (p.get("img") or [])[:4],
        "brand": {"@type": "Brand", "name": "Lensun"},
        "category": p.get("cat", ""),
        "offers": offers if len(offers) > 1 else offers[0],
    }
    props = []
    if p.get("w"):
        props.append({"@type": "PropertyValue", "name": "Výkon", "value": f"{p['w']} W"})
    if p.get("v"):
        props.append({"@type": "PropertyValue", "name": "Napätie", "value": f"{p['v']} V"})
    if p.get("kg"):
        props.append({"@type": "PropertyValue", "name": "Hmotnosť", "value": f"{p['kg']} kg"})
    if p.get("b"):
        props.append({"@type": "PropertyValue", "name": "Značka vozidla", "value": p["b"]})
    if props:
        out["additionalProperty"] = props
    return out


def faq_page(pairs):
    """pairs — dvojice (otázka, odpoveď v HTML)."""
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer",
                                "text": re.sub(r"<[^>]+>", " ", a).strip()}}
            for q, a in pairs],
    }


def blog_post(post, lang, url):
    i = 0 if lang == "sk" else 1
    return {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": post["title"][i], "description": post["lead"][i],
        "image": post["hero"], "datePublished": post["date"],
        "dateModified": post["date"], "url": url,
        "inLanguage": "sk" if lang == "sk" else "cs",
        "author": {"@id": SITE + "/#organizacia"},
        "publisher": {"@id": SITE + "/#organizacia"},
        "mainEntityOfPage": url,
    }


def website():
    return {
        "@context": "https://schema.org", "@type": "WebSite",
        "@id": SITE + "/#web", "url": SITE, "name": "RNC Explore",
        "publisher": {"@id": SITE + "/#organizacia"},
        "inLanguage": ["sk", "cs"],
    }

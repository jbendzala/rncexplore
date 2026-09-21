# -*- coding: utf-8 -*-
"""Vygeneruje sitemap.xml a robots.txt.

Sitemap nesie pri každej adrese aj odkaz na jej druhojazyčnú verziu
(xhtml:link). Vyhľadávač tak vie, že slovenská a česká stránka sú tá
istá vec v dvoch jazykoch, a nepovažuje ich za duplicitu.
"""
import datetime
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.rncexplore.com/"

# Stránky, ktoré do indexu nepatria — nemajú samostatnú informačnú hodnotu
# a v košíku by vyhľadávač indexoval prázdny stav.
SKIP = {"cz.html", "kosik.html", "cz/kosik.html"}


def _priority(rel):
    if rel in ("index.html", "cz/index.html"):
        return "1.0"
    if rel.endswith("produkty.html"):
        return "0.9"
    if rel.startswith(("produkt/", "cz/produkt/")):
        return "0.8"
    if rel.startswith(("blog/", "cz/blog/")):
        return "0.6"
    return "0.5"


def _pair(rel):
    """K adrese vráti jej slovenskú a českú obdobu."""
    cz = rel.startswith("cz/")
    sk_rel = rel[3:] if cz else rel
    sk = BASE + ("" if sk_rel == "index.html" else sk_rel)
    czu = BASE + "cz/" + ("" if sk_rel == "index.html" else sk_rel)
    return sk, czu


def build():
    rels = []
    for dirpath, dirnames, files in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", ".github", "tools", "data", "assets")]
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
            if rel in SKIP:
                continue
            rels.append(rel)

    today = datetime.date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel in sorted(rels):
        loc = BASE + ("" if rel == "index.html" else rel)
        sk, cz = _pair(rel)
        out.append(
            f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod>"
            f"<priority>{_priority(rel)}</priority>"
            f'<xhtml:link rel="alternate" hreflang="sk" href="{sk}"/>'
            f'<xhtml:link rel="alternate" hreflang="cs" href="{cz}"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{sk}"/>'
            "</url>")
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        "\n".join(out) + "\n")

    # Jazykové modely dnes odpovedajú na otázky typu „panel na kapotu Defendera“
    # a zdroje pritom citujú. Ich roboty preto púšťame dnu rovnako ako
    # vyhľadávače — bez toho by nás v odpovediach nespomenuli.
    robots = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /kosik.html",
        "Disallow: /cz/kosik.html",
        "",
        "# Vyhľadávače aj jazykové modely majú prístup k celému katalógu.",
        "User-agent: GPTBot",
        "Allow: /",
        "",
        "User-agent: OAI-SearchBot",
        "Allow: /",
        "",
        "User-agent: ClaudeBot",
        "Allow: /",
        "",
        "User-agent: PerplexityBot",
        "Allow: /",
        "",
        "User-agent: Google-Extended",
        "Allow: /",
        "",
        "Sitemap: " + BASE + "sitemap.xml",
        "",
    ]
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write("\n".join(robots))
    return len(rels)


if __name__ == "__main__":
    print("URL v sitemape:", build())

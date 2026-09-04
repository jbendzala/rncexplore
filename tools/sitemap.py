# -*- coding: utf-8 -*-
"""Vygeneruje sitemap.xml so všetkými stránkami webu."""
import os, re, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.rncexplore.com/"

def build():
    urls = []
    for dirpath, dirnames, files in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "tools", "data", "assets")]
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
            if rel == "cz.html":          # len presmerovanie
                continue
            loc = BASE + ("" if rel == "index.html" else rel)
            # domovské a katalógové stránky majú vyššiu prioritu
            if rel in ("index.html", "cz/index.html"):      pri = "1.0"
            elif rel.endswith("produkty.html"):             pri = "0.9"
            elif "/produkt/" in rel or rel.startswith("produkt/"): pri = "0.8"
            elif "/blog/" in rel or rel.startswith("blog/"): pri = "0.6"
            else:                                            pri = "0.5"
            urls.append((loc, pri))
    today = datetime.date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri in urls:
        out.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod>"
                   f"<priority>{pri}</priority></url>")
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")

    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nSitemap: " + BASE + "sitemap.xml\n")
    return len(urls)

if __name__ == "__main__":
    print("URL v sitemape:", build())

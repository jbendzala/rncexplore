# -*- coding: utf-8 -*-
"""Vypíše články blogu do CSV, slovenské aj české znenie vedľa seba.

Telo článku sa skladá do HTML, aby sa dalo nahrať do redakčného systému
bez prepisovania. Fotografie a videá zostávajú ako odkazy — sú na
serveri Lensunu a na YouTube, nesťahujeme ich.
"""
import csv, html, os, sys

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TU)
import blog_content as B

CIEL = os.path.expanduser("~/Documents/rncexplore-blog.csv")
WEB = "https://www.rncexplore.com"


def e(x):
    return html.escape(str(x), quote=False)


def telo(clanok, i):
    """i = 0 slovensky, 1 česky."""
    c = []
    if clanok.get("video"):
        c.append(f'<p><iframe width="560" height="315" '
                 f'src="https://www.youtube.com/embed/{clanok["video"]}" '
                 f'title="YouTube" allowfullscreen></iframe></p>')
    for nadpis, odseky in clanok["body"]:
        c.append("<h2>" + e(nadpis[i]) + "</h2>")
        c += ["<p>" + e(o[i]) + "</p>" for o in odseky]
    return "".join(c)


def main():
    with open(CIEL, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Adresa", "Dátum", "Rubrika SK", "Rubrika CZ",
                    "Názov SK", "Perex SK", "Telo SK (HTML)",
                    "Názov CZ", "Perex CZ", "Telo CZ (HTML)",
                    "Hlavná fotografia", "Video (YouTube)", "Zdroj",
                    "Odkaz SK", "Odkaz CZ"])
        for p in B.POSTS:
            rub = B.CAT.get(p["cat"], (p["cat"], p["cat"]))
            w.writerow([
                p["slug"], p["date"], rub[0], rub[1],
                p["title"][0], p["lead"][0], telo(p, 0),
                p["title"][1], p["lead"][1], telo(p, 1),
                p.get("hero") or "", p.get("video") or "", p.get("source") or "",
                f'{WEB}/blog/{p["slug"]}.html',
                f'{WEB}/cz/blog/{p["slug"]}.html',
            ])
    print(f"{len(B.POSTS)} článkov -> {CIEL}")


if __name__ == "__main__":
    main()

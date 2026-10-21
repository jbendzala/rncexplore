# -*- coding: utf-8 -*-
"""Vypíše články blogu do CSV, slovenské aj české znenie vedľa seba.

Telo článku sa skladá do HTML, aby sa dalo nahrať do redakčného systému
bez prepisovania. Fotografie a videá zostávajú ako odkazy — sú na
serveri Lensunu a na YouTube, nesťahujeme ich.
"""
import csv, html, os, re, sys

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TU)
import blog_content as B
import vystup

CIEL = vystup.kam(vystup.NASE, "blog-prehlad.csv")
# Články sa do Shoptetu nedajú naimportovať — produktový XML nesie len
# produkty. Vkladajú sa teda ručne, a z bunky v tabuľke sa HTML kopíruje
# zle. Preto píšeme aj súbor na článok: otvoriť, označiť všetko, vložiť.
CIEL_HTML = vystup.kam(vystup.VLOZIT, "blog")
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

    os.makedirs(CIEL_HTML, exist_ok=True)
    print(f"\npo článkoch na vloženie do Shoptetu -> {CIEL_HTML}")
    for p in B.POSTS:
        for i, pr in ((0, ""), (1, "cz-")):
            # perex je v Shoptete samostatné pole, do tela nepatrí
            t = telo(p, i)
            with open(os.path.join(CIEL_HTML, f'{pr}{p["slug"]}.html'),
                      "w", encoding="utf-8") as f:
                f.write(re.sub(r">\s*<", ">\n<", t).strip() + "\n")
    print(f"  {len(B.POSTS) * 2} súborov (slovensky aj česky)")

    # Prehľad na vkladanie — čo kam a v akom poradí, od najstaršieho.
    sup = os.path.join(CIEL_HTML, "_prehlad.txt")
    with open(sup, "w", encoding="utf-8") as f:
        f.write("Články na vloženie do Shoptetu (Obsah -> Články).\n"
                "Poradie je od najstaršieho, aby dátumy v blogu vyšli.\n\n")
        for p in sorted(B.POSTS, key=lambda x: x["date"]):
            rub = B.CAT.get(p["cat"], (p["cat"], p["cat"]))
            f.write(f'{p["date"]}  {rub[0]:<22} {p["title"][0]}\n'
                    f'          adresa: {p["slug"]}\n'
                    f'          telo:   {p["slug"]}.html / cz-{p["slug"]}.html\n'
                    f'          perex:  {p["lead"][0][:96]}\n')
            if p.get("hero"):
                f.write(f'          foto:   {p["hero"]}\n')
            if p.get("video"):
                f.write(f'          video:  https://youtu.be/{p["video"]}\n')
            f.write("\n")
    print(f"  _prehlad.txt — zoznam s perexmi, fotkami a poradím")


if __name__ == "__main__":
    main()

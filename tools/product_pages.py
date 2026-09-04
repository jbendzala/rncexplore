# -*- coding: utf-8 -*-
"""Generuje samostatnú stránku pre každý produkt (SK aj CZ).

Statické je všetko, čo má vidieť vyhľadávač: názov, popis, parametre,
obsah balenia, fotografie, video a hodnotenia. Ceny a prevedenia
dopĺňa prehliadač, aby sa dali meniť v config.js.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPEC_LABEL = {
 "w":   ("Špičkový výkon", "Špičkový výkon"),
 "eff": ("Účinnosť článkov", "Účinnost článků"),
 "vmp": ("Napätie pri max. výkone", "Napětí při max. výkonu"),
 "imp": ("Prúd pri max. výkone", "Proud při max. výkonu"),
 "voc": ("Napätie naprázdno", "Napětí naprázdno"),
 "isc": ("Skratový prúd", "Zkratový proud"),
 "vsys":("Max. napätie systému", "Max. napětí systému"),
 "dim": ("Rozmery", "Rozměry"),
 "kg":  ("Hmotnosť", "Hmotnost"),
 "jbox":("Pripojovacia skrinka", "Připojovací skříňka"),
}
SPEC_ORDER = ["w","eff","vmp","imp","voc","isc","vsys","dim","kg","jbox"]

def esc(s):
    return (str(s).replace("&","&amp;").replace("<","&lt;")
            .replace(">","&gt;").replace('"',"&quot;"))

def T(sk, cs, lang):
    return sk if lang == "sk" else cs

def _rel(p, ALL, n=4):
    """Podobné produkty: rovnaká značka, inak rovnaká kategória."""
    same = [x for x in ALL if x["id"] != p["id"] and p["b"] and x["b"] == p["b"]]
    if len(same) < n:
        same += [x for x in ALL if x["id"] != p["id"] and x["cat"] == p["cat"]
                 and x not in same]
    return same[:n]


def render(p, ALL, lang, reviews, base):
    """base ukazuje na koreň webu (z /produkt/ je to ../)."""
    name = p["n"][lang]; desc = p["d"][lang]
    i = 0 if lang == "sk" else 1

    # ---------- galéria ----------
    imgs = p["img"] or []
    thumbs = "".join(
        f'<button type="button" data-src="{esc(u)}?width=1000" aria-current="{str(k==0).lower()}">'
        f'<img loading="lazy" src="{esc(u)}?width=160" alt=""></button>'
        for k, u in enumerate(imgs[:8]))
    gallery = (f'<div class="pd-main"><img id="pdMain" src="{esc(imgs[0])}?width=1000" '
               f'alt="{esc(name)}"></div>'
               + (f'<div class="pd-thumbs">{thumbs}</div>' if len(imgs) > 1 else "")
               ) if imgs else '<div class="pd-main"></div>'

    # ---------- parametre ----------
    spec = p.get("spec") or {}
    rows = "".join(
        f'<tr><th>{esc(SPEC_LABEL[k][i])}</th><td>{esc(spec[k])}</td></tr>'
        for k in SPEC_ORDER if spec.get(k))
    if p.get("b"):
        rows += f'<tr><th>{T("Značka vozidla","Značka vozidla",lang)}</th><td>{esc(p["b"])}</td></tr>'
    if p.get("sku"):
        rows += f'<tr><th>{T("Kód produktu","Kód produktu",lang)}</th><td>{esc(p["sku"])}</td></tr>'
    spec_html = (f'<h2>{T("Technické parametre","Technické parametry",lang)}</h2>'
                 f'<div class="table-wrap"><table class="data">{rows}</table></div>') if rows else ""

    # ---------- obsah balenia ----------
    pack = p.get("pack") or []
    pack_html = ""
    if pack:
        items = "".join(f"<li>{esc(x[lang])}</li>" for x in pack)
        pack_html = (f'<h2>{T("Obsah balenia","Obsah balení",lang)}</h2>'
                     f'<ul class="pack">{items}</ul>')

    # ---------- video ----------
    video = ""
    if p.get("vid"):
        video = (f'<h2>{T("Video","Video",lang)}</h2>'
                 f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{esc(p["vid"])}" '
                 f'title="{esc(name)}" loading="lazy" allowfullscreen '
                 f'allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"></iframe></div>')

    # ---------- hodnotenia k tomuto produktu ----------
    rev_html = ""
    mine = [r for r in reviews if r.get("pid") == p["id"]]
    if mine:
        cards = []
        for r in mine:
            stars = ('<svg viewBox="0 0 24 24"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8'
                     'l-6.2 3.2L7 14.2l-5-4.9 6.9-1z"/></svg>') * 5
            cards.append(
                f'<figure class="review"><div class="review-body">'
                f'<div class="review-head"><span class="avatar" aria-hidden="true">{esc(r["ini"])}</span>'
                f'<span class="review-who"><b>{esc(r["who"])}</b><span>{esc(r["car"])}</span></span></div>'
                f'<div class="stars">{stars}</div>'
                f'<blockquote>{r[lang]}</blockquote></div></figure>')
        rev_html = (f'<section class="sec alt"><div class="wrap">'
                    f'<h2>{T("Hodnotenia tohto produktu","Hodnocení tohoto produktu",lang)}</h2>'
                    f'<div class="reviews">{"".join(cards)}</div></div></section>')

    # ---------- podobné produkty ----------
    rel = _rel(p, ALL)
    rel_html = ""
    if rel:
        rel_html = (f'<section class="sec"><div class="wrap">'
                    f'<div class="sec-head"><h2>{T("Mohlo by sa hodiť","Mohlo by se hodit",lang)}</h2></div>'
                    f'<div class="grid" id="related"></div></div></section>')

    # produkt + podobné do stránky (kvôli cenám, ktoré závisia od config.js)
    embed = json.dumps([p] + rel, ensure_ascii=False, separators=(",", ":"))

    cat_name = {"hood": T("Panely na kapotu","Panely na kapotu",lang)}.get(p["cat"], "")

    return f'''
<section class="sec"><div class="wrap pd">
  <div class="pd-media">{gallery}</div>
  <div class="pd-buy">
    <p class="card-cat">{esc(cat_name)}</p>
    <h1>{esc(name)}</h1>
    <div id="pdPrice" class="pd-price"></div>
    <div id="pdSwatch" class="swatches"></div>
    <div class="pd-actions">
      <label class="pd-qty"><span>{T("Počet","Počet",lang)}</span>
        <input id="pdQty" type="number" min="1" max="99" value="1"></label>
      <button class="btn lg" id="pdOrder">{T("Objednať","Objednat",lang)}</button>
    </div>
    <p class="note">{T("Objednávka je nezáväzná. Ozveme sa vám s cenovou ponukou a termínom dodania.","Objednávka je nezávazná. Ozveme se vám s cenovou nabídkou a termínem dodání.",lang)}</p>
  </div>
</div></section>

<section class="sec alt"><div class="wrap"><div class="prose">
  <h2>{T("Popis","Popis",lang)}</h2>
  <p>{esc(desc)}</p>
  {video}
  {spec_html}
  {pack_html}
</div></div></section>
{rev_html}
{rel_html}
<script>window.PRODUCT_ID={json.dumps(p["id"])};window.CATALOG_META={{"cats":[],"brands":[],"count":0}};window.PRODUCTS={embed};</script>
'''

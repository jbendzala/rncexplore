# -*- coding: utf-8 -*-
"""Doplní do data/products.js fotografie, technické parametre, obsah balenia
a video z exportu zo Shopify.

Použitie:  python3 tools/enrich_products.py [cesta/k/products_export.csv]
"""
import csv, re, html, os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "products.js")

# štítok v exporte -> náš kľúč
SPEC_KEYS = [
    ("Peak power", "w"), ("Rated Power Output", "w"),
    ("Solar cell efficiency", "eff"), ("Solar Cells Efficiency", "eff"),
    ("Maximum power voltage", "vmp"), ("Optimum Operating Voltage", "vmp"),
    ("Maximum power current", "imp"), ("Optimum Operating Current", "imp"),
    ("Open circuit voltage", "voc"), ("Open Circuit Voltage", "voc"),
    ("Short circuit current", "isc"), ("Short Circuit Current", "isc"),
    ("Maximum system voltage", "vsys"),
    ("Net Weight", "kg"), ("Net. Weight", "kg"),
    ("Dimensions", "dim"), ("J-Box", "jbox"),
]

def strip_tags(h):
    h = re.sub(r"<br\s*/?>", "\n", h)
    h = re.sub(r"</(p|h\d|li|div)>", "\n", h)
    return html.unescape(re.sub(r"<[^>]+>", "", h))

def tidy(v, key=None):
    """Zjednotí zápis jednotiek, zahodí imperiálne miery a použije desatinnú čiarku."""
    v = " ".join(v.split()).strip(" .;")
    # pripojovacia skrinka -> krátky jazykovo neutrálny zápis
    if key == "jbox":
        ip = re.search(r"IP\s*(\d{2})", v, re.I)
        cab = re.search(r"([\d.]+)\s*m\b", v)
        parts = []
        if ip: parts.append("IP " + ip.group(1))
        if cab: parts.append(cab.group(1).replace(".", ",") + " m")
        return " · ".join(parts) if parts else ""
    # zahodí palce, stopy a libry v akomkoľvek tvare za lomkou
    v = re.split(r"\s*/\s*[\d.x×]+\s*(?:lbs?|inch|in|ft)\b", v)[0]
    v = re.sub(r"\s*/\s*[\d.]+\s*(?:lbs?|inch|in|ft)\b.*$", "", v, flags=re.I)
    if key == "dim":
        nums = re.findall(r"[\d.]+", v.split("/")[0])
        if len(nums) >= 2:
            return " × ".join(n.replace(".", ",") for n in nums[:3]) + " mm"
    v = re.sub(r"(\d)\s*kgs?\b", r"\1 kg", v, flags=re.I)
    v = re.sub(r"(\d)\s*([WVA])\b", r"\1 \2", v)
    v = re.sub(r"(\d)\s*(mm|m)\b", r"\1 \2", v)
    v = re.sub(r"(\d)\s*%", r"\1 %", v)
    v = re.sub(r"(\d)\.(\d)", r"\1,\2", v)
    return v[:40]

PACK = [
    (r"hood|bonnet.*solar panel", ("solárny panel na kapotu", "solární panel na kapotu")),
    (r"vinyl decal",              ("vinylová fólia (voliteľne)", "vinylová fólie (volitelně)")),
    (r"solar controller|regulator|mppt", ("solárny regulátor (voliteľne)", "solární regulátor (volitelně)")),
    (r"extend(?:ed)? cable|extension cable", ("predlžovací kábel", "prodlužovací kabel")),
    (r"adaptor cable|adapter cable", ("adaptérový kábel", "adaptérový kabel")),
    (r"y adaptor|y connector",     ("Y konektory", "Y konektory")),
    (r"carry bag|carrying bag",    ("prepravná taška", "přepravní taška")),
    (r"solar blanket|blanket panel", ("solárna deka", "solární deka")),
    (r"foldable solar panel",      ("skladací solárny panel", "skládací solární panel")),
    (r"flexible solar panel",      ("flexibilný solárny panel", "flexibilní solární panel")),
    (r"solar panel",               ("solárny panel", "solární panel")),
]

def parse_pack(t):
    m = re.search(r"Pack(?:ing|age Includes)[:\s]*\n(.{0,420})", t, re.S | re.I)
    if not m:
        return []
    out = []
    for line in m.group(1).split("\n"):
        line = line.strip()
        if not line or len(line) > 90:
            continue
        q = re.match(r"^(\d+)\s*[xX]\s*(.+)$", line)
        if not q:
            if out: break
            continue
        n, rest = q.group(1), q.group(2).lower()
        watt = re.search(r"(\d+)\s*w\b", rest)
        amp = re.search(r"(\d+)\s*a\b", rest)
        length = re.search(r"(\d+)\s*m\b", rest)
        label = None
        for pat, names in PACK:
            if re.search(pat, rest):
                label = names; break
        if not label:
            continue
        sk, cs = label
        extra = ""
        if watt and "panel" in sk: extra = f" {watt.group(1)} W"
        elif amp and "regul" in sk: extra = f" {amp.group(1)} A"
        elif length and "kábel" in sk: extra = f" {length.group(1)} m"
        out.append({"sk": f"{n}× {sk}{extra}", "cs": f"{n}× {cs}{extra}"})
        if len(out) >= 5: break
    return out

def main(csv_path):
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
    raw = {}
    for r in rows:
        h = (r.get("Handle") or "").strip()
        if not h: continue
        p = raw.setdefault(h, {"imgs": [], "body": ""})
        if (r.get("Body (HTML)") or "").strip():
            p["body"] = r["Body (HTML)"]
        src = (r.get("Image Src") or "").strip().split("?")[0]
        if src and src not in p["imgs"]:
            p["imgs"].append(src)

    src_js = open(DATA, encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", src_js, re.S).group(1))
    meta = re.search(r"window\.CATALOG_META=(\{.*?\});", src_js, re.S).group(1)

    n_spec = n_pack = n_vid = 0
    for p in P:
        r = raw.get(p["id"])
        if not r: continue
        if r["imgs"]:
            p["img"] = r["imgs"][:8]
        t = strip_tags(r["body"])
        specs = {}
        for line in t.split("\n"):
            line = line.strip()
            for label, key in SPEC_KEYS:
                if key in specs: continue
                m = re.match(re.escape(label) + r"\s*[:：]\s*(.+)$", line, re.I)
                if m:
                    val = tidy(m.group(1), key)
                    if val: specs[key] = val
        if specs:
            p["spec"] = specs; n_spec += 1
        pack = parse_pack(t)
        if pack:
            p["pack"] = pack; n_pack += 1
        vid = re.search(r"(?:youtube\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)([A-Za-z0-9_-]{8,})", r["body"])
        if vid:
            p["vid"] = vid.group(1); n_vid += 1

    with open(DATA, "w", encoding="utf-8") as f:
        f.write("/* Generované dáta katalógu — negenerujte ručne. */\n")
        f.write("window.CATALOG_META=" + meta + ";\n")
        f.write("window.PRODUCTS=" + json.dumps(P, ensure_ascii=False, separators=(",", ":")) + ";\n")

    print(f"produktov: {len(P)}")
    print(f"  s parametrami: {n_spec}")
    print(f"  s obsahom balenia: {n_pack}")
    print(f"  s videom: {n_vid}")
    print(f"  fotografií spolu: {sum(len(x['img']) for x in P)}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Downloads/products_export.csv"))

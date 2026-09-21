# -*- coding: utf-8 -*-
"""Porovná ceny v katalógu s aktuálnymi cenami na lensunsolar.com.

Spustenie:  python3 tools/check_prices.py
Web nemení, len vypíše rozdiely. Produkt, ktorý má Lensun pod iným
názvom, si nesie ich handle v poli "src".
"""
import json, re, time, urllib.error, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
ROOT = __file__.rsplit("/", 2)[0]


def catalog():
    src = open(f"{ROOT}/data/products.js", encoding="utf-8").read()
    return json.loads(re.search(r'window\.PRODUCTS=(\[.*?\]);\s*\n', src, re.S).group(1))


def fetch(handle):
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f"https://lensunsolar.com/products/{handle}.json", headers=UA)
            d = json.load(urllib.request.urlopen(req, timeout=30))["product"]
            return [{"sku": v.get("sku") or "", "p": float(v["price"])}
                    for v in d["variants"]]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(10 * (attempt + 1))
        except Exception:
            time.sleep(6)
    return "fail"


def suffix(sku):
    return sku.split("+", 1)[1] if "+" in sku else "base"


def main():
    ps = catalog()
    diffs, gone, failed, ok = [], [], [], 0
    for i, p in enumerate(ps, 1):
        lv = fetch(p.get("src") or p["id"])
        if lv is None:
            gone.append(p["id"])
        elif lv == "fail":
            failed.append(p["id"])
        else:
            by_sku = {v["sku"]: v for v in lv if v["sku"]}
            by_suf = {}
            for v in lv:
                by_suf.setdefault(suffix(v["sku"]), v)
            clean = True
            for v in (p.get("var") or []):
                lm = by_sku.get(v.get("sku")) or by_suf.get(suffix(v.get("sku") or ""))
                if lm is None or abs(lm["p"] - v["p"]) > 0.005:
                    diffs.append((p["id"], v.get("sku"), v["p"],
                                  lm["p"] if lm else None))
                    clean = False
            if clean:
                ok += 1
        if i % 20 == 0:
            print(f"  ... {i}/{len(ps)}", flush=True)
        time.sleep(1.6)

    print(f"\nv katalógu {len(ps)} produktov, bez rozdielu {ok}")
    if diffs:
        print(f"\nZMENENÉ CENY ({len(diffs)}):")
        for pid, sku, a, b in diffs:
            print(f"  {pid[:44]:<46} {str(sku)[:22]:<24} "
                  f"{a:>7.0f} -> {('zrušené' if b is None else f'{b:.0f}'):>8}")
    if gone:
        print(f"\nU LENSUNU UŽ NIE SÚ ({len(gone)}):")
        for g in gone:
            print("  " + g)
    if failed:
        print(f"\nNENAČÍTANÉ ({len(failed)}):")
        for f in failed:
            print("  " + f)
    if not (diffs or gone or failed):
        print("Všetko sedí.")


if __name__ == "__main__":
    main()

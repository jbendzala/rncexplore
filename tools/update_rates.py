# -*- coding: utf-8 -*-
"""Aktualizuje kurzy v config.js podľa Európskej centrálnej banky.

Ceny produktov sú vedené v dolároch (cenník Lensunu) a prepočítavajú sa
kurzom v config.js. Tento skript ho udržiava blízko skutočnosti.

Zámerne NEMENÍ kurz pri každom spustení:

  * PRIRÁŽKA  — ku kurzu ECB pripočíta rezervu, aby bežné kolísanie meny
                nešlo z marže. Zároveň pokrýva kurzový rozdiel banky.
  * PRAH      — zmenu zapíše, len keď je väčšia než prah. Bez neho by sa
                ceny hýbali každý týždeň a commitov by pribúdalo zbytočne.

Spustenie:
    python3 tools/update_rates.py            # zapíše, ak treba
    python3 tools/update_rates.py --dry-run  # len ukáže, čo by urobil
"""
import json
import os
import re
import sys
import urllib.request

BUFFER = 0.03          # +3 % ku kurzu ECB
THRESHOLD = 0.015      # zapíše až pri zmene nad 1,5 %
API = "https://api.frankfurter.dev/v1/latest?base=USD&symbols=EUR,CZK"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "config.js")


def current():
    """Kurzy, ktoré sú teraz v config.js."""
    s = open(CONFIG, encoding="utf-8").read()
    m = re.search(r"rates:\s*\{\s*EUR:\s*([\d.]+)\s*,\s*CZK:\s*([\d.]+)\s*\}", s)
    if not m:
        raise SystemExit("config.js: riadok s kurzami sa nenašiel")
    return {"EUR": float(m.group(1)), "CZK": float(m.group(2))}


def ecb():
    """Referenčný kurz ECB, základ USD."""
    req = urllib.request.Request(API, headers={"User-Agent": "rncexplore/1.0"})
    d = json.load(urllib.request.urlopen(req, timeout=30))
    return d["date"], d["rates"]


def write(rates):
    s = open(CONFIG, encoding="utf-8").read()
    new = "rates: { EUR: %s, CZK: %s }" % (rates["EUR"], rates["CZK"])
    s2 = re.sub(r"rates:\s*\{\s*EUR:\s*[\d.]+\s*,\s*CZK:\s*[\d.]+\s*\}", new, s, count=1)
    if s2 == s:
        raise SystemExit("config.js: kurzy sa nepodarilo prepísať")
    open(CONFIG, "w", encoding="utf-8").write(s2)


def main():
    dry = "--dry-run" in sys.argv
    old = current()
    date, raw = ecb()

    want = {
        "EUR": round(raw["EUR"] * (1 + BUFFER), 4),
        "CZK": round(raw["CZK"] * (1 + BUFFER), 3),
    }
    print(f"kurz ECB z {date}:")
    for k in ("EUR", "CZK"):
        drift = (want[k] - old[k]) / old[k] * 100
        print(f"  1 USD = {raw[k]:>9.4f} {k}   s prirážkou {BUFFER:.0%}: {want[k]:>9.4f}"
              f"   v config.js: {old[k]:<8} ({drift:+.1f} %)")

    biggest = max(abs(want[k] - old[k]) / old[k] for k in want)
    if biggest < THRESHOLD:
        print(f"\nzmena {biggest:.1%} je pod prahom {THRESHOLD:.1%} — kurzy nechávam tak")
        return 0

    # ceny v korunách a eurách by mali navzájom sedieť
    cross_old = old["CZK"] / old["EUR"]
    cross_new = want["CZK"] / want["EUR"]
    print(f"\nkurz EUR/CZK: {cross_old:.2f} -> {cross_new:.2f} Kč za euro")

    if dry:
        print(f"zmena {biggest:.1%} nad prahom — bez --dry-run by som kurzy zapísal")
        return 0

    write(want)
    print(f"zmena {biggest:.1%} nad prahom — kurzy v config.js aktualizované")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

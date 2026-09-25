# -*- coding: utf-8 -*-
"""Aktualizuje prepočet na koruny v config.js podľa Európskej centrálnej banky.

Maloobchodná cena bez DPH je dolárová cena Lensunu braná jedna k jednej
ako eurá — kurz do nej nevstupuje a `rates.EUR` preto zostáva 1.0.
Mení sa len `rates.CZK`, ktorý tú eurovú cenu prepočítava na koruny,
a spolu s ním aj korunová cena dopravy, aby obe čísla sedeli.

Zámerne NEMENÍ kurz pri každom spustení:

  * PRIRÁŽKA  — ku kurzu ECB pripočíta rezervu, aby bežné kolísanie koruny
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
API = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=CZK"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "config.js")

RATES_RE = r"rates:\s*\{\s*EUR:\s*([\d.]+)\s*,\s*CZK:\s*([\d.]+)\s*\}"
SHIP_RE = r"shippingGross:\s*\{\s*EUR:\s*([\d.]+)\s*,\s*CZK:\s*([\d.]+)\s*\}"


def current():
    """Čo je teraz v config.js: kurz koruny a ceny dopravy."""
    s = open(CONFIG, encoding="utf-8").read()
    m = re.search(RATES_RE, s)
    if not m:
        raise SystemExit("config.js: riadok s kurzami sa nenašiel")
    n = re.search(SHIP_RE, s)
    if not n:
        raise SystemExit("config.js: riadok s dopravou sa nenašiel")
    return float(m.group(2)), float(n.group(1)), float(n.group(2))


def ecb():
    """Referenčný kurz ECB. Bez hlavičky User-Agent služba odpovie 403."""
    req = urllib.request.Request(API, headers={"User-Agent": "rncexplore/1.0"})
    d = json.load(urllib.request.urlopen(req, timeout=30))
    return d["date"], d["rates"]["CZK"]


def write(czk, ship_czk):
    s = open(CONFIG, encoding="utf-8").read()
    s2 = re.sub(RATES_RE, "rates: { EUR: 1.0, CZK: %s }" % czk, s, count=1)
    m = re.search(SHIP_RE, s2)
    s2 = re.sub(SHIP_RE, "shippingGross: { EUR: %s, CZK: %s }"
                % (_short(m.group(1)), ship_czk), s2, count=1)
    if s2 == s:
        raise SystemExit("config.js: hodnoty sa nepodarilo prepísať")
    open(CONFIG, "w", encoding="utf-8").write(s2)


def _short(v):
    """20.0 -> 20, aby v config.js nepribúdali zbytočné desatinné nuly."""
    f = float(v)
    return int(f) if f == int(f) else f


def main():
    dry = "--dry-run" in sys.argv
    old, ship_eur, old_ship = current()
    date, raw = ecb()

    want = round(raw * (1 + BUFFER), 3)
    drift = (want - old) / old * 100
    print(f"kurz ECB z {date}:")
    print(f"  1 EUR = {raw:.3f} Kč   s prirážkou {BUFFER:.0%}: {want:.3f}"
          f"   v config.js: {old} ({drift:+.1f} %)")

    # doprava v korunách sa drží toho istého kurzu, zaokrúhlená na desiatky
    ship_czk = int(round(ship_eur * want / 10.0) * 10)
    print(f"  doprava {_short(ship_eur)} € -> {ship_czk} Kč   "
          f"v config.js: {_short(old_ship)} Kč")

    if abs(want - old) / old < THRESHOLD and ship_czk == old_ship:
        print(f"\nzmena {abs(drift):.1f} % je pod prahom {THRESHOLD:.1%}"
              " — nechávam tak")
        return 0

    if dry:
        print("\nbez --dry-run by som hodnoty zapísal")
        return 0

    write(want, ship_czk)
    print(f"\nzmena {abs(drift):.1f} % nad prahom — config.js aktualizovaný")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

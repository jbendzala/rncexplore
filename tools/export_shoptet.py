# -*- coding: utf-8 -*-
"""Vypíše katalóg do CSV vo formáte, aký Shoptet sám exportuje.

Štruktúra je odpozeraná z ukážkového exportu z nášho obchodu — rovnaké
stĺpce, rovnaké úvodzovky, bodkočiarka, desatinná čiarka, UTF-8 s BOM
a konce riadkov CRLF. Vďaka tomu sa súbor dá nahrať tým istým importom.

Prevedenia jedného produktu drží pokope stĺpec pairCode: všetky riadky
toho istého panela majú rovnaké číslo. Produkt s jediným prevedením ho
má prázdny, presne ako v ukážke.

Pozor: tento formát nenesie popisy, fotografie ani zaradenie do
kategórií — na to má Shoptet iný import. Tento súbor zakladá produkty,
ceny a prevedenia.
"""
import hashlib, json, os, re, sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo

CIEL = os.path.expanduser("~/Documents/rncexplore-shoptet-produkty.csv")

# Shoptet veľký súbor odmietol, hoci malý s tou istou hlavičkou prešiel —
# ide teda o strop na objem, nie o formát. Súbor preto píšeme aj po
# dávkach. Produkt sa nikdy nerozdelí: jeho prevedenia musia prísť spolu,
# inak by Shoptet založil ten istý panel dvakrát.
DAVKA = 40          # koľko produktov najviac do jedného súboru

# Názov stĺpca s prevedením sa v Shoptete stane názvom parametra,
# ktorý zákazník uvidí nad výberom.
PARAMETER = "Prevedenie"

# Koľko kusov zapísať na sklad. Nevedieme sklad a tovar objednávame od
# Lensunu, takže nula je pravda — ale v Shoptete treba produktom nastaviť
# predaj aj pri nulovom sklade, inak sa budú tváriť ako vypredané.
SKLAD = "0"


def kod(p, v):
    """Jedinečný kód pre Shoptet.

    Lensun používa ten istý kód na rôzne autá — LS-100FX2-Max+DC nesie
    deväť rôznych panelov a tri z nich majú odlišnú cenu. Shoptet podľa
    kódu produkty páruje, takže by si ich pomiešal a prepísal navzájom.
    Preto za kód Lensunu pridávame krátku značku odvodenú z adresy
    produktu: je stále rovnaká, nemení sa pri pridaní ďalšieho panela a
    kód Lensunu zostáva na začiatku, takže objednávanie je bez zmeny.
    """
    znacka = hashlib.sha1(p["id"].encode("utf-8")).hexdigest()[:4].upper()
    return f'{v.get("sku", "")}-{znacka}'


def pole(v, uvodzovky=True):
    """Prázdna hodnota ide bez úvodzoviek, presne ako v ukážke."""
    if v == "" or v is None:
        return '""' if uvodzovky else ""
    return '"' + str(v).replace('"', '""') + '"'


def main():
    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))

    hlavicka = ("code;pairCode;name;guid;price;standardPrice;purchasePrice;"
                f'actionPrice;actionFrom;actionUntil;"variant:{PARAMETER}";stock;')
    riadky = [hlavicka]
    skupina = 0
    produktov = prevedeni = 0

    for p in P:
        viac = len(p["var"]) > 1
        if viac:
            skupina += 1
        for v in p["var"]:
            cena = f'{seo.price(v["p"], "EUR"):.2f}'.replace(".", ",")
            riadky.append(";".join([
                pole(kod(p, v)),                        # code
                pole(skupina if viac else "", False),    # pairCode
                pole(p["n"]["sk"]),                      # name
                pole("", False),                         # guid — nový produkt
                pole(cena),                              # price (s DPH)
                pole(""),                                # standardPrice
                pole(""),                                # purchasePrice
                pole(""),                                # actionPrice
                pole("", False),                         # actionFrom
                pole("", False),                         # actionUntil
                pole(v["sk"] if viac else "", False),    # variant:Prevedenie
                pole(SKLAD),                             # stock
                "",                                      # prázdny stĺpec na konci
            ]))
            prevedeni += 1
        produktov += 1

    with open(CIEL, "w", encoding="utf-8-sig", newline="") as f:
        f.write("\r\n".join(riadky) + "\r\n")
    print(f"{produktov} produktov, {prevedeni} prevedení -> {CIEL}")

    # to isté po dávkach
    davky, teraz, kusov = [], [], 0
    for p in P:
        if kusov and kusov % DAVKA == 0:
            davky.append(teraz); teraz = []
        teraz.append(p); kusov += 1
    if teraz:
        davky.append(teraz)

    print(f"\npo dávkach (najviac {DAVKA} produktov na súbor):")
    skupina = 0
    for i, cast in enumerate(davky, 1):
        rr = [hlavicka]
        for p in cast:
            viac = len(p["var"]) > 1
            if viac:
                skupina += 1
            for v in p["var"]:
                cena = f'{seo.price(v["p"], "EUR"):.2f}'.replace(".", ",")
                rr.append(";".join([
                    pole(kod(p, v)), pole(skupina if viac else "", False),
                    pole(p["n"]["sk"]), pole("", False), pole(cena),
                    pole(""), pole(""), pole(""), pole("", False), pole("", False),
                    pole(v["sk"] if viac else "", False), pole(SKLAD), "",
                ]))
        c = os.path.expanduser(f"~/Documents/rncexplore-shoptet-{i}-z-{len(davky)}.csv")
        with open(c, "w", encoding="utf-8-sig", newline="") as f:
            f.write("\r\n".join(rr) + "\r\n")
        print(f"  {os.path.basename(c):<34} {len(cast):>3} produktov · "
              f"{len(rr)-1:>3} riadkov")


if __name__ == "__main__":
    main()

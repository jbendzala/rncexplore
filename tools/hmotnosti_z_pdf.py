# -*- coding: utf-8 -*-
"""Doplní do katalógu prepravné hmotnosti z cenníkov Lensunu.

Pole kg v data/products.js bolo odhad — a zlý. Pri paneli 120 W pre ARB
stan som odhadoval 12 kg, kým skutočnosť je 4,29. Shoptet z toho počíta
cenu dopravy, takže na tom záleží.

Lensun posiela špecifikácie v PDF a v nich sú dva stĺpce: Net Weight
(samotný panel) a Packing Gross Weight (zabalená zásielka). Nás zaujíma
ten druhý.

Pozor na poradie stĺpcov — v cenníku panelov na kapotu je prepravná
hmotnosť pred čistou, v ostatných dvoch naopak. Preto sa poradie zadáva
pri každom súbore zvlášť a výsledok sa kontroluje: prepravná nemôže byť
menšia než čistá.

Katalóg a cenníky sa prekrývajú len čiastočne — zhoduje sa zhruba
dvetretiny kódov. Pre zvyšok sa hmotnosť odhadne z mediánu rovnako
výkonných panelov v cenníku, čo je stále oveľa bližšie než pôvodné
čísla. Viacpanelové zostavy sa neodhadujú vôbec: balia sa inak a rozptyl
je priveľký, tie zostanú na pôvodnej hodnote a vypíšu sa.

Potrebuje poppler (pdftotext).

Spustenie:  python3 tools/hmotnosti_z_pdf.py [--zapis]
"""
import json
import os
import re
import statistics
import subprocess
import sys

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import vystup

ZDROJ = os.path.expanduser("~/Documents/rncexplore-podklady/hmotnosti")

# Poradie stĺpcov s hmotnosťami sa medzi cenníkmi líši.
PORADIE = {
    "Hood solar panels": "prepravna-prva",
    "Ikamper": "cista-prva",
    "Foldable": "cista-prva",
}

KOD = r"(?:\d+\*)?LS-[A-Za-z0-9][A-Za-z0-9+*/\-]*"
RIADOK = re.compile(
    rf"({KOD})\b(.{{0,300}}?)(\d+(?:\.\d+)?)\s*W\*?\d*(.{{0,200}}?)"
    r"(\d+(?:\.\d+)?)\s*kgs?\s+(\d+(?:\.\d+)?)\s*kgs?", re.S)

# Zostavy z viacerých panelov. Balia sa inak a odhadovať ich nemá zmysel.
# Hľadať to treba aj v názvoch prevedení — GMC Sierra sa volá „solárne
# panely na kryt korby“ a že sú dva alebo tri, je až v prevedení.
# Pozor na „FX2“ v kódoch — x2 sa smie chytiť len vtedy, keď pred ním nie
# je písmeno, inak by sa za viacpanelovú zostavu označil takmer každý
# produkt v katalógu.
VIAC_PANELOV = re.compile(
    r"\bdva\b|\btri\b|(?<![A-Za-z])x\s*[23]\b|\d+\s*[*x]\s*\d+\s*W", re.I)


def viac_panelov(p):
    texty = [p["n"]["sk"], p.get("sku", "")] + [v["sk"] for v in p["var"]] \
            + [v.get("sku", "") for v in p["var"]]
    return any(VIAC_PANELOV.search(t) for t in texty if t)


def norm(k):
    return re.sub(r"[^A-Z0-9]", "", k.upper())


def z_pdf():
    """Vytiahne z cenníkov trojice kód, výkon, prepravná hmotnosť."""
    if not os.path.isdir(ZDROJ):
        sys.exit(f"priečinok s cenníkmi neexistuje: {ZDROJ}")
    riadky, sporne = [], []
    for subor in sorted(os.listdir(ZDROJ)):
        if not subor.lower().endswith(".pdf"):
            continue
        poradie = next((v for k, v in PORADIE.items() if k.lower() in subor.lower()),
                       None)
        if poradie is None:
            print(f"   preskakujem {subor} — neviem poradie stĺpcov")
            continue
        try:
            txt = subprocess.run(["pdftotext", "-layout",
                                  os.path.join(ZDROJ, subor), "-"],
                                 capture_output=True, text=True, check=True).stdout
        except FileNotFoundError:
            sys.exit("chýba pdftotext — nainštaluj poppler")
        n = 0
        for m in RIADOK.finditer(txt):
            a, b = float(m.group(5)), float(m.group(6))
            prepravna, cista = (a, b) if poradie == "prepravna-prva" else (b, a)
            if prepravna < cista:                 # poradie stĺpcov nesedí
                sporne.append((subor, m.group(1), cista, prepravna))
                continue
            riadky.append((m.group(1), float(m.group(3)), prepravna))
            n += 1
        print(f"   {subor[:46]:<48} {n:>3} riadkov")
    if sporne:
        print(f"\n   POZOR: {len(sporne)} riadkov má prepravnú menšiu než čistú")
        for s in sporne[:5]:
            print(f"      {s[0][:28]} {s[1]} — čistá {s[2]}, prepravná {s[3]}")
    return riadky


def main():
    zapisat = "--zapis" in sys.argv
    print("čítam cenníky:")
    riadky = z_pdf()
    podla_kodu = {}
    for kod, w, kg in riadky:
        podla_kodu.setdefault(norm(kod), kg)
    print(f"\nrôznych kódov: {len(podla_kodu)}")

    s = open(os.path.join(KOREN, "data", "products.js"), encoding="utf-8").read()
    P = json.loads(re.search(r"window\.PRODUCTS=(\[.*\]);", s, re.S).group(1))

    z_cennika = odhad = nechane = 0
    zmeny = []
    for p in P:
        stara = p["kg"]
        kod = norm(p.get("sku", ""))
        if kod in podla_kodu:
            nova, ako = podla_kodu[kod], "z cenníka"
            z_cennika += 1
        elif viac_panelov(p):
            nechane += 1
            continue
        else:
            # medián rovnako výkonných panelov v cenníku
            okolie = [kg for _, w, kg in riadky if abs(w - (p["w"] or 0)) <= 10]
            if not okolie:
                nechane += 1
                continue
            nova, ako = round(statistics.median(okolie), 2), "odhad podľa výkonu"
            odhad += 1
        if abs(nova - stara) > 0.01:
            zmeny.append((p["n"]["sk"], p["w"], stara, nova, ako))
        p["kg"] = nova

    print(f"\nz cenníka presne:        {z_cennika:>4}")
    print(f"odhad podľa výkonu:      {odhad:>4}")
    print(f"ponechané (viac panelov) {nechane:>4}")
    print(f"zmenených hmotností:     {len(zmeny):>4}")
    if zmeny:
        stare = [z[2] for z in zmeny]; nove = [z[3] for z in zmeny]
        print(f"priemer pred {statistics.mean(stare):>5.1f} kg  "
              f"po {statistics.mean(nove):>5.1f} kg")
        print("\nnajväčšie rozdiely:")
        for n, w, a, b, ako in sorted(zmeny, key=lambda z: -(z[2] - z[3]))[:10]:
            print(f"   {n[:42]:<44} {w:>4} W   {a:>5} -> {b:<6} {ako}")

    sprava = vystup.kam(vystup.NASE, "hmotnosti.csv")
    with open(sprava, "w", encoding="utf-8-sig", newline="") as f:
        f.write("Produkt;Výkon (W);Pôvodná (kg);Nová (kg);Zdroj\n")
        for n, w, a, b, ako in sorted(zmeny, key=lambda z: z[0]):
            f.write(f"{n};{w};{str(a).replace('.', ',')};"
                    f"{str(b).replace('.', ',')};{ako}\n")
    print(f"\nprehľad zmien -> {sprava}")

    if not zapisat:
        print("\nKATALÓG SA NEZMENIL. Keď je to v poriadku, spusti znova s --zapis")
        return
    meta = re.search(r"window\.CATALOG_META=(\{.*?\});", s, re.S).group(1)
    with open(os.path.join(KOREN, "data", "products.js"), "w", encoding="utf-8") as f:
        f.write("/* Generované dáta katalógu — negenerujte ručne. */\n")
        f.write("window.CATALOG_META=" + meta + ";\n")
        f.write("window.PRODUCTS=" + json.dumps(P, ensure_ascii=False,
                                                separators=(",", ":")) + ";\n")
    print("katalóg zapísaný")


if __name__ == "__main__":
    main()

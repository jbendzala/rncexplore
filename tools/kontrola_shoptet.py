# -*- coding: utf-8 -*-
"""Porovná export zo Shoptetu s našim katalógom.

Spustenie:  python3 tools/kontrola_shoptet.py ~/Downloads/products.xml

Export obchodu má desaťtisíce riadkov, takže sa nedá prečítať očami ani
poslať do správy. Tento skript z neho urobí pár riadkov: počty, čo chýba,
ktoré kódy sa nespárovali a kde nesúhlasí cena alebo názov prevedenia.

Čo nájde, je vždy jedna z troch vecí: buď sa niečo neimportovalo, alebo
sa kód pri importe premenil inak, než čakáme, alebo niekto zmenil údaj
v administrácii a náš katalóg o tom nevie.
"""
import json, os, re, sys, xml.etree.ElementTree as ET

TU = os.path.dirname(os.path.abspath(__file__))
KOREN = os.path.dirname(TU)
sys.path.insert(0, TU)
import seo
from export_shoptet_xml import shoptet_kod, DELIT

def nas_katalog():
    s = open(os.path.join(KOREN, 'data', 'products.js'), encoding='utf-8').read()
    P = json.loads(re.search(r'window\.PRODUCTS=(\[.*\]);', s, re.S).group(1))
    meta = json.loads(re.search(r'window\.CATALOG_META=(\{.*?\});', s, re.S).group(1))
    kat = {c['k']: c['sk'] for c in meta['cats']}
    naše = {}
    for p in P:
        for v in p['var']:
            naše[shoptet_kod(p, v)] = {
                'nazov': p['n']['sk'], 'prev': v['sk'],
                'cena': round(seo.price(v['p'], 'EUR'), 2),
                'kat': kat[p['cat']], 'fotiek': len(p.get('img') or []),
            }
    return P, naše, kat

def main(cesta):
    P, naše, kategorie = nas_katalog()
    r = ET.parse(cesta).getroot()
    polozky = r.findall('SHOPITEM')

    print(f'súbor      {os.path.basename(cesta)}  '
          f'{os.path.getsize(cesta)/1024/1024:.1f} MB')
    print(f'produktov  {len(polozky):>5}   katalóg {len(P)}')

    v_shope, bez_popisu, bez_fotiek, bez_kat = {}, [], [], []
    kat_produktu = {}
    for it in polozky:
        nazov = (it.findtext('NAME') or '').strip()
        if not (it.findtext('DESCRIPTION') or '').strip():
            bez_popisu.append(nazov)
        if it.find('IMAGES') is None or not it.findall('IMAGES/IMAGE'):
            bez_fotiek.append(nazov)
        kat_produktu[nazov] = {k.text for k in it.findall('CATEGORIES/CATEGORY')}
        if not kat_produktu[nazov]:
            bez_kat.append(nazov)
        varianty = it.findall('VARIANTS/VARIANT') or [it]
        for v in varianty:
            k = (v.findtext('CODE') or '').strip()
            if not k:
                continue
            cena = v.findtext('PRICE')
            v_shope[k] = {
                'nazov': nazov,
                'prev': (v.findtext('PARAMETERS/PARAMETER/VALUE') or '').strip(),
                'cena': round(float(cena), 2) if cena else None,
            }

    print(f'prevedení  {len(v_shope):>5}   katalóg {len(naše)}')
    print(f'fotografií {len(list(r.iter("IMAGE"))):>5}   '
          f'katalóg {sum(len(p.get("img") or []) for p in P)}')
    print()
    print(f'bez popisu      {len(bez_popisu):>4}')
    print(f'bez fotografie  {len(bez_fotiek):>4}')
    print(f'bez kategórie   {len(bez_kat):>4}')
    for m, z in (('bez popisu', bez_popisu), ('bez fotografie', bez_fotiek),
                 ('bez kategórie', bez_kat)):
        if z and len(z) <= 8:
            for n in z:
                print(f'   {m}: {n}')

    chyba = sorted(set(naše) - set(v_shope))
    navyse = sorted(set(v_shope) - set(naše))
    print()
    print(f'kódy, ktoré v obchode chýbajú   {len(chyba):>4}')
    print(f'kódy v obchode navyše           {len(navyse):>4}')
    for k in chyba[:6]: print(f'   chýba:  {k}  {naše[k]["nazov"][:46]}')
    for k in navyse[:6]: print(f'   navyše: {k}  {v_shope[k]["nazov"][:46]}')

    zlecena, zlestitok, bezceny = [], [], []
    for k in sorted(set(naše) & set(v_shope)):
        a, b = naše[k], v_shope[k]
        if b['cena'] is None:
            bezceny.append(k)
        elif abs(a['cena'] - b['cena']) > 0.005:
            zlecena.append((k, a['cena'], b['cena'], a['nazov']))
        if b['prev'] and a['prev'] != b['prev']:
            zlestitok.append((k, a['prev'], b['prev']))

    # Zaradenie do kategórií. Posielame rodiča aj podkategóriu, ale Shoptet
    # rodiča zahodí — produkt v podkategórii považuje za zaradený aj v nej,
    # takže vo výpise rodiča sa objaví tak či tak. Za správne preto berieme
    # obe podoby.
    zle_kat = []
    for p in P:
        kat = kategorie[p['cat']]
        pod = f'{kat} > {p["b"]}' if p['cat'] in DELIT and p.get('b') else None
        ok = [{kat}] if pod is None else [{pod}, {kat, pod}]
        maju = kat_produktu.get(p['n']['sk'])
        if maju is None or maju not in ok:
            zle_kat.append((p['n']['sk'], sorted(maju) if maju else None,
                            sorted(ok[-1])))
    print()
    print(f'zlé zaradenie do kategórií {len(zle_kat):>4}')
    for n, m, c in zle_kat[:8]:
        print(f'   {n[:44]:<46} má {m}  čakáme {c}')

    print()
    print(f'prevedení bez ceny      {len(bezceny):>4}')
    print(f'nesúhlasná cena         {len(zlecena):>4}')
    print(f'nesúhlasný názov prev.  {len(zlestitok):>4}')
    for k in bezceny[:6]: print(f'   bez ceny: {k}')
    for k, m, s_, n in zlecena[:10]:
        print(f'   cena: {k:<30} naše {m:>8.2f}  shoptet {s_:>8.2f}  {n[:34]}')
    for k, m, s_ in zlestitok[:10]:
        print(f'   názov: {k:<30} naše „{m}“  shoptet „{s_}“')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('použitie: python3 tools/kontrola_shoptet.py cesta/k/exportu.xml')
    main(sys.argv[1])

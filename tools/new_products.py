# -*- coding: utf-8 -*-
"""Čo pridať do katalógu z aktuálnej ponuky Lensunu.

Z Lensunu sa dá stiahnuť cena, prevedenia, fotografie aj technické údaje,
ale nie slovenský a český text — ten je tu. Zvyšok doplní add_products.py.
Súbor drží vždy práve rozpracovanú dávku; čo už v katalógu je, skript
preskočí, takže sa nič nezduplikuje.

Výber sleduje pravidlo, podľa ktorého katalóg vznikol: vozidlá predávané
v Európe a univerzálna výbava. Americké, austrálske a japonské modely
(Tacoma, Tundra, 4Runner, Sequoia, GMC Sierra) a nadstavby prívesov, ktoré
sa u nás nepredávajú (Load Trail, TurtleBack, Kimberley, Intrepid), v ňom
nie sú a nepribúdajú.
"""


def _dvoj(sk, cs):
    return sk, cs


def hood(model_sk, model_cs, w):
    """Popis panela na kapotu. Vo všetkých je tá istá veta, mení sa vozidlo."""
    return _dvoj(
        f"Solárny panel s výkonom {w} W tvarovaný presne na kapotu vozidla "
        f"{model_sk}. Dobíja štartovaciu aj trakčnú batériu počas státia, takže "
        "chladnička, kamera či osvetlenie fungujú bez naštartovania motora. "
        "Lepí sa priamo na plech, bez vŕtania.",
        f"Solární panel o výkonu {w} W tvarovaný přesně na kapotu vozu "
        f"{model_cs}. Dobíjí startovací i trakční baterii při stání, takže "
        "lednice, kamera či osvětlení fungují bez nastartování motoru. "
        "Lepí se přímo na plech, bez vrtání.")


def flexi(w):
    """Univerzálny flexibilný panel bez väzby na konkrétne vozidlo."""
    return _dvoj(
        f"Flexibilný panel {w} W s hrúbkou niekoľkých milimetrov sa prispôsobí "
        "zakriveniu strechy, kapoty alebo nadstavby. Montuje sa nalepením, bez "
        "hliníkového rámu a bez zásahu do karosérie.",
        f"Flexibilní panel {w} W o tloušťce několika milimetrů se přizpůsobí "
        "zakřivení střechy, kapoty nebo nástavby. Montuje se nalepením, bez "
        "hliníkového rámu a bez zásahu do karoserie.")


def stan(w, stan_sk, stan_cs):
    """Panel tvarovaný na konkrétny strešný stan alebo nadstavbu."""
    return _dvoj(
        f"Panel {w} W tvarovaný na {stan_sk}. Kopíruje tvar škrupiny a dobíja "
        "batériu tábora bez toho, aby ste prišli o miesto na streche.",
        f"Panel {w} W tvarovaný na {stan_cs}. Kopíruje tvar skořepiny a dobíjí "
        "baterii tábora, aniž byste přišli o místo na střeše.")


def rec(h, cat, b, w, sk, cs, dsk, dcs, spec=None):
    """spec sa použije len tam, kde Lensun parametre nepíše v riadkoch
    „Peak power: …“, ale rozsypané vo vetách — inak si ich skript stiahne."""
    z = {"h": h, "cat": cat, "b": b, "w": w,
         "sk": sk, "cs": cs, "dsk": dsk, "dcs": dcs}
    if spec:
        z["spec"] = spec
    return z


def hrec(h, b, w, sk, cs, model_sk, model_cs):
    dsk, dcs = hood(model_sk, model_cs, w)
    return rec(h, "hood", b, w, sk, cs, dsk, dcs)


def frec(h, w, sk, cs):
    dsk, dcs = flexi(w)
    return rec(h, "flexible", None, w, sk, cs, dsk, dcs)


def srec(h, w, sk, cs, stan_sk, stan_cs):
    dsk, dcs = stan(w, stan_sk, stan_cs)
    return rec(h, "rooftent", None, w, sk, cs, dsk, dcs)


def box(w, co_sk, co_cs):
    """Panel tvarovaný na nadstavbu prívesu alebo kryt korby."""
    return _dvoj(
        f"Panel {w} W tvarovaný na {co_sk}. Lepí sa priamo na plech a dobíja "
        "batériu prívesu či vozidla počas státia, bez strešného nosiča a bez "
        "vŕtania.",
        f"Panel {w} W tvarovaný na {co_cs}. Lepí se přímo na plech a dobíjí "
        "baterii přívěsu či vozu při stání, bez střešního nosiče a bez "
        "vrtání.")


def brec(h, cat, w, sk, cs, co_sk, co_cs):
    dsk, dcs = box(w, co_sk, co_cs)
    return rec(h, cat, None, w, sk, cs, dsk, dcs)


NAHRADY = []          # tentoraz Lensun nič nestiahol, len pridal

NOVE = [
    # ---------------------------------------------------------- Nissan
    hrec("nissan-navara-d21-lensun-110w-hood-bonnet-solar-panel", "Nissan", 110,
         "Nissan Navara D21 – 110W solárny panel na kapotu",
         "Nissan Navara D21 – 110W solární panel na kapotu",
         "Nissan Navara D21", "Nissan Navara D21"),
    hrec("nissan-navara-2nd-3rd-gen-lensun-90w-bonnet-solar-panel", "Nissan", 90,
         "Nissan Navara 2. a 3. generácia (2005–2021) – 90W solárny panel na kapotu",
         "Nissan Navara 2. a 3. generace (2005–2021) – 90W solární panel na kapotu",
         "Nissan Navara 2. a 3. generácia (2005–2021)",
         "Nissan Navara 2. a 3. generace (2005–2021)"),
    hrec("nissan-navara-lensun-82w-bonnet-hood-solar-panel", "Nissan", 82,
         "Nissan Navara (2021–súčasnosť) – 82W solárny panel na kapotu",
         "Nissan Navara (2021–současnost) – 82W solární panel na kapotu",
         "Nissan Navara (2021–súčasnosť)", "Nissan Navara (2021–současnost)"),

    hrec("nissan-pathfinder-3rd-gen-lensun-100w-hood-flexible-solar-panel", "Nissan", 100,
         "Nissan Pathfinder 3. generácia (2004–2011) – 100W flexibilný solárny panel na kapotu",
         "Nissan Pathfinder 3. generace (2004–2011) – 100W flexibilní solární panel na kapotu",
         "Nissan Pathfinder 3. generácia (2004–2011)",
         "Nissan Pathfinder 3. generace (2004–2011)"),
    hrec("pathfinder-4th-gen-lensun-90w-hood-solar-panel", "Nissan", 90,
         "Nissan Pathfinder 4. generácia (2012–2021) – 90W solárny panel na kapotu",
         "Nissan Pathfinder 4. generace (2012–2021) – 90W solární panel na kapotu",
         "Nissan Pathfinder 4. generácia (2012–2021)",
         "Nissan Pathfinder 4. generace (2012–2021)"),
    hrec("nissan-pathfinder-5th-gen-lensun-100w-hood-flexible-solar-panel", "Nissan", 100,
         "Nissan Pathfinder 5. generácia (2022–súčasnosť) – 100W solárny panel na kapotu",
         "Nissan Pathfinder 5. generace (2022–současnost) – 100W solární panel na kapotu",
         "Nissan Pathfinder 5. generácia (2022–súčasnosť)",
         "Nissan Pathfinder 5. generace (2022–současnost)"),

    hrec("nissan-patrol-y61-y62-with-scoop-lensun-125w-bonnet-flexible-solar-panel", "Nissan", 125,
         "Nissan Patrol Y61 a Y62 so vzduchovodom – 125W flexibilný solárny panel na kapotu",
         "Nissan Patrol Y61 a Y62 se vzduchovodem – 125W flexibilní solární panel na kapotu",
         "Nissan Patrol Y61 a Y62 so vzduchovodom na kapote",
         "Nissan Patrol Y61 a Y62 se vzduchovodem na kapotě"),
    hrec("nissan-patrol-y61-no-scoop-lensun-110w-bonnet-flexible-solar-panel", "Nissan", 110,
         "Nissan Patrol 5. generácia Y61 bez vzduchovodu – 110W flexibilný solárny panel na kapotu",
         "Nissan Patrol 5. generace Y61 bez vzduchovodu – 110W flexibilní solární panel na kapotu",
         "Nissan Patrol 5. generácia Y61 bez vzduchovodu na kapote",
         "Nissan Patrol 5. generace Y61 bez vzduchovodu na kapotě"),
    hrec("nissan-patrol-gr-y61-lensun-100w-bonnet-flexible-solar-panel", "Nissan", 100,
         "Nissan Patrol GR Y61 (1997–2016) – 100W flexibilný solárny panel na kapotu",
         "Nissan Patrol GR Y61 (1997–2016) – 100W flexibilní solární panel na kapotu",
         "Nissan Patrol GR Y61 (1997–2016)", "Nissan Patrol GR Y61 (1997–2016)"),
    hrec("nissan-patrol-gq-y60-lensun-110w-bonnet-flexible-solar-panel", "Nissan", 110,
         "Nissan Patrol GQ Y60 (1987–1997) – 110W flexibilný solárny panel na kapotu",
         "Nissan Patrol GQ Y60 (1987–1997) – 110W flexibilní solární panel na kapotu",
         "Nissan Patrol GQ Y60 (1987–1997)", "Nissan Patrol GQ Y60 (1987–1997)"),
    hrec("nissan-patrol-y60-lensun-120w-hood-bonnet-flexible-solar-panel", "Nissan", 120,
         "Nissan Patrol Y60 (1993–2001) – 120W flexibilný solárny panel na kapotu",
         "Nissan Patrol Y60 (1993–2001) – 120W flexibilní solární panel na kapotu",
         "Nissan Patrol Y60 (1993–2001)", "Nissan Patrol Y60 (1993–2001)"),
    hrec("nissan-patrol-y62-lensun-60w-hood-flexible-solar-panel", "Nissan", 60,
         "Nissan Patrol Y62 (2020–súčasnosť) – 60W flexibilný solárny panel na kapotu",
         "Nissan Patrol Y62 (2020–současnost) – 60W flexibilní solární panel na kapotu",
         "Nissan Patrol Y62 (2020–súčasnosť)", "Nissan Patrol Y62 (2020–současnost)"),

    hrec("x-trail-lensun-90w-hood-bonnet-solar-panel", "Nissan", 90,
         "Nissan X-Trail 2. generácia (2007–2013) – 90W solárny panel na kapotu",
         "Nissan X-Trail 2. generace (2007–2013) – 90W solární panel na kapotu",
         "Nissan X-Trail 2. generácia (2007–2013)",
         "Nissan X-Trail 2. generace (2007–2013)"),

    # ---------------------------------------------------------- Porsche
    hrec("porsche-cayenne-lensun-75w-hood-bonnet-flexible-solar-panel", "Porsche", 75,
         "Porsche Cayenne 1. generácia Turbo (2003–2010) – 75W flexibilný solárny panel na kapotu",
         "Porsche Cayenne 1. generace Turbo (2003–2010) – 75W flexibilní solární panel na kapotu",
         "Porsche Cayenne 1. generácia Turbo (2003–2010)",
         "Porsche Cayenne 1. generace Turbo (2003–2010)"),
    hrec("porsche-cayenne-2nd-gen-lensun-75w-hood-solar-panel", "Porsche", 75,
         "Porsche Cayenne 2. generácia (2010–2018) – 75W solárny panel na kapotu",
         "Porsche Cayenne 2. generace (2010–2018) – 75W solární panel na kapotu",
         "Porsche Cayenne 2. generácia (2010–2018)",
         "Porsche Cayenne 2. generace (2010–2018)"),

    # ------------------------------------------- univerzálne flexibilné
    frec("lensunsolar-20w-black-flexible-solar-panel", 20,
         "Flexibilný solárny panel 20W", "Flexibilní solární panel 20W"),
    frec("lensunsolar-30w-12v-black-flexible-solar-panel", 30,
         "Flexibilný solárny panel 30W", "Flexibilní solární panel 30W"),
    frec("lensunsolar-50w-12v-full-black-flexible-solar-panel", 50,
         "Flexibilný solárny panel 50W", "Flexibilní solární panel 50W"),
    frec("lensunsolar-70w-black-12v-flexible-solar-panel", 70,
         "Flexibilný solárny panel 70W", "Flexibilní solární panel 70W"),
    frec("lensun-100w-flexible-solar-panel", 100,
         "Flexibilný solárny panel 100W", "Flexibilní solární panel 100W"),
    frec("lensun-110w-12v-full-black-flexible-solar-panel", 110,
         "Flexibilný solárny panel 110W", "Flexibilní solární panel 110W"),
    frec("lensun-120w-full-black-flexible-solar-panel", 120,
         "Flexibilný solárny panel 120W", "Flexibilní solární panel 120W"),
    frec("lensun-130w-black-flexible-solar-panel", 130,
         "Flexibilný solárny panel 130W", "Flexibilní solární panel 130W"),
    frec("lensun-150w-black-flexible-solar-panel", 150,
         "Flexibilný solárny panel 150W", "Flexibilní solární panel 150W"),
    frec("lensun-300w-150w-flexible-solar-panel", 300,
         "Flexibilný solárny panel 300W (2 × 150 W)",
         "Flexibilní solární panel 300W (2 × 150 W)"),

    # ------------------------------------------ prenosné a skladacie
    rec("lensun-24w-waterproof-solar-charger", "foldable", None, 24,
        "Solárna nabíjačka 24W s USB a USB-C",
        "Solární nabíječka 24W s USB a USB-C",
        "Solárna nabíjačka 24 W s výstupom USB aj USB-C. Váži 380 gramov, "
        "zavesí sa na batoh alebo stan a nabíja telefón či powerbanku priamo, "
        "bez ďalšej elektroniky. Krytie IP67 znesie dážď aj prach.",
        "Solární nabíječka 24 W s výstupem USB i USB-C. Váží 380 gramů, "
        "zavěsí se na batoh nebo stan a nabíjí telefon či powerbanku přímo, "
        "bez další elektroniky. Krytí IP67 snese déšť i prach."),
    rec("lensun-30w-waterproof-solar-charger", "foldable", None, 30,
        "Solárna nabíjačka 30W s USB a USB-C",
        "Solární nabíječka 30W s USB a USB-C",
        "Solárna nabíjačka 30 W s výstupom USB aj USB-C a s vyklápacími "
        "nožičkami, ktoré ju natočia k slnku. Zavesí sa na batoh alebo stan, "
        "krytie IP67 znesie dážď aj prach.",
        "Solární nabíječka 30 W s výstupem USB i USB-C a s vyklápěcími "
        "nožičkami, které ji natočí ke slunci. Zavěsí se na batoh nebo stan, "
        "krytí IP67 snese déšť i prach."),
    rec("lensunsolar-60w-waterproof-foldable-solar-panel", "foldable", None, 60,
        "Skladacia solárna nabíjačka 60W", "Skládací solární nabíječka 60W",
        "Skladacia nabíjačka 60 W so štyrmi výstupmi — dvakrát USB, USB-C a "
        "jednosmerný konektor pre elektrocentrálu. Zložená má necelé dva "
        "kilogramy a rozmer bežného zošita.",
        "Skládací nabíječka 60 W se čtyřmi výstupy — dvakrát USB, USB-C a "
        "stejnosměrný konektor pro elektrocentrálu. Složená má necelé dva "
        "kilogramy a rozměr běžného sešitu."),
    rec("lensun-55w-solar-panel-with-kickstand", "foldable", None, 55,
        "Solárny panel 55W s hliníkovým rámom a stojanom",
        "Solární panel 55W s hliníkovým rámem a stojanem",
        "Panel 55 W v hliníkovom ráme s vyklápacím stojanom, ktorý ho natočí "
        "k slnku a získa tak približne o štvrtinu viac energie než panel "
        "položený naplocho. Váži dva kilogramy, v balení je prenosná taška.",
        "Panel 55 W v hliníkovém rámu s vyklápěcím stojanem, který jej natočí "
        "ke slunci a získá tak přibližně o čtvrtinu více energie než panel "
        "položený naplocho. Váží dva kilogramy, v balení je přenosná taška."),
    rec("lensun-innovative-30w-solar-panel-with-aluminium-frame", "foldable", None, 30,
        "Solárny panel 30W s hliníkovým rámom a stojanom",
        "Solární panel 30W s hliníkovým rámem a stojanem",
        "Panel 30 W v hliníkovom ráme so stojanom, celý váži 1,3 kilogramu. "
        "Rohy sú chránené, takže znesie prevoz v batožinovom priestore aj "
        "postavenie na kameni.",
        "Panel 30 W v hliníkovém rámu se stojanem, celý váží 1,3 kilogramu. "
        "Rohy jsou chráněné, takže snese převoz v zavazadlovém prostoru i "
        "postavení na kameni.",
        spec={"w": "30 W", "eff": "23,5 %", "kg": "1,3 kg"}),
    rec("lensun-70w-foldable-solar-panel", "foldable", None, 70,
        "Skladacia solárna nabíjačka 70W pre telefón a notebook",
        "Skládací solární nabíječka 70W pro telefon a notebook",
        "Skladacia nabíjačka 70 W so štyrmi výstupmi naraz — USB, USB s "
        "rýchlonabíjaním, USB-C a jednosmerných 18 V pre notebook alebo "
        "elektrocentrálu. V balení je osem redukcií.",
        "Skládací nabíječka 70 W se čtyřmi výstupy naráz — USB, USB s "
        "rychlonabíjením, USB-C a stejnosměrných 18 V pro notebook nebo "
        "elektrocentrálu. V balení je osm redukcí."),
    rec("lensun-100w-waterproof-foldable-solar-panel", "foldable", None, 100,
        "Vodotesný skladací solárny panel 100W",
        "Vodotěsný skládací solární panel 100W",
        "Skladací panel 100 W v jedenásťvrstvovej laminácii s krytím IP67. "
        "Zložený má rozmer 61 × 54 cm a váži 3,3 kilogramu. V balení je "
        "redukcia štyri v jednom, ktorá sadne na bežné elektrocentrály.",
        "Skládací panel 100 W v jedenáctivrstvé laminaci s krytím IP67. "
        "Složený má rozměr 61 × 54 cm a váží 3,3 kilogramu. V balení je "
        "redukce čtyři v jednom, která sedne na běžné elektrocentrály."),
    rec("lensun-200w-waterproof-foldable-solar-panel", "foldable", None, 200,
        "Vodotesný skladací solárny panel 200W",
        "Vodotěsný skládací solární panel 200W",
        "Skladací panel 200 W v jedenásťvrstvovej laminácii s krytím IP67, "
        "zložený váži 5,75 kilogramu. Vyklápacie nožičky ho natočia k slnku a "
        "získajú tak približne o tretinu viac energie než poloha naplocho.",
        "Skládací panel 200 W v jedenáctivrstvé laminaci s krytím IP67, "
        "složený váží 5,75 kilogramu. Vyklápěcí nožičky jej natočí ke slunci a "
        "získají tak přibližně o třetinu více energie než poloha naplocho."),
    rec("lensun-200w-36v-foldable-solar-panel", "foldable", None, 200,
        "Skladací solárny panel 200W pre 24V batériu (36 V)",
        "Skládací solární panel 200W pro 24V baterii (36 V)",
        "Skladací panel 200 W s pracovným napätím 36 V pre 24V batérie a "
        "elektrocentrály, ktoré vyžadujú vyššie napätie na vstupe. Zložený "
        "váži 5,9 kilogramu a v balení sú tri redukcie.",
        "Skládací panel 200 W s pracovním napětím 36 V pro 24V baterie a "
        "elektrocentrály, které vyžadují vyšší napětí na vstupu. Složený "
        "váží 5,9 kilogramu a v balení jsou tři redukce."),
    rec("lensun-innovative-waterproof-300w-foldable-solar-panel", "foldable", None, 300,
        "Skladací solárny kufrík 300W", "Skládací solární kufřík 300W",
        "Skladacia zostava 300 W v hliníkovom ráme s magnetickým uzáverom, "
        "ktorá sa prenáša ako kufrík. Váži 11 kilogramov namiesto dvadsiatich "
        "piatich pri sklenenom paneli rovnakého výkonu.",
        "Skládací sestava 300 W v hliníkovém rámu s magnetickým uzávěrem, "
        "která se přenáší jako kufřík. Váží 11 kilogramů namísto dvaceti "
        "pěti u skleněného panelu stejného výkonu.",
        spec={"w": "300 W", "eff": "23,5 %", "kg": "11 kg"}),
    rec("lensun-waterproof-500w-portable-solar-panel-suitcase", "foldable", None, 500,
        "Skladací solárny kufrík 500W", "Skládací solární kufřík 500W",
        "Skladacia zostava 500 W s článkami s účinnosťou 25,8 % a krytím "
        "IP67. Váži 9,2 kilogramu, čo je výrazne menej než iné panely tohto "
        "výkonu, a zložená sa zmestí aj za sedadlo.",
        "Skládací sestava 500 W s články s účinností 25,8 % a krytím "
        "IP67. Váží 9,2 kilogramu, což je výrazně méně než jiné panely "
        "tohoto výkonu, a složená se vejde i za sedadlo."),

    # ---------------------------------------------------------- deka
    rec("lensunsolar-300w-12v-solar-blanket-for-power-station-12v-battery",
        "blanket", None, 300,
        "Solárna deka 300W pre 12V batériu", "Solární deka 300W pro 12V baterii",
        "Solárna deka 300 W pre 12V batériu alebo elektrocentrálu. Zloží sa na "
        "deviatinu veľkosti a váži 7,6 kg. Vodotesná tkanina znesie prach aj "
        "dážď a pracuje od −40 do 85 °C.",
        "Solární deka 300 W pro 12V baterii nebo elektrocentrálu. Složí se na "
        "devítinu velikosti a váží 7,6 kg. Vodotěsná tkanina snese prach i "
        "déšť a pracuje od −40 do 85 °C."),

    # -------------------------------------------------- na strešné stany
    srec("lensun-110w-flexible-solar-panel-for-ikamper-roof-tent", 110,
         "Solárny panel 110W na strešný stan iKamper Skycamp",
         "Solární panel 110W na střešní stan iKamper Skycamp",
         "strešný stan iKamper Skycamp 2.0 a 3.0",
         "střešní stan iKamper Skycamp 2.0 a 3.0"),
    srec("ikamper-skycamp-roof-tent-lensun-330w-flexible-solar-panel", 330,
         "Solárny panel 330W na strešný stan iKamper Skycamp 3.0",
         "Solární panel 330W na střešní stan iKamper Skycamp 3.0",
         "strešný stan iKamper Skycamp 3.0 ako zostava troch panelov",
         "střešní stan iKamper Skycamp 3.0 jako sestava tří panelů"),
    srec("ikamper-skycamp-4-0-roof-tent-lensun-300w-flexible-solar-panel", 300,
         "Solárny panel 300W na strešný stan iKamper Skycamp 4.0",
         "Solární panel 300W na střešní stan iKamper Skycamp 4.0",
         "strešný stan iKamper Skycamp 4.0", "střešní stan iKamper Skycamp 4.0"),
    srec("lensun-120w-flexible-solar-panel-for-arb-esperance-v2-rooftop-tent", 120,
         "Solárny panel 120W na strešný stan ARB Esperance V2",
         "Solární panel 120W na střešní stan ARB Esperance V2",
         "strešný stan ARB Esperance V2 ako zostava troch panelov",
         "střešní stan ARB Esperance V2 jako sestava tří panelů"),
    srec("alu-cab-rooftent-lensun-300w-flexible-solar-panel", 300,
         "Solárny panel 300W na strešný stan Alu-Cab RT-4S",
         "Solární panel 300W na střešní stan Alu-Cab RT-4S",
         "strešný stan Alu-Cab RT-4S generácie 3-R, 3 a 3.1",
         "střešní stan Alu-Cab RT-4S generace 3-R, 3 a 3.1"),
    srec("lensun-480w-240w-flexible-solar-panel-for-roof-tent", 480,
         "Solárny panel 480W na strešný stan (2 × 240 W)",
         "Solární panel 480W na střešní stan (2 × 240 W)",
         "strešný stan ako dvojica panelov s článkami Back Contact",
         "střešní stan jako dvojice panelů s články Back Contact"),

    # ------------------------ doplnené na žiadosť zákazníka (29. 9. 2026)
    # Pôvodne vynechané ako takmer-duplikáty alebo mimoeurópske vozidlá.
    # Keď je cieľom veľkoobchod, partner si vyberá z celej ponuky.
    frec("lensunsolar-100w-flexible-solar-panel-9bb", 100,
         "Flexibilný solárny panel 100W s článkami PERC 9BB",
         "Flexibilní solární panel 100W s články PERC 9BB"),
    rec("lensunsolar-100w-flexible-solar-panel-with-back-junction-box",
        "flexible", None, 100,
        "Flexibilný solárny panel 100W so zadnou pripojovacou skrinkou",
        "Flexibilní solární panel 100W se zadní připojovací skříňkou",
        "Flexibilný panel 100 W s pripojovacou skrinkou na zadnej strane — "
        "kábel vychádza pod panel, nie po jeho boku. Hodí sa tam, kde sa "
        "prevŕta strecha a vedenie má zmiznúť rovno pod ňou.",
        "Flexibilní panel 100 W s připojovací skříňkou na zadní straně — "
        "kabel vychází pod panel, ne po jeho boku. Hodí se tam, kde se "
        "provrtá střecha a vedení má zmizet rovnou pod ní."),
    rec("30w-12v-flexible-solar-panel-cable-on-the-back-side",
        "flexible", None, 30,
        "Flexibilný solárny panel 30W s káblom na zadnej strane",
        "Flexibilní solární panel 30W s kabelem na zadní straně",
        "Flexibilný panel 30 W s káblom vyvedeným zozadu. Okraj zostane "
        "čistý, takže panel sadne aj tam, kde nie je kam viesť kábel po "
        "povrchu.",
        "Flexibilní panel 30 W s kabelem vyvedeným zezadu. Okraj zůstane "
        "čistý, takže panel sedne i tam, kde není kudy vést kabel po "
        "povrchu.",
        spec={"w": "30 W", "eff": "23,5 %"}),
    rec("lensunsolar-55w-flexible-solar-panel-with-backside-cable",
        "flexible", None, 55,
        "Flexibilný solárny panel 55W s káblom na zadnej strane",
        "Flexibilní solární panel 55W s kabelem na zadní straně",
        "Flexibilný panel 55 W s káblom vyvedeným zozadu, rozmer 1000 × 350 mm. "
        "Úzky tvar sadne na strechu karavanu medzi strešné okno a okraj.",
        "Flexibilní panel 55 W s kabelem vyvedeným zezadu, rozměr 1000 × 350 mm. "
        "Úzký tvar sedne na střechu karavanu mezi střešní okno a okraj."),
    rec("lensunsolar-300w-solar-panel-blanket-with-controller",
        "blanket", None, 300,
        "Solárna deka 300W v kompletnej sade s MPPT regulátorom",
        "Solární deka 300W v kompletní sadě s MPPT regulátorem",
        "Solárna deka 300 W dodaná ako hotová zostava — s vodotesným 20A MPPT "
        "regulátorom, poistkami, svorkami na batériu a päťmetrovým káblom. "
        "Netreba doobjednávať nič, po rozbalení sa rovno pripojí.",
        "Solární deka 300 W dodaná jako hotová sestava — s vodotěsným 20A MPPT "
        "regulátorem, pojistkami, svorkami na baterii a pětimetrovým kabelem. "
        "Netřeba doobjednávat nic, po rozbalení se rovnou připojí."),
    rec("lensunsolar-400w-flexible-solar-panel", "flexible", None, 400,
        "Flexibilný solárny panel 400W, ohybný do 250°",
        "Flexibilní solární panel 400W, ohebný do 250°",
        "Najväčší flexibilný panel v ponuke — 1825 × 1142 mm a 400 W pri "
        "hmotnosti 7 kg. Ohne sa až do 250°, takže sadne aj na výrazne "
        "klenutú strechu. Lensun ho vedie ako veľkoobchodnú položku, "
        "dostupnosť preto overujeme pri objednávke.",
        "Největší flexibilní panel v nabídce — 1825 × 1142 mm a 400 W při "
        "hmotnosti 7 kg. Ohne se až do 250°, takže sedne i na výrazně "
        "klenutou střechu. Lensun jej vede jako velkoobchodní položku, "
        "dostupnost proto ověřujeme při objednávce."),

    # nadstavby prívesov a kryty korby
    brec("turtleback-expedition-trailers-lensun-66w-flexible-solar-panel",
         "rv", 66,
         "TurtleBack Expedition – 66W solárny panel na úložný box prívesu",
         "TurtleBack Expedition – 66W solární panel na úložný box přívěsu",
         "úložný box expedičného prívesu TurtleBack",
         "úložný box expedičního přívěsu TurtleBack"),
    brec("load-trail-14k-dump-trailer-tapered-storage-box-lensun-80w-12v-flexible-solar-panel",
         "rv", 80,
         "Load Trail 14k – 80W solárny panel na úložný box prívesu",
         "Load Trail 14k – 80W solární panel na úložný box přívěsu",
         "zošikmený úložný box sklápacieho prívesu Load Trail 14k",
         "zešikmený úložný box sklápěcího přívěsu Load Trail 14k"),
    brec("load-trail-14k-dump-trailer-tapered-small-storage-box-lensun-30w-flexible-solar-panel",
         "rv", 30,
         "Load Trail 14k – 30W solárny panel na malý úložný box prívesu",
         "Load Trail 14k – 30W solární panel na malý úložný box přívěsu",
         "malý zošikmený úložný box sklápacieho prívesu Load Trail 14k",
         "malý zešikmený úložný box sklápěcího přívěsu Load Trail 14k"),
    brec("gmc-sierra-1500-bakflip-mx4-tonneau-cover-lensun-80w-solar-panel",
         "tonneau", 240,
         "GMC Sierra 1500 – solárne panely na kryt korby BAKFlip MX4",
         "GMC Sierra 1500 – solární panely na kryt korby BAKFlip MX4",
         "pevný kryt korby BAKFlip MX4 ako zostava dvoch alebo troch "
         "osemdesiatwattových panelov",
         "pevný kryt korby BAKFlip MX4 jako sestava dvou nebo tří "
         "osmdesátiwattových panelů"),

    # strešné stany a karavany mimo Európy, doplnené pre úplnosť ponuky
    srec("intrepid-camp-gear-geo-2-5-rooftop-tent-lensun-200w-flexible-solar-panel", 200,
         "Solárny panel 200W na strešný stan Intrepid Camp Gear Geo 2.5",
         "Solární panel 200W na střešní stan Intrepid Camp Gear Geo 2.5",
         "strešný stan Intrepid Camp Gear Geo 2.5",
         "střešní stan Intrepid Camp Gear Geo 2.5"),
    rec("lensunsolar-55w-flexible-solar-panel-for-kimberley-kampers",
        "flexible", None, 55,
        "Flexibilný solárny panel 55W pre karavany Kimberley Kampers",
        "Flexibilní solární panel 55W pro karavany Kimberley Kampers",
        "Flexibilný panel 55 W s káblom vyvedeným zozadu, pripravený na "
        "karavany Kimberley Kampers. Je to ten istý panel ako univerzálna "
        "55W verzia, len s inou etiketou.",
        "Flexibilní panel 55 W s kabelem vyvedeným zezadu, připravený na "
        "karavany Kimberley Kampers. Je to tentýž panel jako univerzální "
        "55W verze, jen s jinou etiketou."),
]

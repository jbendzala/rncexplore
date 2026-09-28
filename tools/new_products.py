# -*- coding: utf-8 -*-
"""Čo pridať do katalógu z aktuálnej ponuky Lensunu.

Z Lensunu sa dá stiahnuť cena, prevedenia, fotografie aj technické údaje,
ale nie slovenský a český text — ten je tu. Zvyšok doplní add_products.py.

Výber sleduje pravidlo, podľa ktorého katalóg vznikol: vozidlá predávané
v Európe a univerzálna výbava. Americké a japonské modely (Tacoma, Tundra,
4Runner, Sequoia, Venza, Voxy, Atlas, Taos) v ňom nie sú a nepribúdajú —
zákazník na Slovensku ani v Česku také auto nekúpi.
"""


def hood(model_sk, model_cs, w):
    """Popis panela na kapotu. Vo všetkých je tá istá veta, mení sa vozidlo."""
    return (
        f"Solárny panel s výkonom {w} W tvarovaný presne na kapotu vozidla "
        f"{model_sk}. Dobíja štartovaciu aj trakčnú batériu počas státia, takže "
        "chladnička, kamera či osvetlenie fungujú bez naštartovania motora. "
        "Lepí sa priamo na plech, bez vŕtania.",
        f"Solární panel o výkonu {w} W tvarovaný přesně na kapotu vozu "
        f"{model_cs}. Dobíjí startovací i trakční baterii při stání, takže "
        "lednice, kamera či osvětlení fungují bez nastartování motoru. "
        "Lepí se přímo na plech, bez vrtání.",
    )


def rec(h, cat, b, w, sk, cs, dsk, dcs):
    return {"h": h, "cat": cat, "b": b, "w": w,
            "sk": sk, "cs": cs, "dsk": dsk, "dcs": dcs}


def hrec(h, b, w, sk, cs, model_sk, model_cs):
    dsk, dcs = hood(model_sk, model_cs, w)
    return rec(h, "hood", b, w, sk, cs, dsk, dcs)


# ---------------------------------------------------------------- náhrady
# Lensun tieto tri prepublikoval so silnejším panelom pod novým odkazom.
# Staré z ponuky zmizli, takže ich v katalógu nahradíme nástupcami.
NAHRADY = [
    ("toyota-hilux-lensun-solar-100w-bonnet-flexible-solar-panel",
     hrec("toyota-hilux-lensun-solar-110w-bonnet-flexible-solar-panel",
          "Toyota", 110,
          "Toyota Hilux (2005–2008) – 110W flexibilný solárny panel na kapotu",
          "Toyota Hilux (2005–2008) – 110W flexibilní solární panel na kapotu",
          "Toyota Hilux (2005–2008)", "Toyota Hilux (2005–2008)")),

    ("toyota-land-cruiser-80series-j80-lensun-90w-hood-bonnet-solar-panel",
     hrec("toyota-land-cruiser-80series-j80-lensun-110w-hood-bonnet-solar-panel",
          "Toyota", 110,
          "Toyota Land Cruiser 80 Series J80 – 110W solárny panel na kapotu",
          "Toyota Land Cruiser 80 Series J80 – 110W solární panel na kapotu",
          "Toyota Land Cruiser 80 Series J80", "Toyota Land Cruiser 80 Series J80")),

    ("vw-amarok-2nd-gen-lensun-100w-bonnet-solar-panel",
     hrec("vw-amarok-lensun-110w-hood-bonnet-solar-panel",
          "Volkswagen", 110,
          "Volkswagen Amarok 2. generácia (2022–súčasnosť) – 110W solárny panel na kapotu",
          "Volkswagen Amarok 2. generace (2022–současnost) – 110W solární panel na kapotu",
          "Volkswagen Amarok 2. generácia (2022–súčasnosť)",
          "Volkswagen Amarok 2. generace (2022–současnost)")),
]

# ---------------------------------------------------------------- novinky
NOVE = [
    # --- Volkswagen: doteraz sme mali len Amarok, pritom T-rady a Caddy
    #     sú na našom trhu medzi obytnými prestavbami najbežnejšie ---
    hrec("vw-t5-t6-van-lensun-80w-hood-flexible-solar-panel", "Volkswagen", 80,
         "Volkswagen T5 a T6 Transporter – 80W solárny panel na kapotu",
         "Volkswagen T5 a T6 Transporter – 80W solární panel na kapotu",
         "Volkswagen T5 a T6 Transporter", "Volkswagen T5 a T6 Transporter"),

    hrec("vw-caddy-lensun-100w-bonnet-flexible-solar-panel", "Volkswagen", 100,
         "Volkswagen Caddy 4. generácia (2020–súčasnosť) – 100W flexibilný solárny panel na kapotu",
         "Volkswagen Caddy 4. generace (2020–současnost) – 100W flexibilní solární panel na kapotu",
         "Volkswagen Caddy 4. generácia (2020–súčasnosť)",
         "Volkswagen Caddy 4. generace (2020–současnost)"),

    hrec("vw-caddy-3rd-gen-lensun-60w-bonnet-solar-panel", "Volkswagen", 60,
         "Volkswagen Caddy 3. generácia (2003–2021) – 60W flexibilný solárny panel na kapotu",
         "Volkswagen Caddy 3. generace (2003–2021) – 60W flexibilní solární panel na kapotu",
         "Volkswagen Caddy 3. generácia (2003–2021)",
         "Volkswagen Caddy 3. generace (2003–2021)"),

    hrec("vw-crafter-lensun-70w-12v-bonnet-solar-panel", "Volkswagen", 70,
         "Volkswagen Crafter 1. generácia (2006–2017) – 70W flexibilný solárny panel na kapotu",
         "Volkswagen Crafter 1. generace (2006–2017) – 70W flexibilní solární panel na kapotu",
         "Volkswagen Crafter 1. generácia (2006–2017)",
         "Volkswagen Crafter 1. generace (2006–2017)"),

    hrec("vw-tiguan-lensun-100w-bonnet-flexible-solar-panel", "Volkswagen", 100,
         "Volkswagen Tiguan (2007–súčasnosť) – 100W solárny panel na kapotu",
         "Volkswagen Tiguan (2007–současnost) – 100W solární panel na kapotu",
         "Volkswagen Tiguan (2007–súčasnosť)", "Volkswagen Tiguan (2007–současnost)"),

    rec("lensun-85w-12v-flexible-solar-panel-for-vw-t4-camper-roof",
        "flexible", "Volkswagen", 85,
        "Volkswagen T4 – 85W flexibilný solárny panel na strechu",
        "Volkswagen T4 – 85W flexibilní solární panel na střechu",
        "Flexibilný panel 85 W na strechu obytnej prestavby Volkswagen T4. Má "
        "tri milimetre, takže nezvyšuje výšku vozidla ani ťažisko, a lepí sa "
        "priamo na plech bez hliníkového rámu a bez vŕtania.",
        "Flexibilní panel 85 W na střechu obytné přestavby Volkswagen T4. Má "
        "tři milimetry, takže nezvyšuje výšku vozu ani těžiště, a lepí se "
        "přímo na plech bez hliníkového rámu a bez vrtání."),

    rec("volkswagen-vw-t6-camper-van-front-over-cab-lensun-135w-solar-panel",
        "flexible", "Volkswagen", 135,
        "Volkswagen T6 obytný – 135W solárny panel nad kabínu",
        "Volkswagen T6 obytný – 135W solární panel nad kabinu",
        "Panel 135 W tvarovaný na prednú časť strechy nad kabínou obytného "
        "Volkswagenu T6. Využije plochu, ktorá inak zostáva prázdna, a "
        "nezaberie miesto strešnému oknu ani nosiču.",
        "Panel 135 W tvarovaný na přední část střechy nad kabinou obytného "
        "Volkswagenu T6. Využije plochu, která jinak zůstává prázdná, a "
        "nezabere místo střešnímu oknu ani nosiči."),

    rec("vw-grand-california-600-front-over-cab-lensun-130w-solar-panel",
        "flexible", "Volkswagen", 130,
        "Volkswagen Grand California 600 – 130W solárny panel nad kabínu",
        "Volkswagen Grand California 600 – 130W solární panel nad kabinu",
        "Panel 130 W na mieru prednej časti strechy nad kabínou vozidla "
        "Volkswagen Grand California 600. Dobíja trakčnú batériu počas státia, "
        "takže chladnička a kúrenie vydržia bez pripojenia do siete.",
        "Panel 130 W na míru přední části střechy nad kabinou vozu "
        "Volkswagen Grand California 600. Dobíjí trakční baterii při stání, "
        "takže lednice a topení vydrží bez připojení do sítě."),

    # --- Toyota: modely, ktoré sa u nás predávajú ---
    hrec("toyota-landcruiser-prado-250-lensun-115w-bonnet-flexible-solar-panel",
         "Toyota", 115,
         "Toyota Land Cruiser Prado 250 (2024–súčasnosť) – 115W flexibilný solárny panel na kapotu",
         "Toyota Land Cruiser Prado 250 (2024–současnost) – 115W flexibilní solární panel na kapotu",
         "Toyota Land Cruiser Prado 250 (2024–súčasnosť)",
         "Toyota Land Cruiser Prado 250 (2024–současnost)"),

    hrec("toyota-rav4-5th-gen-lensun-85w-hood-flexible-solar-panel", "Toyota", 85,
         "Toyota RAV4 5. generácia (2019–súčasnosť) – 85W flexibilný solárny panel na kapotu",
         "Toyota RAV4 5. generace (2019–současnost) – 85W flexibilní solární panel na kapotu",
         "Toyota RAV4 5. generácia (2019–súčasnosť)",
         "Toyota RAV4 5. generace (2019–současnost)"),

    hrec("toyota-rav4-lensun-50w-hood-flexible-solar-panel", "Toyota", 50,
         "Toyota RAV4 4. generácia (2016–2019) – 50W flexibilný solárny panel na kapotu",
         "Toyota RAV4 4. generace (2016–2019) – 50W flexibilní solární panel na kapotu",
         "Toyota RAV4 4. generácia (2016–2019)", "Toyota RAV4 4. generace (2016–2019)"),

    hrec("toyota-land-crusier-bj45-lensun-70w-bonnet-solar-panel", "Toyota", 70,
         "Toyota Land Cruiser BJ45 – 70W solárny panel na kapotu",
         "Toyota Land Cruiser BJ45 – 70W solární panel na kapotu",
         "Toyota Land Cruiser BJ45", "Toyota Land Cruiser BJ45"),

    # --- univerzálne, bez väzby na konkrétne auto ---
    rec("lensun-200w-flexible-solar-panel-n-type-cell", "flexible", None, 200,
        "Flexibilný solárny panel 200W – články N-type",
        "Flexibilní solární panel 200W – články N-type",
        "Flexibilný panel 200 W s článkami N-type a účinnosťou 25 %, čo je z "
        "rovnakej plochy viac prúdu než pri bežných článkoch. Deväťvrstvová "
        "laminácia s fóliou z leteckých okien znesie vibrácie aj krupobitie.",
        "Flexibilní panel 200 W s články N-type a účinností 25 %, což je ze "
        "stejné plochy více proudu než u běžných článků. Devítivrstvá "
        "laminace s fólií z leteckých oken snese vibrace i krupobití."),

    rec("lensunsolar-200w-12v-solar-panel-blanket", "blanket", None, 200,
        "Solárna deka 200W pre 12V batériu",
        "Solární deka 200W pro 12V baterii",
        "Solárna deka 200 W pre 12V batériu alebo elektrocentrálu. Zloží sa na "
        "deviatinu veľkosti a váži 5,2 kg, takže sa vezme aj tam, kde na pevný "
        "panel nie je miesto. Vodotesná tkanina znesie prach aj dážď.",
        "Solární deka 200 W pro 12V baterii nebo elektrocentrálu. Složí se na "
        "devítinu velikosti a váží 5,2 kg, takže se vezme i tam, kde na pevný "
        "panel není místo. Vodotěsná tkanina snese prach i déšť."),

    rec("lensunsolar-200w-36v-solar-blanket-for-24v-battery-power-station",
        "blanket", None, 200,
        "Solárna deka 200W pre 24V batériu (36 V)",
        "Solární deka 200W pro 24V baterii (36 V)",
        "Solárna deka 200 W s pracovným napätím 36 V pre 24V batérie a "
        "elektrocentrály, ktoré vyžadujú vyššie napätie na vstupe. Zloží sa do "
        "rozmeru 38 × 38 cm a váži 5,2 kg.",
        "Solární deka 200 W s pracovním napětím 36 V pro 24V baterie a "
        "elektrocentrály, které vyžadují vyšší napětí na vstupu. Složí se do "
        "rozměru 38 × 38 cm a váží 5,2 kg."),

    # --- na strešné stany ---
    rec("lensun-80w-flexible-solar-panel-ikamper-skycamp-mini", "rooftent", None, 80,
        "Solárny panel 80W na strešný stan iKamper Skycamp Mini",
        "Solární panel 80W na střešní stan iKamper Skycamp Mini",
        "Panel 80 W tvarovaný na škrupinu strešného stanu iKamper Skycamp Mini "
        "2.0 a 3.0. Dobíja batériu tábora bez toho, aby ste prišli o miesto na "
        "streche. V balení je predlžovací kábel 5 m.",
        "Panel 80 W tvarovaný na skořepinu střešního stanu iKamper Skycamp Mini "
        "2.0 a 3.0. Dobíjí baterii tábora, aniž byste přišli o místo na "
        "střeše. V balení je prodlužovací kabel 5 m."),

    rec("ikamper-skycamp-mini-roof-tent-240w-flexible-solar-panel", "rooftent", None, 240,
        "Solárny panel 240W na strešný stan iKamper Skycamp Mini",
        "Solární panel 240W na střešní stan iKamper Skycamp Mini",
        "Zostava troch panelov s celkovým výkonom 240 W na strešný stan "
        "iKamper Skycamp Mini 2.0 a 3.0. Pokryje celú škrupinu, takže nabíja aj "
        "vtedy, keď časť plochy zatieni strom.",
        "Sestava tří panelů s celkovým výkonem 240 W na střešní stan "
        "iKamper Skycamp Mini 2.0 a 3.0. Pokryje celou skořepinu, takže nabíjí "
        "i tehdy, když část plochy zastíní strom."),

    rec("alu-cab-modcap-camper-roof-tent-lensun-400w-flexible-solar-panel",
        "rooftent", None, 400,
        "Solárny panel 400W na nadstavbu Alu-Cab ModCAP",
        "Solární panel 400W na nástavbu Alu-Cab ModCAP",
        "Dvojica panelov s celkovým výkonom 400 W na strechu obytnej nadstavby "
        "Alu-Cab ModCAP. Články N-type s účinnosťou 25 % a deväťvrstvová "
        "laminácia, ktorá znesie terén aj počasie.",
        "Dvojice panelů s celkovým výkonem 400 W na střechu obytné nástavby "
        "Alu-Cab ModCAP. Články N-type s účinností 25 % a devítivrstvá "
        "laminace, která snese terén i počasí."),
]

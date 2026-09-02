# -*- coding: utf-8 -*-
"""Obsah jednotlivých stránok v slovenčine a češtine."""

import blog_content as _blog

# naplní build.py pred vykreslením stránok
N_PRODUCTS = 0
N_BRANDS = 0

def T(sk, cs, lang):
    return sk if lang == "sk" else cs

def todo(t):
    return f'<span class="todo">{t}</span>'

def stars(n=5):
    s = ('<svg viewBox="0 0 24 24"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8'
         'l-6.2 3.2L7 14.2l-5-4.9 6.9-1z"/></svg>')
    return '<div class="stars" aria-label="%d/5">%s</div>' % (n, s * n)


# --------------------------------------------------------------- hodnotenia
# Skutočné hodnotenia zákazníkov výrobcu Lensun, preložené a skrátené.
# Zdroj: lensunsolar.com. Meno a vozidlo sú zachované tak, ako ich uviedli.
REVIEWS = [
 dict(who="Steve Mills", ini="SM", car="Dacia Duster 3 (2023–), 40 W",
   pid="dacia-duster-lensun-40w-hood-bonnet-solar-panel",
   img="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Dacia-Duster-_Lensun-40W-Hood-Bonnet-Solar-Panel.jpg",
   sk="Duster mi neustále hlásil vybitú batériu. Nepomohla ani väčšia AGM batéria. "
      "Lensun mi vyrobil panel presne na rozmer kapoty a odvtedy sa hláška neobjavila. "
      "Montáž bola jednoduchšia, než som čakal.",
   cs="Duster mi neustále hlásil vybitou baterii. Nepomohla ani větší AGM baterie. "
      "Lensun mi vyrobil panel přesně na rozměr kapoty a od té doby se hláška neobjevila. "
      "Montáž byla jednodušší, než jsem čekal."),
 dict(who="Tim Korade", ini="TK", car="Toyota Land Cruiser 100, 100 W",
   pid="toyota-land-cruiser-100-series-lensun-100w-hood-flexible-solar-panel",
   img="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Toyota_LandCruiser_100_Series_J100_Lensun_100W_Hood_Flexible_Solar_Panel-1.jpg",
   sk="Namontované na Land Cruiseri z roku 2004 s druhou batériou a DC-DC regulátorom. "
      "Vozidlo používame na pátracie a záchranné akcie — výkon pokryje našu techniku bez toho, "
      "aby motor musel bežať na voľnobeh. Zvládlo aj 40 °C a krupobitie.",
   cs="Namontované na Land Cruiseru z roku 2004 s druhou baterií a DC-DC regulátorem. "
      "Vozidlo používáme na pátrací a záchranné akce — výkon pokryje naši techniku, aniž by "
      "motor musel běžet na volnoběh. Zvládlo i 40 °C a krupobití."),
 dict(who="El Gars du coin", ini="EG", car="Jeep, 400 W (2× 200 W)",
   pid="lensun-400w-200w-flexible-solar-panel",
   img="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/2pcs-lensun-200w-flexible-solar-panel-1.jpg",
   sk="Sadu 400 W som zapojil do systému s MPPT regulátorom Victron a batériou 200 Ah LiFePO4. "
      "Napája Starlink, 12 V chladničku aj vodné čerpadlo. Nízky profil flexibilných panelov "
      "bol pre moju zostavu ideálny.",
   cs="Sadu 400 W jsem zapojil do systému s MPPT regulátorem Victron a baterií 200 Ah LiFePO4. "
      "Napájí Starlink, 12V lednici i vodní čerpadlo. Nízký profil flexibilních panelů "
      "byl pro moji sestavu ideální."),
]


def reviews_html(lang):
    cards = []
    for r in REVIEWS:
        href = ("produkty.html?q=" + r["pid"]) if r.get("pid") else ""
        photo = (f'<a class="review-photo" href="{href}">'
                 f'<img loading="lazy" decoding="async" src="{r["img"]}?width=700" '
                 f'alt="{r["car"]}"></a>') if r.get("img") else ""
        cards.append(
            f'<figure class="review">{photo}'
            f'<div class="review-body">'
            f'<div class="review-head">'
            f'<span class="avatar" aria-hidden="true">{r["ini"]}</span>'
            f'<span class="review-who"><b>{r["who"]}</b><span>{r["car"]}</span></span>'
            f'</div>{stars(5)}'
            f'<blockquote>{r["sk"] if lang=="sk" else r["cs"]}</blockquote>'
            f'</div></figure>')
    return "".join(cards)


# ---------------------------------------------------------------- domov
def home(lang, base):
    sk = lang == "sk"
    cats_t   = T("Kategórie", "Kategorie", lang)
    cats_h   = T("Vyberte, čo hľadáte", "Vyberte, co hledáte", lang)
    why_t    = T("Prečo solárny panel na vozidle", "Proč solární panel na vozidle", lang)
    feat_t   = T("Odporúčame", "Doporučujeme", lang)
    feat_h   = T("Najvýhodnejšie kúsky z katalógu", "Nejvýhodnější kousky z katalogu", lang)
    rev_t    = T("Čo hovoria používatelia", "Co říkají uživatelé", lang)
    all_btn  = T("Zobraziť celý katalóg", "Zobrazit celý katalog", lang)
    brands_t = T("Značky vozidiel", "Značky vozidel", lang)
    brands_h = T("Vyberte značku svojho auta", "Vyberte značku svého auta", lang)

    why = [
        (T("Energia bez motora", "Energie bez motoru", lang),
         T("Panel dobíja batériu počas státia aj jazdy. Chladnička, kamera, kúrenie "
           "či telefóny fungujú bez naštartovania a bez rizika vybitej batérie.",
           "Panel dobíjí baterii při stání i za jízdy. Lednice, kamera, topení "
           "či telefony fungují bez nastartování a bez rizika vybité baterie.", lang)),
        (T("Tvarované na konkrétne auto", "Tvarované na konkrétní auto", lang),
         T("Panely na kapotu sú vyrobené podľa tvaru konkrétneho modelu a generácie. "
           "Nelepíte univerzálny obdĺžnik — sadne to na plech.",
           "Panely na kapotu jsou vyrobené podle tvaru konkrétního modelu a generace. "
           "Nelepíte univerzální obdélník — sedne to na plech.", lang)),
        (T("Montáž bez vŕtania", "Montáž bez vrtání", lang),
         T("Flexibilné panely majú pár milimetrov a lepia sa priamo na povrch. "
           "Žiadne diery do karosérie, žiadny rám, minimálny odpor vzduchu.",
           "Flexibilní panely mají pár milimetrů a lepí se přímo na povrch. "
           "Žádné díry do karoserie, žádný rám, minimální odpor vzduchu.", lang)),
        (T("Odolné do terénu", "Odolné do terénu", lang),
         T("Konštrukcia počíta s vetrom, dažďom, prachom aj vibráciami. "
           "Panely sú určené na trvalé vonkajšie použitie.",
           "Konstrukce počítá s větrem, deštěm, prachem i vibracemi. "
           "Panely jsou určené pro trvalé venkovní použití.", lang)),
    ]
    why_html = "".join(
        f'<div class="box"><h3>{t}</h3><p>{d}</p></div>' for t, d in why)

    rev_lead = T(
        "Skúsenosti majiteľov vozidiel, ktorí panely Lensun používajú v praxi.",
        "Zkušenosti majitelů vozidel, kteří panely Lensun používají v praxi.", lang)
    rev_src = T(
        "Hodnotenia zákazníkov výrobcu Lensun, preložené zo stránky lensunsolar.com. "
        "Mená a vozidlá uvádzame tak, ako ich uviedli autori.",
        "Hodnocení zákazníků výrobce Lensun, přeložená ze stránky lensunsolar.com. "
        "Jména a vozidla uvádíme tak, jak je uvedli autoři.", lang)

    return f"""
<section class="hero hero-img"><div class="wrap">
  <p class="eyebrow">{T("Katalóg produktov","Katalog produktů",lang)}</p>
  <h1>{T("Solárna energia<br>pre <em>vozidlá</em> a karavany","Solární energie<br>pro <em>vozidla</em> a karavany",lang)}</h1>
  <p>{T("Prezrite si celý sortiment. Vyberte produkt, vyplňte kontaktné údaje a my sa vám ozveme s cenovou ponukou a termínom dodania.","Prohlédněte si celý sortiment. Vyberte produkt, vyplňte kontaktní údaje a my se vám ozveme s cenovou nabídkou a termínem dodání.",lang)}</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>{cats_t}</h2><span class="eyebrow">{cats_h}</span></div>
  <div class="mosaic" id="mosaic" data-href="{base}produkty.html"></div>
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>{why_t}</h2>
  <div class="cols">{why_html}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><h2>{feat_t}</h2><span class="eyebrow">{feat_h}</span></div>
  <div class="feat" id="featured" data-count="4"></div>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head"><h2>{brands_t}</h2><span class="eyebrow">{brands_h}</span></div>
  <div class="brand-grid" id="brandGrid" data-href="{base}produkty.html"></div>
  <p style="margin-top:26px"><a class="btn" href="{base}produkty.html">{all_btn}</a></p>
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>{rev_t}</h2>
  <p class="lead">{rev_lead}</p>
  <div class="reviews">{reviews_html(lang)}</div>
  <p class="note" style="margin-top:20px">{rev_src}</p>
</div></section>
{_blog.blog_teaser(lang, base)}
"""


# ---------------------------------------------------------------- produkty
def produkty(lang, base):
    return f"""
<section class="filters" id="catalog"><div class="wrap">
  <div class="f-row">
    <div class="search">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <input id="q" type="search" autocomplete="off" aria-label="{T('Hľadať','Hledat',lang)}">
    </div>
    <select id="brand" aria-label="{T('Značka vozidla','Značka vozidla',lang)}"></select>
    <select id="sort" aria-label="{T('Zoradiť','Seřadit',lang)}"></select>
  </div>
  <div class="chips" id="chips" role="group"></div>
  <div class="f-meta"><span id="count"></span><button class="link-btn" id="resetBtn"></button></div>
</div></section>

<main class="wrap">
  <div class="grid" id="grid"></div>
  <div class="more" id="more"></div>
</main>
"""


MODALS = """
<div class="ov" id="detailOv" hidden role="dialog" aria-modal="true">
  <div class="modal">
    <button class="m-close" data-close="detailOv" aria-label="%(close)s">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
        <path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <div id="detailBody"></div>
  </div>
</div>

<div class="ov" id="orderOv" hidden role="dialog" aria-modal="true">
  <div class="modal sm">
    <button class="m-close" data-close="orderOv" aria-label="%(close)s">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
        <path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <form class="form" id="orderForm" novalidate>
      <h2 id="orderTitle"></h2>
      <p class="note" id="orderLead"></p>
      <div class="f-prod" id="ofProd"></div>
      <div class="fields">
        <label class="full" id="ofVariantWrap"><span id="lbVariant"></span><select id="ofVariant"></select></label>
        <label><span id="lbQty"></span><input id="ofQty" type="number" min="1" max="99" value="1"></label>
        <label><span></span><input id="ofName" type="text" placeholder=" " autocomplete="name"></label>
        <label><span></span><input id="ofEmail" type="email" placeholder=" " autocomplete="email"></label>
        <label><span></span><input id="ofPhone" type="tel" placeholder=" " autocomplete="tel"></label>
        <label><span></span><input id="ofCompany" type="text" placeholder=" " autocomplete="organization"></label>
        <label class="full"><span></span><input id="ofStreet" type="text" placeholder=" " autocomplete="street-address"></label>
        <label><span></span><input id="ofCity" type="text" placeholder=" " autocomplete="address-level2"></label>
        <label><span></span><input id="ofZip" type="text" placeholder=" " autocomplete="postal-code"></label>
        <label class="full"><span></span><input id="ofCountry" type="text" placeholder=" " autocomplete="country-name"></label>
        <label class="full"><span id="lbNote"></span><textarea id="ofNote"></textarea></label>
      </div>
      <div class="msg" id="ofMsgBox"></div>
      <div class="f-actions">
        <button class="btn" type="submit" id="btnSend"></button>
        <button class="btn ghost" type="button" id="btnCopy"></button>
      </div>
    </form>
  </div>
</div>
"""


# ---------------------------------------------------------------- veľkoobchod
def velkoobchod(lang, base):
    sk = lang == "sk"
    boxes = [
        (T("Veľkoobchodné ceny", "Velkoobchodní ceny", lang),
         T("Ceny odstupňované podľa objemu objednávky. Konkrétnu cenníkovú úroveň "
           "dohodneme podľa predpokladaného ročného odberu.",
           "Ceny odstupňované podle objemu objednávky. Konkrétní cenovou úroveň "
           "domluvíme podle předpokládaného ročního odběru.", lang)),
        (T("Sortiment na sklade aj na objednávku", "Sortiment skladem i na objednávku", lang),
         T("Bežné typy panelov a regulátorov držíme dostupné, tvarované panely na "
           "konkrétne vozidlá vyrábame na objednávku.",
           "Běžné typy panelů a regulátorů držíme dostupné, tvarované panely na "
           "konkrétní vozidla vyrábíme na objednávku.", lang)),
        (T("Podklady pre predaj", "Podklady pro prodej", lang),
         T("Produktové fotografie, technické listy a parametre poskytneme v "
           "elektronickej podobe na použitie vo vašom e-shope.",
           "Produktové fotografie, technické listy a parametry poskytneme "
           "elektronicky k použití ve vašem e-shopu.", lang)),
        (T("Technická podpora", "Technická podpora", lang),
         T("Poradíme s výberom panela k vozidlu, dimenzovaním regulátora aj "
           "riešením montáže u vášho zákazníka.",
           "Poradíme s výběrem panelu k vozidlu, dimenzováním regulátoru i "
           "řešením montáže u vašeho zákazníka.", lang)),
    ]
    bx = "".join(f'<div class="box"><h3>{t}</h3><p>{d}</p></div>' for t, d in boxes)

    steps = [
        (T("Ozvite sa nám", "Ozvěte se nám", lang),
         T("Napíšte nám na e-mail, o aký sortiment máte záujem a aký objem "
           "predpokladáte. Uveďte aj IČO a fakturačné údaje.",
           "Napište nám e-mail, o jaký sortiment máte zájem a jaký objem "
           "předpokládáte. Uveďte také IČO a fakturační údaje.", lang)),
        (T("Dostanete cenník", "Dostanete ceník", lang),
         T("Pošleme vám veľkoobchodný cenník s podmienkami pre vašu úroveň odberu.",
           "Pošleme vám velkoobchodní ceník s podmínkami pro vaši úroveň odběru.", lang)),
        (T("Prvá objednávka", "První objednávka", lang),
         T("Objednávku potvrdíme, doplníme termín dodania a vystavíme zálohovú faktúru.",
           "Objednávku potvrdíme, doplníme termín dodání a vystavíme zálohovou fakturu.", lang)),
        (T("Priebežná spolupráca", "Průběžná spolupráce", lang),
         T("Ďalšie objednávky už riešime priamo, vrátane rezervácie tovaru "
           "a plánovania dodávok.",
           "Další objednávky už řešíme přímo, včetně rezervace zboží "
           "a plánování dodávek.", lang)),
    ]
    st = "".join(f'<div class="step"><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d in steps)

    return f"""
<section class="sec"><div class="wrap">
  <div class="prose">
    <p class="lead">{T("Predávate outdoorové vybavenie, staviate obytné vozidlá alebo prevádzkujete autoservis? Sortiment solárnych panelov dodávame aj veľkoobchodne.","Prodáváte outdoorové vybavení, stavíte obytná vozidla nebo provozujete autoservis? Sortiment solárních panelů dodáváme i velkoobchodně.",lang)}</p>
  </div>
  <div class="cols">{bx}</div>
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>{T("Ako začať spoluprácu","Jak začít spolupráci",lang)}</h2>
  <div class="steps">{st}</div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>{T("Orientačné úrovne odberu","Orientační úrovně odběru",lang)}</h2>
  <p class="lead">{T("Presné ceny a hranice si dohodneme individuálne — nasledujúca tabuľka je len rámcová.","Přesné ceny a hranice si domluvíme individuálně — následující tabulka je jen rámcová.",lang)}</p>
  <div class="table-wrap"><table class="data">
    <thead><tr>
      <th>{T("Úroveň","Úroveň",lang)}</th>
      <th>{T("Ročný odber","Roční odběr",lang)}</th>
      <th>{T("Podmienky","Podmínky",lang)}</th>
    </tr></thead>
    <tbody>
      <tr><td><strong>{T("Začínajúci partner","Začínající partner",lang)}</strong></td><td>{todo(T("doplňte","doplňte",lang))}</td><td>{T("Veľkoobchodný cenník, podpora pri výbere","Velkoobchodní ceník, podpora při výběru",lang)}</td></tr>
      <tr><td><strong>{T("Stály partner","Stálý partner",lang)}</strong></td><td>{todo(T("doplňte","doplňte",lang))}</td><td>{T("Lepšie ceny, rezervácia tovaru","Lepší ceny, rezervace zboží",lang)}</td></tr>
      <tr><td><strong>{T("Kľúčový partner","Klíčový partner",lang)}</strong></td><td>{todo(T("doplňte","doplňte",lang))}</td><td>{T("Individuálne ceny, plánované dodávky","Individuální ceny, plánované dodávky",lang)}</td></tr>
    </tbody>
  </table></div>
</div></section>

<section class="cta"><div class="wrap cta-in">
  <div>
    <h2>{T("Máte záujem o veľkoobchod?","Máte zájem o velkoobchod?",lang)}</h2>
    <p>{T("Napíšte nám a pošleme vám cenník aj podmienky.","Napište nám a pošleme vám ceník i podmínky.",lang)}</p>
  </div>
  <a class="btn signal lg js-mail" href="#"></a>
</div></section>
"""


# ---------------------------------------------------------------- na mieru
def na_mieru(lang, base):
    steps = [
        (T("Napíšte nám o vozidle", "Napište nám o vozidle", lang),
         T("Značka, model, rok výroby a generácia. Pomôže fotografia kapoty alebo "
           "strechy spredu aj zboku.",
           "Značka, model, rok výroby a generace. Pomůže fotografie kapoty nebo "
           "střechy zepředu i zboku.", lang)),
        (T("Zameranie plochy", "Zaměření plochy", lang),
         T("Podľa podkladov určíme využiteľnú plochu a maximálny rozumný výkon. "
           "Ak treba, pošleme vám jednoduchý návod na premeranie.",
           "Podle podkladů určíme využitelnou plochu a maximální rozumný výkon. "
           "Pokud je třeba, pošleme vám jednoduchý návod na přeměření.", lang)),
        (T("Ponuka a schválenie", "Nabídka a schválení", lang),
         T("Dostanete návrh rozmerov, výkonu a cenu. Až po vašom odsúhlasení "
           "ide panel do výroby.",
           "Dostanete návrh rozměrů, výkonu a cenu. Až po vašem odsouhlasení "
           "jde panel do výroby.", lang)),
        (T("Výroba a dodanie", "Výroba a dodání", lang),
         T("Panel sa vyrába na mieru, preto počítajte s dlhším termínom ako "
           "pri skladových kusoch.",
           "Panel se vyrábí na míru, proto počítejte s delším termínem než "
           "u skladových kusů.", lang)),
    ]
    st = "".join(f'<div class="step"><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d in steps)
    return f"""
<section class="sec"><div class="wrap">
  <div class="prose">
    <p class="lead">{T("Vaše vozidlo nie je v katalógu? Väčšinu tvarovaných panelov vieme vyrobiť na mieru — podľa rozmerov konkrétnej kapoty, strechy, krytu korby alebo strešného stanu.","Vaše vozidlo není v katalogu? Většinu tvarovaných panelů umíme vyrobit na míru — podle rozměrů konkrétní kapoty, střechy, krytu korby nebo střešního stanu.",lang)}</p>
    <p>{T("Na mieru riešime aj netypické inštalácie: nadstavby úžitkových vozidiel, prívesy, lodné nadstavby alebo zostavy s viacerými panelmi a spoločným regulátorom.","Na míru řešíme i netypické instalace: nástavby užitkových vozidel, přívěsy, lodní nástavby nebo sestavy s více panely a společným regulátorem.",lang)}</p>
  </div>
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>{T("Ako to prebieha","Jak to probíhá",lang)}</h2>
  <div class="steps">{st}</div>
</div></section>

<section class="cta"><div class="wrap cta-in">
  <div>
    <h2>{T("Pošlite nám údaje o vozidle","Pošlete nám údaje o vozidle",lang)}</h2>
    <p>{T("Ozveme sa s návrhom riešenia a cenou.","Ozveme se s návrhem řešení a cenou.",lang)}</p>
  </div>
  <a class="btn signal lg js-mail" href="#"></a>
</div></section>
"""


# ---------------------------------------------------------------- montáž
def montaz(lang, base):
    steps = [
        (T("Očistite a odmastite plochu", "Očistěte a odmastěte plochu", lang),
         T("Povrch musí byť suchý, čistý a bez vosku. Zvyšky leštenky sú "
           "najčastejšou príčinou toho, že lepenie nedrží.",
           "Povrch musí být suchý, čistý a bez vosku. Zbytky leštěnky jsou "
           "nejčastější příčinou toho, že lepení nedrží.", lang)),
        (T("Panel najprv priložte nasucho", "Panel nejprve přiložte nasucho", lang),
         T("Skontrolujte, či tvar sadne a kadiaľ povediete kábel. Polohu si "
           "vyznačte maskovacou páskou.",
           "Zkontrolujte, zda tvar sedne a kudy povedete kabel. Polohu si "
           "vyznačte maskovací páskou.", lang)),
        (T("Lepte za vhodnej teploty", "Lepte za vhodné teploty", lang),
         T("Obojstranná páska VHB potrebuje teplo — lepte v hale alebo cez "
           "teplý deň. V mraze spoj nespoľahlivo vytvrdne.",
           "Oboustranná páska VHB potřebuje teplo — lepte v hale nebo za "
           "teplého dne. V mrazu spoj nespolehlivě vytvrdne.", lang)),
        (T("Priveďte kábel do interiéru", "Přiveďte kabel do interiéru", lang),
         T("Použite existujúcu priechodku alebo vodotesnú káblovú priechodku. "
           "Kábel istite proti odieraniu o hrany.",
           "Použijte existující průchodku nebo vodotěsnou kabelovou průchodku. "
           "Kabel jistěte proti odírání o hrany.", lang)),
        (T("Zapojte regulátor a batériu", "Zapojte regulátor a baterii", lang),
         T("Vždy cez regulátor nabíjania — nikdy nie priamo na batériu. "
           "Najprv pripojte batériu k regulátoru, až potom panel.",
           "Vždy přes regulátor nabíjení — nikdy ne přímo na baterii. "
           "Nejprve připojte baterii k regulátoru, teprve potom panel.", lang)),
    ]
    st = "".join(f'<div class="step"><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d in steps)
    notes = [
        (T("Nechajte spoj vytvrdnúť", "Nechte spoj vytvrdnout", lang),
         T("Lepený spoj dosahuje plnú pevnosť postupne, spravidla za niekoľko "
           "desiatok hodín. Prvý deň vozidlo zbytočne nemyte tlakovou vodou.",
           "Lepený spoj dosahuje plné pevnosti postupně, zpravidla za několik "
           "desítek hodin. První den vozidlo zbytečně nemyjte tlakovou vodou.", lang)),
        (T("Pozor na tieň", "Pozor na stín", lang),
         T("Aj čiastočné zatienenie výrazne zníži výkon celého panela. "
           "Vyhnite sa miestam pod strešným nosičom alebo anténou.",
           "I částečné zastínění výrazně sníží výkon celého panelu. "
           "Vyhněte se místům pod střešním nosičem nebo anténou.", lang)),
        (T("Automyčka a škrabky", "Myčka a škrabky", lang),
         T("Kefová automyčka a škrabka na ľad môžu povrch panela poškodiť. "
           "Umývajte radšej ručne mäkkou hubkou.",
           "Kartáčová myčka a škrabka na led mohou povrch panelu poškodit. "
           "Myjte raději ručně měkkou houbou.", lang)),
    ]
    nb = "".join(f'<div class="box"><h3>{t}</h3><p>{d}</p></div>' for t, d in notes)
    return f"""
<section class="sec"><div class="wrap">
  <div class="prose">
    <p class="lead">{T("Flexibilné panely sa lepia priamo na povrch — bez vŕtania, bez rámu a bez zásahu do karosérie. Montáž zvládne šikovný domáci kutil, pri zložitejších inštaláciách odporúčame odborný servis.","Flexibilní panely se lepí přímo na povrch — bez vrtání, bez rámu a bez zásahu do karoserie. Montáž zvládne šikovný domácí kutil, u složitějších instalací doporučujeme odborný servis.",lang)}</p>
    <p>{T("Nasledujúci postup je všeobecný. Vždy sa riaďte pokynmi priloženými ku konkrétnemu produktu.","Následující postup je obecný. Vždy se řiďte pokyny přiloženými ke konkrétnímu produktu.",lang)}</p>
  </div>
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>{T("Postup montáže","Postup montáže",lang)}</h2>
  <div class="steps">{st}</div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>{T("Na čo si dať pozor","Na co si dát pozor",lang)}</h2>
  <div class="cols">{nb}</div>
</div></section>

<section class="cta"><div class="wrap cta-in">
  <div>
    <h2>{T("Neviete si rady s montážou?","Nevíte si rady s montáží?",lang)}</h2>
    <p>{T("Napíšte nám — poradíme s výberom aj zapojením.","Napište nám — poradíme s výběrem i zapojením.",lang)}</p>
  </div>
  <a class="btn signal lg js-mail" href="#"></a>
</div></section>
"""


# ---------------------------------------------------------------- o nás
def o_nas(lang, base):
    return f"""
<section class="sec"><div class="wrap"><div class="prose">
  <p class="lead">{T("Dodávame solárne panely a príslušenstvo pre vozidlá, karavany a outdoor na slovenskom a českom trhu.","Dodáváme solární panely a příslušenství pro vozidla, karavany a outdoor na slovenském a českém trhu.",lang)}</p>

  <h2>{T("Čím sa zaoberáme","Čím se zabýváme",lang)}</h2>
  <p>{T("Špecializujeme sa na solárne panely tvarované na konkrétne modely vozidiel — na kapotu, strechu, kryt korby aj strešný stan. Okrem panelov dodávame regulátory nabíjania, meniče napätia a montážne príslušenstvo.","Specializujeme se na solární panely tvarované na konkrétní modely vozidel — na kapotu, střechu, kryt korby i střešní stan. Kromě panelů dodáváme regulátory nabíjení, měniče napětí a montážní příslušenství.",lang)}</p>
  <p>{T(f"Katalóg obsahuje {N_PRODUCTS} produktov pre {N_BRANDS} značiek vozidiel. Ak vaše vozidlo v katalógu nenájdete, panel vieme vyrobiť na mieru.",f"Katalog obsahuje {N_PRODUCTS} produktů pro {N_BRANDS} značek vozidel. Pokud své vozidlo v katalogu nenajdete, panel umíme vyrobit na míru.",lang)}</p>

  <h2>{T("Ako nakupujete","Jak nakupujete",lang)}</h2>
  <p>{T("Tento web je katalóg, nie e-shop. Vyberiete si produkt, odošlete nezáväznú objednávku a my sa vám ozveme s cenovou ponukou, dostupnosťou a termínom dodania. Až potom sa rozhodujete.","Tento web je katalog, nikoli e-shop. Vyberete si produkt, odešlete nezávaznou objednávku a my se vám ozveme s cenovou nabídkou, dostupností a termínem dodání. Teprve pak se rozhodujete.",lang)}</p>
  <p>{T("Vďaka tomu vám vieme poradiť s výberom správneho panela k vozidlu a dimenzovaním regulátora ešte pred tým, než niečo zaplatíte.","Díky tomu vám umíme poradit s výběrem správného panelu k vozidlu a dimenzováním regulátoru ještě dříve, než něco zaplatíte.",lang)}</p>

  <h2>{T("Firemné údaje","Firemní údaje",lang)}</h2>
  <p>
    <strong class="js-company"></strong><br>
    {T("Sídlo","Sídlo",lang)}: {todo(T("doplňte adresu","doplňte adresu",lang))}<br>
    {T("IČO","IČO",lang)}: {todo(T("doplňte","doplňte",lang))} &nbsp;
    {T("DIČ","DIČ",lang)}: {todo(T("doplňte","doplňte",lang))}<br>
    {T("Zapísaná v","Zapsána v",lang)}: {todo(T("doplňte register","doplňte rejstřík",lang))}
  </p>
</div></div></section>

<section class="cta"><div class="wrap cta-in">
  <div>
    <h2>{T("Poradíme s výberom","Poradíme s výběrem",lang)}</h2>
    <p>{T("Napíšte nám značku a model vozidla.","Napište nám značku a model vozidla.",lang)}</p>
  </div>
  <a class="btn signal lg" href="{base}produkty.html">{T("Prejsť do katalógu","Přejít do katalogu",lang)}</a>
</div></section>
"""


# ---------------------------------------------------------------- FAQ
def faq(lang, base):
    qa = [
        (T("Ako si vyberiem správny panel na moje auto?",
           "Jak si vyberu správný panel na moje auto?", lang),
         T("<p>V katalógu filtrujte podľa značky vozidla a potom nájdite svoj model "
           "a generáciu — tvarované panely na kapotu sú viazané na konkrétnu generáciu, "
           "pretože kopírujú tvar plechu.</p><p>Ak si nie ste istí generáciou, napíšte nám "
           "značku, model a rok výroby a overíme to za vás.</p>",
           "<p>V katalogu filtrujte podle značky vozidla a poté najděte svůj model "
           "a generaci — tvarované panely na kapotu jsou vázané na konkrétní generaci, "
           "protože kopírují tvar plechu.</p><p>Pokud si generací nejste jistí, napište nám "
           "značku, model a rok výroby a ověříme to za vás.</p>", lang)),
        (T("Potrebujem k panelu regulátor nabíjania?",
           "Potřebuji k panelu regulátor nabíjení?", lang),
         T("<p>Áno. Panel sa nikdy nepripája priamo na batériu — bez regulátora hrozí "
           "prebitie a poškodenie batérie.</p><p>Väčšina panelov v katalógu sa dá objednať "
           "v sade s MPPT regulátorom. Regulátor MPPT vyťaží z panela viac energie než "
           "jednoduchší typ PWM, najmä pri oblačnosti a nižších teplotách.</p>",
           "<p>Ano. Panel se nikdy nepřipojuje přímo na baterii — bez regulátoru hrozí "
           "přebití a poškození baterie.</p><p>Většina panelů v katalogu jde objednat "
           "v sadě s MPPT regulátorem. Regulátor MPPT vytěží z panelu více energie než "
           "jednodušší typ PWM, zejména při oblačnosti a nižších teplotách.</p>", lang)),
        (T("Aký výkon panela potrebujem?", "Jaký výkon panelu potřebuji?", lang),
         T("<p>Závisí od toho, čo napájate. Na udržiavanie štartovacej batérie a nabíjanie "
           "telefónov stačí menší panel. Na chladničku, kúrenie alebo prenosnú elektrocentrálu "
           "počítajte s vyšším výkonom.</p><p>Napíšte nám, aké spotrebiče chcete napájať a ako "
           "dlho, a odporučíme vhodnú zostavu.</p>",
           "<p>Závisí na tom, co napájíte. Na udržování startovací baterie a nabíjení "
           "telefonů stačí menší panel. Na lednici, topení nebo přenosnou elektrocentrálu "
           "počítejte s vyšším výkonem.</p><p>Napište nám, jaké spotřebiče chcete napájet a jak "
           "dlouho, a doporučíme vhodnou sestavu.</p>", lang)),
        (T("Musím pri montáži vŕtať do karosérie?",
           "Musím při montáži vrtat do karoserie?", lang),
         T("<p>Nie. Flexibilné panely sa lepia obojstrannou páskou priamo na povrch. "
           "Vŕtať treba nanajvýš pri privedení kábla do interiéru, a aj to sa dá často "
           "vyriešiť existujúcou priechodkou.</p>",
           "<p>Ne. Flexibilní panely se lepí oboustrannou páskou přímo na povrch. "
           "Vrtat je třeba nanejvýš při zavedení kabelu do interiéru, a i to lze často "
           "vyřešit stávající průchodkou.</p>", lang)),
        (T("Vydrží panel umývanie a zimu?", "Vydrží panel mytí a zimu?", lang),
         T("<p>Panely sú určené na trvalé vonkajšie použitie a znesú dážď, prach aj mráz. "
           "Vyhnite sa však kefovej automyčke a škrabaniu ľadu z povrchu panela — mechanické "
           "poškodenie povrchu je najčastejšia príčina reklamácií.</p>",
           "<p>Panely jsou určené pro trvalé venkovní použití a snesou déšť, prach i mráz. "
           "Vyhněte se však kartáčové myčce a škrabání ledu z povrchu panelu — mechanické "
           "poškození povrchu je nejčastější příčina reklamací.</p>", lang)),
        (T("Ako prebieha objednávka?", "Jak probíhá objednávka?", lang),
         T("<p>Tento web je katalóg, nie e-shop. Pri produkte kliknite na <strong>Objednať</strong>, "
           "vyplňte kontaktné údaje a odošlite. Príde nám e-mail s vybraným produktom a vašimi "
           "údajmi.</p><p>Ozveme sa vám s cenovou ponukou, dostupnosťou a termínom dodania. "
           "Objednávka je nezáväzná — nič neplatíte vopred.</p>",
           "<p>Tento web je katalog, nikoli e-shop. U produktu klikněte na <strong>Objednat</strong>, "
           "vyplňte kontaktní údaje a odešlete. Přijde nám e-mail s vybraným produktem a vašimi "
           "údaji.</p><p>Ozveme se vám s cenovou nabídkou, dostupností a termínem dodání. "
           "Objednávka je nezávazná — nic neplatíte předem.</p>", lang)),
        (T("Sú ceny v katalógu konečné?", "Jsou ceny v katalogu konečné?", lang),
         T("<p>Ceny v katalógu sú orientačné a slúžia na porovnanie produktov. Záväznú cenu "
           "vrátane dopravy dostanete v cenovej ponuke e-mailom.</p>",
           "<p>Ceny v katalogu jsou orientační a slouží k porovnání produktů. Závaznou cenu "
           "včetně dopravy dostanete v cenové nabídce e-mailem.</p>", lang)),
        (T("Moje vozidlo nie je v katalógu. Čo teraz?",
           "Moje vozidlo není v katalogu. Co teď?", lang),
         T("<p>Väčšinu tvarovaných panelov vieme vyrobiť na mieru podľa rozmerov vášho vozidla. "
           "Napíšte nám značku, model, rok výroby a priložte fotografie.</p>",
           "<p>Většinu tvarovaných panelů umíme vyrobit na míru podle rozměrů vašeho vozidla. "
           "Napište nám značku, model, rok výroby a přiložte fotografie.</p>", lang)),
    ]
    items = "".join(
        f'<div class="faq-i"><button class="faq-q" aria-expanded="false">{q}'
        f'<span class="pm" aria-hidden="true"></span></button>'
        f'<div class="faq-a">{a}</div></div>' for q, a in qa)
    return f"""
<section class="sec"><div class="wrap">
  <p class="lead">{T("Najčastejšie otázky k výberu, montáži a objednávaniu. Ak tu odpoveď nenájdete, napíšte nám.","Nejčastější dotazy k výběru, montáži a objednávání. Pokud tu odpověď nenajdete, napište nám.",lang)}</p>
  <div class="faq">{items}</div>
</div></section>

<section class="cta"><div class="wrap cta-in">
  <div>
    <h2>{T("Nenašli ste odpoveď?","Nenašli jste odpověď?",lang)}</h2>
    <p>{T("Ozvite sa, radi poradíme.","Ozvěte se, rádi poradíme.",lang)}</p>
  </div>
  <a class="btn signal lg js-mail" href="#"></a>
</div></section>
"""


# ---------------------------------------------------------------- kontakt
def kontakt(lang, base):
    return f"""
<section class="sec"><div class="wrap">
  <p class="lead">{T("Napíšte nám, s čím potrebujete poradiť — značku a model vozidla, prípadne aké spotrebiče chcete napájať. Ozveme sa s odporúčaním a cenou.","Napište nám, s čím potřebujete poradit — značku a model vozidla, případně jaké spotřebiče chcete napájet. Ozveme se s doporučením a cenou.",lang)}</p>
  <div class="contact">
    <div class="box">
      <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><path d="M4 6h16v12H4z"/><path d="M4 7l8 6 8-6"/></svg></div>
      <strong>{T("E-mail","E-mail",lang)}</strong>
      <p><a class="js-mail" href="#"></a></p>
    </div>
    <div class="box">
      <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><path d="M5 4h4l2 5-3 2a12 12 0 005 5l2-3 5 2v4a1 1 0 01-1 1A16 16 0 014 5a1 1 0 011-1z"/></svg></div>
      <strong>{T("Telefón","Telefon",lang)}</strong>
      <p><a class="js-phone" href="#"></a></p>
    </div>
    <div class="box">
      <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="10" r="3"/><path d="M12 21s-6-5.3-6-10a6 6 0 1112 0c0 4.7-6 10-6 10z"/></svg></div>
      <strong>{T("Adresa","Adresa",lang)}</strong>
      <p>{todo(T("doplňte adresu","doplňte adresu",lang))}</p>
    </div>
    <div class="box">
      <div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>
      <strong>{T("Kedy sme dostupní","Kdy jsme dostupní",lang)}</strong>
      <p>{todo(T("doplňte otváracie hodiny","doplňte otevírací dobu",lang))}</p>
    </div>
  </div>
</div></section>

<section class="sec alt"><div class="wrap"><div class="prose">
  <h2>{T("Objednávka z katalógu","Objednávka z katalogu",lang)}</h2>
  <p>{T("Najrýchlejšie to ide priamo z katalógu: pri produkte kliknite na Objednať, vyplňte údaje a odošlite. Príde nám e-mail s presným produktom, prevedením aj počtom kusov — nemusíte nič prepisovať.","Nejrychleji to jde přímo z katalogu: u produktu klikněte na Objednat, vyplňte údaje a odešlete. Přijde nám e-mail s přesným produktem, provedením i počtem kusů — nemusíte nic přepisovat.",lang)}</p>
  <p><a class="btn" href="{base}produkty.html">{T("Prejsť do katalógu","Přejít do katalogu",lang)}</a></p>
</div></div></section>
"""


# ---------------------------------------------------------------- podmienky
def podmienky(lang, base):
    d = todo(T("doplňte", "doplňte", lang))
    return f"""
<section class="sec"><div class="wrap"><div class="prose">
  <p class="lead">{T("Nasledujúce informácie sú rámcové. Pred zverejnením ich prosím doplňte a nechajte skontrolovať — obchodné podmienky sú právny dokument.","Následující informace jsou rámcové. Před zveřejněním je prosím doplňte a nechte zkontrolovat — obchodní podmínky jsou právní dokument.",lang)}</p>

  <h2>{T("Predávajúci","Prodávající",lang)}</h2>
  <p><strong class="js-company"></strong><br>
     {T("Sídlo","Sídlo",lang)}: {d}<br>IČO: {d} &nbsp; DIČ: {d}<br>
     E-mail: <a class="js-mail" href="#"></a></p>

  <h2>{T("Objednávka a uzavretie zmluvy","Objednávka a uzavření smlouvy",lang)}</h2>
  <p>{T("Odoslanie formulára z katalógu je nezáväzný dopyt, nie objednávka. Kúpna zmluva vzniká až potvrdením cenovej ponuky oboma stranami.","Odeslání formuláře z katalogu je nezávazná poptávka, nikoli objednávka. Kupní smlouva vzniká až potvrzením cenové nabídky oběma stranami.",lang)}</p>

  <h2>{T("Ceny","Ceny",lang)}</h2>
  <p>{T("Ceny uvedené v katalógu sú orientačné. Záväzná je cena v cenovej ponuke. Informácia o DPH a nákladoch na dopravu:","Ceny uvedené v katalogu jsou orientační. Závazná je cena v cenové nabídce. Informace o DPH a nákladech na dopravu:",lang)} {d}</p>

  <h2>{T("Dodanie","Dodání",lang)}</h2>
  <p>{T("Spôsob dopravy, cena a obvyklý termín dodania:","Způsob dopravy, cena a obvyklý termín dodání:",lang)} {d}</p>

  <h2>{T("Záruka a reklamácie","Záruka a reklamace",lang)}</h2>
  <p>{T("Dĺžka záruky a postup pri reklamácii:","Délka záruky a postup při reklamaci:",lang)} {d}</p>
  <p>{T("Záruka sa nevzťahuje na mechanické poškodenie povrchu panela, napríklad škrabancom pri odstraňovaní ľadu alebo kefovou automyčkou.","Záruka se nevztahuje na mechanické poškození povrchu panelu, například škrábancem při odstraňování ledu nebo kartáčovou myčkou.",lang)}</p>

  <h2>{T("Odstúpenie od zmluvy","Odstoupení od smlouvy",lang)}</h2>
  <p>{T("Spotrebiteľ má pri nákupe na diaľku právo odstúpiť od zmluvy v zákonnej lehote. Podrobný postup:","Spotřebitel má při nákupu na dálku právo odstoupit od smlouvy v zákonné lhůtě. Podrobný postup:",lang)} {d}</p>
  <p>{T("Pri paneloch vyrobených na mieru podľa rozmerov vášho vozidla sa právo na odstúpenie nemusí uplatniť — ide o tovar upravený na želanie zákazníka.","U panelů vyrobených na míru podle rozměrů vašeho vozidla se právo na odstoupení nemusí uplatnit — jde o zboží upravené na přání zákazníka.",lang)}</p>

  <h2>{T("Ochrana osobných údajov","Ochrana osobních údajů",lang)}</h2>
  <p>{T("Údaje z objednávkového formulára (meno, e-mail, telefón, adresa) použijeme výhradne na vybavenie vášho dopytu. Formulár neodosiela dáta na náš server — otvorí váš e-mailový klient a správu odosielate vy.","Údaje z objednávkového formuláře (jméno, e-mail, telefon, adresa) použijeme výhradně k vyřízení vaší poptávky. Formulář neodesílá data na náš server — otevře váš e-mailový klient a zprávu odesíláte vy.",lang)}</p>
  <p>{T("Web nepoužíva analytické ani reklamné cookies. Do prehliadača ukladáme len vašu voľbu svetlého alebo tmavého režimu.","Web nepoužívá analytické ani reklamní cookies. Do prohlížeče ukládáme pouze vaši volbu světlého nebo tmavého režimu.",lang)}</p>
  <p>{T("Prevádzkovateľ a kontakt pre uplatnenie práv:","Správce a kontakt pro uplatnění práv:",lang)} {d}</p>

  <h2>{T("Orgán dozoru","Orgán dozoru",lang)}</h2>
  <p>{d}</p>
</div></div></section>
"""

# -*- coding: utf-8 -*-
"""Blog: články pre slovenskú a českú verziu.

Texty sú napísané pre tento web na základe technických údajov a skúseností
zverejnených na lensunsolar.com. Videá a fotografie pochádzajú z pôvodných
článkov, na ktoré každý príspevok odkazuje.
"""

SRC = "https://lensunsolar.com/blogs/"

# Rubriky blogu. Kľúč sa používa v článkoch aj vo filtri, dvojica je názov
# pre slovenskú a českú verziu.
CATS = [
    ("kapota",   ("Panely na kapotu",     "Panely na kapotu")),
    ("montaz",   ("Skúsenosti z montáže", "Zkušenosti z montáže")),
    ("prenosne", ("Prenosné panely",      "Přenosné panely")),
    ("technika", ("Technika",             "Technika")),
]
CAT = dict(CATS)

POSTS = [
 dict(
  slug="solarny-panel-na-kapotu",
  video="jAs6KkkX_Vs",
  hero="https://lensunsolar.com/cdn/shop/files/lensunsolar-hood-solar-panel-2_1780x.jpg",
  date="2026-02-11",
  source=SRC + "hood-solar-panel/lensun-hood-solar-panel",
  product=None,
  cat="kapota",
  title=("Prečo solárny panel práve na kapotu",
         "Proč solární panel právě na kapotu"),
  lead=("Kapota je najväčšia rovná plocha na aute, ktorá sa nedá využiť na nič iné. "
        "Presne preto je pre solárny panel ideálna.",
        "Kapota je největší rovná plocha na autě, kterou nelze využít na nic jiného. "
        "Právě proto je pro solární panel ideální."),
  body=[
   (("Problém, ktorý panel rieši", "Problém, který panel řeší"),
    [("Štartovacia batéria sa počas bežnej jazdy dobije len čiastočne. Keď auto stojí "
      "dva či tri týždne, alebo keď z neho napájate chladničku, palubnú kameru a "
      "osvetlenie, kapacita klesá rýchlejšie, než ju alternátor stihne doplniť.",
      "Startovací baterie se během běžné jízdy dobije jen částečně. Když auto stojí "
      "dva až tři týdny, nebo když z něj napájíte lednici, palubní kameru a "
      "osvětlení, kapacita klesá rychleji, než ji alternátor stihne doplnit."),
     ("Panel na kapote dopĺňa batériu vždy, keď na ňu svieti slnko — počas státia aj "
      "jazdy. Nemusíte štartovať motor len preto, aby ste dobili batériu.",
      "Panel na kapotě doplňuje baterii vždy, když na ni svítí slunce — při stání i "
      "za jízdy. Nemusíte startovat motor jen proto, abyste dobili baterii.")]),
   (("Prečo tvarovaný a nie univerzálny", "Proč tvarovaný a ne univerzální"),
    [("Panely sú vyrobené podľa tvaru kapoty konkrétneho modelu a generácie. Kopírujú "
      "jej zaoblenie, rebrovanie aj hrany, takže na plechu nezostávajú medzery, v "
      "ktorých by sa držala voda a nečistoty.",
      "Panely jsou vyrobené podle tvaru kapoty konkrétního modelu a generace. Kopírují "
      "její zaoblení, žebrování i hrany, takže na plechu nezůstávají mezery, ve "
      "kterých by se držela voda a nečistoty."),
     ("Univerzálny obdĺžnik na zaoblenej kapote nikdy nedosadne celou plochou. Vzniká "
      "pnutie, ktoré časom poškodí články a lepený spoj.",
      "Univerzální obdélník na zaoblené kapotě nikdy nedosedne celou plochou. Vzniká "
      "pnutí, které časem poškodí články i lepený spoj.")]),
   (("Čo je súčasťou zostavy", "Co je součástí sestavy"),
    [("K panelu patrí regulátor nabíjania — bez neho sa panel na batériu nepripája. "
      "MPPT regulátor vyťaží z panela viac než jednoduchší PWM typ, najmä pri "
      "oblačnosti a nižších teplotách.",
      "K panelu patří regulátor nabíjení — bez něj se panel na baterii nepřipojuje. "
      "MPPT regulátor vytěží z panelu více než jednodušší PWM typ, zejména při "
      "oblačnosti a nižších teplotách."),
     ("Odporúčame aj vinylovú fóliu medzi panel a lak. Chráni plech pred oderom a "
      "pri prípadnej demontáži uľahčí odstránenie lepidla.",
      "Doporučujeme také vinylovou fólii mezi panel a lak. Chrání plech před oděrem a "
      "při případné demontáži usnadní odstranění lepidla.")]),
  ]),

 dict(
  slug="land-rover-discovery-110w",
  video="aISR3CdTZPc",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Land_Rover_Discovery_LR3_LR4_Lensun_110W_Hood_Bonnet_Flexible_Solar_Panel.jpg",
  date="2026-03-04",
  source=SRC + "hood-solar-panel/hood-solar-panel-installation-experience-for-110w-land-rover-discovery-lr3-lr4",
  product="land-rover-discovery-lensun-110w-hood-bonnet-solar-panel",
  cat="montaz",
  title=("Land Rover Discovery LR3/LR4: 110 W na kapote",
         "Land Rover Discovery LR3/LR4: 110 W na kapotě"),
  lead=("Majiteľ Discovery LR3 najprv skúsil lacný univerzálny panel z inzerátu. "
        "Vydržal pár sezón. Potom prešiel na panel tvarovaný priamo na túto kapotu.",
        "Majitel Discovery LR3 nejprve zkusil levný univerzální panel z inzerátu. "
        "Vydržel pár sezon. Potom přešel na panel tvarovaný přímo na tuto kapotu."),
  body=[
   (("Prečo výmena", "Proč výměna"),
    [("Pôvodný osemdesiatwattový panel z bazáru fungoval, ale mal nízku účinnosť a po "
      "niekoľkých rokoch prestal dodávať energiu. Typická slabina lacných panelov je "
      "fólia, ktorá pod UV žiarením zožltne a začne sa oddeľovať od článkov.",
      "Původní osmdesátiwattový panel z bazaru fungoval, ale měl nízkou účinnost a po "
      "několika letech přestal dodávat energii. Typická slabina levných panelů je "
      "fólie, která pod UV zářením zežloutne a začne se oddělovat od článků.")]),
   (("Čo priniesol tvarovaný panel", "Co přinesl tvarovaný panel"),
    [("Panel s výkonom 110 W je vyrobený na kapotu Discovery LR3 a LR4 ročníkov "
      "2005 – 2016. Sadne na plech bez medzier a vizuálne pôsobí ako súčasť auta, "
      "nie ako dodatočný doplnok.",
      "Panel s výkonem 110 W je vyrobený na kapotu Discovery LR3 a LR4 ročníků "
      "2005 – 2016. Sedne na plech bez mezer a vizuálně působí jako součást auta, "
      "ne jako dodatečný doplněk."),
     ("Montáž zvládli dvaja ľudia. Panel sa lepí obojstrannou páskou, kábel sa vedie "
      "do motorového priestoru a odtiaľ na regulátor.",
      "Montáž zvládli dva lidé. Panel se lepí oboustrannou páskou, kabel se vede "
      "do motorového prostoru a odtud na regulátor.")]),
   (("Na čo myslieť pred lepením", "Na co myslet před lepením"),
    [("Plech musí byť čistý, suchý a odmastený — zvyšky vosku alebo leštenky sú "
      "najčastejšou príčinou toho, že páska nedrží. Lepte za tepla, ideálne v hale "
      "alebo cez teplý deň.",
      "Plech musí být čistý, suchý a odmaštěný — zbytky vosku nebo leštěnky jsou "
      "nejčastější příčinou toho, že páska nedrží. Lepte za tepla, ideálně v hale "
      "nebo za teplého dne.")]),
  ]),

 dict(
  slug="jeep-wrangler-jk-105w",
  video="TCQyQjHDT2c",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Jeep_Wrangler_JK_Lensun_105W_Hood_Bonnet_Flexible_Solar_Panel.jpg",
  date="2026-03-18",
  source=SRC + "hood-solar-panel/hood-solar-panel-installation-experience-for-105w-jeep-wrangler-jk",
  product="jeep-wrangler-jk-lensun-105w-hood-flexible-solar-panel",
  cat="montaz",
  title=("Jeep Wrangler JK: 105 W a batéria, ktorá vydrží",
         "Jeep Wrangler JK: 105 W a baterie, která vydrží"),
  lead=("Majiteľ Wrangleru z roku 2011 chcel z auta napájať chladničku a mať istotu, "
        "že ho po víkende v teréne naštartuje.",
        "Majitel Wrangleru z roku 2011 chtěl z auta napájet lednici a mít jistotu, "
        "že ho po víkendu v terénu nastartuje."),
  body=[
   (("Bežné použitie", "Běžné použití"),
    [("Panel drží batériu nabitú aj vtedy, keď auto dlhšie stojí s vypnutým motorom — "
      "pri táborení, na parkovisku pred túrou alebo počas sezóny mimo prevádzky.",
      "Panel drží baterii nabitou i tehdy, když auto delší dobu stojí s vypnutým motorem — "
      "při táboření, na parkovišti před túrou nebo během sezony mimo provoz.")]),
   (("Montáž", "Montáž"),
    [("Wrangler má takmer rovnú kapotu, takže lepenie je jednoduchšie než pri "
      "výrazne tvarovaných kapotách. Panel drží obojstrannou páskou, kábel sa vedie "
      "popri hrane kapoty a existujúcou priechodkou do interiéru.",
      "Wrangler má téměř rovnou kapotu, takže lepení je jednodušší než u "
      "výrazně tvarovaných kapot. Panel drží oboustrannou páskou, kabel se vede "
      "podél hrany kapoty a stávající průchodkou do interiéru."),
     ("Pozor pri modeloch Rubicon s vyvýšeným stredom kapoty — pre ne existuje iný "
      "tvar panela. Pred objednávkou si overte tvar svojej kapoty.",
      "Pozor u modelů Rubicon s vyvýšeným středem kapoty — pro ně existuje jiný "
      "tvar panelu. Před objednávkou si ověřte tvar své kapoty.")]),
  ]),

 dict(
  slug="kolko-energie-panel-naozaj-dodava",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/The-Solar-Panels-Output-In-The-Real-World-LensunSolar-1_480x480.jpg",
  date="2026-04-08",
  source=SRC + "solar-technology-information/how-much-power-can-you-really-get-from-a-solar-panel",
  product=None,
  cat="technika",
  title=("Koľko energie panel naozaj dodá",
         "Kolik energie panel opravdu dodá"),
  lead=("Stowattový panel takmer nikdy nedodá sto wattov. Nie je to chyba — "
        "je to rozdiel medzi laboratóriom a cestou.",
        "Stowattový panel téměř nikdy nedodá sto wattů. Není to chyba — "
        "je to rozdíl mezi laboratoří a silnicí."),
  body=[
   (("Čo znamená údaj na štítku", "Co znamená údaj na štítku"),
    [("Výkon panela sa meria za štandardných skúšobných podmienok (STC): teplota "
      "článku 25 °C, intenzita žiarenia 1000 W/m² a takzvaná vzduchová hmota 1,5. "
      "Je to jasný deň so slnkom takmer kolmo nad panelom.",
      "Výkon panelu se měří za standardních zkušebních podmínek (STC): teplota "
      "článku 25 °C, intenzita záření 1000 W/m² a takzvaná vzduchová hmota 1,5. "
      "Je to jasný den se sluncem téměř kolmo nad panelem."),
     ("Tieto podmienky sa v praxi stretnú len zriedka a väčšinou len na pár minút "
      "denne. Preto je bežné, že stowattový panel dodáva 60 až 80 wattov.",
      "Tyto podmínky se v praxi sejdou jen zřídka a většinou jen na pár minut "
      "denně. Proto je běžné, že stowattový panel dodává 60 až 80 wattů.")]),
   (("Čo výkon znižuje", "Co výkon snižuje"),
    [("<b>Teplota.</b> Články na rozpálenej kapote majú aj 60 °C. S rastúcou teplotou "
      "napätie klesá, takže v horúci deň dostanete menej než na jar pri rovnakom slnku.",
      "<b>Teplota.</b> Články na rozpálené kapotě mají i 60 °C. S rostoucí teplotou "
      "napětí klesá, takže v horký den dostanete méně než na jaře při stejném slunci."),
     ("<b>Uhol dopadu.</b> Panel naplocho na kapote dostane plný výkon len okolo "
      "poludnia. Ráno a večer svetlo dopadá šikmo.",
      "<b>Úhel dopadu.</b> Panel naplocho na kapotě dostane plný výkon jen kolem "
      "poledne. Ráno a večer světlo dopadá šikmo."),
     ("<b>Tieň a nečistoty.</b> Aj čiastočné zatienenie vetvou alebo vrstva prachu "
      "zníži výkon celého panela, nielen zatienenej časti.",
      "<b>Stín a nečistoty.</b> I částečné zastínění větví nebo vrstva prachu "
      "sníží výkon celého panelu, nejen zastíněné části."),
     ("<b>Straty vo vedení.</b> Dlhý alebo tenký kábel a účinnosť regulátora uberú "
      "ďalších pár percent.",
      "<b>Ztráty ve vedení.</b> Dlouhý nebo tenký kabel a účinnost regulátoru uberou "
      "dalších pár procent.")]),
   (("Ako s tým počítať", "Jak s tím počítat"),
    [("Pri návrhu zostavy počítajte reálne so 60 – 70 % menovitého výkonu. Ak "
      "potrebujete denne 300 Wh, nestačí panel, ktorý by ich teoreticky dodal za "
      "tri hodiny — počítajte s rezervou.",
      "Při návrhu sestavy počítejte reálně s 60 – 70 % jmenovitého výkonu. Pokud "
      "potřebujete denně 300 Wh, nestačí panel, který by je teoreticky dodal za "
      "tři hodiny — počítejte s rezervou.")]),
  ]),

 dict(
  slug="meranie-napatia-a-prudu",
  video="8eK1Qts1RbY",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/How-to-Measure-Solar-Panel-Voltage-and-Current-2_480x480.jpg",
  date="2026-05-06",
  source=SRC + "solar-technology-information/how-to-measure-solar-panel-voltage-and-current",
  product=None,
  cat="technika",
  title=("Ako zmerať napätie a prúd solárneho panela",
         "Jak změřit napětí a proud solárního panelu"),
  lead=("Multimetrom overíte za pár minút, či panel dodáva to, čo má. "
        "Dôležité je merať správne — inak vám čísla povedia nezmysel.",
        "Multimetrem ověříte za pár minut, jestli panel dodává to, co má. "
        "Důležité je měřit správně — jinak vám čísla řeknou nesmysl."),
  body=[
   (("Kedy merať", "Kdy měřit"),
    [("Merajte za jasného dňa okolo poludnia, s panelom nasmerovaným kolmo na slnko. "
      "Meranie v tieni alebo pri oblačnosti nič nevypovedá — hodnoty budú nízke aj "
      "pri úplne zdravom paneli.",
      "Měřte za jasného dne kolem poledne, s panelem nasměrovaným kolmo na slunce. "
      "Měření ve stínu nebo při oblačnosti nic nevypovídá — hodnoty budou nízké i "
      "u zcela zdravého panelu.")]),
   (("Napätie naprázdno (Voc)", "Napětí naprázdno (Voc)"),
    [("Panel odpojte od regulátora aj batérie. Multimeter prepnite na jednosmerné "
      "napätie v rozsahu nad 20 V a hroty priložte na kladný a záporný konektor "
      "panela. Nameraná hodnota by mala byť blízko údaju Voc na štítku.",
      "Panel odpojte od regulátoru i baterie. Multimetr přepněte na stejnosměrné "
      "napětí v rozsahu nad 20 V a hroty přiložte na kladný a záporný konektor "
      "panelu. Naměřená hodnota by měla být blízko údaji Voc na štítku.")]),
   (("Skratový prúd (Isc)", "Zkratový proud (Isc)"),
    [("Multimeter prepnite na jednosmerný prúd a použite zdierku pre 10 A. Hroty "
      "spojte priamo s konektormi panela — pri tomto meraní je skrat v poriadku, "
      "panel je prúdovo obmedzený.",
      "Multimetr přepněte na stejnosměrný proud a použijte zdířku pro 10 A. Hroty "
      "spojte přímo s konektory panelu — při tomto měření je zkrat v pořádku, "
      "panel je proudově omezený."),
     ("Overte si, že prúd panela nepresahuje rozsah vášho multimetra, inak "
      "prepálite jeho poistku. Merajte krátko a hodnotu porovnajte s údajom Isc.",
      "Ověřte si, že proud panelu nepřesahuje rozsah vašeho multimetru, jinak "
      "spálíte jeho pojistku. Měřte krátce a hodnotu porovnejte s údajem Isc.")]),
   (("Ako výsledok čítať", "Jak výsledek číst"),
    [("Napätie výrazne nižšie než Voc naznačuje poškodený článok alebo prerušený "
      "spoj. Správne napätie pri nízkom prúde býva vecou tieňa, nečistôt alebo "
      "šikmého dopadu svetla.",
      "Napětí výrazně nižší než Voc naznačuje poškozený článek nebo přerušený "
      "spoj. Správné napětí při nízkém proudu bývá věcí stínu, nečistot nebo "
      "šikmého dopadu světla.")]),
  ]),

 dict(
  slug="etfe-a-pet",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/lensun-flexible-solar-panel-anti-crack-film.jpg",
  date="2026-05-27",
  source=SRC + "solar-technology-information/the-performance-of-etfe-and-pet",
  product=None,
  cat="technika",
  title=("ETFE a PET: prečo je vrchná fólia dôležitejšia, než sa zdá",
         "ETFE a PET: proč je vrchní fólie důležitější, než se zdá"),
  lead=("Dva flexibilné panely môžu mať rovnaký výkon na štítku a pritom úplne "
        "odlišnú životnosť. Rozdiel býva v materiáli vrchnej vrstvy.",
        "Dva flexibilní panely mohou mít stejný výkon na štítku a přitom zcela "
        "odlišnou životnost. Rozdíl bývá v materiálu vrchní vrstvy."),
  body=[
   (("Čo vrchná fólia robí", "Co vrchní fólie dělá"),
    [("Vrchná vrstva flexibilného panela musí prepustiť čo najviac svetla a zároveň "
      "roky odolávať UV žiareniu, teplu, dažďu a mechanickému namáhaniu. Je to "
      "jediná ochrana kremíkových článkov pod ňou.",
      "Vrchní vrstva flexibilního panelu musí propustit co nejvíce světla a zároveň "
      "roky odolávat UV záření, teplu, dešti a mechanickému namáhání. Je to "
      "jediná ochrana křemíkových článků pod ní.")]),
   (("PET: lacnejšie riešenie", "PET: levnější řešení"),
    [("PET je bežný plast s nižšou priepustnosťou svetla. Pod UV žiarením postupne "
      "žltne a matnie, čím klesá výkon panela. Na vozidle, kde je panel na slnku "
      "trvalo, sa to prejaví rýchlo — často už po jednej či dvoch sezónach.",
      "PET je běžný plast s nižší propustností světla. Pod UV zářením postupně "
      "žloutne a matní, čímž klesá výkon panelu. Na vozidle, kde je panel na slunci "
      "trvale, se to projeví rychle — často už po jedné či dvou sezonách.")]),
   (("ETFE: fluoropolymérová fólia", "ETFE: fluoropolymerová fólie"),
    [("ETFE prepúšťa okolo 95 % svetla a je odolné voči UV, teplu aj korózii. "
      "Povrch je mikroskopicky hladký, takže sa naň menej lepí špina a väčšinu "
      "nečistôt spláchne dážď.",
      "ETFE propouští okolo 95 % světla a je odolné vůči UV, teplu i korozi. "
      "Povrch je mikroskopicky hladký, takže se na něj méně lepí špína a většinu "
      "nečistot spláchne déšť."),
     ("Pri paneli, ktorý má na aute vydržať roky, je rozdiel v cene medzi PET a "
      "ETFE takmer vždy dobrá investícia.",
      "U panelu, který má na autě vydržet roky, je rozdíl v ceně mezi PET a "
      "ETFE téměř vždy dobrá investice.")]),
  ]),
 
 dict(
  slug="motor-a-teplo-pod-panelom",
  video=None,
  hero="https://lensunsolar.com/cdn/shop/articles/does-engine-heat-affect-lensun-hood-solar-panel-6_1066x.jpg",
  date="2026-06-10",
  source=SRC + "hood-solar-panel/does-engine-heat-affect-lensun-hood-solar-panel-heres-the-real-answer",
  product=None,
  cat="kapota",
  title=("Nepoškodí panel teplo od motora?",
         "Nepoškodí panel teplo od motoru?"),
  lead=("Najčastejšia otázka pred kúpou: pod kapotou je horúci motor, panel je na nej "
        "nalepený. Vydrží to?",
        "Nejčastější dotaz před koupí: pod kapotou je horký motor, panel je na ní "
        "nalepený. Vydrží to?"),
  body=[
   (("Panel neleží priamo na plechu", "Panel neleží přímo na plechu"),
    [("Medzi lakom a panelom je vinylová fólia a nad ňou vrstva obojstrannej lepiacej "
      "pásky VHB. Tie dve vrstvy nie sú tam len kvôli držaniu — fungujú aj ako tepelná "
      "izolácia, ktorá oddelí panel od rozohriateho plechu.",
      "Mezi lakem a panelem je vinylová fólie a nad ní vrstva oboustranné lepicí "
      "pásky VHB. Ty dvě vrstvy tam nejsou jen kvůli držení — fungují také jako tepelná "
      "izolace, která oddělí panel od rozehřátého plechu."),
     ("Zadná strana panela je z materiálov, ktoré sú na vyššie teploty stavané. "
      "Sklolaminátová podložka odvádza teplo lepšie než lacnejšia PET fólia.",
      "Zadní strana panelu je z materiálů, které jsou na vyšší teploty stavěné. "
      "Sklolaminátová podložka odvádí teplo lépe než levnější PET fólie.")]),
   (("Za jazdy kapota chladne, nie hreje", "Za jízdy kapota chladne, ne hřeje"),
    [("Predstava, že sa kapota za jazdy prehreje, je opačná než realita. Prúdiaci "
      "vzduch nad kapotou ju ochladzuje — panel je pri jazde spravidla chladnejší, "
      "než keď auto stojí na priamom slnku.",
      "Představa, že se kapota za jízdy přehřeje, je opačná než realita. Proudící "
      "vzduch nad kapotou ji ochlazuje — panel je při jízdě zpravidla chladnější, "
      "než když auto stojí na přímém slunci.")]),
   (("Panel pracuje hlavne s vypnutým motorom", "Panel pracuje hlavně s vypnutým motorem"),
    [("Zmysel panela je dobíjať batériu vtedy, keď auto stojí. Počas jazdy prácu "
      "preberá alternátor. Panel teda nie je zaťažený práve vtedy, keď je pod ním "
      "najviac tepla.",
      "Smysl panelu je dobíjet baterii tehdy, když auto stojí. Během jízdy práci "
      "přebírá alternátor. Panel tedy není zatížený právě tehdy, když je pod ním "
      "nejvíc tepla."),
     ("Praktický dôsledok: teplo od motora nie je dôvod na obavy. Skutočne dôležité "
      "je čisté a odmastené podložie pri lepení a použitie fólie pod panelom.",
      "Praktický důsledek: teplo od motoru není důvod k obavám. Skutečně důležité "
      "je čistý a odmaštěný podklad při lepení a použití fólie pod panelem.")]),
  ]),

 dict(
  slug="preco-panel-na-kapotu-a-nie-na-strechu",
  video=None,
  hero="https://lensunsolar.com/cdn/shop/articles/lensun-90w-hood-solar-panel-for-toyota-tacoma-3rd-gen-2016-2023-250718-blog-1_065f2a9e-64e7-4912-be47-42d00bd1c9b6_1066x.jpg",
  date="2026-06-24",
  source=SRC + "hood-solar-panel/why-serious-overlanders-are-upgrading-to-hood-solar-panels",
  product=None,
  cat="kapota",
  title=("Kapota, strecha alebo prenosný panel?",
         "Kapota, střecha nebo přenosný panel?"),
  lead=("Na streche býva nosič alebo stanový box, prenosný panel zaberá miesto v "
        "kufri. Kapota je plocha, ktorú na aute nič iné nevyužíva.",
        "Na střeše bývá nosič nebo stanový box, přenosný panel zabírá místo v "
        "kufru. Kapota je plocha, kterou na autě nic jiného nevyužívá."),
  body=[
   (("Strecha je zvyčajne obsadená", "Střecha je obvykle obsazená"),
    [("Terénne a cestovateľské autá majú na streche nosič, strešný stan alebo box. "
      "Pevný panel tam už nemá kam ísť a panel na stane funguje len vtedy, keď je "
      "stan rozložený.",
      "Terénní a cestovatelská auta mají na střeše nosič, střešní stan nebo box. "
      "Pevný panel tam už nemá kam jít a panel na stanu funguje jen tehdy, když je "
      "stan rozložený.")]),
   (("Prenosný panel treba zakaždým rozložiť", "Přenosný panel je třeba pokaždé rozložit"),
    [("Skladací panel je dobrý na dovolenku, kde stojíte na jednom mieste. Pri "
      "presunoch ho ale musíte pri každom zastavení vybrať, natočiť za slnkom a pred "
      "odchodom zložiť. A počas jazdy neprodukuje nič.",
      "Skládací panel je dobrý na dovolenou, kde stojíte na jednom místě. Při "
      "přesunech ho ale musíte při každém zastavení vyndat, natočit za sluncem a před "
      "odjezdem složit. A během jízdy neprodukuje nic."),
     ("Panel na kapote je nainštalovaný natrvalo. Nemá čo pokaziť sa pri manipulácii "
      "a nezaberá miesto v batožinovom priestore.",
      "Panel na kapotě je nainstalovaný natrvalo. Nemá se co pokazit při manipulaci "
      "a nezabírá místo v zavazadlovém prostoru.")]),
   (("Prečo moderné autá batériu podvýživujú", "Proč moderní auta baterii podvyživují"),
    [("Autá vyrobené zhruba po roku 2012 riadia dobíjanie tak, aby ušetrili palivo. "
      "Alternátor sa počas jazdy často odpojí a batériu dobíja až vtedy, keď napätie "
      "klesne. Batéria tak dlhodobo beží na časti kapacity.",
      "Auta vyrobená zhruba po roce 2012 řídí dobíjení tak, aby ušetřila palivo. "
      "Alternátor se během jízdy často odpojí a baterii dobíjí až tehdy, když napětí "
      "klesne. Baterie tak dlouhodobě běží na části kapacity."),
     ("Trvalé mierne podnabitie je hlavný dôvod, prečo štartovacie batérie vydržia "
      "dva až tri roky namiesto piatich. Panel, ktorý dopĺňa energiu vždy, keď svieti "
      "slnko, tento cyklus preruší.",
      "Trvalé mírné podbití je hlavní důvod, proč startovací baterie vydrží "
      "dva až tři roky místo pěti. Panel, který doplňuje energii vždy, když svítí "
      "slunce, tento cyklus přeruší.")]),
   (("Čo panel na kapote reálne utiahne", "Co panel na kapotě reálně utáhne"),
    [("Chladnička, osvetlenie, nabíjanie telefónov a tabletov, vysielačka, palubná "
      "kamera. Pri väčších paneloch aj dobíjanie prenosnej elektrocentrály typu "
      "Jackery či EcoFlow cez redukciu.",
      "Lednice, osvětlení, nabíjení telefonů a tabletů, vysílačka, palubní kamera. "
      "U větších panelů i dobíjení přenosné elektrocentrály typu Jackery či EcoFlow "
      "přes redukci.")]),
  ]),

 dict(
  slug="land-rover-defender-90w",
  video="nw-sylzF1SY",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Land_Rover_Defender_2020-present_Lensun_90W_Hood_Bonnet_Flexible_Solar_Panel.jpg",
  date="2026-04-22",
  source=SRC + "hood-solar-panel/hood-solar-panel-installation-experience-for-90w-land-rover-defender-2020-present",
  product="land-rover-defender-lensun-90w-hood-bonnet-flexible-solar-panel",
  cat="montaz",
  title=("Land Rover Defender 2020+: 90 W a bluetooth regulátor",
         "Land Rover Defender 2020+: 90 W a bluetooth regulátor"),
  lead=("Grant namontoval panel na nový Defender 110 sám za jedno popoludnie. "
        "Zaujímavá je najmä jednoduchosť zapojenia.",
        "Grant namontoval panel na nový Defender 110 sám za jedno odpoledne. "
        "Zajímavá je hlavně jednoduchost zapojení."),
  body=[
   (("Priebeh montáže", "Průběh montáže"),
    [("Panel sa lepí obojstrannou automobilovou páskou a zapája sa priamo do "
      "regulátora. Z regulátora vedú dva káble na plusový a mínusový štartovací bod "
      "v motorovom priestore — nič viac netreba rozoberať.",
      "Panel se lepí oboustrannou automobilovou páskou a zapojuje se přímo do "
      "regulátoru. Z regulátoru vedou dva kabely na plusový a minusový startovací bod "
      "v motorovém prostoru — nic víc není třeba rozebírat."),
     ("Práve preto ide o zákrok, ktorý nezasahuje do elektroniky vozidla a dá sa "
      "vrátiť do pôvodného stavu.",
      "Právě proto jde o zákrok, který nezasahuje do elektroniky vozidla a dá se "
      "vrátit do původního stavu.")]),
   (("Regulátor s aplikáciou", "Regulátor s aplikací"),
    [("Voliteľný 10 A MPPT regulátor má bluetooth. V telefóne vidíte okamžitý výkon "
      "panela, napätie batérie aj dennú výťažnosť. Pri prvých týždňoch je to "
      "najlepší spôsob, ako overiť, že je zapojenie v poriadku.",
      "Volitelný 10A MPPT regulátor má bluetooth. V telefonu vidíte okamžitý výkon "
      "panelu, napětí baterie i denní výtěžnost. V prvních týdnech je to "
      "nejlepší způsob, jak ověřit, že je zapojení v pořádku."),
     ("Regulátor je vodotesný a má ochranu proti prepólovaniu, prebitiu, skratu aj "
      "spätnému prúdu. Zvláda olovené, AGM, gélové aj lítiové batérie.",
      "Regulátor je vodotěsný a má ochranu proti přepólování, přebití, zkratu i "
      "zpětnému proudu. Zvládá olověné, AGM, gelové i lithiové baterie.")]),
   (("Parametre panela", "Parametry panelu"),
    [("Špičkový výkon 90 W, napätie v bode maximálneho výkonu 17,5 V, prúd 5,14 A. "
      "Hmotnosť 2,5 kg, hrúbka 3 mm. Prípojná skrinka má krytie IP 68 a dva metre "
      "kábla so štandardnými konektormi.",
      "Špičkový výkon 90 W, napětí v bodě maximálního výkonu 17,5 V, proud 5,14 A. "
      "Hmotnost 2,5 kg, tloušťka 3 mm. Připojovací krabice má krytí IP 68 a dva metry "
      "kabelu se standardními konektory."),
     ("Pracovné napätie 17,5 V je zvolené tak, aby panel dobíjal dvanásťvoltovú "
      "sústavu aj pri oblačnosti, keď napätie klesá.",
      "Pracovní napětí 17,5 V je zvolené tak, aby panel dobíjel dvanáctivoltovou "
      "soustavu i při oblačnosti, kdy napětí klesá.")]),
  ]),

 dict(
  slug="suzuki-jimny-panel-na-kapotu",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Suzuki_Jimny_4th_Gen_2018-present_Lensun_80W_Hood_Bonnet_Flexible_Solar_Panel-1.jpg",
  date="2026-05-13",
  source=SRC + "solar-panel-review/review-of-suzuki-jimny-4th-gen2018-present-lensunsolar-75w-car-hood-solar-panel-installation",
  product="suzuki-jimny-lensun-85w-bonnet-solar-panel",
  cat="montaz",
  title=("Suzuki Jimny: malé auto, plná kapota",
         "Suzuki Jimny: malé auto, plná kapota"),
  lead=("Jimny má krátku a takmer rovnú kapotu. Pre solárny panel je to ideálny tvar "
        "a Jorge z neho napája prenosnú elektrocentrálu.",
        "Jimny má krátkou a téměř rovnou kapotu. Pro solární panel je to ideální tvar "
        "a Jorge z něj napájí přenosnou elektrocentrálu."),
  body=[
   (("Montáž v troch krokoch", "Montáž ve třech krocích"),
    [("Najprv prišla na plech vinylová fólia narezaná presne na tvar kapoty. Na ňu "
      "obojstranná páska 3M a na pásku panel. Celý postup zvládol majiteľ sám a "
      "označil ho za príjemnú prácu, nie za montážnu drinu.",
      "Nejprve přišla na plech vinylová fólie nařezaná přesně na tvar kapoty. Na ni "
      "oboustranná páska 3M a na pásku panel. Celý postup zvládl majitel sám a "
      "označil ho za příjemnou práci, ne za montážní dřinu."),
     ("Kabeláž viedla k prenosnej elektrocentrále Jackery, ktorá sa začala nabíjať "
      "hneď po zapojení.",
      "Kabeláž vedla k přenosné elektrocentrále Jackery, která se začala nabíjet "
      "hned po zapojení.")]),
   (("Na čo Jimny panel využíva", "Na co Jimny panel využívá"),
    [("Nabíjanie telefónov, USB osvetlenie a drobná elektronika na výletoch. Na malé "
      "auto s malou batériou je práve trvalé dobíjanie to najužitočnejšie — Jimny "
      "sa často používa nepravidelne a batéria má čas vybiť sa.",
      "Nabíjení telefonů, USB osvětlení a drobná elektronika na výletech. Na malé "
      "auto s malou baterií je právě trvalé dobíjení to nejužitečnější — Jimny "
      "se často používá nepravidelně a baterie má čas se vybít.")]),
   (("Ktoré generácie pokrývame", "Které generace pokrýváme"),
    [("V katalógu máme panely pre druhú, tretiu aj štvrtú generáciu Jimny. Každá má "
      "iný tvar kapoty, preto sa panely nedajú medzi generáciami zamieňať — pri "
      "objednávke uveďte rok výroby.",
      "V katalogu máme panely pro druhou, třetí i čtvrtou generaci Jimny. Každá má "
      "jiný tvar kapoty, proto se panely nedají mezi generacemi zaměňovat — při "
      "objednávce uveďte rok výroby.")]),
  ]),

 dict(
  slug="vw-touareg-120w",
  video="ECb2OqIzEWs",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Volkswagen_VW_Touareg_Lensun_100W_Hood_Flexible_Solar_Panel.jpg",
  date="2026-07-08",
  source=SRC + "hood-solar-panel/hood-solar-panel-installation-experience-for-120w-volkswagen-vw-touareg",
  product=None,
  cat="montaz",
  title=("VW Touareg: druhý panel, ktorý konečne stačil na chladničku",
         "VW Touareg: druhý panel, který konečně stačil na lednici"),
  lead=("Jerahmel mal 120 W na strešnom stane. Chladnička mu vydržala dve noci. "
        "Až druhý panel na kapote problém vyriešil.",
        "Jerahmel měl 120 W na střešním stanu. Lednice mu vydržela dvě noci. "
        "Až druhý panel na kapotě problém vyřešil."),
  body=[
   (("Prečo jeden panel nestačil", "Proč jeden panel nestačil"),
    [("Panel na strešnom stane dobíjal elektrocentrálu EcoFlow s kapacitou 768 Wh. "
      "Chladnička ju vyčerpala rýchlejšie, než ju stihol jeden panel doplniť — po "
      "dvoch nociach bola centrála prázdna.",
      "Panel na střešním stanu dobíjel elektrocentrálu EcoFlow s kapacitou 768 Wh. "
      "Lednice ji vyčerpala rychleji, než ji stihl jeden panel doplnit — po "
      "dvou nocích byla centrála prázdná."),
     ("Po pridaní druhého 120 W panela na kapotu sa nabíjanie zdvojnásobilo a "
      "chladnička už beží bez prestávky.",
      "Po přidání druhého 120W panelu na kapotu se nabíjení zdvojnásobilo a "
      "lednice už běží bez přestávky.")]),
   (("Dva panely nie sú prepych", "Dva panely nejsou přepych"),
    [("Ak z auta napájate chladničku, počítajte skôr s 200 W a viac. Jeden panel "
      "udrží batériu nabitú, dva panely dokážu pokryť aj trvalú spotrebu.",
      "Pokud z auta napájíte lednici, počítejte spíš s 200 W a více. Jeden panel "
      "udrží baterii nabitou, dva panely dokážou pokrýt i trvalou spotřebu."),
     ("Panely na kapote a na streche sa dopĺňajú aj preto, že sú v inom uhle. Keď "
      "auto stojí v čiastočnom tieni, jeden z nich takmer vždy niečo vyrába.",
      "Panely na kapotě a na střeše se doplňují i proto, že jsou v jiném úhlu. Když "
      "auto stojí v částečném stínu, jeden z nich téměř vždy něco vyrábí.")]),
   (("Parametre 120 W panela", "Parametry 120W panelu"),
    [("Špičkový výkon 120 W, napätie 19,5 V, prúd 6,15 A, účinnosť článkov 22,5 %. "
      "Hmotnosť 3,5 kg pri hrúbke 3 mm.",
      "Špičkový výkon 120 W, napětí 19,5 V, proud 6,15 A, účinnost článků 22,5 %. "
      "Hmotnost 3,5 kg při tloušťce 3 mm."),
     ("Z vozidiel Volkswagen máme v katalógu panely na Amarok prvej aj druhej "
      "generácie. Na iné modely vieme panel vyrobiť na mieru podľa rozmerov kapoty.",
      "Z vozidel Volkswagen máme v katalogu panely na Amarok první i druhé "
      "generace. Na jiné modely umíme panel vyrobit na míru podle rozměrů kapoty.")]),
  ]),

 dict(
  slug="panel-na-strechu-bez-vrtania",
  video="hhKDgQNPhJE",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/lensunsolar-200w-flexible-solar-panel-rv-camper.jpg",
  date="2026-07-22",
  source=SRC + "solar-panel-installation/how-to-install-flexible-solar-panel-on-rv-camper-bus-trailer-car-roof-with-no-holes-a-helpful-installing-reivew-of-2pcs-lensun-100w-flexible-solar-panel-from-mr-smith",
  product=None,
  cat="montaz",
  title=("Panel na strechu dodávky bez jediného otvoru",
         "Panel na střechu dodávky bez jediného otvoru"),
  lead=("Do strechy obytnej dodávky sa nikomu vŕtať nechce. Dva flexibilné panely sa "
        "dajú prilepiť tak, že strecha zostane neporušená.",
        "Do střechy obytné dodávky se nikomu vrtat nechce. Dva flexibilní panely se "
        "dají přilepit tak, že střecha zůstane neporušená."),
  body=[
   (("Čo je potrebné", "Co je potřeba"),
    [("Strešná tesniaca páska Eternabond, univerzálny silikón a stierka. Nič viac. "
      "Flexibilný panel váži okolo dvoch kilogramov, takže nepotrebuje mechanické "
      "uchytenie.",
      "Střešní těsnicí páska Eternabond, univerzální silikon a stěrka. Nic víc. "
      "Flexibilní panel váží kolem dvou kilogramů, takže nepotřebuje mechanické "
      "uchycení.")]),
   (("Orientácia panelov", "Orientace panelů"),
    [("Panely umiestnite radšej pozdĺžne než priečne a do stredu strechy. Zostane vám "
      "priestor po stranách na strešné okno, ventiláciu alebo ďalší panel neskôr.",
      "Panely umístěte raději podélně než příčně a doprostřed střechy. Zůstane vám "
      "prostor po stranách na střešní okno, ventilaci nebo další panel později."),
     ("Nechajte medzi panelmi aj okolo nich niekoľko centimetrov. Voda tak má kadiaľ "
      "odtiecť a pod panelmi sa nedrží nečistota.",
      "Nechte mezi panely i kolem nich několik centimetrů. Voda tak má kudy "
      "odtéct a pod panely se nedrží nečistota.")]),
   (("Prečo bez vŕtania", "Proč bez vrtání"),
    [("Každý otvor v streche je miesto, ktoré môže začať zatekať — a pri obytnej "
      "vstavbe je to najdrahšia možná porucha. Lepený spoj s poriadnou páskou drží "
      "roky a strechu neoslabí.",
      "Každý otvor ve střeše je místo, které může začít zatékat — a u obytné "
      "vestavby je to nejdražší možná porucha. Lepený spoj s pořádnou páskou drží "
      "roky a střechu neoslabí.")]),
  ]),

 dict(
  slug="pwm-alebo-mppt-regulator",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/lensun-40a-waterproof-mppt-solar-controller-01.jpg",
  date="2026-06-03",
  source=SRC + "solar-technology-information/which-type-of-solar-charge-controller-is-the-best-choice-for-your-solar-system-whats-different-between-pwm-controller-and-mppt-controller",
  product=None,
  cat="technika",
  title=("PWM alebo MPPT? Rozdiel je až 30 % energie",
         "PWM nebo MPPT? Rozdíl je až 30 % energie"),
  lead=("Regulátor nabíjania je povinná súčasť každej zostavy. Vybrať sa dá z dvoch "
        "technológií a rozdiel medzi nimi nie je len v cene.",
        "Regulátor nabíjení je povinná součást každé sestavy. Vybrat se dá ze dvou "
        "technologií a rozdíl mezi nimi není jen v ceně."),
  body=[
   (("Prečo regulátor vôbec potrebujete", "Proč regulátor vůbec potřebujete"),
    [("Panel označený ako dvanásťvoltový dáva naprázdno 16 až 21 V. Batéria potrebuje "
      "na plné nabitie 13 až 14,5 V. Bez regulátora by ju panel prebíjal a zničil.",
      "Panel označený jako dvanáctivoltový dává naprázdno 16 až 21 V. Baterie potřebuje "
      "k plnému nabití 13 až 14,5 V. Bez regulátoru by ji panel přebíjel a zničil.")]),
   (("PWM: jednoduchý spínač", "PWM: jednoduchý spínač"),
    [("PWM regulátor je v podstate rýchly spínač, ktorý panel pripája k batérii v "
      "krátkych impulzoch. Napätie panela sa tým stiahne na napätie batérie.",
      "PWM regulátor je v podstatě rychlý spínač, který panel připojuje k baterii v "
      "krátkých impulzech. Napětí panelu se tím stáhne na napětí baterie."),
     ("Príklad: stowattový panel s údajmi 18 V a 5,56 A dodá do batérie 5,56 A pri "
      "12 V, teda asi 66 W. Zvyšných 34 W sa jednoducho nevyužije.",
      "Příklad: stowattový panel s údaji 18 V a 5,56 A dodá do baterie 5,56 A při "
      "12 V, tedy asi 66 W. Zbylých 34 W se prostě nevyužije.")]),
   (("MPPT: hľadá bod maximálneho výkonu", "MPPT: hledá bod maximálního výkonu"),
    [("MPPT regulátor priebežne mení vstupné napätie tak, aby z panela vytiahol čo "
      "najviac, a potom prebytočné napätie premení na prúd. Z toho istého "
      "stowattového panela dostanete okolo 16,7 A pri 12 V.",
      "MPPT regulátor průběžně mění vstupní napětí tak, aby z panelu vytáhl co "
      "nejvíc, a potom přebytečné napětí promění na proud. Ze stejného "
      "stowattového panelu dostanete kolem 16,7 A při 12 V."),
     ("Zisk oproti PWM je 10 až 40 %. Najväčší je pri nízkych teplotách článkov "
      "(pod 45 °C), pri veľmi vysokých (nad 75 °C) a pri slabom osvetlení — teda "
      "presne v našich zimných a jesenných podmienkach.",
      "Zisk oproti PWM je 10 až 40 %. Největší je při nízkých teplotách článků "
      "(pod 45 °C), při velmi vysokých (nad 75 °C) a při slabém osvětlení — tedy "
      "přesně v našich zimních a podzimních podmínkách.")]),
   (("Ktorý si teda vybrať", "Který si tedy vybrat"),
    [("Do zostáv približne do 150 W je PWM regulátor rozumné a lacné riešenie. Nad "
      "150 až 200 W sa MPPT zaplatí sám tým, čo navyše vyrobí.",
      "Do sestav přibližně do 150 W je PWM regulátor rozumné a levné řešení. Nad "
      "150 až 200 W se MPPT zaplatí sám tím, co navíc vyrobí."),
     ("MPPT má ešte jednu výhodu: znesie na vstupe vyššie napätie, takže panely "
      "môžete zapojiť do série. Vyššie napätie znamená nižší prúd a tenší, lacnejší "
      "kábel pri rovnakých stratách.",
      "MPPT má ještě jednu výhodu: snese na vstupu vyšší napětí, takže panely "
      "můžete zapojit do série. Vyšší napětí znamená nižší proud a tenčí, levnější "
      "kabel při stejných ztrátách.")]),
  ]),

 dict(
  slug="chyby-pri-lepeni-flexibilneho-panela",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/800-lensunsolar-200w-flexible-solar-panel-5.jpg",
  date="2026-08-05",
  source=SRC + "solar-technology-information/you-should-know-before-installing-flexible-solar-panels-a-number-of-important-considerations",
  product=None,
  cat="technika",
  title=("Deväť chýb, ktoré zabijú flexibilný panel",
         "Devět chyb, které zabijí flexibilní panel"),
  lead=("Flexibilné panely majú povesť nespoľahlivých. Väčšinou za to nemôže panel, "
        "ale spôsob, akým bol namontovaný.",
        "Flexibilní panely mají pověst nespolehlivých. Většinou za to nemůže panel, "
        "ale způsob, jakým byl namontovaný."),
  body=[
   (("Podklad musí byť pevný", "Podklad musí být pevný"),
    [("Plocha, na ktorú panel lepíte, sa nesmie prehýbať vo vetre, pod snehom ani pri "
      "jazde. Opakované ohýbanie podkladu prenáša pnutie do článkov a spojov — to je "
      "najčastejšia príčina toho, že panel po roku prestane dodávať výkon.",
      "Plocha, na kterou panel lepíte, se nesmí prohýbat ve větru, pod sněhem ani při "
      "jízdě. Opakované ohýbání podkladu přenáší pnutí do článků a spojů — to je "
      "nejčastější příčina toho, že panel po roce přestane dodávat výkon.")]),
   (("Ohýbajte len von a len keď treba", "Ohýbejte jen ven a jen když je třeba"),
    [("Mierne prehnutie do oblúka strechy je hlavná výhoda flexibilného panela. "
      "Platia však dve pravidlá: ohýbať len smerom dozadu, nikdy dovnútra, a hĺbka "
      "prehnutia nesmie presiahnuť 20 % dĺžky panela.",
      "Mírné prohnutí do oblouku střechy je hlavní výhoda flexibilního panelu. "
      "Platí však dvě pravidla: ohýbat jen směrem dozadu, nikdy dovnitř, a hloubka "
      "prohnutí nesmí přesáhnout 20 % délky panelu."),
     ("Videá, na ktorých niekto panel skrúti do U, urobili flexibilným panelom zlé "
      "meno. Takto poškodený panel nezlyhá hneď — rozpadne sa o pár mesiacov neskôr.",
      "Videa, na kterých někdo panel zkroutí do U, udělala flexibilním panelům špatné "
      "jméno. Takto poškozený panel neselže hned — rozpadne se o pár měsíců později.")]),
   (("Manipulácia pred montážou", "Manipulace před montáží"),
    [("Nenoste panel na hlave ani pod pazuchou, nepokladajte naň predmety a nikdy "
      "naň nestúpajte. Aj bežné nadhadzovanie pri prenášaní dokáže v článkoch "
      "vytvoriť mikrotrhliny, ktoré nie sú vidieť.",
      "Nenoste panel na hlavě ani pod paží, nepokládejte na něj předměty a nikdy "
      "na něj nestoupejte. I běžné nadhazování při přenášení dokáže v článcích "
      "vytvořit mikrotrhliny, které nejsou vidět."),
     ("Panel nechajte v originálnom obale až do chvíle montáže.",
      "Panel nechte v originálním obalu až do chvíle montáže.")]),
   (("Lepiť, nie vŕtať", "Lepit, ne vrtat"),
    [("Ak to povrch dovolí, je lepené uchytenie páskou 3M VHB alebo tmelom Sikaflex "
      "lepšie než skrutky s otvormi. Otvory oslabujú konštrukciu panela aj podklad.",
      "Pokud to povrch dovolí, je lepené uchycení páskou 3M VHB nebo tmelem Sikaflex "
      "lepší než šrouby s otvory. Otvory oslabují konstrukci panelu i podklad.")]),
   (("Elektrická bezpečnosť pri montáži", "Elektrická bezpečnost při montáži"),
    [("Panel vyrába prúd vždy, keď naň svieti svetlo — aj počas montáže. Pred "
      "zapájaním ho zakryte nepriehľadnou látkou, nedotýkajte sa svoriek a používajte "
      "izolované náradie a rukavice.",
      "Panel vyrábí proud vždy, když na něj svítí světlo — i během montáže. Před "
      "zapojováním ho zakryjte neprůhlednou látkou, nedotýkejte se svorek a používejte "
      "izolované nářadí a rukavice.")]),
   (("A nakoniec", "A nakonec"),
    [("Panel nerozoberajte, neodstraňujte z neho štítky, nemaľujte ho a nesmerujte "
      "naň sústredené slnečné svetlo napríklad zrkadlom.",
      "Panel nerozebírejte, neodstraňujte z něj štítky, nemalujte ho a nesměrujte "
      "na něj soustředěné sluneční světlo například zrcadlem.")]),
  ]),

 dict(
  slug="panely-do-serie-alebo-paralelne",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/LensunSolar-150W-Flexible-Solar-Panel-System-Connection-Diagram.jpg",
  date="2026-08-19",
  source=SRC + "solar-panel-installation/how-to-connect-12v-solar-panels-together",
  product=None,
  cat="technika",
  title=("Dva panely: do série alebo paralelne?",
         "Dva panely: do série nebo paralelně?"),
  lead=("Keď pridávate druhý panel, máte dve možnosti zapojenia. Jedna zvýši napätie, "
        "druhá prúd — a od toho závisí aj voľba regulátora a hrúbka kábla.",
        "Když přidáváte druhý panel, máte dvě možnosti zapojení. Jedna zvýší napětí, "
        "druhá proud — a od toho závisí i volba regulátoru a tloušťka kabelu."),
  body=[
   (("Paralelné zapojenie: pripočíta prúd", "Paralelní zapojení: přičte proud"),
    [("Spojíte všetky plusové vývody dohromady a všetky mínusové dohromady. Napätie "
      "zostane rovnaké, prúdy sa sčítajú.",
      "Spojíte všechny plusové vývody dohromady a všechny minusové dohromady. Napětí "
      "zůstane stejné, proudy se sčítají."),
     ("Štyri panely 12 V / 5 A zapojené paralelne dajú 12 V a 20 A. Výhodou je, že "
      "keď jeden panel zatieni strom, ostatné pracujú ďalej.",
      "Čtyři panely 12 V / 5 A zapojené paralelně dají 12 V a 20 A. Výhodou je, že "
      "když jeden panel zastíní strom, ostatní pracují dál.")]),
   (("Sériové zapojenie: pripočíta napätie", "Sériové zapojení: přičte napětí"),
    [("Plus prvého panela spojíte s mínusom druhého a tak ďalej. Napätia sa sčítajú, "
      "prúd zostáva rovnaký ako z jedného panela.",
      "Plus prvního panelu spojíte s minusem druhého a tak dále. Napětí se sčítají, "
      "proud zůstává stejný jako z jednoho panelu."),
     ("Tie isté štyri panely dajú v sérii 48 V a 5 A. Sériový obvod má však jednu "
      "cestu — keď jeden panel zatieni, klesne výkon celej vetvy.",
      "Tytéž čtyři panely dají v sérii 48 V a 5 A. Sériový obvod má však jednu "
      "cestu — když jeden panel zastíní, klesne výkon celé větve.")]),
   (("Prakticky: čo si vybrať", "Prakticky: co si vybrat"),
    [("Na aute a v karavane s PWM regulátorom voľte paralelné zapojenie — napätie "
      "musí zodpovedať batérii a čiastočné tienenie je bežné.",
      "Na autě a v karavanu s PWM regulátorem volte paralelní zapojení — napětí "
      "musí odpovídat baterii a částečné zastínění je běžné."),
     ("Sériové zapojenie má zmysel s MPPT regulátorom pri dlhšej kabeláži. Straty vo "
      "vedení rastú s druhou mocninou prúdu, takže dvojnásobné napätie umožní použiť "
      "štvornásobne tenší vodič pri rovnakých stratách.",
      "Sériové zapojení má smysl s MPPT regulátorem při delší kabeláži. Ztráty ve "
      "vedení rostou s druhou mocninou proudu, takže dvojnásobné napětí umožní použít "
      "čtyřnásobně tenčí vodič při stejných ztrátách.")]),
   (("Zásada, na ktorú sa zabúda", "Zásada, na kterou se zapomíná"),
    [("Do jednej vetvy spájajte len panely s rovnakými parametrami. Panel s nižším "
      "prúdom v sérii stiahne celú vetvu na svoju hodnotu, panel s nižším napätím "
      "paralelne odoberá z ostatných.",
      "Do jedné větve spojujte jen panely se stejnými parametry. Panel s nižším "
      "proudem v sérii stáhne celou větev na svoji hodnotu, panel s nižším napětím "
      "paralelně odebírá z ostatních.")]),
  ]),
 dict(
  slug="toyota-land-cruiser-80-90w",
  video="qugwHNNU41o",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Toyota_LandCruiser_80_Series_J80_Fz80_Lensun_90W_Hood_Flexible_Solar_Panel-1.jpg",
  date="2026-04-15",
  source=SRC + "hood-solar-panel/is-it-any-good-lensun-90w-hood-mounted-solar-panel-kit-for-lc80-cruisinmiles-review",
  product="toyota-land-cruiser-80series-j80-lensun-90w-hood-bonnet-solar-panel",
  cat="kapota",
  title=("Land Cruiser 80: keď alternátor na AGM batériu nestačí",
         "Land Cruiser 80: když alternátor na AGM baterii nestačí"),
  lead=("Rok a pol prevádzky na J80. Zaujímavý je dôvod, prečo panel na tomto aute "
        "urobil väčší rozdiel než na modernejších vozidlách.",
        "Rok a půl provozu na J80. Zajímavý je důvod, proč panel na tomto autě "
        "udělal větší rozdíl než na modernějších vozidlech."),
  body=[
   (("Slabina osemdesiatky", "Slabina osmdesátky"),
    [("Sériový alternátor Land Cruisera 80 dáva 80 A. Na dobíjanie AGM batérie to "
      "vyzerá ako dosť, lenže AGM potrebuje na plné nabitie vyššie napätie a dlhší "
      "čas, než mu bežná jazda dopraje. Batéria sa preto zastaví okolo 90 % kapacity.",
      "Sériový alternátor Land Cruiseru 80 dává 80 A. Na dobíjení AGM baterie to "
      "vypadá jako dost, jenže AGM potřebuje k plnému nabití vyšší napětí a delší "
      "čas, než mu běžná jízda dopřeje. Baterie se proto zastaví kolem 90 % kapacity."),
     ("Panel s MPPT regulátorom dotiahne posledných desať percent tam, kde na to "
      "alternátor nemá čas. Rozdiel medzi 90 a 100 % pritom rozhoduje o životnosti "
      "AGM batérie — nedobitá AGM sulfatuje.",
      "Panel s MPPT regulátorem dotáhne posledních deset procent tam, kde na to "
      "alternátor nemá čas. Rozdíl mezi 90 a 100 % přitom rozhoduje o životnosti "
      "AGM baterie — nedobitá AGM sulfatuje.")]),
   (("Čo je v zostave", "Co je v sestavě"),
    [("Panel, vinylová fólia na ochranu laku a MPPT regulátor. Regulátor sám "
      "rozhoduje, kam energiu pošle, a po dosiahnutí plného nabitia panel odpojí.",
      "Panel, vinylová fólie na ochranu laku a MPPT regulátor. Regulátor sám "
      "rozhoduje, kam energii pošle, a po dosažení plného nabití panel odpojí."),
     ("Regulátor komunikuje cez bluetooth s aplikáciou, takže stav batérie aj "
      "okamžitý výkon panela vidíte v telefóne. Sústava sa dá neskôr rozšíriť o "
      "druhý panel a druhú batériu.",
      "Regulátor komunikuje přes bluetooth s aplikací, takže stav baterie i "
      "okamžitý výkon panelu vidíte v telefonu. Soustava se dá později rozšířit o "
      "druhý panel a druhou baterii.")]),
   (("Prečo práve na osemdesiatku sadne", "Proč právě na osmdesátku sedne"),
    [("Kapota J80 je veľká a takmer rovná — panel na nej má kde ležať a nemusí sa "
      "prehýbať. Čierny povrch s ETFE fóliou navyše ladí s karosériou a nepôsobí "
      "ako dodatočný doplnok.",
      "Kapota J80 je velká a téměř rovná — panel na ní má kde ležet a nemusí se "
      "prohýbat. Černý povrch s ETFE fólií navíc ladí s karoserií a nepůsobí "
      "jako dodatečný doplněk.")]),
  ]),

 dict(
  slug="mercedes-g-wagen-135w",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Mercedes-Benz-G-Wagen-G-Class-Lensun-135W-Hood-Bonnet-Flexible-Solar-Panel.jpg",
  date="2026-07-29",
  source=SRC + "hood-solar-panel/real-g-wagen-owners-share-why-the-lensun-135w-hood-solar-panel-changed-their-overlanding-game-1",
  product="mercedes-benz-g-wagen-g-class-lensun-135w-hood-flexible-solar-panel",
  cat="kapota",
  title=("Mercedes G: 135 W a koniec voľnobehu kvôli chladničke",
         "Mercedes G: 135 W a konec volnoběhu kvůli lednici"),
  lead=("Hranatá kapota triedy G je pre solárny panel takmer ideálna plocha. "
        "So 135 W ide o jeden z najvýkonnejších panelov na kapotu v ponuke.",
        "Hranatá kapota třídy G je pro solární panel téměř ideální plocha. "
        "Se 135 W jde o jeden z nejvýkonnějších panelů na kapotu v nabídce."),
  body=[
   (("Parametre", "Parametry"),
    [("Špičkový výkon 135 W, účinnosť článkov 23,5 %, napätie v bode maximálneho "
      "výkonu 16,5 V a prúd 8,18 A. Hmotnosť 3,5 kg, hrúbka 3 mm.",
      "Špičkový výkon 135 W, účinnost článků 23,5 %, napětí v bodě maximálního "
      "výkonu 16,5 V a proud 8,18 A. Hmotnost 3,5 kg, tloušťka 3 mm."),
     ("Panel je tvarovaný pre modely W460 a W463. Prípojná skrinka má krytie IP 68, "
      "takže zimné soľné postreky ani letné búrky jej neuškodia.",
      "Panel je tvarovaný pro modely W460 a W463. Připojovací krabice má krytí IP 68, "
      "takže zimní solné postřiky ani letní bouřky jí neuškodí.")]),
   (("Čo 135 W utiahne", "Co 135 W utáhne"),
    [("Chladnička s odberom 45 až 60 W, LED osvetlenie 15 až 30 W, palubná kamera "
      "v režime nepretržitého záznamu 5 až 10 W, nabíjanie telefónov a tabletov. "
      "Pri dobrom počasí zvýši aj na dobíjanie prenosnej elektrocentrály.",
      "Lednice s odběrem 45 až 60 W, LED osvětlení 15 až 30 W, palubní kamera "
      "v režimu nepřetržitého záznamu 5 až 10 W, nabíjení telefonů a tabletů. "
      "Za dobrého počasí zbude i na dobíjení přenosné elektrocentrály.")]),
   (("Úspora, na ktorú sa zabúda", "Úspora, na kterou se zapomíná"),
    [("Kto nechá motor bežať na voľnobeh, aby udržal chladničku, spáli zhruba dva "
      "až štyri litre nafty za hodinu. Pri dvadsiatich až tridsiatich dňoch v "
      "teréne za rok to nie sú zanedbateľné peniaze.",
      "Kdo nechá motor běžet na volnoběh, aby udržel lednici, spálí zhruba dva "
      "až čtyři litry nafty za hodinu. Při dvaceti až třiceti dnech v terénu "
      "za rok to nejsou zanedbatelné peníze."),
     ("Voľnobeh navyše opotrebúva motor viac, než zodpovedá prejdenej vzdialenosti "
      "— filter pevných častíc pri nízkych otáčkach nemá ako regenerovať.",
      "Volnoběh navíc opotřebovává motor víc, než odpovídá ujeté vzdálenosti "
      "— filtr pevných částic při nízkých otáčkách nemá jak regenerovat.")]),
   (("Montáž", "Montáž"),
    [("Podľa majiteľov trvá montáž hodinu až dve. Kapotu treba dôkladne vyčistiť, "
      "priložiť ochrannú fóliu, umiestniť panel a zapojiť predpripravenú kabeláž "
      "s poistkami a konektormi.",
      "Podle majitelů trvá montáž hodinu až dvě. Kapotu je třeba důkladně vyčistit, "
      "přiložit ochrannou fólii, umístit panel a zapojit předpřipravenou kabeláž "
      "s pojistkami a konektory.")]),
  ]),

 dict(
  slug="range-rover-l322",
  video="oCwL47aFH94",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/Ranger_Rover_L322_2001-2012_Lensun_100W_12V_Hood_Bonnet_Flexible_Solar_Panel-1.jpg",
  date="2026-08-26",
  source=SRC + "solar-panel-review/90w-bonnet-hood-solar-panel-on-range-rover-l322-overlanding-4wd-review",
  product="ranger-rover-l322-lensun-100w-hood-bonnet-flexible-solar-panel",
  cat="kapota",
  title=("Range Rover L322: hodina práce a zopár trikov navyše",
         "Range Rover L322: hodina práce a pár triků navíc"),
  lead=("Montáž na L322 je dobre zdokumentovaná a ukazuje niekoľko detailov, ktoré "
        "v návode nenájdete — od výberu dňa až po medzeru na prúdenie vzduchu.",
        "Montáž na L322 je dobře zdokumentovaná a ukazuje několik detailů, které "
        "v návodu nenajdete — od výběru dne až po mezeru na proudění vzduchu."),
  body=[
   (("Fóliu lepte v zamračený deň", "Fólii lepte v zamračený den"),
    [("Vinylová fólia je o niečo väčšia než panel a musí kopírovať zaoblenie kapoty. "
      "Na priamom slnku sa lepidlo chytí okamžite a fóliu už neposuniete — preto je "
      "lepší zamračený deň alebo tieň haly.",
      "Vinylová fólie je o něco větší než panel a musí kopírovat zaoblení kapoty. "
      "Na přímém slunci se lepidlo chytí okamžitě a fólii už neposunete — proto je "
      "lepší zamračený den nebo stín haly."),
     ("Pomôže mydlová voda: fólia po nej kĺže, dá sa presne usadiť a až potom "
      "vytlačíte vodu stierkou od stredu k okrajom.",
      "Pomůže mýdlová voda: fólie po ní klouže, dá se přesně usadit a až potom "
      "vytlačíte vodu stěrkou od středu k okrajům.")]),
   (("Príprava povrchu rozhoduje", "Příprava povrchu rozhoduje"),
    [("Kapotu umyte a potom prejdite izopropylalkoholom. Vosk, leštenka ani zvyšky "
      "autošampónu na plechu ostať nesmú — na nich páska VHB nedrží.",
      "Kapotu umyjte a potom přejděte izopropylalkoholem. Vosk, leštěnka ani zbytky "
      "autošamponu na plechu zůstat nesmí — na nich páska VHB nedrží."),
     ("Na spoj medzi páskou a vinylovou fóliou sa oplatí použiť aktivačný prípravok "
      "3M. Je to drobnosť za pár eur, ktorá výrazne zvýši pevnosť lepenia.",
      "Na spoj mezi páskou a vinylovou fólií se vyplatí použít aktivační přípravek "
      "3M. Je to drobnost za pár eur, která výrazně zvýší pevnost lepení.")]),
   (("Nechajte pod panelom prúdiť vzduch", "Nechte pod panelem proudit vzduch"),
    [("Páska VHB sa nedáva po celej ploche, ale do pruhov. Panel tak zostane mierne "
      "nadvihnutý a pod ním prúdi vzduch, ktorý ho chladí. Chladnejší článok má "
      "vyššiu účinnosť.",
      "Páska VHB se nedává po celé ploše, ale do pruhů. Panel tak zůstane mírně "
      "nadzvednutý a pod ním proudí vzduch, který ho chladí. Chladnější článek má "
      "vyšší účinnost.")]),
   (("Kabeláž a regulátor", "Kabeláž a regulátor"),
    [("Regulátor sa uchytí páskou VHB v motorovom priestore, kábel sa vedie cez "
      "existujúci prieduch. Celá montáž trvá zhruba tri štvrte hodiny až hodinu — "
      "a práve na nej sa neoplatí ponáhľať.",
      "Regulátor se uchytí páskou VHB v motorovém prostoru, kabel se vede přes "
      "existující průduch. Celá montáž trvá zhruba tři čtvrtě hodiny až hodinu — "
      "a právě na ní se nevyplatí spěchat."),
     ("Pre L322 máme v katalógu panel s výkonom 100 W. Ďalšie modely Land Rover "
      "vrátane Discovery, Defendera, Freelandera a Range Roveru Sport nájdete "
      "vo filtri podľa značky.",
      "Pro L322 máme v katalogu panel s výkonem 100 W. Další modely Land Rover "
      "včetně Discovery, Defenderu, Freelanderu a Range Roveru Sport najdete "
      "ve filtru podle značky.")]),
  ]),

 dict(
  slug="ako-nalepit-panel-na-kapotu",
  video=None,
  hero="/assets/hood-install.jpg",
  date="2026-09-02",
  source=SRC + "hood-solar-panel/is-it-any-good-lensun-90w-hood-mounted-solar-panel-kit-for-lc80-cruisinmiles-review",
  product=None,
  cat="kapota",
  title=("Postup montáže krok za krokom",
         "Postup montáže krok za krokem"),
  lead=("Panel na kapotu zvládne namontovať aj bežne zručný človek. Celá práca "
        "zaberie hodinu až dve a nepotrebujete na ňu špeciálne náradie.",
        "Panel na kapotu zvládne namontovat i běžně zručný člověk. Celá práce "
        "zabere hodinu až dvě a nepotřebujete na ni speciální nářadí."),
  body=[
   (("Čo si pripravte", "Co si připravte"),
    [("Izopropylalkohol, mikrovláknovú utierku, rozprašovač s mydlovou vodou, "
      "stierku, maliarsku pásku na značenie, príchytky na kábel a nožnice. "
      "Ak montujete v zime, aj teplovzdušnú pištoľ na nahriatie plechu.",
      "Izopropylalkohol, mikrovláknovou utěrku, rozprašovač s mýdlovou vodou, "
      "stěrku, malířskou pásku na značení, příchytky na kabel a nůžky. "
      "Pokud montujete v zimě, také horkovzdušnou pistoli na nahřátí plechu.")]),
   (("1. Rozbaľte a skontrolujte", "1. Rozbalte a zkontrolujte"),
    [("Prejdite si obsah balenia podľa zoznamu — panel, fólia, regulátor, káble, "
      "poistky, konektory. Panel nechajte v obale, kým naň nepríde rad.",
      "Projděte si obsah balení podle seznamu — panel, fólie, regulátor, kabely, "
      "pojistky, konektory. Panel nechte v obalu, dokud na něj nepřijde řada.")]),
   (("2. Vyčistite kapotu", "2. Vyčistěte kapotu"),
    [("Umyte, osušte a nakoniec prejdite izopropylalkoholom. Toto je krok, ktorý "
      "sa najčastejšie odbije — a potom sa panel po pár mesiacoch odlepí.",
      "Umyjte, osušte a nakonec přejděte izopropylalkoholem. Tohle je krok, který "
      "se nejčastěji odbyde — a potom se panel po pár měsících odlepí.")]),
   (("3. Nalepte ochrannú fóliu", "3. Nalepte ochrannou fólii"),
    [("Fóliu usaďte na mydlovú vodu, skontrolujte medzery po obvode a až potom "
      "vytlačte vodu stierkou od stredu von. Fólia chráni lak a pri prípadnej "
      "demontáži uľahčí odstránenie lepidla.",
      "Fólii usaďte na mýdlovou vodu, zkontrolujte mezery po obvodu a až potom "
      "vytlačte vodu stěrkou od středu ven. Fólie chrání lak a při případné "
      "demontáži usnadní odstranění lepidla.")]),
   (("4. Umiestnite a prilepte panel", "4. Umístěte a přilepte panel"),
    [("Polohu si najprv vyznačte maliarskou páskou. Pásku VHB nalepte v pruhoch, "
      "nie po celej ploche — pod panelom má prúdiť vzduch. Potom sťahujte krycí "
      "papier postupne a panel priťahujte od stredu k okrajom.",
      "Polohu si nejprve vyznačte malířskou páskou. Pásku VHB nalepte v pruzích, "
      "ne po celé ploše — pod panelem má proudit vzduch. Potom stahujte krycí "
      "papír postupně a panel přitlačujte od středu k okrajům.")]),
   (("5. Veďte kábel a zapojte", "5. Veďte kabel a zapojte"),
    [("Kábel veďte existujúcim prieduchom do motorového priestoru, uchyťte ho "
      "príchytkami mimo horúcich a pohyblivých častí. Pripojte panel na regulátor "
      "a až potom regulátor na batériu.",
      "Kabel veďte existujícím průduchem do motorového prostoru, uchyťte ho "
      "příchytkami mimo horké a pohyblivé části. Připojte panel na regulátor "
      "a až potom regulátor na baterii."),
     ("Kým zapájate, panel zakryte nepriehľadnou látkou. Na svetle vyrába napätie "
      "a svorky sú pod prúdom.",
      "Dokud zapojujete, panel zakryjte neprůhlednou látkou. Na světle vyrábí napětí "
      "a svorky jsou pod proudem.")]),
   (("Kedy nelepit", "Kdy nelepit"),
    [("Pod 15 °C lepidlo nechytá tak, ako má. Ak nemáte vyhriatu garáž, počkajte "
      "na teplejší deň — alebo nám auto privezte, montáž robíme v Bytči.",
      "Pod 15 °C lepidlo nechytá tak, jak má. Pokud nemáte vytopenou garáž, počkejte "
      "na teplejší den — nebo nám auto přivezte, montáž děláme v Bytči.")]),
  ]),

 dict(
  slug="vw-t4-t5-panely-na-strechu",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/lensunsolar-240w-flexible-solar-panel-1.jpg",
  date="2026-06-17",
  source=SRC + "solar-panel-installation/volkswagen-vw-t4-or-t5-camping-vans-bus-install-flexible-solar-panels-guide-how-many-ways-to-install-the-flexible-solar-panels-on-the-campers-or-caravans-roof",
  product=None,
  cat="montaz",
  title=("VW T4, T5 a T6: štyri spôsoby uchytenia panela",
         "VW T4, T5 a T6: čtyři způsoby uchycení panelu"),
  lead=("Na streche obytnej dodávky sa flexibilný panel dá uchytiť štyrmi spôsobmi. "
        "Líšia sa v tom, či musíte vŕtať a ako ľahko panel neskôr dolu dostanete.",
        "Na střeše obytné dodávky se flexibilní panel dá uchytit čtyřmi způsoby. "
        "Liší se v tom, jestli musíte vrtat a jak snadno panel později dolů dostanete."),
  body=[
   (("1. Skrutky priamo cez oká panela", "1. Šrouby přímo přes oka panelu"),
    [("Najrýchlejšie a najlacnejšie. Znamená to však otvory v streche, ktoré treba "
      "poriadne utesniť — a každý otvor je potenciálne miesto zatekania.",
      "Nejrychlejší a nejlevnější. Znamená to však otvory ve střeše, které je třeba "
      "pořádně utěsnit — a každý otvor je potenciální místo zatékání.")]),
   (("2. Hliníkové profily", "2. Hliníkové profily"),
    [("Panel sa uchytí na profily a tie sa priskrutkujú alebo prilepia na strechu. "
      "Vzniká medzera na prúdenie vzduchu, panel sa menej prehrieva a dá sa "
      "jednoducho demontovať.",
      "Panel se uchytí na profily a ty se přišroubují nebo přilepí na střechu. "
      "Vzniká mezera na proudění vzduchu, panel se méně přehřívá a dá se "
      "jednoduše demontovat."),
     ("Toto je najlepší kompromis, ak vám nevadí o niečo väčšia stavebná výška.",
      "Tohle je nejlepší kompromis, pokud vám nevadí o něco větší stavební výška.")]),
   (("3. Páska VHB priamo na strechu", "3. Páska VHB přímo na střechu"),
    [("Bez vŕtania, bez otvorov. Vyžaduje čistý a rovný povrch a teplotu nad "
      "pätnásť stupňov. Panel drží roky, demontáž je však prácna.",
      "Bez vrtání, bez otvorů. Vyžaduje čistý a rovný povrch a teplotu nad "
      "patnáct stupňů. Panel drží roky, demontáž je však pracná.")]),
   (("4. Lepenie tmelom", "4. Lepení tmelem"),
    [("Sikaflex alebo podobný pružný tmel po obvode panela. Spoj je vodotesný a "
      "znesie aj mierne pnutie strechy. Nevýhodou je dlhší čas vytvrdnutia.",
      "Sikaflex nebo podobný pružný tmel po obvodu panelu. Spoj je vodotěsný a "
      "snese i mírné pnutí střechy. Nevýhodou je delší čas vytvrzení.")]),
   (("Aký výkon na T4 alebo T5", "Jaký výkon na T4 nebo T5"),
    [("Na strechu transportéra sa najčastejšie dávajú panely 50 až 100 W, prípadne "
      "dva vedľa seba. Na zdvíhaciu strechu voľte ľahší a menší panel — nosnosť "
      "zdvíhacieho mechanizmu je obmedzená.",
      "Na střechu transportéru se nejčastěji dávají panely 50 až 100 W, případně "
      "dva vedle sebe. Na zvedací střechu volte lehčí a menší panel — nosnost "
      "zvedacího mechanismu je omezená."),
     ("Ak vám štandardný rozmer nesadne, panel vieme vyrobiť na mieru — vrátane "
      "polohy prípojnej skrinky a dĺžky káblov.",
      "Pokud vám standardní rozměr nesedne, panel umíme vyrobit na míru — včetně "
      "polohy připojovací krabice a délky kabelů.")]),
  ]),

 dict(
  slug="panel-na-strechu-obytneho-auta",
  video="nTP2G3q6f7s",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/LensunSolar-150W-12V-Flexible-Solar-Panel-Installed-on-Roof-Tent.jpg",
  date="2026-08-12",
  source=SRC + "solar-panel-installation/how-to-mount-lensun-100w-etfe-flexible-solar-panel-complete-kit-on-the-roof-of-motorhomes-rvs-campers-or-caravans",
  product=None,
  cat="montaz",
  title=("Sto wattov na streche obytného auta",
         "Sto wattů na střeše obytného auta"),
  lead=("Kompletná zostava so 100 W panelom, regulátorom a káblami sa na strechu "
        "obytného auta či karavanu montuje rovnako ako na dodávku — s pár rozdielmi.",
        "Kompletní sestava se 100W panelem, regulátorem a kabely se na střechu "
        "obytného auta či karavanu montuje stejně jako na dodávku — s pár rozdíly."),
  body=[
   (("Kde panel umiestniť", "Kam panel umístit"),
    [("Strecha karavanu býva plná — strešné okno, ventilácia, anténa, klimatizácia. "
      "Panel dajte tak, aby naň v priebehu dňa nepadal tieň týchto prvkov; aj "
      "čiastočné zatienenie výrazne zníži výkon.",
      "Střecha karavanu bývá plná — střešní okno, ventilace, anténa, klimatizace. "
      "Panel dejte tak, aby na něj v průběhu dne nepadal stín těchto prvků; i "
      "částečné zastínění výrazně sníží výkon."),
     ("Nechajte okolo panela priestor na umytie strechy a odtok vody.",
      "Nechte kolem panelu prostor na umytí střechy a odtok vody.")]),
   (("Prestup káblov cez strechu", "Prostup kabelů přes střechu"),
    [("Použite strešnú káblovú priechodku a utesnite ju tmelom určeným na strešné "
      "plášte. Toto je jediné miesto, kde sa vŕtaniu spravidla nevyhnete — o to "
      "dôkladnejšie ho utesnite.",
      "Použijte střešní kabelovou průchodku a utěsněte ji tmelem určeným na střešní "
      "pláště. Tohle je jediné místo, kde se vrtání zpravidla nevyhnete — o to "
      "důkladněji ho utěsněte.")]),
   (("Regulátor patrí čo najbližšie k batérii", "Regulátor patří co nejblíže k baterii"),
    [("Nie k panelu. Medzi panelom a regulátorom tečie nižší prúd pri vyššom napätí, "
      "medzi regulátorom a batériou naopak — a práve tam sa straty prejavia najviac.",
      "Ne k panelu. Mezi panelem a regulátorem teče nižší proud při vyšším napětí, "
      "mezi regulátorem a baterií naopak — a právě tam se ztráty projeví nejvíc.")]),
   (("Nezabudnite na poistku", "Nezapomeňte na pojistku"),
    [("Medzi regulátor a batériu patrí poistka čo najbližšie k plusovej svorke. "
      "V kompletných zostavách býva súčasťou dodávky.",
      "Mezi regulátor a baterii patří pojistka co nejblíže k plusové svorce. "
      "V kompletních sestavách bývá součástí dodávky.")]),
  ]),

 dict(
  slug="panel-na-stresny-stan",
  video="bB_NPOikh4w",
  hero="https://lensunsolar.com/cdn/shop/articles/img-1743583970744_6a76eda4-f43c-4d9c-b493-b60a6f897734_1024x1024.jpg",
  date="2026-07-15",
  source=SRC + "solar-panel-review/stay-off-grid-longer-lensun-solar-80w-ikamper-skycamp-mini-panel-install-and-review-by-horizon-bound",
  product="lensun-400w-flexible-solar-panel-for-roof-tent",
  cat="prenosne",
  title=("Solárny panel na strešný stan",
         "Solární panel na střešní stan"),
  lead=("Strešný stan zaberie celú strechu a panel už nemá kam. Riešením je nalepiť "
        "ho priamo na škrupinu stanu — plocha, ktorá inak nič nerobí.",
        "Střešní stan zabere celou střechu a panel už nemá kam. Řešením je nalepit "
        "ho přímo na skořepinu stanu — plocha, která jinak nic nedělá."),
  body=[
   (("Prečo práve na stan", "Proč právě na stan"),
    [("Škrupina zloženého strešného stanu je rovná, tvrdá a celý deň na slnku. "
      "Flexibilný panel s hrúbkou tri milimetre na nej takmer nie je vidieť a "
      "nepridá výšku, ktorá by prekážala v garáži.",
      "Skořepina složeného střešního stanu je rovná, tvrdá a celý den na slunci. "
      "Flexibilní panel s tloušťkou tři milimetry na ní téměř není vidět a "
      "nepřidá výšku, která by vadila v garáži."),
     ("Podmienkou je, aby sa škrupina neprehýbala. Mäkký alebo tenký plášť na "
      "lepenie panela nie je vhodný.",
      "Podmínkou je, aby se skořepina neprohýbala. Měkký nebo tenký plášť na "
      "lepení panelu není vhodný.")]),
   (("Postup", "Postup"),
    [("Strechu stanu očistite mikrovláknovou utierkou a izopropylalkoholom. Polohu "
      "vyznačte maliarskou páskou, panel usaďte na obojstrannú pásku a kábel "
      "veďte príchytkami dolu k regulátoru.",
      "Střechu stanu očistěte mikrovláknovou utěrkou a izopropylalkoholem. Polohu "
      "vyznačte malířskou páskou, panel usaďte na oboustrannou pásku a kabel "
      "veďte příchytkami dolů k regulátoru."),
     ("Kábel musí mať vôľu na otváranie a zatváranie stanu. Toto je najčastejšia "
      "chyba — priveľmi napnutý kábel sa po pár otvoreniach preruší.",
      "Kabel musí mít vůli na otevírání a zavírání stanu. Tohle je nejčastější "
      "chyba — příliš napnutý kabel se po pár otevřeních přeruší.")]),
   (("Regulátor s aplikáciou sa hodí", "Regulátor s aplikací se hodí"),
    [("Pri paneli, na ktorý nevidíte, je bluetooth regulátor obzvlášť užitočný. "
      "V telefóne skontrolujete, že panel vyrába, bez toho, aby ste liezli na "
      "strechu.",
      "U panelu, na který nevidíte, je bluetooth regulátor obzvlášť užitečný. "
      "V telefonu zkontrolujete, že panel vyrábí, aniž byste lezli na střechu.")]),
  ]),

 dict(
  slug="solarna-deka-po-dvoch-rokoch",
  video="2Mvw8KzfGNE",
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/lensunsolar-400w-solar-blanket-panel-1.png",
  date="2026-08-30",
  source=SRC + "solar-panel-review/lensun-300w-solar-panel-blanket-wandering-beast-2-year-review",
  product="lensunsolar-400w-36v-solar-blanket-for-24v-battery-or-power-station",
  cat="prenosne",
  title=("Solárna deka po dvoch rokoch používania",
         "Solární deka po dvou letech používání"),
  lead=("Deka nie je len skladací panel v inom obale. Má zmysel presne tam, kde "
        "pevný panel na streche naráža na svoje limity.",
        "Deka není jen skládací panel v jiném obalu. Má smysl přesně tam, kde "
        "pevný panel na střeše naráží na své limity."),
  body=[
   (("Auto môže stáť v tieni", "Auto může stát ve stínu"),
    [("Toto je hlavná výhoda. V lete zaparkujete pod stromom, kde je v aute "
      "znesiteľne, a deku rozložíte o dvadsať metrov ďalej na slnku. Pevný panel "
      "vás núti stáť tam, kde je horúco.",
      "Tohle je hlavní výhoda. V létě zaparkujete pod stromem, kde je v autě "
      "snesitelně, a deku rozložíte o dvacet metrů dál na slunci. Pevný panel "
      "vás nutí stát tam, kde je horko."),
     ("V zime je to naopak: pevný panel zapadne snehom a ľadom, deku vytiahnete "
      "z auta až vtedy, keď svieti slnko.",
      "V zimě je to naopak: pevný panel zapadne sněhem a ledem, deku vytáhnete "
      "z auta až tehdy, když svítí slunce.")]),
   (("Čo utiahne", "Co utáhne"),
    [("Tristowattová deka dodá okolo pätnástich ampérov. To stačí aj na spotrebiče, "
      "ktoré by ste od jedného panela nečakali — teplovzdušnú fritézu alebo "
      "indukčnú platničku cez menič.",
      "Třistawattová deka dodá kolem patnácti ampérů. To stačí i na spotřebiče, "
      "které byste od jednoho panelu nečekali — horkovzdušnou fritézu nebo "
      "indukční plotýnku přes měnič.")]),
   (("Praktické detaily", "Praktické detaily"),
    [("Deka sa zloží na rozmer zhruba 57 × 39 × 7 cm a váži okolo deviatich "
      "kilogramov. Vozí sa vo vnútri auta, takže zostáva čistá a nezvetráva.",
      "Deka se složí na rozměr zhruba 57 × 39 × 7 cm a váží kolem devíti "
      "kilogramů. Vozí se uvnitř auta, takže zůstává čistá a nezvětrává."),
     ("Po dvoch rokoch bežného používania nemal obal viditeľné škrabance. Konektory "
      "Anderson a suchý zips sú tie časti, ktoré sa opotrebujú ako prvé — stojí za "
      "to ich občas prezrieť.",
      "Po dvou letech běžného používání neměl obal viditelné škrábance. Konektory "
      "Anderson a suchý zip jsou ty části, které se opotřebují jako první — stojí za "
      "to je občas prohlédnout.")]),
   (("Deka ako záloha", "Deka jako záloha"),
    [("Aj keď máte panel na kapote alebo na streche, deka sa hodí ako druhý zdroj "
      "s vlastným regulátorom. Keď zlyhá hlavná sústava, máte čím dobiť.",
      "I když máte panel na kapotě nebo na střeše, deka se hodí jako druhý zdroj "
      "s vlastním regulátorem. Když selže hlavní soustava, máte čím dobít.")]),
  ]),

 dict(
  slug="skladaci-panel-na-kempovanie",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/1000-lensunsolar-400w-waterproof-solar-panel-1.jpg",
  date="2026-05-20",
  source=SRC + "solar-panel-review/keep-your-battery-topped-off-on-the-camping-trip-review-of-lensun-100w-foldable-solar-panel",
  product="lensunsolar-400w-waterproof-foldable-solar-panel",
  cat="prenosne",
  title=("Skladací panel: pre karavan a stan",
         "Skládací panel: pro karavan a stan"),
  lead=("Skladací panel je najjednoduchší spôsob, ako mať na dovolenke elektrinu "
        "bez toho, aby ste čokoľvek lepili alebo vŕtali.",
        "Skládací panel je nejjednodušší způsob, jak mít na dovolené elektřinu "
        "bez toho, abyste cokoli lepili nebo vrtali."),
  body=[
   (("Pre koho má zmysel", "Pro koho má smysl"),
    [("Pre toho, kto stojí niekoľko dní na jednom mieste — obytný príves, kemping "
      "so stanom, chata bez prípojky. Panel ráno rozložíte, natočíte za slnkom a "
      "večer zložíte späť do obalu.",
      "Pro toho, kdo stojí několik dní na jednom místě — obytný přívěs, kempování "
      "se stanem, chata bez přípojky. Panel ráno rozložíte, natočíte za sluncem a "
      "večer složíte zpátky do obalu."),
     ("Ak sa každý deň presúvate, bude vás rozkladanie a skladanie otravovať — "
      "tam je lepší panel na kapote.",
      "Pokud se každý den přesouváte, bude vás rozkládání a skládání otravovat — "
      "tam je lepší panel na kapotě.")]),
   (("Typické parametre", "Typické parametry"),
    [("Stowattový skladací panel má rozložený rozmer okolo 130 × 57 cm, zložený "
      "58 × 44 × 6 cm a váži necelé štyri kilogramy. Pracovné napätie 18 V, "
      "prúd 5,56 A, účinnosť článkov okolo 21 %.",
      "Stowattový skládací panel má rozložený rozměr kolem 130 × 57 cm, složený "
      "58 × 44 × 6 cm a váží necelé čtyři kilogramy. Pracovní napětí 18 V, "
      "proud 5,56 A, účinnost článků kolem 21 %.")]),
   (("Čo býva v balení", "Co bývá v balení"),
    [("Panel, regulátor, päťmetrový kábel s konektormi Anderson a krátky kábel s "
      "krokosvorkami na priame pripojenie k batérii. Niektoré modely majú aj "
      "USB výstupy priamo na paneli.",
      "Panel, regulátor, pětimetrový kabel s konektory Anderson a krátký kabel s "
      "krokosvorkami na přímé připojení k baterii. Některé modely mají i "
      "USB výstupy přímo na panelu.")]),
   (("Na čo si dať pozor pri kúpe", "Na co si dát pozor při koupi"),
    [("Lacné skladacie panely s látkovým povrchom po jednej sezóne blednú a "
      "krivia sa. Rozdiel je v povrchovej fólii — ETFE laminát znesie UV žiarenie "
      "podstatne lepšie než mäkká PET vrstva.",
      "Levné skládací panely s látkovým povrchem po jedné sezoně blednou a "
      "kroutí se. Rozdíl je v povrchové fólii — ETFE laminát snese UV záření "
      "podstatně lépe než měkká PET vrstva.")]),
  ]),

 dict(
  slug="perc-clanky",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/lensun-back-contact-solar-cell.jpg",
  date="2026-04-29",
  source=SRC + "solar-technology-information/whats-perc-solar-cells-whats-the-difference-between-the-standard-and-perc-solar-cells",
  product=None,
  cat="technika",
  title=("Čo znamená PERC na štítku panela",
         "Co znamená PERC na štítku panelu"),
  lead=("Skratka PERC sa objavuje v parametroch takmer každého kvalitného panela. "
        "Ide o jednu vrstvu navyše, ktorá zvýši účinnosť o niekoľko percent.",
        "Zkratka PERC se objevuje v parametrech téměř každého kvalitního panelu. "
        "Jde o jednu vrstvu navíc, která zvýší účinnost o několik procent."),
  body=[
   (("Ako vyzerá bežný článok", "Jak vypadá běžný článek"),
    [("Klasický kryštalický článok má zhora nadol strieborné kontakty, "
      "antireflexnú vrstvu, kremíkovú doštičku s prechodom P-N a na zadnej strane "
      "hliníkovú vrstvu. Táto stavba sa používa vyše tridsať rokov.",
      "Klasický krystalický článek má shora dolů stříbrné kontakty, "
      "antireflexní vrstvu, křemíkovou destičku s přechodem P-N a na zadní straně "
      "hliníkovou vrstvu. Tato stavba se používá přes třicet let.")]),
   (("Čo pridáva PERC", "Co přidává PERC"),
    [("PERC znamená pasivovaný emitor a zadná strana článku. Medzi kremík a zadnú "
      "hliníkovú vrstvu pribudne dielektrická pasivačná vrstva. Tá robí tri veci "
      "naraz.",
      "PERC znamená pasivovaný emitor a zadní strana článku. Mezi křemík a zadní "
      "hliníkovou vrstvu přibude dielektrická pasivační vrstva. Ta dělá tři věci "
      "najednou."),
     ("Po prvé obmedzí rekombináciu elektrónov, ktorá inak bráni ich voľnému toku. "
      "Po druhé odrazí neabsorbované svetlo späť do článku na druhý pokus. Po "
      "tretie vypustí von vlnové dĺžky, ktoré by článok len zohrievali.",
      "Zaprvé omezí rekombinaci elektronů, která jinak brání jejich volnému toku. "
      "Zadruhé odrazí neabsorbované světlo zpět do článku na druhý pokus. "
      "Zatřetí vypustí ven vlnové délky, které by článek jen zahřívaly.")]),
   (("Čo z toho máte", "Co z toho máte"),
    [("Účinnosť okolo 21,5 až 22,5 % namiesto zhruba 19 % u bežných článkov. Pri "
      "rovnakej ploche kapoty to znamená o desatinu až pätinu vyšší výkon.",
      "Účinnost kolem 21,5 až 22,5 % místo zhruba 19 % u běžných článků. Při "
      "stejné ploše kapoty to znamená o desetinu až pětinu vyšší výkon."),
     ("Tretí bod — odvod tepla — je pri paneli na kapote obzvlášť užitočný. "
      "Chladnejší článok má vyššiu účinnosť a dlhšiu životnosť.",
      "Třetí bod — odvod tepla — je u panelu na kapotě obzvlášť užitečný. "
      "Chladnější článek má vyšší účinnost a delší životnost.")]),
   (("Čo znamená 5BB", "Co znamená 5BB"),
    [("Údaj 4BB alebo 5BB hovorí o počte zberných pásikov na článku. Viac pásikov "
      "znamená kratšiu cestu pre elektróny, nižšie odporové straty a menšiu "
      "citlivosť na mikrotrhliny.",
      "Údaj 4BB nebo 5BB říká o počtu sběrných pásků na článku. Více pásků "
      "znamená kratší cestu pro elektrony, nižší odporové ztráty a menší "
      "citlivost na mikrotrhliny.")]),
  ]),

 dict(
  slug="druha-bateria-a-solar",
  video=None,
  hero="https://cdn.shopify.com/s/files/1/0595/2156/4737/files/lensunsolar-20a-waterproof-mppt-solar-controller-01.jpg",
  date="2026-09-01",
  source=SRC + "solar-panel-installation/how-do-you-set-your-offroad-overland-vehicles-solar-system-why-you-need-solar-powered",
  product=None,
  cat="technika",
  title=("Druhá batéria v aute a prečo k nej patrí solár",
         "Druhá baterie v autě a proč k ní patří solár"),
  lead=("Bez solárneho panela je druhá batéria v modernom aute z veľkej časti "
        "zbytočná. Dôvodom je inteligentný alternátor.",
        "Bez solárního panelu je druhá baterie v moderním autě z velké části "
        "zbytečná. Důvodem je inteligentní alternátor."),
  body=[
   (("Prečo samotné prepojenie batérií nefunguje", "Proč samotné propojení baterií nefunguje"),
    [("Najjednoduchšie riešenie — spojiť obe batérie a nechať to na alternátor — "
      "v starých autách fungovalo. V moderných nie: inteligentný alternátor vidí "
      "len prednú batériu, a keď je plná, obe považuje za nabité.",
      "Nejjednodušší řešení — spojit obě baterie a nechat to na alternátor — "
      "ve starých autech fungovalo. V moderních ne: inteligentní alternátor vidí "
      "jen přední baterii, a když je plná, obě považuje za nabité."),
     ("Zadná batéria potom dostáva len udržiavací prúd a postupne odchádza. "
      "Oddeľovač batérií tento problém nerieši, len ho posunie.",
      "Zadní baterie potom dostává jen udržovací proud a postupně odchází. "
      "Oddělovač baterií tento problém neřeší, jen ho posune.")]),
   (("Správna zostava", "Správná sestava"),
    [("Nabíjačka DC-DC medzi štartovacou a druhou batériou. Zvýši napätie na "
      "hodnotu, ktorú druhá batéria naozaj potrebuje, a od štartovacej ju "
      "elektricky oddelí.",
      "Nabíječka DC-DC mezi startovací a druhou baterií. Zvýší napětí na "
      "hodnotu, kterou druhá baterie skutečně potřebuje, a od startovací ji "
      "elektricky oddělí."),
     ("Solárny panel sa pripája na tú istú nabíjačku alebo na vlastný regulátor. "
      "Alternátor nabíja počas jazdy, panel počas státia — a to je väčšina času, "
      "keď auto stojí v kempe.",
      "Solární panel se připojuje na tutéž nabíječku nebo na vlastní regulátor. "
      "Alternátor nabíjí za jízdy, panel při stání — a to je většina času, "
      "kdy auto stojí v kempu.")]),
   (("Koľko wattov naozaj potrebujete", "Kolik wattů skutečně potřebujete"),
    [("Chladnička s odberom päť ampérov pri dvanástich voltoch spotrebuje pri "
      "polovičnom chode zhruba 700 Wh za deň. Aby ste to v našich šírkach pokryli, "
      "počítajte v lete so zhruba 200 W panelov, na jar a jeseň s dvojnásobkom.",
      "Lednice s odběrem pět ampérů při dvanácti voltech spotřebuje při "
      "polovičním chodu zhruba 700 Wh za den. Abyste to v našich šířkách pokryli, "
      "počítejte v létě se zhruba 200 W panelů, na jaře a na podzim s dvojnásobkem."),
     ("V praxi sa preto kombinuje pevný panel na kapote alebo streche s dekou "
      "alebo skladacím panelom, ktorý rozložíte, keď je horúco a chladnička "
      "beží častejšie.",
      "V praxi se proto kombinuje pevný panel na kapotě nebo střeše s dekou "
      "nebo skládacím panelem, který rozložíte, když je horko a lednice "
      "běží častěji.")]),
   (("Batéria musí odber uniesť", "Baterie musí odběr unést"),
    [("Kapacitu druhej batérie voľte podľa nočnej spotreby, nie podľa výkonu "
      "panelov. Osemdesiatampérhodinová batéria pokryje chladničku, osvetlenie a "
      "nabíjanie drobnej elektroniky cez noc s rezervou.",
      "Kapacitu druhé baterie volte podle noční spotřeby, ne podle výkonu "
      "panelů. Osmdesátiampérhodinová baterie pokryje lednici, osvětlení a "
      "nabíjení drobné elektroniky přes noc s rezervou.")]),
  ]),
]


def T(sk, cs, lang):
    return sk if lang == "sk" else cs

def _i(pair, lang):
    return pair[0] if lang == "sk" else pair[1]


def _card(p, lang, base):
    """Jedna karta článku — používa ju prehľad aj domovská stránka."""
    return (
            f'<a class="post" data-cat="{p["cat"]}" href="{base}blog/{p["slug"]}.html">'
            f'<span class="post-img">'
            f'<img loading="lazy" decoding="async" src="{p["hero"]}?width=760" alt="">'
            + ('<span class="post-play" aria-hidden="true">'
               '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>'
               if p["video"] else "") +
            f'</span>'
            f'<span class="post-b">'
            f'<span class="post-cat">{_i(CAT[p["cat"]], lang)}</span>'
            f'<b>{_i(p["title"], lang)}</b>'
            f'<span class="post-lead">{_i(p["lead"], lang)}</span>'
            f'<time datetime="{p["date"]}">{p["date"]}</time>'
            f'</span></a>')


def newest(n=None):
    """Články od najnovšieho po najstarší."""
    out = sorted(POSTS, key=lambda x: x["date"], reverse=True)
    return out[:n] if n else out


def blog_list(lang, base):
    """Prehľad všetkých článkov s filtrom rubrík."""
    posts = newest()
    cards = "".join(_card(p, lang, base) for p in posts)

    chips = ['<button class="chip" type="button" data-cat="" aria-pressed="true">'
             '%s<b>%d</b></button>' % (T("Všetky", "Všechny", lang), len(posts))]
    for key, name in CATS:
        n = sum(1 for p in posts if p["cat"] == key)
        if not n:
            continue
        chips.append('<button class="chip" type="button" data-cat="%s" aria-pressed="false">'
                     "%s<b>%d</b></button>" % (key, _i(name, lang), n))

    return f'''
<section class="sec"><div class="wrap">
  <p class="lead">{T("Skúsenosti z montáže, technika a praktické rady k solárnym panelom na vozidlách.","Zkušenosti z montáže, technika a praktické rady k solárním panelům na vozidlech.",lang)}</p>
  <div class="chips" id="blogCats" role="group" aria-label="{T("Rubriky","Rubriky",lang)}">{"".join(chips)}</div>
  <div class="posts" id="blogPosts">{cards}</div>
</div></section>
'''


def blog_teaser(lang, base, n=3):
    """Najnovšie články na domovskej stránke."""
    cards = "".join(_card(p, lang, base) for p in newest(n))
    return f'''
<section class="sec"><div class="wrap">
  <div class="sec-head">
    <h2>{T("Z blogu","Z blogu",lang)}</h2>
    <span class="eyebrow">{T("Skúsenosti a technika","Zkušenosti a technika",lang)}</span>
  </div>
  <div class="posts three">{cards}</div>
  <p style="margin-top:26px"><a class="btn ghost" href="{base}blog.html">
    {T("Všetky články","Všechny články",lang)}</a></p>
</div></section>
'''


def blog_post(p, lang, base):
    """Detail článku. base ukazuje na koreň webu (z /blog/ je to ../)."""
    secs = []
    for head, paras in p["body"]:
        ps = "".join(f"<p>{_i(t, lang)}</p>" for t in paras)
        secs.append(f"<h2>{_i(head, lang)}</h2>{ps}")

    video = ""
    if p["video"]:
        video = (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{p["video"]}" '
                 f'title="{_i(p["title"], lang)}" loading="lazy" allowfullscreen '
                 f'allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"></iframe></div>')

    prod = ""
    if p["product"]:
        prod = (f'<aside class="post-cta">'
                f'<b>{T("Produkt z článku","Produkt z článku",lang)}</b>'
                f'<a class="btn" href="{base}produkty.html?q={p["product"]}">'
                f'{T("Zobraziť v katalógu","Zobrazit v katalogu",lang)}</a></aside>')

    src_note = T(
        f'Článok pripravený pre tento web na základe technických údajov a skúseností '
        f'zverejnených na <a href="{p["source"]}" rel="nofollow noopener" target="_blank">lensunsolar.com</a>. '
        f'Video a fotografie pochádzajú z pôvodného článku.',
        f'Článek připravený pro tento web na základě technických údajů a zkušeností '
        f'zveřejněných na <a href="{p["source"]}" rel="nofollow noopener" target="_blank">lensunsolar.com</a>. '
        f'Video a fotografie pocházejí z původního článku.', lang)

    return f'''
<article class="sec"><div class="wrap post-single">
  <figure class="post-hero"><img src="{p["hero"]}?width=1400" alt="{_i(p["title"], lang)}"></figure>
  <div class="prose">
    <p class="lead">{_i(p["lead"], lang)}</p>
    {video}
    {"".join(secs)}
  </div>
  {prod}
  <p class="note post-src">{src_note}</p>
  <p style="margin-top:26px"><a class="btn ghost" href="{base}blog.html">
    {T("Späť na blog","Zpět na blog",lang)}</a></p>
</div></article>
'''

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

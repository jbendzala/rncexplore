# -*- coding: utf-8 -*-
"""Všeobecné obchodné podmienky.

Základ dokumentu poskytol partner zo svojej pôvodnej firmy (azkotol.sk,
Fabrika SK s.r.o.). Všeobecné ustanovenia sú prevzaté, obchodne špecifické
časti sú prepísané na Fabrika SAIL s.r.o. — iný sortiment, iný kraj, iné
platobné a dodacie podmienky.

Miesta označené TODO sú údaje, ktoré poznať nemôžeme a musí ich doplniť
majiteľ. Vykreslia sa ako žltý štítok, aby ich nebolo možné prehliadnuť.
"""

TODO = "\x00TODO\x00"          # nahradí sa žltým štítkom pri vykreslení

EFFECTIVE = "20. 09. 2026"
EFFECTIVE_CS = "20. 09. 2026"


def p(sk, cs):
    return ("p", (sk, cs))


def ul(*items):
    return ("ul", list(items))


# ---------------------------------------------------------------------------
# Jednotlivé články. Text vychádza z podkladu partnera; obchodne špecifické
# pasáže (sortiment, platby, doprava, kraj, GDPR) sú napísané nanovo.
# ---------------------------------------------------------------------------

SECTIONS = [
 (("1. Všeobecné ustanovenia", "1. Všeobecná ustanovení"), [
  p("Týmito všeobecnými obchodnými podmienkami (ďalej aj ako „VOP“) sa riadia "
    "právne vzťahy medzi subjektom <strong class=\"js-company\"></strong>, "
    "<span class=\"js-address\"></span>, IČO: <span class=\"js-ico\"></span>, "
    "DIČ: <span class=\"js-dic\"></span>, zapísaná v Obchodnom "
    "registri " + TODO + ", e-mail <a class=\"js-mail\" href=\"#\"></a>, "
    "tel. č. <a class=\"js-phone\" href=\"#\"></a> (ďalej len „predávajúci“) a každou "
    "osobou, ktorá je kupujúcim tovaru ponúkaného predávajúcim prostredníctvom "
    "internetového obchodu https://www.rncexplore.com/, ktoré vznikajú pri kúpe "
    "uvedeného tovaru.",
    "Těmito všeobecnými obchodními podmínkami (dále také jako „VOP“) se řídí "
    "právní vztahy mezi subjektem <strong class=\"js-company\"></strong>, "
    "<span class=\"js-address\"></span>, IČO: <span class=\"js-ico\"></span>, "
    "DIČ: <span class=\"js-dic\"></span>, zapsaná v Obchodním "
    "rejstříku " + TODO + ", e-mail <a class=\"js-mail\" href=\"#\"></a>, "
    "tel. č. <a class=\"js-phone\" href=\"#\"></a> (dále jen „prodávající“) a každou "
    "osobou, která je kupujícím zboží nabízeného prodávajícím prostřednictvím "
    "internetového obchodu https://www.rncexplore.com/, které vznikají při koupi "
    "uvedeného zboží."),
  p("Orgán dozoru: Inšpektorát SOI pre Žilinský kraj, Predmestská 71, "
    "P. O. BOX B-89, 011 79 Žilina 1, Odbor výkonu dohľadu, "
    "tel. č. 041/763 21 30, 041/724 58 68.",
    "Orgán dozoru: Inšpektorát SOI pre Žilinský kraj, Predmestská 71, "
    "P. O. BOX B-89, 011 79 Žilina 1, Odbor výkonu dohľadu, "
    "tel. č. +421 41/763 21 30. Spotřebitel s bydlištěm v České republice se "
    "může obrátit také na Českou obchodní inspekci, Gorazdova 1969/24, "
    "120 00 Praha 2."),
  p("Kupujúci v kúpnej zmluve, resp. potvrdením v objednávke pristupuje k VOP "
    "a zaväzuje sa riadiť sa nimi. Od týchto VOP je možné sa odchýliť len na "
    "základe písomnej dohody predávajúceho a kupujúceho.",
    "Kupující v kupní smlouvě, resp. potvrzením v objednávce přistupuje k VOP "
    "a zavazuje se řídit se jimi. Od těchto VOP je možné se odchýlit pouze na "
    "základě písemné dohody prodávajícího a kupujícího."),
  p("V prípade, že predávajúci a kupujúci uzatvoria písomnú kúpnu zmluvu, "
    "v ktorej si dohodnú podmienky odchylne od VOP, budú ustanovenia takejto "
    "kúpnej zmluvy uprednostnené pred VOP.",
    "V případě, že prodávající a kupující uzavřou písemnou kupní smlouvu, "
    "ve které si dohodnou podmínky odchylně od VOP, budou ustanovení takové "
    "kupní smlouvy upřednostněna před VOP."),
  p("Právne vzťahy sa riadia právnym poriadkom Slovenskej republiky. Ak má "
    "kupujúci bydlisko v inom členskom štáte Európskej únie, táto voľba práva "
    "ho nezbavuje ochrany, ktorú mu poskytujú kogentné ustanovenia právneho "
    "poriadku štátu jeho obvyklého pobytu.",
    "Právní vztahy se řídí právním řádem Slovenské republiky. Má-li kupující "
    "bydliště v jiném členském státě Evropské unie, tato volba práva jej "
    "nezbavuje ochrany, kterou mu poskytují kogentní ustanovení právního řádu "
    "státu jeho obvyklého pobytu."),
 ]),

 (("2. Vymedzenie základných pojmov", "2. Vymezení základních pojmů"), [
  ul(("„Kupujúci“ je fyzická alebo právnická osoba, ktorá si objednala a zaplatila "
      "za tovar prostredníctvom internetového obchodu https://www.rncexplore.com/.",
      "„Kupující“ je fyzická nebo právnická osoba, která si objednala a zaplatila "
      "za zboží prostřednictvím internetového obchodu https://www.rncexplore.com/."),
     ("„Príjemca“ je fyzická alebo právnická osoba, ktorej má byť objednaný tovar "
      "doručený.",
      "„Příjemce“ je fyzická nebo právnická osoba, které má být objednané zboží "
      "doručeno."),
     ("„Tovar“ je produkt objednaný prostredníctvom internetového obchodu "
      "https://www.rncexplore.com/ — najmä solárne panely tvarované na konkrétne "
      "modely vozidiel, flexibilné, skladacie a prenosné solárne panely, solárne "
      "deky, regulátory nabíjania a súvisiace príslušenstvo.",
      "„Zboží“ je produkt objednaný prostřednictvím internetového obchodu "
      "https://www.rncexplore.com/ — zejména solární panely tvarované na konkrétní "
      "modely vozidel, flexibilní, skládací a přenosné solární panely, solární "
      "deky, regulátory nabíjení a související příslušenství."),
     ("„Tovar na mieru“ je tovar vyrobený alebo upravený podľa osobitných "
      "požiadaviek kupujúceho, najmä panel vyrobený podľa rozmerov konkrétneho "
      "vozidla.",
      "„Zboží na míru“ je zboží vyrobené nebo upravené podle zvláštních "
      "požadavků kupujícího, zejména panel vyrobený podle rozměrů konkrétního "
      "vozidla.")),
 ]),

 (("3. Práva a povinnosti predávajúceho", "3. Práva a povinnosti prodávajícího"), [
  p("Predávajúci je povinný:", "Prodávající je povinen:"),
  ul(("dodať príjemcovi tovar v dohodnutom množstve a kvalite,",
      "dodat příjemci zboží v dohodnutém množství a kvalitě,"),
     ("umožniť príjemcovi nadobudnutie vlastníckeho práva k tovaru,",
      "umožnit příjemci nabytí vlastnického práva ke zboží,"),
     ("odovzdať kupujúcemu doklad o kúpe a potrebnú dokumentáciu k tovaru.",
      "předat kupujícímu doklad o koupi a potřebnou dokumentaci ke zboží.")),
  p("Predávajúci má právo na riadne zaplatenie kúpnej ceny od kupujúceho za "
    "dodaný tovar.",
    "Prodávající má právo na řádné zaplacení kupní ceny od kupujícího za "
    "dodané zboží."),
 ]),

 (("4. Práva a povinnosti kupujúceho", "4. Práva a povinnosti kupujícího"), [
  p("Kupujúci je povinný:", "Kupující je povinen:"),
  ul(("zaplatiť predávajúcemu kúpnu cenu za objednaný tovar,",
      "zaplatit prodávajícímu kupní cenu za objednané zboží,"),
     ("úplne a presne uviesť všetky požadované údaje v objednávke,",
      "úplně a přesně uvést všechny požadované údaje v objednávce,"),
     ("prevziať objednaný tovar.",
      "převzít objednané zboží.")),
  p("Kupujúci má právo na dodanie tovaru príjemcovi špecifikovanému "
    "v objednávke, a to v množstve, akosti, termíne a mieste stanovenom "
    "v objednávke.",
    "Kupující má právo na dodání zboží příjemci specifikovanému "
    "v objednávce, a to v množství, jakosti, termínu a místě stanoveném "
    "v objednávce."),
 ]),

 (("5. Objednávka — uzatvorenie zmluvy", "5. Objednávka — uzavření smlouvy"), [
  p("Kupujúci si vyberie tovar v internetovom obchode, vloží ho do košíka, "
    "vyplní doručovacie a fakturačné údaje a objednávku odošle tlačidlom "
    "„Objednávka zaväzujúca k platbe“. Odoslanie objednávky je spojené "
    "s povinnosťou platby.",
    "Kupující si vybere zboží v internetovém obchodě, vloží je do košíku, "
    "vyplní doručovací a fakturační údaje a objednávku odešle tlačítkem "
    "„Objednávka zavazující k platbě“. Odeslání objednávky je spojeno "
    "s povinností platby."),
  p("Zmluvný vzťah medzi predávajúcim a kupujúcim, ktorý sa považuje v súlade "
    "so zákonom č. 102/2014 Z. z. v znení neskorších predpisov za zmluvu "
    "uzatváranú na diaľku, vzniká potvrdením objednávky zo strany predávajúceho "
    "(e-mailom) kupujúcemu. Predávajúci má povinnosť potvrdiť vznik zmluvného "
    "vzťahu najneskôr do 24 hodín od prijatia objednávky. Automatické oznámenie "
    "o prijatí objednávky sa nepovažuje za jej potvrdenie.",
    "Smluvní vztah mezi prodávajícím a kupujícím, který se považuje za smlouvu "
    "uzavíranou na dálku, vzniká potvrzením objednávky ze strany prodávajícího "
    "(e-mailem) kupujícímu. Prodávající má povinnost potvrdit vznik smluvního "
    "vztahu nejpozději do 24 hodin od přijetí objednávky. Automatické oznámení "
    "o přijetí objednávky se nepovažuje za její potvrzení."),
  p("Spolu s potvrdením objednávky predávajúci zašle kupujúcemu faktúru s QR "
    "kódom na zaplatenie, ktorá obsahuje aj cenu dopravy.",
    "Spolu s potvrzením objednávky prodávající zašle kupujícímu fakturu s QR "
    "kódem k zaplacení, která obsahuje i cenu dopravy."),
  p("Na e-mailovú adresu uvedenú v objednávke budú kupujúcemu v prípade potreby "
    "zasielané všetky ďalšie informácie týkajúce sa objednávky.",
    "Na e-mailovou adresu uvedenou v objednávce budou kupujícímu v případě "
    "potřeby zasílány všechny další informace týkající se objednávky."),
 ]),

 (("6. Stornovanie objednávky a odstúpenie od zmluvy",
   "6. Stornování objednávky a odstoupení od smlouvy"), [
  p("Objednávku je možné bezodplatne stornovať do okamihu jej potvrdenia, a to "
    "zaslaním e-mailu predávajúcemu na <a class=\"js-mail\" href=\"#\"></a>.",
    "Objednávku je možné bezplatně stornovat do okamžiku jejího potvrzení, a to "
    "zasláním e-mailu prodávajícímu na <a class=\"js-mail\" href=\"#\"></a>."),
  p("Predávajúci má právo zrušiť objednávku a od zmluvy odstúpiť, ak z dôvodu "
    "nedostupnosti tovaru ani pri vynaložení všetkého úsilia, ktoré možno od neho "
    "spravodlivo požadovať, nie je schopný dodať tovar kupujúcemu v požadovanej "
    "lehote.",
    "Prodávající má právo zrušit objednávku a od smlouvy odstoupit, pokud "
    "z důvodu nedostupnosti zboží ani při vynaložení veškerého úsilí, které lze "
    "od něj spravedlivě požadovat, není schopen dodat zboží kupujícímu "
    "v požadované lhůtě."),
  p("V prípade už zaplatenej kúpnej ceny alebo jej časti budú finančné "
    "prostriedky vrátené kupujúcemu na ním určený účet do 14 dní od platného "
    "zrušenia objednávky.",
    "V případě již zaplacené kupní ceny nebo její části budou finanční "
    "prostředky vráceny kupujícímu na jím určený účet do 14 dnů od platného "
    "zrušení objednávky."),
  p("Spotrebiteľ má právo odstúpiť od zmluvy bez uvedenia dôvodu do 14 dní odo "
    "dňa prevzatia tovaru (v zmysle zákona č. 102/2014 Z. z. o ochrane "
    "spotrebiteľa pri predaji tovaru alebo poskytovaní služieb na základe zmluvy "
    "uzavretej na diaľku). Spotrebiteľ má právo v rámci tejto lehoty tovar "
    "rozbaliť a odskúšať obdobným spôsobom, ako je obvyklé pri nákupe "
    "v kamennom obchode, a to v rozsahu potrebnom na zistenie povahy, "
    "charakteristík a fungovania tovaru. Spotrebiteľ zodpovedá za zníženie "
    "hodnoty tovaru, ktoré vzniklo zaobchádzaním nad tento rámec.",
    "Spotřebitel má právo odstoupit od smlouvy bez uvedení důvodu do 14 dnů ode "
    "dne převzetí zboží. Spotřebitel má právo v rámci této lhůty zboží "
    "rozbalit a vyzkoušet obdobným způsobem, jako je obvyklé při nákupu "
    "v kamenném obchodě, a to v rozsahu potřebném ke zjištění povahy, "
    "vlastností a funkčnosti zboží. Spotřebitel odpovídá za snížení hodnoty "
    "zboží, které vzniklo zacházením nad tento rámec."),
  p("<strong>Právo na odstúpenie od zmluvy sa neuplatní pri tovare vyrobenom "
    "na mieru</strong> podľa osobitných požiadaviek kupujúceho, najmä pri "
    "paneloch vyrobených podľa rozmerov konkrétneho vozidla, ktoré sú "
    "zhotovené na zákazku a nemožno ich ďalej predať.",
    "<strong>Právo na odstoupení od smlouvy se neuplatní u zboží vyrobeného "
    "na míru</strong> podle zvláštních požadavků kupujícího, zejména u panelů "
    "vyrobených podle rozměrů konkrétního vozidla, které jsou zhotoveny "
    "na zakázku a nelze je dále prodat."),
  p("Odstúpenie od zmluvy oznámi spotrebiteľ predávajúcemu e-mailom na "
    "<a class=\"js-mail\" href=\"#\"></a> alebo poštou na adresu sídla. "
    "Na odstúpenie môže použiť formulár, ktorého vzor je prílohou zákona.",
    "Odstoupení od smlouvy oznámí spotřebitel prodávajícímu e-mailem na "
    "<a class=\"js-mail\" href=\"#\"></a> nebo poštou na adresu sídla. "
    "K odstoupení může použít formulář, jehož vzor je přílohou zákona."),
  p("Ak spotrebiteľ od zmluvy odstúpi, musí na vlastné náklady doručiť tovar "
    "bezpečným spôsobom na adresu <strong class=\"js-company\"></strong>, "
    "<span class=\"js-address\"></span>, a to do 14 dní odo dňa odstúpenia. "
    "Odporúčame zásielku poistiť. Tovar je potrebné zaslať späť so všetkými "
    "dokumentmi, ktoré kupujúci obdržal pri jeho kúpe a prevzatí.",
    "Pokud spotřebitel od smlouvy odstoupí, musí na vlastní náklady doručit "
    "zboží bezpečným způsobem na adresu <strong class=\"js-company\"></strong>, "
    "<span class=\"js-address\"></span>, a to do 14 dnů ode dne odstoupení. "
    "Doporučujeme zásilku pojistit. Zboží je třeba zaslat zpět se všemi "
    "dokumenty, které kupující obdržel při jeho koupi a převzetí."),
 ]),

 (("7. Vrátenie peňazí", "7. Vrácení peněz"), [
  p("Predávajúci vráti zaplatené plnenie za tovar vrátane nákladov na dopravu "
    "v zmysle ust. § 9 ods. 3 zákona č. 102/2014 Z. z. do 14 dní odo dňa "
    "doručenia odstúpenia od zmluvy. Predávajúci nemusí vrátiť peniaze skôr, "
    "ako mu je tovar doručený alebo ako spotrebiteľ preukáže jeho zaslanie; to "
    "neplatí, ak predávajúci navrhol, že si tovar vyzdvihne sám.",
    "Prodávající vrátí zaplacené plnění za zboží včetně nákladů na dopravu "
    "do 14 dnů ode dne doručení odstoupení od smlouvy. Prodávající nemusí "
    "vrátit peníze dříve, než mu je zboží doručeno nebo než spotřebitel prokáže "
    "jeho zaslání; to neplatí, pokud prodávající navrhl, že si zboží vyzvedne "
    "sám."),
  p("Ak si spotrebiteľ zvolil iný než najlacnejší bežný spôsob doručenia, ktorý "
    "predávajúci ponúka, vráti predávajúci náklady na doručenie vo výške "
    "zodpovedajúcej najlacnejšiemu ponúkanému spôsobu.",
    "Pokud si spotřebitel zvolil jiný než nejlevnější běžný způsob doručení, "
    "který prodávající nabízí, vrátí prodávající náklady na doručení ve výši "
    "odpovídající nejlevnějšímu nabízenému způsobu."),
 ]),

 (("8. Dodacie podmienky", "8. Dodací podmínky"), [
  p("Tovar doručujeme výhradne kuriérskou spoločnosťou na adresu uvedenú "
    "v objednávke, na území Slovenskej republiky a Českej republiky. Osobný odber "
    "neponúkame.",
    "Zboží doručujeme výhradně kurýrní společností na adresu uvedenou "
    "v objednávce, na území Slovenské republiky a České republiky. Osobní odběr "
    "nenabízíme."),
  p("Tovar expedujeme po pripísaní platby na náš účet. Obvyklé termíny dodania:",
    "Zboží expedujeme po připsání platby na náš účet. Obvyklé termíny dodání:"),
  ul(("tovar dostupný v našom sklade v Nemecku — do 7 pracovných dní,",
      "zboží dostupné v našem skladu v Německu — do 7 pracovních dnů,"),
     ("tovar, ktorý nie je na sklade v Nemecku a expeduje sa od výrobcu — "
      "do 14 pracovných dní,",
      "zboží, které není skladem v Německu a expeduje se od výrobce — "
      "do 14 pracovních dnů,"),
     ("tovar vyrobený na mieru podľa rozmerov vozidla — termín dohodneme "
      "individuálne pri potvrdení objednávky.",
      "zboží vyrobené na míru podle rozměrů vozidla — termín dohodneme "
      "individuálně při potvrzení objednávky.")),
  p("Ak tovar uvedený v objednávke nie je na sklade, kupujúceho o tom budeme "
    "bezodkladne informovať.",
    "Pokud zboží uvedené v objednávce není skladem, kupujícího o tom budeme "
    "neprodleně informovat."),
  p("Kupujúci je povinný tovar od prepravcu prevziať. Odporúčame skontrolovať "
    "neporušenosť obalu a počet balíkov a v prípade nezrovnalostí bezodkladne "
    "kontaktovať predávajúceho.",
    "Kupující je povinen zboží od přepravce převzít. Doporučujeme zkontrolovat "
    "neporušenost obalu a počet balíků a v případě nesrovnalostí neprodleně "
    "kontaktovat prodávajícího."),
  p("Faktúra a daňový doklad budú doručené e-mailom, prípadne vložené "
    "v zásielke.",
    "Faktura a daňový doklad budou doručeny e-mailem, případně vloženy "
    "v zásilce."),
 ]),

 (("9. Ceny a platobné podmienky", "9. Ceny a platební podmínky"), [
  p("Predávajúci si vyhradzuje právo na zmenu ceny tovaru; to sa však "
    "nevzťahuje na už potvrdené kúpne zmluvy. Kupujúci nemá právo dodatočne sa "
    "dožadovať inej ceny, ako ceny vopred dohodnutej v potvrdenej objednávke.",
    "Prodávající si vyhrazuje právo na změnu ceny zboží; to se však "
    "nevztahuje na již potvrzené kupní smlouvy. Kupující nemá právo dodatečně "
    "se dožadovat jiné ceny, než ceny předem dohodnuté v potvrzené objednávce."),
  p("Predávajúci nie je platiteľom dane z pridanej hodnoty. Ceny uvedené pri "
    "produktoch sú konečné ceny za tovar a nezahŕňajú cenu dopravy.",
    "Prodávající není plátcem daně z přidané hodnoty. Ceny uvedené u produktů "
    "jsou konečné ceny za zboží a nezahrnují cenu dopravy."),
  p("Cena dopravy sa určuje podľa hmotnosti zásielky a miesta doručenia a je "
    "uvedená na faktúre, ktorú kupujúci dostane spolu s potvrdením objednávky. "
    "Cenník dopravy: " + TODO + ".",
    "Cena dopravy se určuje podle hmotnosti zásilky a místa doručení a je "
    "uvedena na faktuře, kterou kupující obdrží spolu s potvrzením objednávky. "
    "Ceník dopravy: " + TODO + "."),
  p("Platba je možná výhradne vopred, prevodom na účet predávajúceho na základe "
    "faktúry s QR kódom, ktorú kupujúci dostane e-mailom po potvrdení objednávky. "
    "Dobierku ani platbu kartou neponúkame. Tovar expedujeme po pripísaní platby.",
    "Platba je možná výhradně předem, převodem na účet prodávajícího na základě "
    "faktury s QR kódem, kterou kupující obdrží e-mailem po potvrzení objednávky. "
    "Dobírku ani platbu kartou nenabízíme. Zboží expedujeme po připsání platby."),
 ]),

 (("10. Záruka a reklamácie", "10. Záruka a reklamace"), [
  p("Predávajúci poskytuje na tovar záruku v trvaní 24 mesiacov, pokiaľ nie je "
    "pri konkrétnom výrobku uvedené inak. Záruka začína plynúť dňom prevzatia "
    "tovaru kupujúcim. Kupujúci je povinný pred prvým použitím tovaru riadne sa "
    "oboznámiť s návodom a so záručnými podmienkami.",
    "Prodávající poskytuje na zboží záruku v trvání 24 měsíců, pokud není "
    "u konkrétního výrobku uvedeno jinak. Záruka začíná běžet dnem převzetí "
    "zboží kupujícím. Kupující je povinen před prvním použitím zboží řádně se "
    "seznámit s návodem a se záručními podmínkami."),
  p("Záruka sa nevzťahuje najmä na:", "Záruka se nevztahuje zejména na:"),
  ul(("mechanické poškodenie tovaru kupujúcim, vrátane poškriabania povrchu "
      "panela pri odstraňovaní ľadu alebo prejazde kefovou automyčkou,",
      "mechanické poškození zboží kupujícím, včetně poškrábání povrchu "
      "panelu při odstraňování ledu nebo průjezdu kartáčovou myčkou,"),
     ("neodbornú montáž, nesprávnu manipuláciu, neodbornú inštaláciu a lepenie "
      "panela na neočistený, mastný alebo poškodený podklad,",
      "neodbornou montáž, nesprávnou manipulaci, neodbornou instalaci a lepení "
      "panelu na neočištěný, mastný nebo poškozený podklad,"),
     ("ohnutie flexibilného panela nad rámec pokynov výrobcu, najmä ohnutie "
      "dovnútra alebo prehnutie s hĺbkou väčšou než 20 % dĺžky panela,",
      "ohnutí flexibilního panelu nad rámec pokynů výrobce, zejména ohnutí "
      "dovnitř nebo prohnutí s hloubkou větší než 20 % délky panelu,"),
     ("používanie tovaru v nevhodných podmienkach, zanedbanie starostlivosti "
      "o tovar a neodborný zásah do výrobku inou ako oprávnenou osobou,",
      "používání zboží v nevhodných podmínkách, zanedbání péče o zboží "
      "a neodborný zásah do výrobku jinou než oprávněnou osobou,"),
     ("škody vzniknuté v dôsledku živelnej udalosti, násilného poškodenia alebo "
      "prevádzky v extrémnych a neobvyklých podmienkach.",
      "škody vzniklé v důsledku živelní události, násilného poškození nebo "
      "provozu v extrémních a neobvyklých podmínkách.")),
  p("Reklamáciu kupujúci uplatní e-mailom na <a class=\"js-mail\" href=\"#\"></a> "
    "alebo zaslaním tovaru na adresu <strong class=\"js-company\"></strong>, "
    "<span class=\"js-address\"></span>. Tovar je potrebné vhodne zabaliť, aby "
    "počas prepravy nedošlo k jeho poškodeniu.",
    "Reklamaci kupující uplatní e-mailem na <a class=\"js-mail\" href=\"#\"></a> "
    "nebo zasláním zboží na adresu <strong class=\"js-company\"></strong>, "
    "<span class=\"js-address\"></span>. Zboží je třeba vhodně zabalit, aby "
    "během přepravy nedošlo k jeho poškození."),
  p("Predávajúci potvrdí prijatie reklamácie a vydá kupujúcemu potvrdenie o jej "
    "uplatnení. Za deň uplatnenia reklamácie sa považuje deň jej doručenia "
    "predávajúcemu. Predávajúci je povinný určiť spôsob vybavenia reklamácie "
    "ihneď, v zložitých prípadoch do 3 pracovných dní, v odôvodnených prípadoch "
    "najneskôr do 30 dní odo dňa uplatnenia reklamácie. Vybavenie reklamácie "
    "nesmie trvať dlhšie ako 30 dní odo dňa jej uplatnenia. Po uplynutí tejto "
    "lehoty má kupujúci právo odstúpiť od zmluvy alebo na výmenu tovaru za nový.",
    "Prodávající potvrdí přijetí reklamace a vydá kupujícímu potvrzení o jejím "
    "uplatnění. Za den uplatnění reklamace se považuje den jejího doručení "
    "prodávajícímu. Prodávající je povinen určit způsob vyřízení reklamace "
    "ihned, ve složitých případech do 3 pracovních dnů, v odůvodněných "
    "případech nejpozději do 30 dnů ode dne uplatnění reklamace. Vyřízení "
    "reklamace nesmí trvat déle než 30 dnů ode dne jejího uplatnění. Po uplynutí "
    "této lhůty má kupující právo odstoupit od smlouvy nebo na výměnu zboží."),
  p("Práva kupujúceho pri uplatnení reklamácie:",
    "Práva kupujícího při uplatnění reklamace:"),
  ul(("ak ide o vadu, ktorú možno odstrániť, má kupujúci právo, aby bola "
      "bezodplatne, včas a riadne odstránená bez zbytočného odkladu,",
      "jde-li o vadu, kterou lze odstranit, má kupující právo, aby byla "
      "bezplatně, včas a řádně odstraněna bez zbytečného odkladu,"),
     ("kupujúci môže namiesto odstránenia vady požadovať výmenu veci alebo jej "
      "súčasti, ak tým predávajúcemu nevzniknú neprimerané náklady vzhľadom na "
      "cenu tovaru alebo závažnosť vady,",
      "kupující může místo odstranění vady požadovat výměnu věci nebo její "
      "součásti, pokud tím prodávajícímu nevzniknou nepřiměřené náklady vzhledem "
      "k ceně zboží nebo závažnosti vady,"),
     ("ak ide o vadu, ktorú nemožno odstrániť a ktorá bráni riadnemu používaniu "
      "veci, má kupujúci právo na výmenu veci alebo na odstúpenie od zmluvy,",
      "jde-li o vadu, kterou nelze odstranit a která brání řádnému užívání "
      "věci, má kupující právo na výměnu věci nebo na odstoupení od smlouvy,"),
     ("ak ide o iné neodstrániteľné vady, ktoré nebránia používaniu tovaru, má "
      "kupujúci právo na primeranú zľavu z ceny.",
      "jde-li o jiné neodstranitelné vady, které nebrání užívání zboží, má "
      "kupující právo na přiměřenou slevu z ceny.")),
 ]),

 (("11. Ochrana osobných údajov", "11. Ochrana osobních údajů"), [
  p("Predávajúci spracúva osobné údaje podľa nariadenia Európskeho parlamentu "
    "a Rady (EÚ) 2016/679 (GDPR). Prevádzkovateľom je "
    "<strong class=\"js-company\"></strong>, <span class=\"js-address\"></span>, "
    "kontakt pre uplatnenie práv dotknutej osoby: "
    "<a class=\"js-mail\" href=\"#\"></a>.",
    "Prodávající zpracovává osobní údaje podle nařízení Evropského parlamentu "
    "a Rady (EU) 2016/679 (GDPR). Správcem je "
    "<strong class=\"js-company\"></strong>, <span class=\"js-address\"></span>, "
    "kontakt pro uplatnění práv subjektu údajů: "
    "<a class=\"js-mail\" href=\"#\"></a>."),
  p("Údaje z objednávkového a kontaktného formulára (meno, e-mail, telefón, "
    "adresa, prípadne firemné údaje) spracúvame na účel uzavretia a plnenia "
    "kúpnej zmluvy a na splnenie zákonných povinností, najmä účtovných "
    "a daňových. Údaje uchovávame po dobu vyžadovanú právnymi predpismi.",
    "Údaje z objednávkového a kontaktního formuláře (jméno, e-mail, telefon, "
    "adresa, případně firemní údaje) zpracováváme za účelem uzavření a plnění "
    "kupní smlouvy a ke splnění zákonných povinností, zejména účetních "
    "a daňových. Údaje uchováváme po dobu vyžadovanou právními předpisy."),
  p("Formuláre na tomto webe odosiela sprostredkovateľ formsubmit.co, ktorý "
    "správu doručí na našu e-mailovú adresu. Údaje neposkytujeme ďalším "
    "príjemcom okrem dopravcu, ktorý zásielku doručuje, a našej účtovnej "
    "kancelárie.",
    "Formuláře na tomto webu odesílá zpracovatel formsubmit.co, který zprávu "
    "doručí na naši e-mailovou adresu. Údaje neposkytujeme dalším příjemcům "
    "kromě dopravce, který zásilku doručuje, a naší účetní kanceláře."),
  p("Dotknutá osoba má právo na prístup k údajom, ich opravu, vymazanie, "
    "obmedzenie spracúvania, prenosnosť a právo namietať, ako aj právo podať "
    "sťažnosť dozornému orgánu — Úradu na ochranu osobných údajov Slovenskej "
    "republiky, Hraničná 12, 820 07 Bratislava.",
    "Subjekt údajů má právo na přístup k údajům, jejich opravu, výmaz, omezení "
    "zpracování, přenositelnost a právo vznést námitku, jakož i právo podat "
    "stížnost dozorovému úřadu — v České republice Úřadu pro ochranu osobních "
    "údajů, Pplk. Sochora 27, 170 00 Praha 7."),
 ]),

 (("12. Cookies a ukladanie v prehliadači",
   "12. Cookies a ukládání v prohlížeči"), [
  p("Tento web nepoužíva analytické ani reklamné cookies a nesleduje "
    "návštevníkov. V prehliadači kupujúceho ukladáme len obsah košíka a voľbu "
    "svetlého alebo tmavého režimu. Tieto údaje zostávajú v zariadení "
    "návštevníka a neodosielajú sa nám.",
    "Tento web nepoužívá analytické ani reklamní cookies a nesleduje "
    "návštěvníky. V prohlížeči kupujícího ukládáme pouze obsah košíku a volbu "
    "světlého nebo tmavého režimu. Tato data zůstávají v zařízení návštěvníka "
    "a neodesílají se nám."),
 ]),

 (("13. Zodpovednosť", "13. Odpovědnost"), [
  p("Podmienkou platnosti objednávky je vyplnenie všetkých povinne označených "
    "údajov v objednávkovom formulári.",
    "Podmínkou platnosti objednávky je vyplnění všech povinně označených údajů "
    "v objednávkovém formuláři."),
  p("Predávajúci nezodpovedá za nedoručenie zásielky alebo za jej zdržanie, ak "
    "bolo spôsobené nedostatkami na strane kupujúceho, najmä nesprávne uvedenou "
    "doručovacou adresou, nesprávnym telefonickým kontaktom alebo inými "
    "nepravdivými údajmi, v dôsledku ktorých nemohlo dôjsť k riadnemu doručeniu.",
    "Prodávající neodpovídá za nedoručení zásilky nebo za její zdržení, pokud "
    "bylo způsobeno nedostatky na straně kupujícího, zejména nesprávně uvedenou "
    "doručovací adresou, nesprávným telefonickým kontaktem nebo jinými "
    "nepravdivými údaji, v důsledku kterých nemohlo dojít k řádnému doručení."),
  p("Predávajúci nezodpovedá za nedoručenie tovaru, ak ho osoba uvedená "
    "v objednávke odmietla prevziať alebo bola nezastihnuteľná.",
    "Prodávající neodpovídá za nedoručení zboží, pokud je osoba uvedená "
    "v objednávce odmítla převzít nebo byla nezastižitelná."),
  p("Ak predávajúci nemôže objednaný tovar doručiť z dôvodov na svojej strane, "
    "zaplatená kúpna cena bude kupujúcemu vrátená na bankový účet.",
    "Pokud prodávající nemůže objednané zboží doručit z důvodů na své straně, "
    "zaplacená kupní cena bude kupujícímu vrácena na bankovní účet."),
 ]),

 (("14. Alternatívne riešenie sporov", "14. Mimosoudní řešení sporů"), [
  p("Spotrebiteľ má právo na alternatívny (mimosúdny) spôsob riešenia sporov "
    "podľa zákona č. 391/2015 Z. z. o alternatívnom riešení spotrebiteľských "
    "sporov. Návrh môže podať spôsobom určeným podľa § 12 uvedeného zákona.",
    "Spotřebitel má právo na mimosoudní řešení spotřebitelského sporu. "
    "Subjektem mimosoudního řešení sporů pro spotřebitele s bydlištěm v České "
    "republice je Česká obchodní inspekce, Gorazdova 1969/24, 120 00 Praha 2, "
    "web adr.coi.cz."),
  p("Subjektom alternatívneho riešenia sporov je Slovenská obchodná inšpekcia. "
    "Adresa na podávanie podaní v elektronickej podobe: ars@soi.sk. Spotrebiteľ "
    "má právo voľby, na ktorý zo subjektov alternatívneho riešenia "
    "spotrebiteľských sporov sa obráti.",
    "Spotřebitel se může obrátit rovněž na Slovenskou obchodní inspekci "
    "(subjekt v zemi sídla prodávajícího), adresa pro elektronická podání: "
    "ars@soi.sk."),
  p("Spotrebiteľ môže podať sťažnosť aj prostredníctvom platformy "
    "alternatívneho riešenia sporov RSO, dostupnej online na "
    "http://ec.europa.eu/consumers/odr.",
    "Spotřebitel může podat stížnost také prostřednictvím platformy pro řešení "
    "sporů online, dostupné na http://ec.europa.eu/consumers/odr."),
  p("Subjekt alternatívneho riešenia sporov môže návrh odmietnuť, napríklad ak "
    "vyčísliteľná hodnota sporu nepresahuje sumu 20 eur. Náklady spojené "
    "s alternatívnym riešením sporu znáša každá zo strán samostatne.",
    "Subjekt mimosoudního řešení sporů může návrh odmítnout, například pokud "
    "vyčíslitelná hodnota sporu nepřesahuje částku 20 eur. Náklady spojené "
    "s mimosoudním řešením sporu nese každá ze stran samostatně."),
 ]),

 (("15. Záverečné ustanovenia", "15. Závěrečná ustanovení"), [
  p("Predávajúci si vyhradzuje právo na zmenu týchto všeobecných obchodných "
    "podmienok. Povinnosť písomného oznámenia zmeny je splnená umiestnením "
    "nového znenia na internetovej stránke predávajúceho. Na už uzavreté zmluvy "
    "sa vzťahuje znenie účinné v čase uzavretia zmluvy.",
    "Prodávající si vyhrazuje právo na změnu těchto všeobecných obchodních "
    "podmínek. Povinnost písemného oznámení změny je splněna umístěním nového "
    "znění na internetové stránce prodávajícího. Na již uzavřené smlouvy se "
    "vztahuje znění účinné v době uzavření smlouvy."),
  p("Tieto všeobecné obchodné podmienky nadobúdajú účinnosť voči kupujúcemu "
    "odoslaním objednávky a potvrdením súhlasu s nimi. Kupujúci vyhlasuje, že "
    "si tieto podmienky prečítal a v celom rozsahu s nimi súhlasí.",
    "Tyto všeobecné obchodní podmínky nabývají účinnosti vůči kupujícímu "
    "odesláním objednávky a potvrzením souhlasu s nimi. Kupující prohlašuje, že "
    "si tyto podmínky přečetl a v celém rozsahu s nimi souhlasí."),
  p("Predávajúci a kupujúci sa dohodli, že plne uznávajú elektronickú formu "
    "komunikácie, najmä prostredníctvom elektronickej pošty, ako platnú "
    "a záväznú pre obe zmluvné strany.",
    "Prodávající a kupující se dohodli, že plně uznávají elektronickou formu "
    "komunikace, zejména prostřednictvím elektronické pošty, jako platnou "
    "a závaznou pro obě smluvní strany."),
 ]),
]

/* ==========================================================================
   NASTAVENIE / NASTAVENÍ  —  upravte tieto hodnoty a nič iné.
   Configure these values; nothing else needs editing.
   ========================================================================== */
window.SITE_CONFIG = {
  /* --- 1. VAŠA FIRMA / VAŠE FIRMA ---------------------------------------
     Nahraďte zástupné hodnoty svojimi údajmi.
     Replace these placeholders with your own details.                     */
  company: "Fabrika SAIL s.r.o.",
  street: "Pšurnovice 221",
  city: "014 01 Bytča",
  ico: "56774907",
  dic: "2122424018",
  hours: "9:00 – 18:00",
  orderEmail: "objednavky@rncexplore.com", // sem chodia objednávky / sem chodí objednávky
  phone: "+421 905 698 410",
  web: "www.rncexplore.com",

  /* --- 2. CENY / CENY ----------------------------------------------------
     Ceny v katalógu sú v USD (zdroj výrobcu). Prepočítavajú sa takto:
       zobrazená cena = USD × markup × kurz
     markup = vaša marža (1.0 = bez marže, 1.25 = +25 %).
     Kurzy si podľa potreby aktualizujte.                                   */
  markup: 1.0,
  rates: { EUR: 0.92, CZK: 23.0 },

  /* Zaokrúhlenie zobrazenej ceny: "9"  -> 249 € končí na 9 (249, 259…)
                                   "0"  -> zaokrúhli na celé
                                   null -> presne prepočítané             */
  rounding: "9",

  /* Zobraziť pôvodnú prečiarknutú cenu, ak ju výrobca uvádza?             */
  showCompareAt: true,

  /* Zobraziť ceny vôbec? false = všade "Cena na vyžiadanie"               */
  showPrices: true,

  /* --- 3. ODOSIELANIE OBJEDNÁVOK ----------------------------------------
     Stránka nemá vlastný server, objednávku preto odošle cez službu,
     ktorá ju prepošle e-mailom na adresu orderEmail vyššie.

     "formsubmit" — netreba nič zriaďovať. Pri úplne prvej objednávke
                    príde na orderEmail e-mail od formsubmit.co s odkazom
                    na potvrdenie. Kým naň nekliknete, objednávky nechodia.
     "web3forms"  — na web3forms.com zadáte e-mail, obratom vám pošlú
                    prístupový kľúč. Vložte ho nižšie do formKey.
     "mailto"     — otvorí e-mailového klienta zákazníka (bez služby).

     Ak odoslanie zlyhá, formulár sa vždy prepne na "mailto",
     aby objednávka nezostala visieť.                                     */
  orderSend: "formsubmit",
  formKey: "",

  /* Kam objednávku reálne doručiť. Nechajte prázdne = doručí sa na
     orderEmail. Vyplňte len vtedy, keď schránka orderEmail ešte
     nefunguje alebo sa k nej neviete dostať — na webe sa aj tak
     všade zobrazuje orderEmail, zákazník túto adresu nevidí.
     Príklad: "j.bendzala.j@gmail.com"                                    */
  deliverTo: "objednavky@rncexplore.com",
};

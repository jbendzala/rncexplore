# -*- coding: utf-8 -*-
"""Jazyk generovaných blokov — slovenčina a čeština.

Česká mutácia beží v podadresári /cs/, takže sa neprepínajú len texty,
ale aj adresy odkazov. Preto to nie je obyčajný slovník: každý odkaz
musí prejsť cez odkaz(), inak bude z českej stránky mieriť na slovenskú.

Stav je zámerne v module a číta sa cez funkcie, nie cez import hodnoty.
Keby si ho generátory importovali ako premennú, každý by dostal vlastnú
kópiu a prepnutie jazyka by sa k nim nedostalo.
"""
import sys

PREDPONY = {"sk": "", "cs": "/cs"}

_jazyk = "sk"


def aktualny():
    return _jazyk


def nastav(kod):
    """Prepne jazyk. Neznámy kód je chyba, nie tichý návrat k slovenčine —
    preklep v argumente by inak vyrobil slovenské súbory v českom
    priečinku a nikto by si toho nevšimol."""
    global _jazyk
    if kod not in PREDPONY:
        sys.exit(f"neznámy jazyk {kod!r}; poznám " + ", ".join(PREDPONY))
    _jazyk = kod
    return _jazyk


def z_argumentov(argv=None):
    """Jazyk z prvého argumentu príkazového riadka, inak slovenčina."""
    a = (argv if argv is not None else sys.argv)[1:]
    return nastav(a[0]) if a else _jazyk


def odkaz(cesta):
    """Adresa v aktuálnej mutácii. Absolútne cesty dostanú predponu,
    kotvy a cudzie adresy zostanú tak, ako sú."""
    if not cesta.startswith("/") or cesta.startswith("//"):
        return cesta
    return PREDPONY[_jazyk] + cesta


def t(slovnik):
    """Vetva slovníka pre aktuálny jazyk."""
    return slovnik[_jazyk]


def priecinok(zaklad):
    """Názov výstupného priečinka. Slovenčina ide do pôvodného, aby staré
    postupy sedeli, čeština vedľa."""
    return zaklad if _jazyk == "sk" else f"{zaklad}-{_jazyk}"

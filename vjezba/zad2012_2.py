"""

Napišite leksički analizator za „programski jezik“ koji radi sa skupovima u 
kojima se nalaze cijeli brojevi (niz znamenki). Jezik treba omogućiti

deklariranje skupa (npr. SKUP S), gdje se ime skupa sastoji od jednog 
velikog slova iz engleske abecede (npr. 'S'). Operacije za rad sa 
skupom su uobičajene: provjera je li skup prazan (PRAZAN S),

ubacivanje elementa u skup (UBACI S 2345 32 41), izbacivanje 
elementa iz skupa (IZBACI S 2345 13), provjera da li je element 
u skupu (ELEMENT S 2345), vraćanje broja elemenata u skupu

(VELIČINA S), te ispis skupa (ISPIŠI S). Napišite sintaksni 
analizator za taj programski jezik (svaka vrsta naredbe odgovara 
jednom tipu apstraktnog sintaksnog stabla).

Omogućite da operacije
UBACI i IZBACI mogu primiti više brojeva. Napišite i odgovarajući 
semantički analizator (interpreter).

"""
from setimportpath import *
from pj import *


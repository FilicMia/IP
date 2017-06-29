from setimportpath import *
from RI import *
from pj import *
import cmath

"""
Specijalni znak je naziv za otvorenu ili zatvorenu zagradu,
vertikalnu ili kosu crtu te zvjezdicu. Napišite
funkciju specijalan koja prima znak i vraća je li
specijalan. (Kosa crta je /, a ne
\. Zagrade su samo oble (). Primijetite: razmak nije specijalan).
"""

def specijalan(znak):
    if znak in '/()|*':
        return True
    else:
        return False

"""
Svakom specijalnom znaku odgovara zasebni tip tokena.
Svim ostalim znakovima odgovara jedan tip tokena ZNAK,
čiji sadržaj kaže o kojem se znaku radi. Svi tokeni (osim KRAJ)
imaju sadržaj duljine 1. Napišite odgovarajuće članove Enum-klase Ri.

"""
class Ri(enum.Enum):
    KOSA,OTV,ZATV,ILI,ZVIJEZDA = '/()|*'
    ZNAK = 'a'

"""
Napišite funkciju (generator) ri_lex koja yielda tokene čiji tipovi
su gore navedeni, a čiji sadržaji predstavljaju znakove ulaznog stringa.
"""

def ri_lex(string):
    lex = Tokenizer(string)
    for znak in iter(lex.čitaj,''):
        if specijalan(znak):
            yield lex.token(operator(Ri,znak) or E.GREŠKA)
        else:
            yield lex.token(Ri.ZNAK)

"""
Regularni izrazi grade se od elementarnih jezika koji su
predstavljeni tokenom ZNAK, te praznog jezika /. Grade se
(rastućim prioritetom, kojeg možemo mijenjati zagradama)
unijom (binarni infiksni operator |), konkatenacijom, te
zvjezdicom (unarni postfiksni operator *). Napišite odgovarajuću
beskontekstnu gramatiku nad abecedom koju čine tipovi tokena.
"""

"""
BKG:

ri -> disjunkt ILI ri | disjunkt ri | disjunkt #binarni
disjunkt -> elementarni ZVIJEZDA | elementaran #unarni
elementaran -> ZNAK | KOSA |  OTV ri ZATV #terminalni

"""

"""

Svaki nespecijalni znak α predstavlja jezik koji sadrži samo
jednoslovnu riječ α. Izraz (r) predstavlja isti jezik kao izraz r,
dok izraz r* predstavlja Kleenejevu zvijezdu tog jezika. Napišite
klasu RIParser tako da funkcija
RIParser.parsiraj prima string i vraća RegularanIzraz kojeg on predstavlja.

"""

class RIParser(Parser):

    def start(self):
        ri = False
        while not self >> E.KRAJ:
            noviRi = self.ri()
            if ri:
                ri = Konkatenacija(ri,noviRi)
            else:
                ri = noviRi
        return ri

    def ri(self):
        disjunkt = self.disjunkt()
        if self >> Ri.ILI:
            ri = self.ri()
            return Unija(disjunkt,ri)
        else:
            return disjunkt
        
    def disjunkt(self):
        elementaran = self.elementaran()
        while True:
            if self >> Ri.ZVIJEZDA:
                elementaran = Zvijezda(elementaran)
            else:
                break
        return elementaran

    def elementaran(self):
        if self >> Ri.ZNAK:
            return Elementaran(self.zadnji.sadržaj)
        elif self >> Ri.KOSA:
            return Prazan()
        elif self >> Ri.OTV:
            uzagradi = self.ri()
            self.pročitaj(Ri.ZATV)
            return uzagradi
        else:
            self.greška()
"""
Prijavite korisne poruke o greškama (navodeći poziciju greške,
koji tokeni su očekivani, a koji je pročitan) ako argument
od RI_parse ne predstavlja validan regularan izraz.
(Ovo će biti trivijalno ispunjeno ako koristite pj framework.)
""" #--> koristim pa ispunjeno

tests = [3]
if __name__=='__main__':

    if 1 in tests:
        string = ')'
        print(specijalan('('))

    if 2 in tests:
        string = '/|a(c)*'
        lex = ri_lex(string)
        print('Lexer')
        print(*lex)
    if 3 in tests:
        string = '/|a(c)*'
        lex = ri_lex(string)
        print('parser')
        print(RIParser.parsiraj(lex))

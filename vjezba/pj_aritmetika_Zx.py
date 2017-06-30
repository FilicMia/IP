from setimportpath import *
from RI import *
from pj import *
import cmath

"""
Aritmetika na Zx.. Kako to?
Cjelobroojni polinomi s koeficijentina u Z.
Mogu se reprezentirati s vektorima cijelih
brojeva, gdje duljina vektora implicitno označava potenciju polinoma. 
"""

"""
Lexer.
"""

class Zx(enum.Enum):
    BROJ = 123
    PLUS = '+' #ista razina prioriteta +,-
    MINUS = '-' #ista razina prioriteta +,-
    #MINUS BROJ ĆE BITI KO ODUZIMANJE NULPOLINOMA I BROJA IZA TOGA (MONOMA)
    PUTA = '*' #veći prioritet
    OTV,ZATV = '()'
    X = 'x' # samo malo x dozvoljavamo?, x^3 == x3

def lex_Zx(string):
    lex = Tokenizer(string)
    for znak in iter(lex.čitaj,''):
        if znak.isspace(): lex.token(E.PRAZNO)
        elif znak.isnumeric():
            lex.zvijezda(str.isnumeric)
            yield lex.token(Zx.BROJ)
        else:
            yield lex.token(operator(Zx,znak) or E.GREŠKA)

"""
x -> 1*x
-broj (na početku polinoma) = (0-broj)..prepiši ostalo
"""

"""
BKG:
izraz -> izraz PLUS član | član MINUS izraz | član
član -> član PUTA faktor | faktor | član faktor |MINUS član
faktor -> BROJ X BROJ | BROJ | OTV izraz ZATV |X
"""




class Zxpar(Parser):

    def start(self):
        rez = False
        while not self >> E.KRAJ:
            if rez:
                rez = PUTA(rez,self.polinom())
            else:
                rez = self.polinom()

    def izraz(self):
        izraz = self.član() # za lijevu asociranost potrebno je znanje o desnoj
        while True:
            if self >> Zx.PLUS: izraz = PLUS(izraz,self.član())
            elif self >> Zx.MINUS: izraz = MINUS(izraz,self.član())
            else: return izraz
        
    def član(self):
        član = self.faktor() # za lijevu asociranost potrebno je znanje o desnoj
        while True:
            if self >> Zx.PUTA: član = PLUS(član,self.faktor())
            elif self >> Zx.MINUS:
                if član:
                    član = MINUS(član, self.faktor())
                else:
                    član = MINUS(BROJ('0'), self.faktor())
            else: return član

    def faktor(self):
        if self >> Zx.MINUS:
            self.vrati()
            return False
        elif self >> Zx.BROJ:
            broj = self.zadnji.sadržaj
            x = False
            na = False
            if self.pogledaj() ** Zx.X:
                x = True
                self.čitaj()
                if self.pogledaj() ** Zx.BROJ:
                    na = self.čitaj().sadržaj
                    
            


class BINARNA(AST('prvi drugi')):pass
class PLUS(BINARNA):pass
class PUTA(BINARNA): pass
class MINUS(BINARNA): pass
class MONOM(AST('broj na')): pass #3x8 x 8 9

tests = [2]
if __name__ == '__main__':
    if 1 in tests:
        string = '(5+2*8-3)(3-1)-(-4+2*19)'
        lex = lex_Zx(string)
        print(*lex)

    if 2 in tests:
        string = '(x-2+5x-(7x-5))-(x-2+5x-(7x-5))'
        lex = lex_Zx(string)
        print(*lex)
        
    

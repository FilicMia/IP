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
izraz -> izraz PLUS član | izraz MINUS član | član
član -> član PUTA faktor | faktor | član faktor |MINUS član
faktor -> BROJ X BROJ | BROJ | OTV izraz ZATV |X
"""




class Zxpar(Parser):

    def start(self):
        rez = False
        while not self >> E.KRAJ:
            if rez:
                rez = PUTA(rez,self.izraz())
            else:
                rez = self.izraz()
        return rez

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
                na = '1'
                if self.pogledaj() ** Zx.BROJ:
                    na = self.čitaj().sadržaj
                return MONOM(broj,na)
            
            else:
                return MONOM(broj,'0')
        elif self >> Zx.X:
            na = '1'
            if self.pogledaj() ** Zx.BROJ:
                na = self.čitaj().sadržaj
            return MONOM('1',na)
        elif self >> Zx.OTV:
            izraz = self.izraz()
            self.pročitaj(Zx.ZATV)
            return izraz

"""
Paziti koja okolina je moja okolina.
"""
def izvrši(par):
    okolina = {}
    return par.izvrši(okolina)

class BINARNA(AST('prvi drugi')):pass
class PLUS(BINARNA):
    def izvrši(self,okolina):
        moja_okolina = {}
        okolina1 = self.prvi.izvrši(moja_okolina)
        okolina2 = self.drugi.izvrši(moja_okolina)
        
        for k,v in okolina2.items():
            if k not in okolina1:
                okolina1[k] = 0
            okolina1[k] = okolina1[k]+okolina2[k]
            
        return okolina1

"""class PUTA(BINARNA):
    def izvrši(self, okolina):
        moja_okolina = {}
        okolina1 = self.prvi.izvrši(moja_okolina)
        okolina2 = self.drugi.izvrši(moja_okolina)
        
        return reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.iteritems()), dict1)"""

class MINUS(BINARNA):
    def izvrši(self,okolina):
        moja_okolina = {}
        okolina1 = self.prvi.izvrši(moja_okolina)
        
        okolina2 = self.drugi.izvrši(moja_okolina)
        for k,v in okolina2.items():
            if k not in okolina1:
                okolina1[k] = 0
            okolina1[k] = okolina1[k]-okolina2[k]
            
        
        return okolina1
class MONOM(AST('broj na')): #3x8 x 8 9
    def izvrši(self, okolina):
        okolina = {}
        okolina[self.na] = int(self.broj)
        return okolina

tests = [4]
if __name__ == '__main__':
    if 1 in tests:
        string = '(5+2*8-3)(3-1)-(-4+2*19)'
        lex = lex_Zx(string)
        print(*lex)

    if 2 in tests:
        string = '(x-2+5x-(7x-5))-(x-2+5x-(7x-5))'
        lex = lex_Zx(string)
        print(*lex)
    if 3 in tests:
        string = '(x-2+5x-(7x-5))'
        lex = lex_Zx(string)
        print(Zxpar.parsiraj(lex))
    if 4 in tests:
        string = '(x-2+5x-(7x-5))'
        lex = lex_Zx(string)
        par = Zxpar.parsiraj(lex)
        print(izvrši(par))

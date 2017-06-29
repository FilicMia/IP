from setimportpath import *
from RI import *
from pj import *

"""
Radimo aritmetiku nad N.

Lexer: dakle, bitno je da prepoznajemo brojeve (cijele brojeve) i
PLUS, PUTA, NA, OTV, ZATV = '+*^()'

"""

class N(enum.Enum):
    BROJ = 123
    PLUS, PUTA, NA, OTV, ZATV = '+*^()'

def n_lex(string):
    lex = Tokenizer(string)

    for znak in iter(lex.čitaj,''):
        if znak != '' and znak.isspace():#makni praznine
            lex.token(E.PRAZNO)
            znak = lex.čitaj()

        if znak.isnumeric():
            lex.zvijezda(str.isnumeric)
            yield lex.token(N.BROJ)
        else:
            yield lex.token(operator(N,lex.sadržaj) or E.GREŠKA)

"""
Parser:
Gradi AST:

"""
"""
BESKONTEKSTNA GRAMATIKA: (desno asocirani -- rekurzija)

izraz -> član PLUS izraz | član

član -> faktor PUTA član | faktor

faktor -> baza NA faktor | baza

baza -> OTV izraz ZATV | BROJ
"""

class Npar(Parser):
    
    def start(self):
        return self.izraz()
    
    def izraz(self):
        rez = self.član()
        
        if self >> N.PLUS:
            izraz = self.izraz()
            rez = PLUS(rez,izraz)
        return rez

    def član(self):
        rez = self.faktor()
        if self >> N.PUTA:
            član = self.izraz()
            rez = PUTA(rez,član)
        return rez

    def faktor(self):
        rez = self.baza()
        if self >> N.NA:
            faktor = self.faktor()
            rez = NA(rez,faktor)
        return rez

    
    def baza(self):
        rez = False
        if self >> N.OTV:
            rez = self.izraz()
            self.pročitaj(N.ZATV)
        elif self >> N.BROJ:
            rez = ELEMENT(self.zadnji)
        else:
            self.greška()
        return rez
            

def Ninterp(par):
    return par.izvrši()
    

class BINARAN(AST('faktor1 faktor2')): pass
class PLUS(BINARAN):
    def izvrši(self):
        return self.faktor1.izvrši() + self.faktor2.izvrši()
        
class PUTA(BINARAN):
    def izvrši(self):
        return self.faktor1.izvrši() * self.faktor2.izvrši()
        
class NA(BINARAN):
    def izvrši(self):
        return self.faktor1.izvrši()** self.faktor2.izvrši()
        
        
class ELEMENT(AST('element')):
    def izvrši(self):
        return int(self.element.sadržaj)
        

tests = [3]
if __name__ == '__main__':

    if 1 in tests:
        string = "(2+3)*4^1"
        lex = n_lex(string)
        
        print('lexer')
        print(*n_lex(string))

        print('parser')
        print(Npar.parsiraj(lex))

        print('interpreter')
        lex = n_lex(string)
        par = Npar.parsiraj(lex)
        print(Ninterp(par))

    if 2 in tests:
        string = '2^0^0^0^0'
        lex = n_lex(string)
        
        print('lexer')
        print(*n_lex(string))

        print('parser')
        print(Npar.parsiraj(lex))

        print('interpreter')
        lex = n_lex(string)
        par = Npar.parsiraj(lex)
        print(Ninterp(par))

    if 3 in tests:
        string = '2+(0+1*1*2)'
        lex = n_lex(string)
        
        print('lexer')
        print(*n_lex(string))

        print('parser')
        print(Npar.parsiraj(lex))

        print('interpreter')
        lex = n_lex(string)
        par = Npar.parsiraj(lex)
        print(Ninterp(par))

        

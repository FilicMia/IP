from setimportpath import *
from RI import *
from pj import *

"""
Lexer za regularne izraze.
Iza a.b se može skratiti u ab gdje . predstavja operator konkatenacije.
Dopušteni operatori su *,+,?,.,|

Parser koji pravilno grupira tokene lexera.

Semantička analiza: gradi jezik pretstvalja dani regularni jezik.

"""

class Ri(enum.Enum):
    ZVIJEZDA = '*'
    PLUS = '+'
    UNIJA = '|'
    OTV = '('
    ZATV = ')'
    UPITNIK = '?'
    CONCAT = '.'
    PRAZAN = '/0'
    EPSILON = '/1'
    ZNAK = 'sve ostalo? osim praznina - nevidljive su pa ih ne želim'

def ri_lex(string):
    lex = Tokenizer(string)

    for znak in iter(lex.čitaj,''):
        if znak.isspace():
            lex.token(E.PRAZNO)
            continue
        
        if operator(Ri,znak):
            yield lex.token(operator(Ri,znak))
        elif znak == '/':
            znak = lex.čitaj()
            
            if znak in {'0','1'}:
                yield lex.token(Ri(lex.sadržaj))
                
            elif znak in [e.value for e in Ri]:
                lex.vrati()
                lex.token(E.PRAZNO)
                lex.čitaj()
                yield lex.token(Ri.ZNAK)
                
            else:
                lex.vrati()
                yield lex.token(Ri.ZNAK)
            
        else:
            yield lex.token(Ri.ZNAK)
            
        
"""
BESKONTEKSTNA GRAMATIKA:

izraz -> unarni | binarni | faktor | unarni izraz | binarni izraz | faktor izraz

faktor -> OTV Izraz ZATV | ZNAK znakovi | EPSILON | PRAZAN
znakovi -> ZNAK znakovi | EPS
    
binarni -> faktor bznak faktor 
bznak -> UNIJA | CONCAT | EPS |

unarni -> faktor uznak
uznak -> UPITNIK | ZVIJEZDA | PLUS

"""
  
class ri_par(Parser):
    def start(self):
        naredbe = []
        while not self >> E.KRAJ: naredbe.append(self.naredba())
            

    def naredba(self):
    
        self.faktor = False
        if self >> Ri.OTV:
            f = self.izraz()
            self.pročitaj(Ri.ZATV)
            if self.faktor:
                op = Ri.CONCAT
                faktor_prvi = self.faktor
                faktor_drugi = f
            
                self.faktor = False
                return BINARNI(faktor_prvi,op,faktor_drugi)
            else:
                self.faktor = f
            
        elif self >> Ri.ZNAK:
            Ri.vrati()
            f = self.znakovi()
            if self.faktor:
                op = Ri.CONCAT
                faktor_prvi = self.faktor
                faktor_drugi = f
            
                self.faktor = False
                return BINARNI(faktor_prvi,op,faktor_drugi)
            else:
                self.faktor = f
            
        elif self >> {Ri.CONCAT,Ri.UNIJA}: #binaran
            op = self.zadnji
            
            faktor_prvi = self.faktor
            faktor_drugi = self.izraz()
            print(faktor_prvi, faktor_drugi)
            
            self.faktor = False
            return BINARNI(faktor_prvi,op,faktor_drugi)
        
        elif self >> {Ri.PLUS, Ri.ZVIJEZDA, Ri.UPITNIK}:
            op = self.zadnji
            faktor_prvi = self.faktor
            
            self.faktor = False
            return UNARNI(faktor_prvi,op)
        elif self >> {Ri.EPSILON, Ri.PRAZAN}:
            
            if self.faktor:
                op = Ri.CONCAT
                faktor_prvi = self.faktor
                faktor_drugi = self.zadnji
            
                self.faktor = False
                return BINARNI(faktor_prvi,op,faktor_drugi)
            else:
                self.faktor = self.zadnji
        else:
            self.greška()
            

    def znakovi(self):
        znakovi = []
        while self >> Ri.ZNAK:
            znakovi.append(self.zadnji)
        return znakovi

    def izraz(self):
        if self >> Ri.OTV:
            self.izraz()
            self.pročitaj(Ri.ZATV)
            
    
class PROGRAM(AST('naredbe')): pass
class UNARNI(AST('faktor1 operator')): pass
class BINARNI(AST('faktor1 operator faktor2 ')): pass

if __name__ == '__main__':
    lex = ri_lex('''\
    ** kako
    ''')

    print(*lex)
    regex = '/1|a(/(c?)*'

    print(*ri_lex(regex))
    print(ri_par.parsiraj(ri_lex('/1|a(/(c?)*')))

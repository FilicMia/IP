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
        izrazi = []
        self.faktor1 = False
        while not self >> E.KRAJ:
            self.faktor1 = self.izraz()
            print('...', self.faktor1)
            print('------------------------')

    #ZA LIJEVO ASOCIRANE OPERATORE - BITNO PROVJERITI
#JE LI SE NALAZE IZA BILO KOJE CJELINE NA KOJU SE MOGU PRIMJENITI.
# IZA (...),BINARAN(faktor1, op, faktor2),UNARAN(faktor1, op) cjeline ili ZNAK-a       
    def provjeri_unaran(self,unarni):

        while True:
                sljedeći = self.čitaj()
                if not sljedeći ** {Ri.PLUS, Ri.ZVIJEZDA, Ri.UPITNIK}:
                    self.vrati()
                    break
                unarni = UNARNI(unarni, self.zadnji.sadržaj)
        return unarni

    def izraz(self):
        
        if self >> Ri.OTV:
            self.vrati()
            unarni = self.faktor()
            
            if self.faktor1:
                op = Ri.CONCAT.value
                faktor_prvi = self.faktor1
                faktor_drugi = unarni
            
                self.faktor1 = False
                return self.provjeri_unaran(BINARNI(faktor_prvi,op,faktor_drugi))
            else:
                self.faktor1 = unarni
                return self.izraz()
            
        elif self >> Ri.ZNAK:
            unarni = self.provjeri_unaran(ELEMENT(self.zadnji))
            
            if self.faktor1:
                op = Ri.CONCAT.value
                faktor_prvi = self.faktor1
                self.faktor1 = False
                faktor_drugi = unarni
                
                return self.provjeri_unaran(BINARNI(faktor_prvi,op,faktor_drugi))
            else:
                self.faktor1 = ELEMENT(unarni)
                return self.izraz()
            
        elif self >> {Ri.CONCAT,Ri.UNIJA}: #binaran
            op = self.zadnji.sadržaj
           
            faktor_prvi = self.faktor1
            self.faktor1 = False
            faktor_drugi = self.faktor()
            
            return self.provjeri_unaran(BINARNI(faktor_prvi,op,faktor_drugi))
        
        elif self >> {Ri.PLUS, Ri.ZVIJEZDA, Ri.UPITNIK}:
            self.vrati()
            faktor_prvi = self.faktor1
            
            self.faktor1 = False
            return self.provjeri_unaran(faktor_prvi)
        elif self >> {Ri.EPSILON, Ri.PRAZAN}:
            unarni = self.provjeri_unaran(ELEMENT(self.zadnji))
            
            if self.faktor1:
                op = Ri.CONCAT.value
                faktor_prvi = self.faktor1
                self.faktor1 = unarni
                faktor_drugi = self.izraz()
            
                self.faktor1 = False
                return self.provjeri_unaran(BINARNI(faktor_prvi,op,faktor_drugi))
            else:
                
                self.faktor1 = unarni
                return self.izraz()
        elif self >> {E.KRAJ,Ri.ZATV,Ri.OTV}:
            if self.faktor1:
                self.vrati()
                return self.provjeri_unaran(self.faktor1)
            
        else:
            self.greška()
            

    def faktor(self):
        f = False
        if self >> Ri.OTV: #Ako čitamo otv zagradu, onda se ono unutra ne
            # smije primjeniti  (zagrade su izolacija)
            # na ništa prije. Čistimo self.faktor1, i čuvamo za implicitnu
            # konkatenaciju kasnije.
            # Primjetimo kako ne moče vezivati
            # self.faktor i ono što će biti pročitano jer:
            # Ako je koji od binarnih znakova bio između
            # self.faktor1 i OTV, ova funkcija se ne bi odma pozvala, nego
            # bi ušli u if dio f-je izraz koji bi prvo očistio self.faktor1,
            # ostaje prazan.
            prvi = self.faktor1
            self.faktor1 = False
            f = self.izraz()
            self.pročitaj(Ri.ZATV)
            f = self.provjeri_unaran(f)
            if prvi: # Dakle, tu ne bi ušli. Ako nešto ipak postoji odprije,
                # implicitna konkatenacija s novopročitanim i ovo će
                # to nešto konkatenirati s novopročitanim dijelom
                return self.provjeri_unaran(BINARNI(prvi,Ri.CONCAT.value,f))
        elif self >> Ri.ZNAK:   
            f = self.zadnji
        return self.provjeri_unaran(ELEMENT(f))
            
            
    
class UNARNI(AST('faktor1 operator')): pass # ko binarni
class BINARNI(AST('faktor1 operator faktor2 ')): pass # prema op bira operaciju iz RI
class ELEMENT(AST('element')): pass #samo čita svoj element

if __name__ == '__main__':
    lex = ri_lex('''\
    ** kako
    ''')

    print(*lex)
    regex = '/1|a(/(c?)*'

    print(*ri_lex(regex))
    print(ri_par.parsiraj(ri_lex('/1|a(/(c?)*/1|a(/(c?)*')))

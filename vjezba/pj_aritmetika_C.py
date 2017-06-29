from setimportpath import *
from RI import *
from pj import *
import cmath

"""
Lexer za arimetiku nad C.
Svi zapisi su u notaciji cijeli_broj(e(-?)cijeli_broj)
1.23 je zapisan kao 123e-2.
'i' je imaginarna jedinica i kao takva se ne
koristi kao ime neke varijable.
"""

class C(enum.Enum):
    BROJ = '123e-14' #počine ili brojem ili s e / ne dopuštamo e i pi i ta
    PLUS,MINUS,PUTA,KROZ,OTV,ZATV = '+-*/()'
    MINUS1 = 'unarni -'
    NA = '**'
    IME = 'neko ime'
    I = 'i'
    STRELICA = '->'
    KRAJNAREDBE = '\n' # strelica pridružuje onome imenu
    #na desno izraz na lijevoj str

def broj(lex):
    znak = lex.čitaj()
    if znak.isnumeric():
        lex.zvijezda(str.isnumeric)
    znak = lex.čitaj()
    if znak == 'e':
        znak = lex.pogledaj()
        if znak == '-': lex.čitaj()
        if znak.isnumeric():
            lex.zvijezda(str.isnumeric)
        else:
            lex.vrati() #ako nema iza e broja, e ne pripada broju
    else:
        lex.vrati()
    return
    
    

def lex_C(string):
    lex = Tokenizer(string)
    unarni = True
    for znak in iter(lex.čitaj,''):
        if znak.isspace():
            if znak == '\n':
                unarni = True
                yield lex.token(C.KRAJNAREDBE)
            lex.token(E.PRAZNO)
        elif znak.isnumeric():
            lex.vrati()
            broj(lex)
            unarni = False
            yield lex.token(C.BROJ)
        elif znak == '*':
            unarni = True
            znak = lex.pogledaj()
            if znak == '*':
                lex.čitaj()
                yield lex.token(C.NA)
            else:
                yield lex.token(C.PUTA)
        elif znak == '^':
            unarni = True
            yield lex.token(C.NA)
        elif znak == '-':
            if lex.pogledaj() == '>':
                unarni = True
                lex.čitaj()
                yield lex.token(C.STRELICA)
            else:
                unarni = True
                if unarni:
                    yield lex.token(C.MINUS1)
                else:
                    yield lex.token(C.MINUS)
                    
        elif znak.isalpha():
            unarni = False
            lex.zvijezda(identifikator)
            yield lex.token(operator(C,lex.sadržaj) or C.IME) #ili i ili neko ime
            
        else:
            yield lex.token(operator(C,lex.sadržaj) or E.GREŠKA)
            unarni = znak != ')' #iza ) jedino ne može


"""
Parser:
BKG:
start -> naredba | naredba start # IME je izraz
naredba-> izraz KRAJNAREDBE | izraz STRELICA izraz KRAJNAREDBE
izraz -> član PLUS izraz | član | član MINUS izraz
član -> faktor PUTA član | faktor | faktor KROZ član
faktor -> baza NA faktor | baza
baza -> OTV izraz ZATV | BROJ | MINUS1 BROJ | IME | I

"""

class Cpar(Parser):
    def start(self):
        naredbe = []
        while not self >> E.KRAJ:
            naredbe.append(self.naredba())

        return PROGRAM(naredbe)
        
    def naredba(self):
        izraz = self.izraz()
        if self >> C.KRAJNAREDBE:
            return izraz
        elif self >> C.STRELICA:
            
            izraz2 = self.izraz()
            kraj = self.čitaj()
            if kraj ** E.KRAJ:
                self.vrati()
                return STRELICA(izraz,izraz2) #Svaka naredba svoj red
            elif kraj ** C.KRAJNAREDBE:
                return STRELICA(izraz,izraz2)
            else:
                self.greška()
                
        elif self >> E.KRAJ:
            self.vrati()
            return izraz
        else:
            self.greška()

    def izraz(self):
        član = self.član()
        if self >> C.PLUS:
            izraz = self.izraz()
            return PLUS(član, izraz)
        elif self >> C.MINUS:
            izraz = self.izraz()
            return MINUS(član, izraz)
        else:
            return član
        
    def član(self):
        faktor = self.faktor()
        if self >> C.PUTA:
            član = self.član()
            return PUTA(faktor, član)
        elif self >> C.KROZ:
            član = self.član()
            return KROZ(faktor,član)
        else:
            return faktor
            
    def faktor(self):
        baza = self.baza()
        if self >> C.NA:
            faktor = self.faktor()
            return NA(baza, faktor)
        else:
            return baza
    def baza(self):
        if self >> C.OTV:
            uzagradi = self.izraz()
            self.pročitaj(C.ZATV)
            return uzagradi
        elif self >> C.BROJ:
            return BROJ(self.zadnji)
        elif self >> C.IME:
            return IME(self.zadnji)
        elif self >> C.MINUS1:
            broj = self.pročitaj(C.BROJ,C.IME)
            return MINUS1(broj)
            

def C_inter(par):
    return par.izvrši()

class PROGRAM(AST('naredbe')):
    
    def izvrši(self):
        okolina = {}
        for naredba in self.naredbe:
            naredba.izvrši(okolina)
        return okolina
    
class BINARNI(AST('faktor1 faktor2')): pass
class PUTA(BINARNI):
    def izvrši(self,okolina):
        f1 = self.faktor1.izvrši(okolina)
        f2 = self.faktor2.izvrši(okolina)
       
        return float(f1)*float(f2)

class PLUS(BINARNI):
    def izvrši(self,okolina):
        f1 = self.faktor1.izvrši(okolina)
        f2 = self.faktor2.izvrši(okolina)
        for ime, value in okolina.items():
            if type(f1) != float:
                f1 = f1.replace(ime, str(value))
            if type(f2) != float:
                f2 = f2.replace(ime, str(value))
        return float(f1)+float(f2)
class NA(BINARNI):
    def izvrši(self,okolina):
        f1 = self.faktor1.izvrši(okolina)
        f2 = self.faktor2.izvrši(okolina)
        for ime, value in okolina.items():
            if type(f1) != float:
                f1 = f1.replace(ime, str(value))
            if type(f2) != float:
                f2 = f2.replace(ime, str(value))
        
        return float(f1)**float(f2)
class MINUS(BINARNI):
    def izvrši(self,okolina):
        f1 = self.faktor1.izvrši(okolina)
        f2 = self.faktor2.izvrši(okolina)
        for ime, value in okolina.items():
            if type(f1) != float:
                f1 = f1.replace(ime, str(value))
            if type(f2) != float:
                f2 = f2.replace(ime, str(value))
        
        return float(f1)-float(f2)
class MINUS1(AST('broj')):
    def izvrši(self,okolina):
        broj = self.broj.sadržaj
        for ime, value in okolina.items():
            broj.replace(ime, value)
        return -float(broj)
class BROJ(AST('broj')):
    def izvrši(self,okolina):
        broj = self.broj.sadržaj
    
        return float(broj)
    
class KROZ(BINARNI):
    def izvrši(self,okolina):
        f1 = self.faktor1.izvrši(okolina)
        f2 = self.faktor2.izvrši(okolina)
        for ime, value in okolina.items():
            if type(f1) != float:
                f1 = f1.replace(ime, str(value))
            if type(f2) != float:
                f2 = f2.replace(ime, str(value))
       
        return float(f1)/float(f2)
class STRELICA(BINARNI):
    def izvrši(self,okolina):
        f1 = self.faktor1.izvrši(okolina)
        f2 = self.faktor2.izvrši(okolina)
        for ime, value in okolina.items():
            if type(f1) != float:
                f1 = f1.replace(ime, str(value))
            

        okolina[f2] = float(f1)
        return okolina

class IME(AST('ime')):
    def izvrši(self,okolina):
        return self.ime.sadržaj   


tests = [1]
if __name__ == '__main__':

    if 1 in tests:
        string = '2 -> a \n a^2^2^2^2^0 -> b \n'
        print('Lexer: ')
        print(*lex_C(string))

        print('parser')
        lex = lex_C(string)
        print(Cpar.parsiraj(lex))

        print('inter') #bez imaginarnih brojeva
        lex = lex_C(string)
        par = Cpar.parsiraj(lex)
        print(C_inter(par))











            
            
            
        

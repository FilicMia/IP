from pj import *

#I i iLI su iste razine prioriteta dok ' ima veću
class DS(enum.Enum):
    NE = '\'' #unarni - postfikt lijevoasocirani
    #I = 'nista' #binarni ili više
    ILI = '+' #binarni ili više
    OOTV = '('
    OZATV = ')' # zaseban sklop
    UOTV = '[' #zasebni sklop s negiranim izlazom
    UZATV = ']'
    SLOVO = 'a'

def specijalan(znak):
    return znak in '\'[]()+'
    
def ds_lex(string):
    lex = Tokenizer(string)
    for znak in iter(lex.čitaj, ''):
        if znak.isspace(): lex.token(E.PRAZNO)
        elif specijalan(znak):
            yield lex.token(operator(DS,znak) or E.GREŠKA)
        elif znak.isalpha():
            yield lex.token(DS.SLOVO)
        else:
            yield lex.token(E.GREŠKA)
            
            


""" Beskontekstna gramatika
 sklop -> član
 izraz -> OOTV član OZATV | UOTV član UZATV     #jedna cjelina koja ulazi u
                                                #jedna sklop, obavezno u nekim zagradma
                                                  
 član -> dio ILI zbrojevi | dio faktori | dio
                                           # zaustavlja ih zagrede
                                           #i E.KRAJ 

 zbrojevi ->dio ILI zbrojevi | dio 
 faktori -> dio faktori | dio
 
 dio -> SLOVO | SLOVO NE | izraz | izraz NE
"""
def provjeri_negaciju(par, izraz):
    while True:
            sljedeći = par.čitaj()
            if not sljedeći ** DS.NE:
                par.vrati()
                break
            izraz = Not(izraz)
    return izraz

class DSParser(Parser):
    def sklop(self):
        izrazi = []
        while not self >> E.KRAJ:
            izrazi.append(self.član())

        if len(izrazi) > 1:
            return And(izrazi)
        else:
            return izrazi[0]
    


    def izraz(self):
        if self >> DS.OOTV:
            izraz = self.član()
            self.pročitaj(DS.OZATV)

        elif self >> DS.UOTV:
            izraz = self.član()
            self.pročitaj(DS.UZATV)
            izraz = Not(izraz)
        else:
            self.greška()
            
        return provjeri_negaciju(self,izraz)

    def član(self):
        dio = self.dio() #vraca 1 clan liste
        
        if self >> DS.ILI:
            return self.zbrojevi([dio])
        elif not self >> {E.KRAJ, DS.OZATV, DS.UZATV}:
            return self.faktori([dio])
        else:
            self.vrati()
            return dio

    def zbrojevi(self, prije):
        
        pribrojnici = []+prije
        pribrojnici.append(self.dio())
        
        if self >> DS.ILI:
            return self.zbrojevi(pribrojnici)
        else:
            return Or(pribrojnici)

        
    def faktori(self, prije):
        fakt = []+prije
        fakt.append(self.dio())
        
        if not self >> {E.KRAJ, DS.OZATV, DS.UZATV}:
            return self.faktori(fakt)
        else:
            self.vrati()
            return And(fakt)
        
    def dio(self): # dio -> SLOVO | SLOVO NE | izraz | izraz NE
        if self >> DS.SLOVO:
            iz = self.zadnji
            return provjeri_negaciju(self, iz)
        elif not self >> {E.KRAJ,DS.UZATV,DS.OZATV}:
            iz = self.izraz()
            return provjeri_negaciju(self,iz)
        else:
            self.vrati()

    start = sklop


class And(AST('ulazi')): pass
class Or(AST('ulazi')): pass
class Not(AST('ulaz')): pass

"""
Napišite semantički analizator u obliku NAND-realizatora za jezik DS.
NAND vrata reprezentirajte običnim listama čiji elementi su slova
(stringovi duljine 1) ili iste takve liste. Primjerice, ['x','y',['x']]
je sklop od dva NAND vrata:
jedna imaju 1 ulaz, x, dok druga imaju 3 ulaza: x, y i izlaz
iz prvih (koji je negacija od x)

"""


def uNand(sklop):
    if sklop ** And: #AND je kompozicija od NOT i NAND
        ulazi = [Not(x) for x in sklop.ulazi]
        
        return [[uNand(x) for x in sklop.ulazi]]
        #return uNand(Or(sklop.ulazi))
    elif sklop ** Not:
        if sklop.ulaz ** DS.SLOVO:
            return [sklop.ulaz.sadržaj]
        else:
            return [uNand(sklop.ulaz)]
    elif sklop ** Or: #OR može dobiti de Morganovim pravilom
        return [uNand(Not(x)) for x in sklop.ulazi]
        #ulazi = [Not(x) for x in sklop.ulazi] #(x'y'z')'
        #return uNand(And(ulazi))
    elif sklop ** DS.SLOVO:
        return sklop.sadržaj
    else: assert not 'slučaj'

        
def pod_negacijom(sklop):
    """Vraća x ako je sklop == [x], inače None."""
    if isinstance(sklop, list) and len(sklop) == 1: return sklop[0]

def optimiziraj(nand,početak=True):
    print(str(nand))
    if len(nand) == 1 and len(nand[0]) == 1:
        if not početak:
            return nand[0][0]
        else:
            return nand
    else:
        return [optimiziraj(item,False) for item in nand]


tests = [41]
if __name__ == '__main__':
    if 1 in tests:
        print('parser')
        opis = "x([yxx']+y')"
        tokeni = list(ds_lex(opis))
        print(*tokeni)  # SLOVO'x' OOTV'(' UOTV'[' SLOVO'y' SLOVO'x' SLOVO'x'
                # NE"'" UZATV']' ILI'+' SLOVO'y' NE"'" OZATV')'
    if 11 in tests:    
        print('lexer')
        opis = "[yxx]+y"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        print(ast)  # And(ulazi=[
                    #   SLOVO'x',
                    #   Or(ulazi=[
                    #     Not(ulaz=And(ulazi=[SLOVO'y', SLOVO'x', Not(ulaz=SLOVO'x')])),
                    #     Not(ulaz=SLOVO'y')
                    #   ])
                    # ])
    if 2 in tests:
        print('lexer')
        opis = "x([yxx']+y')"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        print(ast)  # And(ulazi=[
                    #   SLOVO'x',
                    #   Or(ulazi=[
                    #     Not(ulaz=And(ulazi=[SLOVO'y', SLOVO'x', Not(ulaz=SLOVO'x')])),
                    #     Not(ulaz=SLOVO'y')
                    #   ])
                    # ])
    if 21 in tests:
        print('lexer')
        opis = "(pk)"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        print(ast)  # And(ulazi=[
                    #   SLOVO'x',
                    #   Or(ulazi=[
                    #     Not(ulaz=And(ulazi=[SLOVO'y', SLOVO'x', Not(ulaz=SLOVO'x')])),
                    #     Not(ulaz=SLOVO'y')
                    #   ])
                    # ])
        print(ast.ulazi)
        
    if 30 in tests:
        print('lexer')
        opis = "p+k+z"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        print(ast)
        print('ast')
        opis = "p+k+z"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        nand = uNand(ast)
        print(nand)
    if 31 in tests:
        print('ast')
        opis = "pkz"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        nand = uNand(ast)
        print(nand)
        
    if 3 in tests:
        print('uNand')
        opis = "x([yxx']+y')"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        nand = uNand(ast)
        print(nand)  # [['x', [[[[['y', 'x', ['x']]]]], [['y']]]]]
    if 41 in tests:
        opis = "x([yxx']+y')"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        nand = uNand(ast)
        opt = optimiziraj(nand)
        print('opt')
        print(opt)  # [['x', [[['y', 'x', ['x']]], 'y']]]
    if 4 in tests:
        opis = "x([yxx']+y')"
        tokeni = list(ds_lex(opis))
        ast = DSParser.parsiraj(tokeni)
        nand = uNand(ast)
        opt = optimiziraj(nand)
        print(opt)  # [['x', [[['y', 'x', ['x']]], 'y']]]

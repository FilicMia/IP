"""Napišite leksički analizator za JavaScript funkcije. 
JavaScript funkcija počinje ključnom riječi function, zatim slijedi ime 
funkcije, pa lista parametara, te tijelo funkcije unutar vitičastih zagrada. 
Tijelo funkcije sastoji se od linijskih komentara (//) i od naredbi 
(niz znakova koji završava s ;). Npr.

function ime (var x, var y, ...){

         //neke naredbe odvojene s ; ili komentar

}

Napišite sintaksni analizator za prepoznavanje ispravno napisanih 
JavaScript funkcija iz prvog zadatka. Analizator treba pretvoriti 
zadani JavaScript program (koji se sastoji samo od funkcija) 
u apstraktna sintaksna stabla: Program, Funkcija, Naredba. 
U tijelu funkcije dozvolite više naredbi odvojenih s 
; i linijske komentare.
"""
from setimportpath import *
from pj import *
"""
Lexer:
BESKONTEKSTNA GRAMATIKA:

program -> praznine FUNCTION praznine IME praznine OTV praznine parametri praznine 
			ZATV praznine VITOTV praznine tijelo praznine VITZATV praznine
tijelo -> linijskikomentari praznine tijelo | naredbe praznine tijelo | EPS

parametri -> parametar | VAR praznine IME praznine ZAREZ praznine parametri
parametar -> VAR praznine IME | EPS

linijskikomentari -> KOSE KOMENTAR praznine linijskikomentari | EPS
naredbe -> NAREDBA praznine naredbe | EPS

praznine -> EPS

NAREDBA = (asalnum or '_') //nema pokazivača
KOMENTAR = ((\n)^c)*\n //sve dok ne pročitamo znak za novi red ili kraj dokumenta.
"""
class JS(enum.Enum):
	FUNCTION = 'function'
	IMENAREDBA = 'ime_naredba'
	VAR = 'var'
	OTV = '('
	ZATV = ')'
	VITOTV = '{'
	VITZATV = '}'
	KOMENTAR = '//'
	ZAREZ = ','
	TOČKAZAREZ = ';'


def js_lex(string):
	lex = Tokenizer(string)
	for znak in iter(lex.čitaj, ''): #čitaj dok ne dođeš do kraja.
		if znak.isspace(): 
			lex.token(E.PRAZNO)
		elif znak.isalpha(): 
			lex.zvijezda(identifikator)
			yield lex.token(ključna_riječ(JS, lex.sadržaj) or JS.IMENAREDBA)
		elif znak == '/':
			drugi = lex.čitaj()
			if(drugi == '/'):
				lex.zvijezda(lambda znak: znak != '\n') #ne pročita '\n'
				yield lex.token(JS.KOMENTAR)
			else:
				yield lex.token(lex.greška())
		else:
			yield lex.token(operator(JS, znak) or lex.greška())

"""
AST:
start: funkcije
funkcija: ime argumenti tijelo
argumenti: ime <- lista
tijelo: elementi (lista)
element: vrsta (naredba ili komentar) sadržaj
"""

class js_parser(Parser):
	
	def start(self):
		funkcije = []
		while not self >> E.KRAJ: funkcije.append(self.funkcija())
		return Program(funkcije)
		
	def funkcija(self): 
		self.pročitaj(JS.FUNCTION)
		ime = self.pročitaj(JS.IMENAREDBA)# semantička analiza je potrebna
		self.pročitaj(JS.OTV)
		argumenti = self.argumenti()
		tijelo = self.tijelo()
		return Funkcija(ime, argumenti,tijelo)
			
	def argumenti(self):
		argumenti = []
		while True: 
			self.pročitaj(JS.VAR)
			argumenti.append(self.pročitaj(JS.IMENAREDBA).sadržaj)
			if self >> JS.ZATV:
				break
			self.pročitaj(JS.ZAREZ)
		return argumenti
		
	def tijelo(self):
		elementi = []
		if not self >> JS.VITOTV: self.greška()
		while not self >> JS.VITZATV: elementi.append(self.element())
		return elementi
	
	def element(self):
		sadržaj = []
		while not self >> JS.TOČKAZAREZ:
			token = self.pročitaj(JS.IMENAREDBA, JS.KOMENTAR)
			sadržaj.append(token)
			if (token ** {JS.KOMENTAR}):
				break
		return Element('KOMENTAR' if token ** JS.KOMENTAR else 'NAREDBA', sadržaj)
	
			
class Program(AST('funkcije')): pass
class Funkcija(AST('ime argumenti tijelo')): pass
class Element(AST('vrsta sadržaj')): pass	

if __name__ == '__main__':
	lexer = js_lex('''\
        function ime (var x, var y, var z) {
            //neke naredbe odvojenih s ; ili komentar
            naredba; naredba //kom
            naredba
        }
    ''')
	try:
		print(*js_parser.parsiraj(lexer))
	except Exception:
		print("error",Exception)
	print('Next')
	lexer = js_lex('''\
        function ime (var x, var y, var z) {
            //neke naredbe odvojenih s ; ili komentar
            naredba; //kom
            ahsjlhla jasj;
        }
    ''')
	for token in iter(lexer):
		print(token)
	print(*js_parser.parsiraj(js_lex('''\
        function ime (var x, var y, var z) {
            //neke naredbe odvojenih s ; ili komentar
            naredba; //kom
            ahsjlhla jasj;
        }
    ''')))
				
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

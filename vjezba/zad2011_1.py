"""
Napišite leksički analizator za „programski jezik“ koji radi sa vezanom 
listom u kojoj se nalaze cijeli brojevi (niz znamenki). Jezik treba 
omogućiti deklariranje liste (LISTA L1), gdje se ime liste sastoji od 
jednog velikog slova 'L' i jedne znamenke od 1 do 9 (dakle, možemo 
deklarirati maksimalno 9 listi). Operacije za rad sa listom su uobičajene: 
provjera je li lista prazna (PRAZNA L1), stavljanje elementa u listu na 
određeno mjesto (UBACI L1 2345 3 – ubacuje element 2345 na treće mjesto 
u listi L1), brisanje elementa iz liste (IZBACI L1 3 – izbacuje element 
s treće pozicije iz liste L1), dohvat elementa is liste (DOHVATI L1 3 – 
vraća element koji se u listi L1 nalazi na trećoj poziciji) i vraćanje 
duljine liste (KOLIKO L1). Napišite sintaksni analizator za taj 
programski jezik (svaka vrsta naredbe odgovara jednom tipu 
apstraktnog sintaksnog stabla). Napišite i odgovarajući semantički 
analizator (interpreter).

"""
from setimportpath import *
from pj import *

"""
BESKONTEKSTNA GRAMATIKA: hhh
start -> praznine naredba start | EPS
naredba ->  lista |  prazna |  ubaci | 
			 izbaci |  dohvati |  koliko |
			praznine 
lista -> LISTA IMELISTE
prazna -> PRAZNA IMELISTE
ubaci -> UBACI IMELISTE element pozicija
izbaci -> IZBACI IMELISTE pozicija
dohvati -> DOHVATI IMELISTE pozicija
koliko -> KOLIKO IMELISTE
praznine -> EPS

element -> BROJ | MINUSBROJ
pozicija -> BROJ


RI za varijable:
IMELISTE = L[1-9]
BROJ = [1-9][0-9]* ili 0
MINUSBROJ = -[1-9][0-9]*
"""
class LST(enum.Enum):
	IME = "ime"
	BROJ = 123
	MINUSBROJ = -123
	LISTA = "LISTA"
	PRAZNA = "PRAZNA"
	UBACI = "UBACI"
	IZBACI = "IZBACI"
	DOHVATI = "DOHVATI"
	KOLIKO = "KOLIKO"
	


def lista_lex(string):
	lex = Tokenizer(string)
	znak = lex.čitaj()
			
	for znak in iter(lex.čitaj,''):
		if znak.isspace():
			lex.token(E.GREŠKA)
		elif znak.isdigit():
			lex.zvijezda(lambda znak: znak != '' and (not znak.isspace()))
			if lex.sadržaj.isdigit():
				yield lex.token(LST.BROJ)
			else: 
				yield lex.token(E.GREŠKA)
		elif znak == '-':
			lex.zvijezda(lambda znak: znak != '' and (not znak.isspace()))
			if lex.sadržaj.isdigit():
				yield lex.token(LST.MINUSBROJ)
				while znak.isspace(): znak = lex.čitaj()
			else: 
				yield lex.token(E.GREŠKA)
		else:
			if znak == 'L':
				drugi = lex.čitaj()
				if drugi.isdigit():
					yield lex.token(LST.IME)
					continue
			lex.zvijezda(lambda znak: znak != '' and (not znak.isspace()))
			yield lex.token(ključna_riječ(LST,lex.sadržaj,False) or E.GREŠKA)
		
				

class Lista_parser(Parser):
	def start(self):
		naredbe = []
		while not self >> E.KRAJ: naredbe.append(self.naredba()) 
		return naredbe
	
	def naredba(self):
		if self >> LST.LISTA:
			return Lista(self.pročitaj(LST.IME))
		elif self >> LST.PRAZNA:
			return Prazna(self.pročitaj(LST.IME))
		elif self >> LST.UBACI:
			return Ubaci(self.pročitaj(LST.IME),self.pročitaj(LST.BROJ,LST.MINUSBROJ),
			self.pročitaj(LST.BROJ))
		elif self >> LST.IZBACI:
			return Izbaci(self.pročitaj(LST.IME),self.pročitaj(LST.BROJ))
		elif self >> LST.DOHVATI:
			return Dohvati(self.pročitaj(LST.IME),self.pročitaj(LST.BROJ))
		elif self >> LST.KOLIKO:
			return Koliko(self.pročitaj(LST.IME))
		else:
			self.greška()
		

class Lista(AST('ime')): pass
class Prazna(AST('ime')): pass
class Ubaci(AST('ime element pozicija')): pass
class Izbaci(AST('ime pozicija')): pass
class Dohvati(AST('ime pozicija')): pass
class Koliko(AST('ime')): pass

"""
Semantički analizator.

"""

lexer = lista_lex('LSTA L1 889')
for l in lexer:
	print(l)

lexer = lista_lex('LISTA L1')
print(*Lista_parser.parsiraj(lista_lex('''lista L1  lista L3 ubaci L3 45 0  dohvati L3 0''')))





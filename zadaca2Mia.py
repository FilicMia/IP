"""
Napišite leksički analizator za pseudo-XHTML dokument koji sadrži samo liste. Cijeli dokument je uokviren samo u <html> element koji se sastoji od zaglavlja <head> i tijela <body>. Zaglavlje smije sadržavati samo običan tekst, a tijelo se sastoji od običnog teksta i listi. Liste mogu biti uređene <ol> i neuređene <ul>. Lista se sastoji od <li> elemenata. U jednom elementu liste smije se nalaziti običan tekst ili nova lista, ali ne i oboje. Dokument može sadržavati proizvoljan broj listi. Poštujte uobičajena pravila za XHTML dokumente.

Napišite sintaksni analizator za pseudo-XHTML dokumente iz prvog zadatka. Provjerite uobičajena XHTML pravila: je li cijeli dokument uokviren u <html> elemente, je li odnos XHTML elemenata odgovarajući , je li svaki element i zatvoren, jesu li svi elementi napisani malim slovima, jesu li elementi odgovarajuće ugnježdeni, itd. Omogućite i da se u <li> elementu liste, osim običnog teksta, može pojaviti i nova lista (ali ne i oboje). Liste smiju sadržavati samo <li> elemente (ne tekst i ne direktno druge liste).

Napišite i odgovarajući „semantički“ analizator (rendered) za XHTML liste iz prvog zadatka. Za svaki <li> element iz neuređene liste ispišite tabulator, „*“, sadržaj <li> elementa ako se radi o tekstu, te znak za prijelom retka. Ako je sadržaj <li> elementa nova lista, onda samo ispišite novu listu. Elemente liste s prve razine treba ispisati s jednim tabulatorom na početku, a za svaku dodatnu razinu treba ispisati i dodatni tabulator (npr. lista unutar liste počinje s dva tabulatora, itd.).
"""


from pj import *

class XHTML(enum.Enum):
	HTMLOTV = '<html>' #"""cijeli dokument uokviren u ovo - proizvoljno listi"""
	HEADOTV = '<head>' #"""samo obican tekst"""
	BODYOTV = '<body>' #"""samo obican tekst i liste"""
	OLOTV = '<ol>' #"""samo li elemente!!"""
	ULOTV = '<ul>'
	LIOTV = '<li>' #"""ili tekst ili obicna list"""
	HTMLZATV = '</html>' #"""cijeli dokument uokviren u ovo - proizvoljno listi"""
	HEADZATV = '</head>' #"""samo obican tekst"""
	BODYZATV = '</body>' #"""samo obican tekst i liste"""
	OLZATV = '</ol>' #"""samo li elemente!!"""
	ULZATV = '</ul>'
	LIZATV = '</li>' #"""ili tekst ili obicna list"""	

	TEKST = 'nekitekst'

escapeChars = ['<','>','']

"""PRVO lekser pa sintaksni analizator"""


"""Lekser"""


"""
program -> HTMLOTV uhtml HTMLZATV

uhtml -> (HEADOTV TEKST HEADZATV) (BODYOTV ubody BODYZATV) 

ubody  -> TEKST ubody  | LISTA ubody | EPS

LISTA -> OLOTV ulisti OLZATV | ULOTV ulisti ULZATV

ulisti -> LIOTV uli LIZATV ulisti | EPS

uli -> TEKST | LISTA | EPS
"""
"""------------------------------------------------------------
------------------------------------------------------------"""
"""Provjerava je li <(\?)nešto> dobar XHTML tag za dani zadatak."""

def provjeri(lex,prvo,otv=True):
	if prvo == 'h':
		drugo = lex.čitaj() #sadržaj token ačini sve proččitano od kreacije zadnjeg tokena
		if drugo == 't':
			lex.pročitaj('m')
			lex.pročitaj('l')
			lex.zvijezda(str.isspace or '')
			lex.pročitaj('>')
			if otv: yield lex.token(XHTML.HTMLOTV)
			else: yield lex.token(XHTML.HTMLZATV)
		elif drugo == 'e':
			lex.pročitaj('a')
			lex.pročitaj('d')
			lex.zvijezda(str.isspace or '')
			lex.pročitaj('>')
			if otv: yield lex.token(XHTML.HEADOTV)
			else: yield lex.token(XHTML.HEADZATV)
		else: lex.greška('očekiva se tml> ili ead>')

	elif prvo == 'b':
		lex.pročitaj('o')
		lex.pročitaj('d')
		lex.pročitaj('y')
		lex.zvijezda(str.isspace or '')
		lex.pročitaj('>')
		if otv: yield lex.token(XHTML.BODYOTV)
		else: yield lex.token(XHTML.BODYZATV)
	elif prvo == 'o':
		lex.pročitaj('l')
		lex.zvijezda(str.isspace or '')
		lex.pročitaj('>')
		if otv: yield lex.token(XHTML.OLOTV)
		else: yield lex.token(XHTML.OLZATV)

	elif prvo == 'u':
		lex.pročitaj('l')
		lex.zvijezda(str.isspace or '')
		lex.pročitaj('>')
		if otv: yield lex.token(XHTML.ULOTV)
		else: yield lex.token(XHTML.ULZATV)

	elif prvo == 'l':
		lex.pročitaj('i')
		lex.zvijezda(str.isspace or '')
		lex.pročitaj('>')
		if otv: yield lex.token(XHTML.LIOTV)
		else: yield lex.token(XHTML.LIZATV)

	else: yield lex.token(lex.greška())

"""
Lexer
"""
def xhtml_lex(kôd):
	lex = Tokenizer(kôd)
	for znak in iter(lex.čitaj, ''):
		if znak == '<':
			prvo = lex.čitaj()
			if prvo == '/':
				drugo = lex.čitaj()
				for izraz in iter(provjeri(lex,drugo,False)):
					yield izraz #"""pročitaj zatvorene tagove"""	
			else: 
				for izraz in iter(provjeri(lex,prvo)):
					yield izraz
		else:
			lex.zvijezda(lambda znak: znak not in escapeChars) #"""Pridjeli nesto tekstu"""
			yield lex.token(XHTML.TEKST)



"""
Za svaku varijablu koja na desnoj strani nema samo tokene, napisi funkciju,
Za svaku varijablu koja je na lijevoj strani, napiši AST.
"""
"""
program -> HTMLOTV uhtml HTMLZATV

uhtml -> (HEADOTV TEKST HEADZATV) (BODYOTV ubody BODYZATV) 

ubody  -> TEKST ubody  | LISTA ubody | EPS

LISTA -> OLOTV ulisti OLZATV | ULOTV ulisti ULZATV

ulisti -> LIOTV uli LIZATV ulisti | EPS

uli -> TEKST | LISTA | EPS

uli -> TEKST uli | LISTA uli | EPS NAPREDNO!! identicno ko ubody

"""
tests = [1,2,3]
		


"""
AST:
program: html 
html: head body
head: tekst
body: elementi
elementi su tekst,ol,ul cuvani u listi elementi[] koje dodajemo
def start(self):
        elementi = []
        while not self >> E.BODY: elementi.append(self.element())
        #provjera dobrog zatvorenja.
        return Program(elementi)

tekst: string koj cini tekst token.sadržaj
ol/li: vrsta = (ol,ul) clanovi <- list li_jeva
clan:  lista elemenata idi do kada ne oddes na </li>
		sto, definiraj pomoću XHTML.OLOTV/ULOTV ili TEKST
"""

class xhtml_parser(Parser):
	def start(self):
		naredbe = []
		self.pročitaj(XHTML.HTMLOTV)
		while not self >> XHTML.HTMLZATV: naredbe.append(self.naredba())
		if not len(naredbe) == 1: self.greška()
		return Program(naredbe[0])
	#citaj head and body	
	def naredba(self):
		#if prvi ** XHTML.TEKST: 
		#	if not (prvi.sadržaj and prvi.sadržaj.strip()):
		#		return self.greška()

		self.pročitaj(XHTML.HEADOTV)
		head = Head(self.pročitaj(XHTML.TEKST))
		self.pročitaj(XHTML.HEADZATV)
		
		elementi = []
		self.pročitaj(XHTML.BODYOTV)
		while not self >> XHTML.BODYZATV: elementi.append(self.element())
		return Html(head,Body(elementi))
		
	
	#prouči sve elemente			
	def element(self):
			
			if self >> XHTML.TEKST: return Tekst(self.zadnji.sadržaj)
			elif self >> XHTML.OLOTV: 
				sadrzaj = []
				while not self >> XHTML.OLZATV: sadrzaj.append(self.li())
				
				return Lista(XHTML.OLOTV.value,sadrzaj)
			elif self >> XHTML.ULOTV: 
				sadrzaj = []
				while not self >> XHTML.ULZATV: sadrzaj.append(self.li())
				
				return Lista(XHTML.ULOTV.value,sadrzaj)
			else:
				self.greška()
				
	def li(self):
		sadrzi = []
		if self >> XHTML.LIOTV:
			if self >> XHTML.TEKST: 
				self.vrati()
				sadrzi.append(self.element())
				self.pročitaj(XHTML.LIZATV)
			else:
				while not self >> XHTML.LIZATV: #tek kada dode ce ga pročitati, ostale vraća
					self.pročitaj(XHTML.OLOTV,XHTML.ULOTV)
					self.vrati()
					sadrzi.append(self.element())
				
			return Li(sadrzi)
		else:
			self.greška()


class Program(AST('html')):
    """Program u jeziku xhtml."""
    def izvrši(self):
        return self.html.izvrši()

class Html(AST('head body')):
	
    def izvrši(self):
        return [self.head.izvrši(),self.body.izvrši()]

class Head(AST('tekst')):
	
    def izvrši(self):
        return self.tekst.izvrši()

class Body(AST('elementi')):
	
    def izvrši(self):
        izlazi = []
        for element in elementi:
             izrazi.append(element.izvrši())
        return izlazi

class Element(AST('element')):
	
    def izvrši(self):
        return element.izvrši()

class Tekst(AST('string')):
	def izvrši(self):
		return string
		
class Lista(AST('vrsta clanovi')):
	
	def izvrši(self):
		izlazi = []
		for clan in clanovi:
			izrazi.append(clan.izvrši())
		return (self.vrsta,izlazi)
class Li(AST('elementi')):
	
	def izvrši(self):
		izlazi = []
		for element in elementi:
			izrazi.append(element.izvrši())
		return izlazi
	
if __name__ == '__main__':
	if 1 in tests:
		lexer = xhtml_lex('''<html         ><head>
	  Title of document
	</head><body>
	  <ol><li>neki</li></ol>
	</body></html>
		''')
		for token in iter(lexer):
			print(token) 
	if 2 in tests:
		lexer = xhtml_lex('''<html         ><head>
	  Title of document
	</head><body>
	  <ol><li>neki</li></ol>
	</body></html>''')
		print(*xhtml_parser.parsiraj(lexer))
#prekini citanje nakon HTML	

	

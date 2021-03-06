"""
Napišite leksički analizator za pseudo-XHTML dokument koji sadrži samo liste. Cijeli dokument je uokviren samo u <html> element koji se sastoji od zaglavlja <head> i tijela <body>. Zaglavlje smije sadržavati samo običan tekst, a tijelo se sastoji od običnog teksta i listi. Liste mogu biti uređene <ol> i neuređene <ul>. Lista se sastoji od <li> elemenata. U jednom elementu liste smije se nalaziti običan tekst ili nova lista, ali ne i oboje. Dokument može sadržavati proizvoljan broj listi. Poštujte uobičajena pravila za XHTML dokumente.

Napišite sintaksni analizator za pseudo-XHTML dokumente iz prvog zadatka. Provjerite uobičajena XHTML pravila: je li cijeli dokument uokviren u <html> elemente, je li odnos XHTML elemenata odgovarajući , je li svaki element i zatvoren, jesu li svi elementi napisani malim slovima, jesu li elementi odgovarajuće ugnježdeni, itd. Omogućite i da se u <li> elementu liste, osim običnog teksta, može pojaviti i nova lista (ali ne i oboje). Liste smiju sadržavati samo <li> elemente (ne tekst i ne direktno druge liste).

Napišite i odgovarajući „semantički“ analizator (rendered) za XHTML liste iz prvog zadatka. Za svaki <li> element iz neuređene liste ispišite tabulator, „*“, sadržaj <li> elementa ako se radi o tekstu, te znak za prijelom retka. Ako je sadržaj <li> elementa nova lista, onda samo ispišite novu listu. Elemente liste s prve razine treba ispisati s jednim tabulatorom na početku, a za svaku dodatnu razinu treba ispisati i dodatni tabulator (npr. lista unutar liste počinje s dva tabulatora, itd.).
"""

from setimportpath import *
from pj import *
import re

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
	PRAZANTXT = '\n\t ' #prazan tekst izmedu tagova. <html>      <head> i sl.
	TEKST = 'nekitekst'

escapeChars = ['<','>','']


"""Lekser"""
def provjeri(lex,prvo,otv=True):
	if prvo == 'h':
		drugo = lex.čitaj() #sadržaj token ačini sve pročitano od kreacije zadnjeg tokena
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
		lex.vrati()
		lex.zvijezda(str.isspace)
		znak = lex.čitaj()
		if znak == '<':
			lex.vrati()
			if (lex.sadržaj and (not lex.sadržaj.strip())):
				#možemo ih i ovdje 'pojesti'
				yield lex.token(XHTML.PRAZANTXT)
			
			lex.pročitaj('<')
			prvo = lex.čitaj()
			if prvo == '/':
				drugo = lex.čitaj()
				for izraz in iter(provjeri(lex,drugo,False)):
					yield izraz    #"""pročitaj zatvorene tagove"""	
			else: 
				for izraz in iter(provjeri(lex,prvo)):
					yield izraz
		else:
			lex.zvijezda(lambda znak: znak not in escapeChars) #"""Pridjeli nesto tekstu"""
			if (lex.sadržaj) and (not lex.sadržaj.strip()):
				yield lex.token(XHTML.PRAZANTXT)
			else: yield lex.token(XHTML.TEKST)



"""
Za svaku varijablu koja na desnoj strani nema samo tokene, napisi funkciju,
Za svaku varijablu koja je na lijevoj strani, napiši AST.
"""
"""
program -> HTMLOTV uhtml HTMLZATV

uhtml -> HEADOTV TEKST HEADZATV   BODYOTV ubody BODYZATV 

ubody  -> TEKST ubody  | LISTA ubody | EPS

LISTA -> OLOTV ulisti OLZATV | ULOTV ulisti ULZATV

ulisti -> LIOTV uli LIZATV ulisti #po xhtml pravilu bar 1 li!!!

uli -> TEKST | LISTA | EPS

uli -> TEKST | viselisti ............NAPREDNO!! 

viselisti -> LISTA | LISTA viselisti | EPS ..............NAPREDNO!!

"""

""" BESKONTEKSTNA GRAMATIKA KOJA DOPUŠTA PRAZNINE IZMEĐU XHTML TAGOVA
početka jednoga i kraja drugoga i obratno, zanemaruje ih, tj. 
<html>      <head></head>  <body></body>    </html> je isto kao i
<html><head></head><body></body></html>

program -> praznine HTMLOTV uhtml HTMLZATV praznine

uhtml -> praznine HEADOTV TEKST HEADZATV praznine BODYOTV ubody BODYZATV praznine

ubody  -> TEKST ubody  | praznine LISTA ubody | praznine    #praznine mogu ili u EPS pa nema | EPS

LISTA -> OLOTV ulisti OLZATV | ULOTV ulisti ULZATV

ulisti -> praznine LIOTV uli LIZATV ulistidalje     #lista ne može biti prazna

ulistidalje -> praznine LIOTV uli LIZATV ulistidalje | praznine  #praznine mogu ili u EPS pa nema | EPS

uli -> TEKST | viselisti 

viselisti -> praznine LISTA viselisti | praznine | EPS 

praznine -> PRAZANTXT praznine | EPS

"""

"""
AST:
program: html 
html: head body
head: tekst
body: elementi
elementi su tekst,ol,ul cuvani u listi elementi[] koje dodajemo
tekst: string koj cini tekst token.sadržaj
ol/li: vrsta = (ol,ul) clanovi <- list li_jeva
clan:  lista elemenata idi do kada ne oddes na </li>
		sto, definiraj pomoću XHTML.OLOTV/ULOTV ili TEKST
"""

class xhtml_parser(Parser):#samo jedan html dokument
	def start(self):
		naredbe = []
		while self >> XHTML.PRAZANTXT: pass
		
		self.pročitaj(XHTML.HTMLOTV)
		while not self >> XHTML.HTMLZATV: naredbe.append(self.naredba())
		
		while self >> XHTML.PRAZANTXT: pass
		if not self >> E.KRAJ: self.greška() #do dopuštamo ništa van html-a
		if not len(naredbe) == 1: self.greška()
		return Program(naredbe[0])
		
	#citaj head i body	
	def naredba(self):
		while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst
		
		self.pročitaj(XHTML.HEADOTV)
		head = Head(Tekst(self.pročitaj(XHTML.TEKST)))
		self.pročitaj(XHTML.HEADZATV)
		
		elementi = []
		while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst
		self.pročitaj(XHTML.BODYOTV)
		while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst
		
		while not self >> XHTML.BODYZATV: 
			elementi.append(self.element())
			while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst
			
		while self >> XHTML.PRAZANTXT: pass
		return Html(head,Body(elementi))
		
	
	#prouči sve elemente u body			
	def element(self):
			
			if self >> XHTML.TEKST: 
				return Tekst(self.zadnji)
			elif self >> XHTML.OLOTV: 
				sadrzaj = []
				while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst
				while True: 
					sadrzaj.append(self.li())
					while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst
					
					if self >> XHTML.OLZATV:
						break
					
				return Lista(XHTML.OLOTV.value,sadrzaj)
			elif self >> XHTML.ULOTV: 
				sadrzaj = []
				while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst 
				
				while True: 
					sadrzaj.append(self.li())
					while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst
					
					if self >> XHTML.ULZATV:
						break
				
				return Lista(XHTML.ULOTV.value,sadrzaj)
			else:
				self.greška()
				
	def li(self):
		sadrzi = []
		
		if self >> XHTML.LIOTV:
			while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst  <li>         </li>
			if self >> XHTML.TEKST: 
				self.vrati()
				sadrzi.append(self.element())
				self.pročitaj(XHTML.LIZATV)
			else:
				while not self >> XHTML.LIZATV: #tek kada dode ce ga pročitati, ostale vraća
					self.pročitaj(XHTML.OLOTV,XHTML.ULOTV)
					self.vrati()
					sadrzi.append(self.element())
					while self >> XHTML.PRAZANTXT: pass #preskacemo prazan tekst  <li></li>     <li></li>	
			
			return Li(sadrzi)
		else:
			self.greška()


class Program(AST('html')):
	"""Program u jeziku xhtml."""
	def izvrši(self,path=False):
		if path:
			path = open(path,'a')
		self.html.izvrši(path)
		if path: path.close()

class Html(AST('head body')):
	
    def izvrši(self,path=False):
        self.head.izvrši(path)
        self.body.izvrši(path)

class Head(AST('tekst')):
	
    def izvrši(self,path=False):
        #	self.tekst.izvrši(path)
        pass

class Body(AST('elementi')):
	def izvrši(self,path=False):
		
		odvoji = ''
		for element in self.elementi:
			if path:
				path.write(odvoji)
				odvoji = '\n'
			element.izvrši(path)

class Tekst(AST('string')):
	def izvrši(self,path=False,dubina = ''):
		sadržaj =re.sub( '\s+', ' ', self.string.sadržaj).strip() #makni 
		#visestruke razmake.
		if path:
			path.write(dubina)
			if dubina: path.write(' ')
			path.write(sadržaj)
		else:
			print(dubina,sadržaj)
		
class Lista(AST('vrsta clanovi')):
	
	def izvrši(self,path=False,dubina = '' ):
		izlazi = []
		odvoji = ''
		
		if dubina:
			dubina2 = str(dubina[:-2])+'  '
		else: dubina2 = dubina
		
		index = 1
		for clan in self.clanovi:
			if path:
				path.write(odvoji)
			else:
				pass
			bullet = ' *'
			if self.vrsta == XHTML.OLOTV.value: 
				bullet = str(index)+'.'
				index = index+1
			clan.izvrši(path,str(dubina)+'\t'+bullet)
			dubina = dubina2
			odvoji = '\n'
			
class Li(AST('elementi')):
	
	def izvrši(self, path=False,dubina = ''):
		dubina = str(dubina)
		if not self.elementi:
			if path:
				path.write(dubina)
			else:
				print(dubina)
		
		radna_dubina = dubina[:-2]+'  ' 
		odvoji = ''
		for element in (self.elementi):
			if path:
				path.write(odvoji)
			element.izvrši(path,dubina)
			dubina = radna_dubina
			odvoji = '\n'+dubina+'\t-------------------------\n' 
			#razmak izmedu elemenata od li	

"""
Napišite i odgovarajući „semantički“ analizator (rendered) za XHTML 
liste iz prvog zadatka. Za svaki <li> element iz neuređene liste 
ispišite tabulator, „*“, sadržaj <li> elementa ako se radi o tekstu, 
te znak za prijelom retka. Ako je sadržaj <li> elementa nova lista, onda 
samo ispišite novu listu. Elemente liste s prve razine treba ispisati s 
jednim tabulatorom na početku, a za svaku dodatnu razinu treba ispisati 
i dodatni tabulator (npr. lista unutar liste počinje s dva tabulatora, 
itd.).
"""
import os.path
def xhtml_analiziraj(program,izlaz=False):
	while izlaz and os.path.isfile(izlaz):
		izlaz = str(1)+izlaz
	program.izvrši(izlaz)


#tests = [1,11,20,21,22,30]	
tests = [23,33]
if __name__ == '__main__':
	if 1 in tests:
		print('primjer 1')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li></ol>
	</body></html>
		''')
		for token in iter(lexer):
			print(token) 
		print('\n\n')
	if 11 in tests:
		print('primjer 11')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li>
	  <li>neki</li>
	  <li></li>
	  <li>neki</li>
	  </ol>
	</body></html>''')
		for token in iter(lexer):
			print(token) 
		print('\n\n')
	if 20 in tests:
		print('primjer 20')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li></ol>
	</body></html>''')
		print(*xhtml_parser.parsiraj(lexer))
		
	if 21 in tests:
		print('primjer 21')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li>
	  <li>neki</li>
	  <li></li>
	  <li>neki</li>
	  </ol>
	</body></html>''')
		print(*xhtml_parser.parsiraj(lexer))
		
	if 22 in tests:
		print('primjer 22')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>

	  <ol><li>neki</li></ol>
	</body></html>
	''')
		print(*xhtml_parser.parsiraj(lexer))
	
	if 23 in tests:
		print('primjer 23')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	još teksta
	  <ul><li>neki</li>
	  <li>neki</li>
	  <li>
			<ol><li>neki 2</li>
			  <li>
				<ol><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>neki 3</li>
				</ol>
								<ul><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>
						<ul><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>neki 3</li>
				</ul>	
				</li>
				</ul>
				
			  </li>
			  
			  <li>neki 2</li>
			</ol>
	  </li>
	  <li>neki</li>
	  </ul>neki tekst
	</body></html>''')
		print(*xhtml_parser.parsiraj(lexer))
		
	if 24 in tests:#error
		print('primjer 24')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li></ol>
	</body></html> jadfjasj''')
		try:
			print(*xhtml_parser.parsiraj(lexer))
		except Exception:
			print("Dobro je")
			
	if 30 in tests:
		print('primjer 30 -- miče višestruke razmake iz teksta')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li>
	  <li>neki</li>
	  <li></li>
	  <li>neki</li>
	  </ol>

hjsdgh
hasdfhas
hasdfh                iasdhfi aghdfg    
	</body></html>''')
		dokument = xhtml_parser.parsiraj(lexer)
		xhtml_analiziraj(dokument,'izlaz_test30.txt')
	if 31 in tests:
		print('primjer 31')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li>
	  <li>neki</li>
	  <li></li>
	  <li>neki</li>
	  </ol>
	</body></html>''')
		dokument = xhtml_parser.parsiraj(lexer)
		xhtml_analiziraj(dokument,'izlaz_test31.txt')
		

	if 32 in tests:
		print('primjer 32: izlaz u datoteku.')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li>
	  <li>neki</li>
	  <li>
			<ol><li>neki 2</li>
			  <li>neki 2</li>
			  <li></li>
			  <li>neki 2</li>
			</ol>
	  </li>
	  <li>neki</li>
	  </ol>
	</body></html>''')
		dokument = xhtml_parser.parsiraj(lexer)
		xhtml_analiziraj(dokument,'izlaz_test32.txt')
	if 33 in tests:
		print('primjer 33:')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	još teksta
	  <ul><li>neki</li>
	  <li>neki</li>
	  <li>
			<ol><li>neki 2</li>
			  <li>
				<ol><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>neki 3</li>
				</ol>
								<ul><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>
						<ul><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>neki 3</li>
				</ul>	
				</li>
				</ul>
				
			  </li>
			  
			  <li>neki 2</li>
			</ol>
	  </li>
	  <li>neki</li>
	  </ul>neki tekst
	</body></html>''')
		dokument = xhtml_parser.parsiraj(lexer)
		xhtml_analiziraj(dokument)
	if 33 in tests:
		print('primjer 33: u dokument')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	još teksta
	  <ul><li>neki</li>
	  <li>neki</li>
	  <li>
			<ol><li>neki 2</li>
			  <li>
				<ol><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>neki 3</li>
				</ol>
								<ul><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>
						<ul><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>neki 3</li>
				</ul>	
				</li>
				</ul>
				
			  </li>
			  
			  <li>neki 2</li>
			</ol>
	  </li>
	  <li>neki</li>
	  </ul>neki tekst
	</body></html>''')
		dokument = xhtml_parser.parsiraj(lexer)
		xhtml_analiziraj(dokument,'izlaz_pr33')

if 34 in tests:
		print('primjer 33: u dokument - error prazna lista <ul></ul>')
		lexer = xhtml_lex('''<html         >
		<head>
	  Title of document
	</head><body>
	  <ol><li>neki</li>
	  <li>neki</li>
	  <li>
			<ol><li>neki 2</li>
			  <li>
				<ol><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>neki 3</li>
				</ol>
								<ul><li>neki 3</li>
				  <li>neki 3</li>
				  <li></li>
				  <li>neki 3</li>
				</ul>
				
			  </li>
			  
			  <li>neki 2</li>
			</ol>
	  </li>
	  <li>neki</li>
	  </ol>
	  <ul></ul>
	</body></html>''')
		dokument = xhtml_parser.parsiraj(lexer)
		xhtml_analiziraj(dokument,'izlaz_pr33')

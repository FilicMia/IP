
from lexer import *

"""
Parsiranje točno onako kako piše, html ima 2 taga body head,
bez praznina između, tj. nije dopušteno <html>       		<head>neki tekst   
   </head><body>     </body>		</html>

nego <html><head>neki tekst   
   </head><body>     </body></html>
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

"""
program -> HTMLOTV uhtml HTMLZATV

uhtml -> (HEADOTV TEKST HEADZATV) (BODYOTV ubody BODYZATV) 

ubody  -> TEKST ubody  | LISTA ubody | EPS

LISTA -> OLOTV ulisti OLZATV | ULOTV ulisti ULZATV

ulisti -> LIOTV uli LIZATV ulisti | EPS

uli -> TEKST | LISTA | EPS
"""

class xhtml_parser(Parser):
	def start(self):
		naredbe = []
		
		self.pročitaj(XHTML.HTMLOTV)
		while not self >> XHTML.HTMLZATV: naredbe.append(self.naredba())
		if not self >> E.KRAJ: self.greška()
		if not len(naredbe) == 1: self.greška()
		return Program(naredbe[0])
	#citaj head and body	
	def naredba(self):

		self.pročitaj(XHTML.HEADOTV)
		head = Head(self.pročitaj(XHTML.TEKST))
		self.pročitaj(XHTML.HEADZATV)
		
		elementi = []
		self.pročitaj(XHTML.BODYOTV)
		while not self >> XHTML.BODYZATV: elementi.append(self.element())
		return Html(head,Body(elementi))
		
	
	#prouči sve elemente			
	def element(self):
			
			if self >> XHTML.TEKST: return Tekst(self.zadnji)
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
		self.html.izvrši()

class Html(AST('head body')):
	
    def izvrši(self):
        self.head.izvrši()
        self.body.izvrši()

class Head(AST('tekst')):
	
    def izvrši(self):
        pass

class Body(AST('elementi')):
	
    def izvrši(self):
        for element in self.elementi:
             element.izvrši()

class Element(AST('element')):
	
    def izvrši(self,dubina = ''):
        self.element.izvrši(dubina)

class Tekst(AST('string')):
	def izvrši(self,dubina = ''):
		print(dubina,self.string.sadržaj)
		
class Lista(AST('vrsta clanovi')):
	
	def izvrši(self,dubina = '' ):
		izlazi = []
		kraj = ''
		for clan in self.clanovi:
			#print(kraj)
			clan.izvrši(str(dubina)+'\t')
			kraj = '\n'
			
class Li(AST('elementi')):
	
	def izvrši(self,dubina = ''):
		
		dubina = str(dubina)+'*'
		#print(dubina)
		for element in (self.elementi):
			element.izvrši(str(dubina))
		if not self.elementi:
			print(dubina)
	
def xhtml_interpreter(program):
	program.izvrši()
	
tests = [32]	
if __name__ == '__main__':
	if 32 in tests:
		lexer = xhtml_lex('''<html         ><head>
	  Title of document
	</head><body><ol><li>neki</li><li>neki</li><li><ol><li>neki 2</li><li>neki 2</li><li></li><li>neki 2</li></ol></li><li>neki</li></ol></body></html>''')
		dokument = xhtml_parser.parsiraj(lexer)
		xhtml_interpreter(dokument)

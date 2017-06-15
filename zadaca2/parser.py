from defaultpathimport import *
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
def start(self):
        elementi = []
        while not self >> XHTML.BODY: elementi.append(self.element())
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
    pass

class Html(AST('head body')):pass
	
   

class Head(AST('tekst')):pass
	
    

class Body(AST('elementi')):pass
	
    

class Element(AST('element')):pass
	


class Tekst(AST('string')):pass
	
		
class Lista(AST('vrsta clanovi')):pass
	
	
class Li(AST('elementi')):pass
	
	
	
if __name__ == '__main__':
	if 1 in tests:
		lexer = xhtml_lex('''<html         ><head>
	  Title of document
	</head><body>
	  <ol><li>neki</li></ol>
	</body></html>''')
		for token in iter(lexer):
			print(token) 
	if 2 in tests:
		lexer = xhtml_lex('''<html         ><head>
	  Title of document
	</head><body>
	  <ol><li>neki</li></ol>
	</body></html>''')
		print(*xhtml_parser.parsiraj(lexer))

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
dokument -> HTMLOTV uhtml HTMLZATV

uhtml -> (HEADOTV TEKST HEADZATV) (BODYOTV ubody BODYZATV) 

ubody  -> TEKST ubody  | LISTA ubody | EPS

LISTA -> OLOTV ulisti OLZATV | ULOTV ulisti ULZATV

ulisti -> LIOTV uli LIZATV ulisti | epsilon

uli -> TEKST | viselisti

viselisti -> LISTA viselisti | EPS 
"""
"""------------------------------------------------------------
'<' --> html,head,body,ol,ul,li --> '>'
	-->				/ --> html,body,head,ol,ul,li --> '>'


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
def zadaca_lex(kôd):
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

if __name__ == '__main__':
	lexer = zadaca_lex('''<html         >

<head>
  Title of document
</head>

<body>
  <ol><li>neki</li></ol>
</body>

</html>
    ''')
	for token in iter(lexer):
		print(token) 
#prekini citanje nakon HTML
		


"""
AST:
dokument: OTV HTML ZATV uhtml OTV KOSACRTA HTML ZATV
uhtml: 
"""
"""class zadaca_Parser(Parser):
    def dokument(self):
        uhtml = []
        while not self >> E.KRAJ: uhtml.append(self.naredba())
        return Dokument(naredbe)"""

"""def naredba(self):
        if self >> LJ.LISTA: return Deklaracija(self.pročitaj(LJ.ID))
        elif self >> LJ.PRAZNA: return Provjera(self.pročitaj(LJ.ID))
        elif self >> LJ.UBACI: return Ubaci(self.pročitaj(LJ.ID),
            self.pročitaj(LJ.BROJ, LJ.MINUSBROJ), self.pročitaj(LJ.BROJ))
        elif self >> LJ.IZBACI:
            return Izbaci(self.pročitaj(LJ.ID), self.pročitaj(LJ.BROJ))
        elif self >> LJ.DOHVATI:
            return Dohvati(self.pročitaj(LJ.ID), self.pročitaj(LJ.BROJ))
        elif self >> LJ.KOLIKO: return Duljina(self.pročitaj(LJ.ID))
        else: self.greška()"""

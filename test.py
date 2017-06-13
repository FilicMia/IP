"""
Napišite leksički analizator za pseudo-XHTML dokument koji sadrži samo liste. Cijeli dokument je uokviren samo u <html> element koji se sastoji od zaglavlja <head> i tijela <body>. Zaglavlje smije sadržavati samo običan tekst, a tijelo se sastoji od običnog teksta i listi. Liste mogu biti uređene <ol> i neuređene <ul>. Lista se sastoji od <li> elemenata. U jednom elementu liste smije se nalaziti običan tekst ili nova lista, ali ne i oboje. Dokument može sadržavati proizvoljan broj listi. Poštujte uobičajena pravila za XHTML dokumente.

Napišite sintaksni analizator za pseudo-XHTML dokumente iz prvog zadatka. Provjerite uobičajena XHTML pravila: je li cijeli dokument uokviren u <html> elemente, je li odnos XHTML elemenata odgovarajući , je li svaki element i zatvoren, jesu li svi elementi napisani malim slovima, jesu li elementi odgovarajuće ugnježdeni, itd. Omogućite i da se u <li> elementu liste, osim običnog teksta, može pojaviti i nova lista (ali ne i oboje). Liste smiju sadržavati samo <li> elemente (ne tekst i ne direktno druge liste).

Napišite i odgovarajući „semantički“ analizator (rendered) za XHTML liste iz prvog zadatka. Za svaki <li> element iz neuređene liste ispišite tabulator, „*“, sadržaj <li> elementa ako se radi o tekstu, te znak za prijelom retka. Ako je sadržaj <li> elementa nova lista, onda samo ispišite novu listu. Elemente liste s prve razine treba ispisati s jednim tabulatorom na početku, a za svaku dodatnu razinu treba ispisati i dodatni tabulator (npr. lista unutar liste počinje s dva tabulatora, itd.).
"""


from pj import *

class XHTML(enum.Enum):
	HTML = 'html' """cijeli dokument uokviren u ovo - proizvoljno listi"""
	ZAGLAVLJE = 'head' """samo obican tekst"""
	BODY = 'body' """samo obican tekst i liste"""
	OL = 'ol' """samo li elemente!!"""
	UL = 'ul'
	LI = 'li' """ili tekst ili obicna list"""
	TEKST = 'nekitekst'
	OTV = '<'
	ZATV = '>'
	KOSACRTA = '/'

"""PRVO lekser pa sintaksni analizator"""


"""Lekser"""


"""
dokument -> OTV HTML ZATV u_html OTV KOSACRTA HTML ZATV

u_html -> ((OTV HEAD ZATV) TEKST (OTV KOSACRTA HEAD ZATV)) ((OTV BODY ZATV) u_body (OTV KOSACRTA BODY ZATV)) 

u_body  -> TEKST u_body  | LISTA u_body | EPS

LISTA -> (OTV OL ZATV) u_listi (OTV KOSACRTA OL ZATV) | (OTV UL ZATV) u_listi (OTV KOSACRTA UL ZATV)

u_listi -> (OTV LI ZATV) u_li (OTV KOSACRTA LI ZATV) u_listi | epsilon

u_li -> TEKST | viselisti

viselisti -> LISTA viselisti | EPS 
"""
"""------------------------------------------------------------"""
'<' --> html,head,body,ol,ul,li --> '>'
	-->				/ --> html,body,head,ol,ul,li --> '>'


"""------------------------------------------------------------"""
def provjeri(lex,prvo):
	if prvo == 'h':
		drugo = lex.čitaj()
		if drugo == 't':
			lex.pročitaj('m')
			lex.pročitaj('l')
			yield lex.token(XHTML.HTML)
		elif drugo == 'e':
			lex.pročitaj('a')
			lex.pročitaj('d')
			yield lex.token(XHTML.HEAD)
		else: lex.greška('očekiva se tml ili ead')

	elif prvo == 'b':
		lex.pročitaj('o')
		lex.pročitaj('d')
		lex.pročitaj('y')
		yield lex.token(XHTML.BODY)

	elif prvo == 'o':
		lex.pročitaj('l')
		yield lex.token(XHTML.OL)

	elif prvo == 'u':
		lex.pročitaj('l')
		yield lex.token(XHTML.UL)

	elif prvo == 'l':
		lex.pročitaj('i')
		yield lex.token(XHTML.LI)

	else: yield lex.token(lex.greška())

"""
Lexer
"""
def zadaca_lex(kôd):
    lex = Tokenizer(kôd)
    for znak in iter(lex.čitaj, ''):
        if znak == '<':
			yield lex.token(XHTML.OTV)
            prvo = lex.čitaj()
			if prvo == '/':
				yield lex.token(XHTML.KOSACRTA)
				drugo = lex.čitaj()
				provjeri(lex,drugo)
			
			else: 
				provjeri(lex,prvo)

		elif znak == '>':
			yield lex.token(XHTML.ZATV)
		else:
			for slovo in iter(lex.čitaj, '<'): pass
			lex.vrati()
			yield lex.token(XHTML.TEKST)


"""
def zadaca_lex2(kôd):
    lex = Tokenizer(kôd)
    for znak in iter(lex.čitaj, ''):
        if znak == '<':
			yield lex.token(XHTML.OTV)

		elif znak == '>':
			yield lex.token(XHTML.ZATV)

		elif znak == '/':
			yield lex.token(XHTML.KOSACRTA)

		elif: 
			provjeri(lex,prvo)

		else:
			for slovo in iter(lex.čitaj, '<'): pass
			lex.vrati()
			yield lex.token(XHTML.TEKST)

da ne ovisi o kontekstu uope!! --- ako tako, treba dopuniti i gramatiku VISETEKSTA -> TEKST VISETEKSTA | epsilon

"""


"""
dokument -> OTV HTML ZATV u_html OTV KOSACRTA HTML ZATV

u_html -> ((OTV HEAD ZATV) TEKST (OTV KOSACRTA HEAD ZATV)) ((OTV BODY ZATV) u_body (OTV KOSACRTA BODY ZATV)) 

u_body  -> TEKST u_body  | LISTA u_body | EPS

LISTA -> (OTV OL ZATV) u_listi (OTV KOSACRTA OL ZATV) | (OTV UL ZATV) u_listi (OTV KOSACRTA UL ZATV)

u_listi -> (OTV LI ZATV) u_li (OTV KOSACRTA LI ZATV) u_listi | epsilon

u_li -> TEKST | viselisti

viselisti -> LISTA viselisti | EPS 
"""

"""
Za svaku varijablu koja na desnoj strani nema samo tokene, napisi funkciju,
Za svaku varijablu koja je na lijevoj strani, napiši AST.
"""

"""
AST:
dokument: OTV HTML ZATV uhtml OTV KOSACRTA HTML ZATV
uhtml: 
"""
class zadaca_Parser(Parser):
    def dokument(self):
        uhtml = []
        while not self >> E.KRAJ: uhtml.append(self.naredba())
        return Dokument(naredbe)

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























			


from setimportpath import *
from pj import *
#print(sys.path)

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

tests = [1,2,3]

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

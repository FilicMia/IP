"""
Programski jezik μLogo ima tri ključne riječi: FORWARD, LEFT i REPEAT. Ključna riječ 
FORWARD može se skratiti u FD, a LEFT u LT (ne mijenjajući tip tokena). 
U μLogu postoje i prirodni brojevi, te uglate zagrade. Oni mogu biti 
razdvojeni prazninama, koje se zanemaruju. Sve ostalo je leksička greška. 
Napišite potrebne tipove tokena.

Napišite lekser za μLogo. Primjer: ] 57 BLAbla 
REPEAT FD treba generirati tokene ZATV']', BROJ'57', GREŠKA'BLAbla', REPEAT'REPEAT', FORWARD'FD'.

μLogo ima tri vrste naredbi: FORWARD x za pomicanje kursora x piksela u 
trenutnom smjeru, LEFT x za rotaciju trenutnog smjera x stupnjeva 
pozitivno, te REPEAT x [ naredbe ]  za izvršavanje grupe naredbi x puta. 
Argument x predstavlja prirodan broj.

Napišite beskontekstnu gramatiku za μLogo, nad abecedom koju čine tipovi tokena.
Dokažite da bi ta gramatika bila višeznačna da iz jezika izbacimo uglate zagrade.
Napišite parser za μLogo. Parser treba vratiti tip.AST strukturu 
(ili listu njih) ako je ulaz validan μLogo program, 
a prijaviti detaljnu sintaksnu grešku ako nije.

Primjer: REPEAT 4 [LT 90 FD 150] LT 30 FD 150 LT 120 FD 150 crta kućicu. 
Parsira se kao lista [REPEAT(x=4, naredbe=[LEFT(x=90), FORWARD(x=150)]),
LEFT(x=30), FORWARD(x=150), LEFT(x=120), FORWARD(x=150)].

Napišite kompajler μLogo jezika u JavaScript. Koristite canvas.
"""
from setimportpath import *
from pj import *

zagrade = ['[',']']

class LOGO(enum.Enum):
    
    FORWARD = ["FORWARD","FD"]
    LEFT = ["LEFT","LT"]
    REPEAT = "REPEAT"
    OTV = "["
    ZATV = "]"
    BROJ = 123

def logo_lex(string):
    
    lex = Tokenizer(string)
    lex.zvijezda(str.isspace)
    lex.token(E.PRAZNO)
    
    for znak in iter(lex.čitaj,''):
        if znak in zagrade:
            yield lex.token(operator(LOGO,lex.sadržaj))
        else:
            lex.zvijezda(lambda znak: znak != '' and not (str.isspace(znak)) and not (znak in zagrade))
            #probaj po imenu enumeracije
            if str.isnumeric(lex.sadržaj):
                yield lex.token(LOGO.BROJ)
            elif lex.sadržaj in LOGO.LEFT.value:
                yield lex.token(LOGO.LEFT)
            elif lex.sadržaj in LOGO.FORWARD.value:
                yield lex.token(LOGO.FORWARD)
            else:
                yield lex.token(ključna_riječ(LOGO, lex.sadržaj) or E.GREŠKA)
        lex.zvijezda(str.isspace)
        lex.token(E.PRAZNO)


"""
BESKONTEKSTNA GRAMATIKA:
program -> praznine naredba program | praznine
naredba -> forward | left | repeat
naredbe -> naredba program

forward -> FORWARD BROJ
left -> LEFT BROJ
repeat -> REPEAT BROJ OTV [ naredbe ]
praznine -> EPS #zanemaruju se

"""

"""
AST:
program: naredbe
naredbe: lista naredbi
naredba: forwrad left repeat
forward: x
left: x

repeat: lista naredbi
"""

"""
μLogo ima tri vrste naredbi: FORWARD x za pomicanje kursora x piksela u 
trenutnom smjeru, LEFT x za rotaciju trenutnog smjera x stupnjeva 
pozitivno, te REPEAT x [ naredbe ]  za izvršavanje grupe naredbi x puta. 
Argument x predstavlja prirodan broj.

Napišite beskontekstnu gramatiku za μLogo, nad abecedom koju čine tipovi tokena.
Dokažite da bi ta gramatika bila višeznačna da iz jezika izbacimo uglate zagrade.
Napišite parser za μLogo. Parser treba vratiti tip.AST strukturu 
(ili listu njih) ako je ulaz validan μLogo program, 
a prijaviti detaljnu sintaksnu grešku ako nije.
"""
class logo_parser(Parser):
    def start(self):
        naredbe = []
        while not self >> E.KRAJ: naredbe.append(self.naredba())
        return PROGRAM(naredbe)
        
        
    def naredba(self):
        if self >> LOGO.LEFT:
            drugi = self.pročitaj(LOGO.BROJ)
            return LEFT(drugi)
        elif self >> LOGO.FORWARD:
            drugi = self.pročitaj(LOGO.BROJ)
            return FORWARD(drugi)
        elif self >> LOGO.REPEAT:
            naredbe = []
            drugi = self.pročitaj(LOGO.BROJ)
            self.pročitaj(LOGO.OTV)
            while not self >> LOGO.ZATV: naredbe.append(self.naredba())
            
            return REPEAT(drugi,naredbe)
        else:
            self.greška() 


class PROGRAM(AST('naredbe')):
	
	def izvrši(self):
		s = ""
		kontekst = {'x':0, 'y':0, 'fi': 0} #naprijed iznad sebe
		for naredba in self.naredbe:
			s = s+naredba.izvrši(kontekst)
		print(self)
		print("prog")
		return s;
class FORWARD(AST('x')):
	
	def izvrši(self,kontekst):
		print("Forvar")
		s=""
		x = kontekst['x']
		y = kontekst['y']
		fi = kontekst['fi']
		xx = int(self.x.sadržaj)
		
		if fi == 0 :
			x = (x + xx) % 300
			s = s+"ctx.lineTo("+str(x)+","+str(y)+");"
		elif fi == 90:
			y = (y + xx) % 300
			s = s+"ctx.lineTo("+str(x)+","+str(y)+");"
		elif fi == 180:
			x = (x - xx) % 300
			s = s+"ctx.lineTo("+str(x)+","+str(y)+");"
		else: #270
			y = (y - xx) % 300
			s = s+"ctx.lineTo("+str(x)+","+str(y)+");"
		
		
		kontekst['x'] = x
		kontekst['y'] = y
		print(s)
		return s
class LEFT(AST('x')): 
	
	def izvrši(self,kontekst):
		kontekst['fi'] = kontekst['fi']+90 % 360
		return ""
class REPEAT(AST('x naredbe')): 
	
	def izvrši(self,kontekst):
		s = ""
		for naredba in self.naredbe:
			s = s+naredba.izvrši(kontekst)
		return s


"""
Napišite kompajler μLogo jezika u JavaScript. Koristite canvas.
"""

import os.path
def logo_interpreter(lexer):
    početak = '''\
		<!DOCTYPE html><html><head><title>HTML5 Canvas For Absolute Beginners | onlyWebPro.com
		</title><script type=\"text/javascript\">
		function drawShape() 
		{var myCanvas = document.getElementById(\"myCanvas\");
		var ctx = myCanvas.getContext(\"2d\");
		ctx.beginPath();
		ctx.lineTo(0,0);'''
    kraj = '''\
		 ctx.stroke();
		 }</script>
		 </head>
		 <body onload=\"drawShape()\"><canvas id=\"myCanvas\" width=\"300\" height=\"300\">
		 </canvas></body></html>'''
    print("LOGO")
    content = početak+lexer.izvrši()+kraj
    izlaz = 'javascript.html'
    while izlaz and os.path.isfile(izlaz):
        izlaz = str(1)+izlaz
    path = open(izlaz,'a')
    path.write(content)
    path.close()






if __name__ == '__main__':
    """    
        print(*logo_lex('   FORWARD -7 LEFT 9'))
        print(*logo_lex('   FORWARD 7 LEFT 9 REPEAT 7 [LEFT 9]'))
        lj = logo_lex('   FORWARD 7 LEFT 9 REPEAT 7 [LEFT 9 FORWARD 10 ]')
        print(*logo_parser.parsiraj(lj))
    """

    primjer = "FD 150 REPEAT 4 [LT 90 FD 150] LT 30 FD 150 LT 120 FD 150"
    #print(*logo_lex(primjer))
    lj = logo_lex(primjer)
    print(*logo_parser.parsiraj(lj))
    lj = logo_lex(primjer)
    primjerPar = logo_parser.parsiraj(lj)
    logo_interpreter(primjerPar)
    
    
    

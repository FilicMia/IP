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


class PROGRAM(AST('naredbe')): pass
class FORWARD(AST('x')): pass
class LEFT(AST('x')): pass
class REPEAT(AST('x naredbe')): pass


"""
Napišite kompajler μLogo jezika u JavaScript. Koristite canvas.
"""
def logo_interpreter(lexer):
    početak = "<!doctype html> <html lang=\"en\"><head>"+
    "<meta charset=\"utf-8\">

  <title>The HTML5 Herald</title>
  <meta name="description" content="The HTML5 Herald">
  <meta name="author" content="SitePoint">

  <link rel="stylesheet" href="css/styles.css?v=1.0">

  <!--[if lt IE 9]>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.js"></script>
  <![endif]-->
</head>

<body>
  <script src="js/scripts.js"></script>
</body>
</html>"
    






if __name__ == '__main__':
    """    
        print(*logo_lex('   FORWARD -7 LEFT 9'))
        print(*logo_lex('   FORWARD 7 LEFT 9 REPEAT 7 [LEFT 9]'))
        lj = logo_lex('   FORWARD 7 LEFT 9 REPEAT 7 [LEFT 9 FORWARD 10 ]')
        print(*logo_parser.parsiraj(lj))
    """

    primjer = "REPEAT 4 [LT 90 FD 150] LT 30 FD 150 LT 120 FD 150"
    print(*logo_lex(primjer))
    lj = logo_lex(primjer)
    print(*logo_parser.parsiraj(lj))
    

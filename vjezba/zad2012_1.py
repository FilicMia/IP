"""Napišite leksički analizator za JavaScript funkcije. 
JavaScript funkcija počinje ključnom riječi function, zatim slijedi ime 
funkcije, pa lista parametara, te tijelo funkcije unutar vitičastih zagrada. 
Tijelo funkcije sastoji se od linijskih komentara (//) i od naredbi 
(niz znakova koji završava s ;). Npr.

function ime (var x, var y, ...){

         //neke naredbe odvojene s ; ili komentar

}

Napišite sintaksni analizator za prepoznavanje ispravno napisanih 
JavaScript funkcija iz prvog zadatka. Analizator treba pretvoriti 
zadani JavaScript program (koji se sastoji samo od funkcija) 
u apstraktna sintaksna stabla: Program, Funkcija, Naredba. 
U tijelu funkcije dozvolite više naredbi odvojenih s 
; i linijske komentare.
"""
from setimportpath import *
"""
Lexter:
BESKONTEKSTNA GRAMATIKA:

start -> praznine FUNCTION 



"""

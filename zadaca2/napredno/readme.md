Ova mapa sadrži nadopunjeno rješenje zadatka zadanog za zadaću:

"""
Napišite leksički analizator za pseudo-XHTML dokument koji sadrži samo liste. Cijeli dokument je uokviren samo u <html> element koji se sastoji od zaglavlja <head> i tijela <body>. Zaglavlje smije sadržavati samo običan tekst, a tijelo se sastoji od običnog teksta i listi. Liste mogu biti uređene <ol> i neuređene <ul>. Lista se sastoji od <li> elemenata. U jednom elementu liste smije se nalaziti običan tekst ili nova lista, ali ne i oboje. Dokument može sadržavati proizvoljan broj listi. Poštujte uobičajena pravila za XHTML dokumente.

Napišite sintaksni analizator za pseudo-XHTML dokumente iz prvog zadatka. Provjerite uobičajena XHTML pravila: je li cijeli dokument uokviren u <html> elemente, je li odnos XHTML elemenata odgovarajući , je li svaki element i zatvoren, jesu li svi elementi napisani malim slovima, jesu li elementi odgovarajuće ugnježdeni, itd. Omogućite i da se u <li> elementu liste, osim običnog teksta, može pojaviti i nova lista (ali ne i oboje). Liste smiju sadržavati samo <li> elemente (ne tekst i ne direktno druge liste).

Napišite i odgovarajući „semantički“ analizator (rendered) za XHTML liste iz prvog zadatka. Za svaki <li> element iz neuređene liste ispišite tabulator, „*“, sadržaj <li> elementa ako se radi o tekstu, te znak za prijelom retka. Ako je sadržaj <li> elementa nova lista, onda samo ispišite novu listu. Elemente liste s prve razine treba ispisati s jednim tabulatorom na početku, a za svaku dodatnu razinu treba ispisati i dodatni tabulator (npr. lista unutar liste počinje s dva tabulatora, itd.).
"""



Datoteka zadaca2Mia.py sadrži rješenje.
Dio sintaksnog analizatora koji obuhvaća: "jesu li svi elementi napisani malim slovima", prebačen u lexer.
Vakanji XHTML tagovi su </?ime_taga> i </?ime_taga   (blank)*   > jet takve tagove XHTML dopušta,a
ne dopušta <   (blank)+  (/?) (blank)+   ime_taga>

Nisu dozvoljene prazne liste: <ol></ol> jer XHTML ne podržava takve liste.
Također, dopuštaju se znakovi za prazan znak između html-tagova koje parser zanemaruje prilikom
sintaksne analize.
Dakle, dozvoljeno je
<html>
<head></head>                  <body></body></html> i to je jednako <html><head></head><body></body></html>.
Semantički analizator dopušta pisanje izlaza na standardni output, ali i u datoteku.
Unutar istog li elementa, dopušta se ili tekst ili jedna ili više lista (ne samo jedna).
Također, postoje i testni primjeri.
Također, višestruke praznine u TEKST-u se zaminenjuju s jednim ' '(po uzoru na XHTML).
Ukoliko se radu o ol listi, njezini elementi se ispisuju s tabulator, „broj koji odgovara rednom broju li elementa liste“, sadržaj <li> elementa, te znak za prijelom retka.
U slučaju ul liste, ispisuje se kako je predviđeno tekstom zadataka.

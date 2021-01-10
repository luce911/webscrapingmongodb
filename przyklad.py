#Zadanie 11 Zrob prosty web scrapin stron internetowych
#i zapisz je w bazie NoSQL.
import requests
from datetime import datetime
strony=['http://interia.pl','http://money.pl','http://stooq.pl']
bazaStron=klient['bazaN4211']
kolekcja=bazaStron.strony
for s  in strony:
    tresc=requests.get(s)
    strona={
        'url':s,
        'content':tresc.text,
        'date':datetime.today().strftime('%d/%m/%Y')
    }
    #wstawic do kolekcji strony tę pobraną stronę
    rezultat=kolekcja.insert_one(strona)
    #potwierdzic wstawienie
    print("Wstawiono dokument",rezultat.inserted_id)
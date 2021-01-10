from pymongo import MongoClient

klient=MongoClient('mongodb://localhost:27017')
bazaDanych=klient['bazaN4211_LucjaCh']
kolekcja=bazaDanych.rynek
student={
    "nrIndeksu":200200,
    "imie":"Jan",
    "nazwisko":"Kowalski"
}
rezultat=kolekcja.insert_one(student)
print("Wstawiono dokument",rezultat.inserted_id)
from letovi.letovi import matrica_zauzetosti
from konkretni_letovi import konkretni_letovi
from common import konstante
from functools import reduce
from datetime import datetime
import csv
import json
import ast

"""
Brojacka promenljiva koja se automatski povecava pri kreiranju nove karte.
"""
sve_karte = {}
sledeci_broj_karte = 1
def set_u_test(value):
    global u_testu
    u_testu = value
u_testu = True

class Karta:
    def __init__(self, broj_karte: int, sifra_konkretnog_leta: int, kupac: str, prodavac: str, sediste: str,
                       putnici: list, datum_prodaje: datetime, obrisana: bool, status = None):
        self.broj_karte            = int(broj_karte)
        self.sifra_konkretnog_leta = int(sifra_konkretnog_leta)
        if type(kupac) == str:
            self.kupac             = ast.literal_eval(kupac)
        else:
            self.kupac             = kupac
        if type(prodavac) == str:
            self.prodavac          = ast.literal_eval(prodavac)
        else:
            self.prodavac          = prodavac
        self.sediste               = sediste
        if type(putnici) == str:
            self.putnici           = ast.literal_eval(putnici)
        else:
            self.putnici           = putnici
        if type(datum_prodaje) == str and not u_testu:
            self.datum_prodaje    = datetime.strptime(datum_prodaje, "%Y-%m-%d %H:%M:%S")
        else:
            self.datum_prodaje         = datum_prodaje
        if obrisana == "False" or obrisana == False:
            self.obrisana          = False
        else:
            self.obrisana          = True
        if status:
            self.status = status

def da_li_postoji_slobodno_mesto(slobodna_mesta: list) -> bool:
    for red in slobodna_mesta:
        for mesto in red:
            if not mesto:  # Kada pronadjemo jedno slobodno mesto, mozemo zavrsiti pretragu
                return True
    return False

def zauzmi_prvo_slobodno_mesto(sifra_konkretnog_leta: int) -> str:
    zauzetost = matrica_zauzetosti(konkretni_letovi.svi_konkretni_letovi[sifra_konkretnog_leta])
    for i in range(len(zauzetost)):
        for j in range(len(zauzetost[i])):
            if not zauzetost[i][j]:
                konkretni_letovi.svi_konkretni_letovi[sifra_konkretnog_leta]["zauzetost"][i][j] = True
                return chr(j + ord('A')) + str(i+1)

"""
Kupovina karte proverava da li prosledjeni konkretni let postoji i da li ima slobodnih mesta. U tom slucaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosledjuju posebno iako su deo konkretnog leta, zbog lakseg 
testiranja. Baca gresku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguce je dodati saputnike i odabrati povezane letove. 
"""
def kupovina_karte(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    sifra_konkretnog_leta: int,
    putnici: list,
    slobodna_mesta: list,
    kupac: dict,
    **kwargs
) -> (dict, dict):
    if sifra_konkretnog_leta not in svi_konkretni_letovi:
        raise Exception("ERROR: Dati konkretan let ne postoji!")
    if not da_li_postoji_slobodno_mesto(slobodna_mesta):
        raise Exception("ERROR: Nema slobodnih mesta!")
    if kupac["uloga"] != konstante.ULOGA_KORISNIK:
        raise Exception("ERROR: Samo korisnik moze da kupi kartu!")
    if "prodavac" not in kwargs or "datum_prodaje" not in kwargs:
        raise Exception("ERROR: Nedostaju parametri za prodavca i datum prodaje!")
    if kwargs["prodavac"]["uloga"] != konstante.ULOGA_PRODAVAC:
        raise Exception("ERROR: Samo prodavac moze da proda kartu!")

    global sledeci_broj_karte
    if sledeci_broj_karte in sve_karte:
        sledeci_broj_karte = max(sve_karte.keys()) + 1
    nova_karta = {
        "broj_karte": sledeci_broj_karte,
        "putnici": putnici,
        "sifra_konkretnog_leta": sifra_konkretnog_leta,
        "status": konstante.STATUS_NEREALIZOVANA_KARTA,
        "kupac": kupac,
        "obrisana": False,
        "prodavac": kwargs["prodavac"],
        "datum_prodaje": kwargs["datum_prodaje"]
    }
    if konkretni_letovi.svi_konkretni_letovi != {}: # Ne mozemo da pozovemo ovu funkciju tokom testa
        #nova_karta["sediste"] = zauzmi_prvo_slobodno_mesto(sifra_konkretnog_leta)
        nova_karta["sediste"] = "??"
    sve_karte[sledeci_broj_karte] = nova_karta
    sledeci_broj_karte += 1
    return nova_karta, sve_karte


"""
Vraca sve nerealizovane karte za korisnika u listi.
"""
def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter):
    return [karta for karta in sve_karte if karta["status"] == konstante.STATUS_NEREALIZOVANA_KARTA and korisnik in karta["putnici"]]

def pregled_nerealizovanaih_kupljenih_karata(korisnik: dict, sve_karte: dict):
    return [karta for karta in sve_karte.values() if karta["status"] == konstante.STATUS_NEREALIZOVANA_KARTA and karta["kupac"] == korisnik]


"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraca recnik sa svim kartama, 
koji sada sadrzi izmenu.
"""
def izmena_karte(
    sve_karte: iter,
    svi_konkretni_letovi: iter,
    broj_karte: int,
    nova_sifra_konkretnog_leta: int = None,
    nov_datum_polaska: datetime = None,
    sediste = None
) -> dict:
    if broj_karte not in sve_karte:
        raise Exception("ERROR: Data karta ne postoji!")
    if nova_sifra_konkretnog_leta:
        sve_karte[broj_karte]["sifra_konkretnog_leta"] = nova_sifra_konkretnog_leta
    if nov_datum_polaska:
        svi_konkretni_letovi[sve_karte[broj_karte]["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"] = nov_datum_polaska
    if sediste:
        sve_karte[broj_karte]["sediste"] = sediste
    return sve_karte
"""
 Funkcija brisanja karte se ponasa drugacije u zavisnosti od korisnika:
- Prodavac: karta se oznacava za brisanje
- Admin/menadzer: karta se trajno brise
Kao rezultat se vraca nova kolekcija svih karata.
"""
def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:
    if not sve_karte[broj_karte]:
        raise Exception("ERROR: Ta karta ne postoji!")
    if korisnik['uloga'] == konstante.ULOGA_KORISNIK:
        raise Exception("ERROR: Korisnik nema dozvolu da brise kartu!")

    if korisnik['uloga'] == konstante.ULOGA_PRODAVAC:
        sve_karte[broj_karte]["obrisana"] = True
    elif korisnik['uloga'] == konstante.ULOGA_ADMIN:
        del sve_karte[broj_karte]
    else:
        raise Exception("ERROR: Korisnik nema ulogu!")

    return sve_karte

"""
Funkcija vraca sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosledjen.
"""
def pretraga_prodatih_karata(sve_karte: dict, svi_letovi:dict, svi_konkretni_letovi:dict, polaziste: str="",
                             odrediste: str="", datum_polaska: datetime="", datum_dolaska: datetime="",
                             korisnicko_ime_putnika: str="", kupac: str="")->list:
    rezultat = []
    for broj, karta in sve_karte.items():
        sifra = karta["sifra_konkretnog_leta"]
        broj_leta = svi_konkretni_letovi[sifra]["broj_leta"]
        if kupac and karta["kupac"]["korisnicko_ime"] != kupac:
            continue
        if polaziste and svi_letovi[broj_leta]["sifra_polazisnog_aerodroma"] != polaziste:
            continue
        if odrediste and svi_letovi[broj_leta]["sifra_odredisnog_aerodorma"] != odrediste:
            continue
        if datum_polaska and svi_konkretni_letovi[sifra]["datum_i_vreme_polaska"] != datum_polaska:
            continue
        if datum_dolaska and svi_konkretni_letovi[sifra]["datum_i_vreme_dolaska"] != datum_dolaska:
            continue
        if korisnicko_ime_putnika and " " in korisnicko_ime_putnika and karta["putnici"][0]["ime"]+" "+karta["putnici"][0]["prezime"] != korisnicko_ime_putnika:
            continue
        if korisnicko_ime_putnika and " " not in korisnicko_ime_putnika and \
                ("korisnicko_ime" not in karta["putnici"][0] or karta["putnici"][0]["korisnicko_ime"] != korisnicko_ime_putnika):
            continue
        rezultat.append(karta)
    return rezultat

def pretraga_karata_za_brisanje(sve_karte: dict):
    return [karta for karta in sve_karte.values() if karta["obrisana"]]

"""
Funkcija cuva sve karte u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
    with open(putanja, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=separator)
        for broj_karte in sve_karte:
            karta = Karta(**sve_karte[broj_karte]) # da bismo bili sigurni da su fajlovi uvek u istom formatu, koristimo klasu
            csv_writer.writerow(karta.__dict__.values())  # pretvaramo vrednosti iz klase nazad u recnik, i iz recnika
                                                          # u listu koju saljemo funkciji writerow


"""
Funkcija ucitava sve karte iz fajla sa zadate putanje sa zadatim separatorom.
"""
def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    sve_karte = dict()
    with open(putanja, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=separator)
        for row in csv_reader:
            if len(row) == 0:  # U slucaju da je red prazan, preskocicemo ga
                continue
            karta = Karta(*row)  # moramo da otpakujemo listu da bi je poslali kao niz parametara
            sve_karte[karta.broj_karte] = karta.__dict__  # pretvaramo klasu u recnik pomocu ugradjene funkcije
    return sve_karte


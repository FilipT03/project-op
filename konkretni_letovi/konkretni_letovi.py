from datetime import datetime, timedelta
import ast
import csv
from letovi.letovi import podesi_matricu_zauzetosti

svi_konkretni_letovi = {}

class KonkretanLet:
    def __init__(self, sifra: int, broj_leta: str, datum_i_vreme_polaska: datetime,
                       datum_i_vreme_dolaska: datetime, zauzetost: list = None):
        self.sifra = int(sifra)
        self.broj_leta = broj_leta

        if type(datum_i_vreme_polaska) == str:
            self.datum_i_vreme_polaska = datetime.strptime(datum_i_vreme_polaska, "%Y-%m-%d %H:%M:%S")
        else:
            self.datum_i_vreme_polaska = datum_i_vreme_polaska

        if type(datum_i_vreme_dolaska) == str:
            self.datum_i_vreme_dolaska = datetime.strptime(datum_i_vreme_dolaska, "%Y-%m-%d %H:%M:%S")
        else:
            self.datum_i_vreme_dolaska = datum_i_vreme_dolaska

        if type(zauzetost) == list:
            self.zauzetost = zauzetost
        elif zauzetost:
            self.zauzetost = ast.literal_eval(zauzetost)

sledeca_sifra_konkretnog_leta = 1000

"""
Funkcija koja za zadati konkretni let kreira sve konkretne letove u opsegu operativnosti.
Kao rezultat vraća rečnik svih konkretnih letova koji sadrži nove konkretne letove.
"""
def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict) -> dict:
    global sledeca_sifra_konkretnog_leta
    datum = let["datum_pocetka_operativnosti"]
    kraj = let["datum_kraja_operativnosti"]
    while datum < kraj:
        if datum.weekday() in let["dani"]:
            sati, minuti = let["vreme_poletanja"].split(":")
            sati, minuti = int(sati), int(minuti)
            polazak = datum.replace(hour=sati, minute=minuti)
            sati, minuti = let["vreme_sletanja"].split(":")
            sati, minuti = int(sati), int(minuti)
            dolazak = datum.replace(hour=sati, minute=minuti)
            if sledeca_sifra_konkretnog_leta in svi_konkretni_letovi:
                sledeca_sifra_konkretnog_leta = max(svi_konkretni_letovi.keys()) + 1
            try:
                konkretan_let = KonkretanLet(sledeca_sifra_konkretnog_leta, let["broj_leta"], polazak, dolazak).__dict__
            except Exception as e:
                raise Exception("\nERROR: Neispravni podaci:\n" + str(e) + "\n")
            if "model" in let:
                podesi_matricu_zauzetosti({let["broj_leta"]:let},konkretan_let)
            svi_konkretni_letovi[sledeca_sifra_konkretnog_leta] = konkretan_let
            sledeca_sifra_konkretnog_leta += 1
        datum += timedelta(days=1)
    return svi_konkretni_letovi

"""
Funkcija čuva konkretne letove u fajl na zadatoj putanji sa zadatim separatorom. 
"""
def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    with open(putanja, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=separator)
        for sifra in svi_konkretni_letovi:
            konkretan_let = KonkretanLet(**svi_konkretni_letovi[sifra]) # da bismo bili sigurni da su fajlovi uvek u istom formatu, koristimo klasu
            csv_writer.writerow(konkretan_let.__dict__.values()) # pretvaramo vrednosti iz klase nazad u recnik, i iz recnika
                                                                 # u listu koju saljemo funkciji writerow


"""
Funkcija učitava konkretne letove iz fajla na zadatoj putanji sa zadatim separatorom.
"""
def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    svi_konkretni_letovi = dict()
    with open(putanja, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=separator)
        for row in csv_reader:
            if len(row) == 0:  # U slucaju da je red prazan, preskocicemo ga
                continue
            konkretan_let = KonkretanLet(*row)  # moramo da otpakujemo listu da bi je poslali kao niz parametara
            svi_konkretni_letovi[konkretan_let.sifra] = konkretan_let.__dict__  # pretvaramo klasu u recnik pomocu ugradjene funkcije
    return svi_konkretni_letovi

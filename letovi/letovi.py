import ast
from datetime import datetime, date, timedelta
import csv
from model_aviona import model_aviona

svi_letovi = {}

class Let:
    def __init__(self, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                       vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                       dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None,
                       datum_kraja_operativnosti: datetime = None):
        self.broj_leta                   = broj_leta
        self.sifra_polazisnog_aerodroma  = sifra_polazisnog_aerodroma
        self.sifra_odredisnog_aerodorma  = sifra_odredisnog_aerodorma
        self.vreme_poletanja             = vreme_poletanja
        self.vreme_sletanja              = vreme_sletanja
        if sletanje_sutra == "False" or sletanje_sutra == False:
            self.sletanje_sutra          = False
        elif sletanje_sutra == "True" or sletanje_sutra == True:
            self.sletanje_sutra          = True
        self.prevoznik                   = prevoznik
        if type(dani) == str:
            self.dani                    = ast.literal_eval(dani)
        else:
            self.dani                    = dani
        if type(model) == str:
            self.model                   = ast.literal_eval(model)
        else:
            self.model                   = model
        self.cena                        = float(cena)

        if type(datum_pocetka_operativnosti) == str:
            self.datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, "%Y-%m-%d %H:%M:%S")
        elif datum_pocetka_operativnosti:
            self.datum_pocetka_operativnosti = datum_pocetka_operativnosti

        if type(datum_kraja_operativnosti) == str:
            self.datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, "%Y-%m-%d %H:%M:%S")
        elif datum_kraja_operativnosti:
            self.datum_kraja_operativnosti = datum_kraja_operativnosti
    def proveri_podatke(self) -> str:
        greska = "\n"
        if type(self.broj_leta) != str or not self.broj_leta.isalnum() or len(self.broj_leta) != 4:
            greska += "ERROR: Broj leta nije validan!\n"
        if type(self.vreme_poletanja) != str or len(self.vreme_poletanja) != 5 or self.vreme_poletanja[2] != ':' or not self.vreme_poletanja.replace(':','0').isdigit():
            greska += "ERROR: Vreme poletanja nije validno!\n"
        if type(self.vreme_sletanja) != str or len(self.vreme_sletanja) != 5 or self.vreme_sletanja[2] != ':' or not self.vreme_sletanja.replace(':','0').isdigit():
            greska += "ERROR: Vreme sletanja nije validno!\n"
        if len(self.dani) < 1:
            greska += "ERROR: Let mora imati bar jedan dan!"
        for dan in self.dani:
            if type(dan) != int or dan < 0 or dan > 6:
                greska += "ERROR: Dani nisu validni!\n"
                break
        if type(self.model) != dict or len(self.model) == 0:
            greska += "ERROR: Model aviona nije validan!\n"
        if not self.cena or self.cena < 0:
            greska += "ERROR: Cena nije validna!\n"
        if type(self.sifra_polazisnog_aerodroma) != str or len(self.sifra_polazisnog_aerodroma) != 3 or not self.sifra_polazisnog_aerodroma.isalpha():
            greska += "ERROR: Sifra polazisnog aerodroma nije validna!\n"
        if type(self.sifra_odredisnog_aerodorma) != str or len(self.sifra_odredisnog_aerodorma) != 3 or not self.sifra_odredisnog_aerodorma.isalpha():
            greska += "ERROR: Sifra odredisnog aerodroma nije validna!\n"
        if not self.prevoznik:
            greska += "ERROR: Prevoznik nije odredjen!"
        if self.sletanje_sutra is None:
            greska += "ERROR: Parametar sletanje sutra nije odredjen!"
        elif self.sletanje_sutra == False and self.vreme_sletanja <= self.vreme_poletanja:
            pass
        #    greska += "ERROR: Avion ne moze da sleti pre nego sto je poleteo!"
        if self.datum_kraja_operativnosti <= self.datum_pocetka_operativnosti:
            greska += "ERROR: Kraj operativnosti je pre pocetka!"

        if greska == "\n":
            greska = None
        return greska
"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizovanih_letova(svi_letovi: dict) -> list:
    return [let for let in svi_letovi.values() if let["datum_pocetka_operativnosti"] > datetime.now()]

"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "", datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "")->list:
    rezultat = []
    for sifra,let in konkretni_letovi.items():
        broj_leta = let["broj_leta"]
        if polaziste and svi_letovi[broj_leta]["sifra_polazisnog_aerodroma"] != polaziste:
            continue
        if odrediste and svi_letovi[broj_leta]["sifra_odredisnog_aerodorma"] != odrediste:
            continue
        if datum_polaska and let["datum_i_vreme_polaska"] != datum_polaska:
            continue
        if datum_dolaska and let["datum_i_vreme_dolaska"] != datum_dolaska:
            continue
        if vreme_poletanja and svi_letovi[broj_leta]["vreme_poletanja"] != vreme_poletanja:
            continue
        if vreme_sletanja and svi_letovi[broj_leta]["vreme_sletanja"] != vreme_sletanja:
            continue
        if prevoznik and svi_letovi[broj_leta]["prevoznik"] != prevoznik:
            continue
        rezultat.append(let)
    return rezultat

def pretraga_obicnih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str = "", vreme_poletanja: str = "",
                            vreme_sletanja: str = "", prevoznik: str = "", model: str = "", cena: float = "",
                            datum_pocetka_operativnosti: datetime = None, datum_kraja_operativnosti: datetime = None)->list:
    rezultat = []
    for let in svi_letovi.values():
        if polaziste and let["sifra_polazisnog_aerodroma"] != polaziste:
            continue
        if odrediste and let["sifra_odredisnog_aerodorma"] != odrediste:
            continue
        if vreme_poletanja and let["vreme_poletanja"] != vreme_poletanja:
            continue
        if vreme_sletanja and let["vreme_sletanja"] != vreme_sletanja:
            continue
        if prevoznik and let["prevoznik"] != prevoznik:
            continue
        if model and model in model_aviona.svi_modeli_aviona and let["model"] != model_aviona.svi_modeli_aviona[model]:
            continue
        if cena and let["cena"] != cena:
            continue
        if datum_pocetka_operativnosti and let["datum_pocetka_operativnosti"] != datum_pocetka_operativnosti:
            continue
        if datum_kraja_operativnosti and let["datum_kraja_operativnosti"] != datum_kraja_operativnosti:
            continue
        rezultat.append(let)
    return rezultat

"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None,
                     datum_kraja_operativnosti: datetime = None):
    argumenti = locals()
    del argumenti["svi_letovi"]
    try:
        let = Let(**argumenti)
    except Exception as e:
        raise Exception("\nERROR: Neispravni podaci:\n" + str(e) + "\n")

    greska = let.proveri_podatke()
    if broj_leta in svi_letovi:
        greska += "ERROR: Dati let vec postoji!\n"
    if greska:
        raise Exception(greska)

    svi_letovi[let.broj_leta] = let.__dict__
    return svi_letovi

"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def izmena_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str, sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str, dani: list,
                     model: dict, cena: float, datum_pocetka_operativnosti: datetime, datum_kraja_operativnosti: datetime)-> dict:
    argumenti = locals()
    del argumenti["svi_letovi"]
    try:
        let = Let(**argumenti)
    except Exception as e:
        raise Exception("\nERROR: Neispravni podaci:\n" + str(e) + "\n")

    greska = let.proveri_podatke()
    if broj_leta not in svi_letovi:
        greska += "ERROR: Dati let ne postoji!\n"
    if greska:
        raise Exception(greska)

    svi_letovi[let.broj_leta] = let.__dict__
    return svi_letovi
"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    with open(putanja, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=separator)
        for broj_leta in svi_letovi:
            let = Let(**svi_letovi[broj_leta])  # da bi bili sigurni da su fajlovi uvek u istom formatu, koristimo klasu
            csv_writer.writerow(let.__dict__.values())  # pretvaramo vrednosti iz klase nazad u recnik, i iz recnika
                                                        # u listu koju saljemo funkciji writerow

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    svi_letovi = dict()
    with open(putanja, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=separator)
        for row in csv_reader:
            if len(row) == 0:  # U slucaju da je red prazan, preskocicemo ga
                continue
            let = Let(*row)  # moramo da otpakujemo listu da bi je poslali kao niz parametara
            svi_letovi[let.broj_leta] = let.__dict__  # pretvaramo klasu u recnik pomocu ugradjene funkcije
    return svi_letovi


"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi: dict, konkretan_let: dict) -> None:
    try:
        broj_redova  =     svi_letovi[konkretan_let["broj_leta"]]["model"]["broj_redova"]
        broj_sedista = len(svi_letovi[konkretan_let["broj_leta"]]["model"]["pozicije_sedista"])
        konkretan_let["zauzetost"] = [[False for _ in range(broj_sedista)] for _ in range(broj_redova)]
    except Exception as exception:
        raise exception

"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretan_let: dict) -> list:
    return konkretan_let["zauzetost"]

"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""
def checkin(karta, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str) -> (dict, dict):
    if datetime.now() + timedelta(hours=48) > konkretni_let["datum_i_vreme_polaska"]:
        raise Exception("ERROR: Prosao rok za checkin!")
    if not red or not pozicija:
        raise Exception("ERROR: Red ili pozicija su prazni!")
    if "zauzetost" not in konkretni_let or not konkretni_let["zauzetost"]:
        podesi_matricu_zauzetosti(svi_letovi, konkretni_let)
    try: # Imamo try za slucaj da su red ili pozicija previse veliki ili premali
        if matrica_zauzetosti(konkretni_let)[red-1][ord(pozicija) - ord('A')]:
            raise Exception("ERROR: Sediste je zauzeto!")
    except Exception as exception:
        raise exception

    konkretni_let["zauzetost"][red-1][ord(pozicija) - ord('A')] = True
    karta["sediste"]  = pozicija + str(red)

    return konkretni_let, karta


"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""
def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    rezultat = []
    referentan_let = svi_letovi[konkretni_let["broj_leta"]]
    for konk_let in svi_konkretni_letovi.values():
        let = svi_letovi[konk_let["broj_leta"]]
        if let["sifra_polazisnog_aerodroma"] != referentan_let["sifra_odredisnog_aerodorma"]:
            continue
        if konk_let["datum_i_vreme_polaska"] - timedelta(minutes=120) > konkretni_let["datum_i_vreme_dolaska"]:
            continue
        if konk_let["datum_i_vreme_polaska"] < konkretni_let["datum_i_vreme_dolaska"]:
            continue
        rezultat.append(konk_let)
    return rezultat


"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""
def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    rezultat = []
    for konkretan_let in konkretni_letovi.values():
        if konkretan_let["broj_leta"] not in svi_letovi:
            continue
        let = svi_letovi[konkretan_let["broj_leta"]]
        if abs((datum_polaska - konkretan_let["datum_i_vreme_polaska"]).days) <= broj_fleksibilnih_dana:
            if abs((datum_dolaska - konkretan_let["datum_i_vreme_dolaska"]).days) <= broj_fleksibilnih_dana:
                if (not polaziste or let["sifra_polazisnog_aerodroma"] == polaziste) and \
                   (not odrediste or let["sifra_odredisnog_aerodorma"] == odrediste):
                    rezultat.append(konkretan_let)

    return rezultat

def najjeftinijh_10(svi_letovi: dict, polaziste: str, odrediste: str) -> list:
    filtrirani = [let for let in svi_letovi.values() if (not polaziste or let["sifra_polazisnog_aerodroma"] == polaziste)
                                                    and (not odrediste or let["sifra_odredisnog_aerodorma"] == odrediste)]
    if not filtrirani or len(filtrirani) < 2:
        return filtrirani
    sortirani = sorted(filtrirani, key=lambda let: let["cena"])
    top_10 = []
    for i in range(min(10, len(sortirani))-1, -1, -1):
        top_10.append(sortirani[i])
    return top_10
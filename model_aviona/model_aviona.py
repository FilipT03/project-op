import csv
import ast

svi_modeli_aviona = {}

class ModelAviona:
    def __init__(self, id: int, naziv: str = "", broj_redova: str = "", pozicije_sedista: list = ""):
        self.id                   = int(id)
        self.naziv                = naziv
        self.broj_redova          = int(broj_redova)
        if type(pozicije_sedista) == str:
            self.pozicije_sedista = ast.literal_eval(pozicije_sedista)
        else:
            self.pozicije_sedista = pozicije_sedista
    def proveri_podatke(self) -> str:
        greska = "\n"

        if not self.naziv:
            greska += "ERROR: naziv je null!"
        if not self.broj_redova:
            greska += "ERROR: broj_redova je null!"
        if not self.pozicije_sedista:
            greska += "ERROR: pozicije_sedista je null!"

        if greska == "\n":
            greska = None
        return greska

sledeci_id_modela_aviona = 0

"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str ="",
    broj_redova: str = "",
    pozicije_sedista: list = []
) -> dict:
    global sledeci_id_modela_aviona
    try:
        model_aviona = ModelAviona(sledeci_id_modela_aviona, naziv, broj_redova, pozicije_sedista)
    except Exception as e:
        raise Exception("\nERROR: Neispravni podaci:\n" + str(e) + "\n")

    greska = model_aviona.proveri_podatke()
    if greska:
        raise Exception(greska)

    svi_modeli_aviona[sledeci_id_modela_aviona] = model_aviona.__dict__
    sledeci_id_modela_aviona += 1
    return svi_modeli_aviona

"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=separator)
        for id in svi_aerodromi:
            model_aviona = ModelAviona(**svi_aerodromi[id]) # da bismo bili sigurni da su fajlovi uvek u istom formatu, koristimo klasu
            csv_writer.writerow(model_aviona.__dict__.values()) # pretvaramo vrednosti iz klase nazad u recnik, i iz recnika
                                                                # u listu koju saljemo funkciji writerow


"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    svi_modeli_aviona = dict()
    with open(putanja, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=separator)
        for row in csv_reader:
            if len(row) == 0:  # U slucaju da je red prazan, preskocicemo ga
                continue
            model_aviona = ModelAviona(*row)  # moramo da otpakujemo listu da bi je poslali kao niz parametara
            svi_modeli_aviona[model_aviona.id] = model_aviona.__dict__  # pretvaramo klasu u recnik pomocu ugradjene funkcije
    return svi_modeli_aviona

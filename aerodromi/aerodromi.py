import csv

svi_aerodromi = {}

class Aerodrom:
    def __init__(self, skracenica: str ="", pun_naziv: str ="", grad: str ="", drzava: str =""):
        self.skracenica = skracenica
        self.pun_naziv  = pun_naziv
        self.grad       = grad
        self.drzava     = drzava
    def proveri_podatke(self) -> str:
        greska = "\n"

        if not self.skracenica:
            greska += "ERROR: skracenica je null"
        if not self.pun_naziv:
            greska += "ERROR: pun_naziv je null"
        if not self.grad:
            greska += "ERROR: grad je null"
        if not self.drzava:
            greska += "ERROR: drzava je null"

        if greska == "\n":
            greska = None
        return greska

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str ="",
    pun_naziv: str ="",
    grad: str ="",
    drzava: str =""
) -> dict:
    aerodrom = Aerodrom(skracenica, pun_naziv, grad, drzava)

    greska = aerodrom.proveri_podatke()
    if greska:
        raise Exception(greska)

    svi_aerodromi[aerodrom.skracenica] = aerodrom.__dict__
    return svi_aerodromi

"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=separator)
        for skracenica in svi_aerodromi:
            aerodrom = Aerodrom(**svi_aerodromi[skracenica]) # da bismo bili sigurni da su fajlovi uvek u istom formatu, koristimo klasu
            csv_writer.writerow(aerodrom.__dict__.values())  # pretvaramo vrednosti iz klase nazad u recnik, i iz recnika
                                                             # u listu koju saljemo funkciji writerow

"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    svi_aerodromi = dict()
    with open(putanja, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=separator)
        for row in csv_reader:
            if len(row) == 0:  # U slucaju da je red prazan, preskocicemo ga
                continue
            aerodrom = Aerodrom(*row)  # moramo da otpakujemo listu da bi je poslali kao niz parametara
            svi_aerodromi[aerodrom.skracenica] = aerodrom.__dict__  # pretvaramo klasu u recnik pomocu ugradjene funkcije
    return svi_aerodromi
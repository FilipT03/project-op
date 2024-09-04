#Autor: Filip Tot SV14/2022

import common.konstante
from common import konstante
import csv

svi_korisnici = {}

class Korisnik:
    def __init__(self, korisnicko_ime, uloga, lozinka, ime, prezime, email = "", pasos = "", drzavljanstvo = "", telefon = "", pol = ""):
        self.korisnicko_ime = korisnicko_ime
        self.uloga          = uloga
        self.lozinka        = lozinka
        self.ime            = ime
        self.prezime        = prezime
        self.email          = email
        self.pasos          = pasos
        self.drzavljanstvo  = drzavljanstvo
        self.telefon        = telefon
        self.pol            = pol

    def proveri_podatke(self, svi_korisnici, azuriraj, staro_korisnicko_ime) -> str:
        greska = "\n"
        if azuriraj:
            if not svi_korisnici.get(staro_korisnicko_ime):
                greska += "ERROR: Korisnik ne postoji!\n"

        if svi_korisnici.get(self.korisnicko_ime) and self.korisnicko_ime != staro_korisnicko_ime:
            greska += "ERROR: Korisnicko ime je zauzeto!\n"
        if not self.korisnicko_ime:
            greska += "ERROR: Korisnicko ime nije prosledjeno!\n"

        if (self.uloga != konstante.ULOGA_KORISNIK) and (self.uloga != konstante.ULOGA_PRODAVAC) and (self.uloga != konstante.ULOGA_ADMIN):
            greska += "ERROR: Uloga nije validna!\n"
        if not self.lozinka:
            greska += "ERROR: Lozinka nije prosledjena!\n"
        if not self.ime:
            greska += "ERROR: Ime nije prosledjeno!\n"
        if not self.prezime:
            greska += "ERROR: Prezime nije prosledjeno!\n"
        
        if (not self.email) or ((type(self.email) != str) or (self.email.count('@') != 1) or (self.email[0] == '@') or (self.email.split('@')[1].count('.') != 1) or (self.email.split('@')[1][0] == '.') or (len(self.email.split('@')[1].split('.')[1]) == 0)):
            greska += "ERROR: Email nije validan!\n"  # email mora sadrzati tacno jedan @ i tacno jednu .(posle @) i delovi oko njih ne smeju biti prazni
        if self.pasos and (not self.pasos.isdigit() or len(self.pasos) != 9):
            greska += "ERROR: Pasos se ne sastoji od 9 cifara!\n"
        if (not self.telefon) or (not self.telefon.isdigit()):
            greska += "ERROR: Telefon se ne sastoji od cifara!\n"

        if greska == "\n":
            greska = None
        return greska

"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni (ne važi za konverziju brojeva).
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""

def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, 
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:
    korisnik = Korisnik(korisnicko_ime, uloga, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)

    greska = korisnik.proveri_podatke(svi_korisnici, azuriraj, staro_korisnicko_ime)
    if greska:
        raise Exception(greska)

    if azuriraj == False:
        # Kreiramo novog korisnika
        svi_korisnici[korisnicko_ime] = korisnik.__dict__
        return svi_korisnici
    else:
        # Menjamo postojeceg korisnika
        del svi_korisnici[staro_korisnicko_ime]
        svi_korisnici[korisnicko_ime] = korisnik.__dict__
        return svi_korisnici



"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    with open(putanja, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = separator)
        for korisnicko_ime in svi_korisnici:
            korisnik = Korisnik(**svi_korisnici[korisnicko_ime])
            csv_writer.writerow(korisnik.__dict__.values()) # pretvaramo vrednosti iz recnika u listu i saljemo funkciji writerow
"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    svi_korisnici = dict()
    with open(putanja, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = separator)
        for row in csv_reader:
            if len(row) == 0:  # U slucaju da je red prazan, preskocicemo ga
                continue
            korisnik = Korisnik(*row)  # moramo da otpakujemo listu da bi je poslali kao niz parametara
            svi_korisnici[korisnik.korisnicko_ime] = korisnik.__dict__  # pretvaramo klasu u recnik pomocu ugradjene funkcije
    return svi_korisnici


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""

def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    if not svi_korisnici.get(korisnicko_ime) or svi_korisnici[korisnicko_ime]['lozinka'] != lozinka:  # U slucaju da korisnik ne postoji ili je uneta pogresna sifra
        raise Exception("ERROR: Korisničko ime ili lozinka nisu ispravni!")                                # vracaticemo gresku
    return svi_korisnici[korisnicko_ime]


"""
Funkcija koja vrsi log out
*
"""
def logout(korisnicko_ime: str):
    print(f"Korisnik {korisnicko_ime} je sada izlogovan!")
    pass

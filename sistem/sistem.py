#Autor: Filip Tot SV14/2022

import os

from meniji.meniji import *
from common import  konstante

def ucitaj_podatke():
    karte.set_u_test(False)
    if os.path.isfile("data/letovi.csv"):
        letovi.svi_letovi = letovi.ucitaj_letove_iz_fajla("data/letovi.csv","|")
    if os.path.isfile("data/modeli_aviona.csv"):
        model_aviona.svi_modeli_aviona = model_aviona.ucitaj_modele_aviona("data/modeli_aviona.csv","|")
    if os.path.isfile("data/aerodromi.csv"):
        aerodromi.svi_aerodromi = aerodromi.ucitaj_aerodrom("data/aerodromi.csv","|")
    if os.path.isfile("data/korisnici.csv"):
        korisnici.svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla("data/korisnici.csv","|")
    if os.path.isfile("data/konkretni_letovi.csv"):
        konkretni_letovi.svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let("data/konkretni_letovi.csv","|")
    if os.path.isfile("data/karte.csv"):
        karte.sve_karte = karte.ucitaj_karte_iz_fajla("data/karte.csv","|")


def print_meni(meni, username:str = "", short:bool = False, clear_text:bool = True):
    if clear_text: clear()
    if not short:
        print("==============================================================")
        print("Projektni zadatak" + '{:>45}'.format(username))
        print("==============================================================")
    index = 0
    for opcija in meni:
        index += 1
        if index < 10:
            print(f"{index}. {opcija[0]}")
        else:
            print(f"{index}.{opcija[0]}")
    error()

def error(greska_za_ispis = None):
    global greska
    if greska_za_ispis:
        greska = greska_za_ispis
    if greska:
        print(f"\033[91m{greska}\033[0m")
        greska = ""
    else:
        print()

if os.name == "nt":
    def clear(): os.system('cls')
else:
    def clear(): os.system('clear')


def wait_for_continue(new_line = True):
    if new_line: print()
    input("Press ENTER to continue...")

def izbor(opcije):
    global greska
    odluka = input(f"Unesite komandu(1-{len(opcije)}): ")
    if not odluka.isdecimal() or int(odluka) > len(opcije):
        greska = "Pogrešan unos. Pokušajte ponovo..."
    else:
        return opcije[int(odluka)-1][1]()

def start():
    ucitaj_podatke()
    global dezurni_prodavac
    for korisnik in korisnici.svi_korisnici.values():
        if korisnik["uloga"] == konstante.ULOGA_PRODAVAC:
            dezurni_prodavac = korisnik
            break
    global greska
    greska = ""
    while True:
        print_meni(glavni_meni)
        izbor(glavni_meni)

def get_dezurni_prodavac() -> dict:
    global dezurni_prodavac
    return dezurni_prodavac

def set_greska(value: str):
    global greska
    greska = value
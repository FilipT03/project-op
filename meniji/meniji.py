import copy

from tabulate import tabulate

from letovi import letovi
from konkretni_letovi import konkretni_letovi
from korisnici import korisnici
from karte import karte
from aerodromi import aerodromi
from model_aviona import model_aviona
from sistem import sistem
from datetime import datetime
from common import konstante
from izvestaji import izvestaji

let_headers = {"broj_leta": "Broj leta", "sifra_polazisnog_aerodroma": "Šifra pol. aer.",
               "sifra_odredisnog_aerodorma": "Šifra odr. aer.", "vreme_poletanja": "Vreme pol.",
               "vreme_sletanja": "Vreme slet.", "dani": "Dani", "cena": "Cena",
               "datum_pocetka_operativnosti": "Početak oper.", "datum_kraja_operativnosti": "Kraj oper.",
               "prevoznik": "Prevoznik", "sifra": "Šifra konk. leta", "datum_i_vreme_polaska":"Datum i vreme pol.",
               "datum_i_vreme_dolaska":"Datum i vreme dol.", "zauzetost": "Zauzeto"}

karta_headers = {"broj_karte": "Broj karte", "sifra_konkretnog_leta": "Šifra konk. leta", "kupac": "Kupac", "putnici": "Putnik",
                 "prodavac": "Prodavac", "sediste": "Sedište", "datum_prodaje": "Datum prodaje", "status": "Status", "cena": "Cena",
                 "datum_i_vreme_polaska":"Datum i vreme pol.", "datum_i_vreme_dolaska":"Datum i vreme dol.", "obrisana":"Obrisana"}


def login():
    print()
    korisnicko_ime = input("Korisničko ime: ")
    lozinka = input("Lozinka: ")
    print()
    try:
        global korisnik
        korisnik = korisnici.login(korisnici.svi_korisnici, korisnicko_ime, lozinka)
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue()
        return
    if korisnik["uloga"] == konstante.ULOGA_KORISNIK:
        while True:
            sistem.print_meni(korisnicki_meni, korisnicko_ime)
            if sistem.izbor(korisnicki_meni): return
    elif korisnik["uloga"] == konstante.ULOGA_PRODAVAC:
        while True:
            sistem.print_meni(prodavac_meni, korisnicko_ime)
            if sistem.izbor(prodavac_meni): return
    elif korisnik["uloga"] == konstante.ULOGA_ADMIN:
        while True:
            sistem.print_meni(admin_meni, korisnicko_ime)
            if sistem.izbor(admin_meni): return

def register():
    print()
    korisnicko_ime = input("Korisničko ime (obavezno): ")
    lozinka = input("Lozinka (obavezno): ")
    ime = input("Ime (obavezno): ")
    prezime = input("Prezime (obavezno): ")
    email = input("Email (obavezno): ")
    telefon = input("Telefon (obavezno): ")
    pasos = input("Pasoš: ")
    drzavljanstvo = input("Državljanstvo: ")
    pol = input("Pol: ")
    try:
        global korisnik
        korisnik = korisnici.kreiraj_korisnika(korisnici.svi_korisnici, False, "korisnik", "", korisnicko_ime, lozinka,
                                               ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return
    while True:
        sistem.print_meni(korisnicki_meni, korisnicko_ime)
        if sistem.izbor(korisnicki_meni): return

def pregled_nerealizovanih_letova():
    print()
    nerealizovani_letovi = copy.deepcopy(letovi.pregled_nerealizovanih_letova(letovi.svi_letovi))
    dani_skraceno = ["Pon", "Uto", "Sre", "Čet", "Pet", "Sub", "Ned"]
    for let in nerealizovani_letovi:
        del let["model"]
        del let["sletanje_sutra"]
        let["dani"] = ", ".join([dani_skraceno[x] for x in let["dani"]])
    print(tabulate(nerealizovani_letovi, numalign="left", headers=let_headers))
    sistem.wait_for_continue()

def pretraga_letova():
    sistem.clear()
    print("Upišite krijeterijume po kojima želite da pretražite letove (pritisnite ENTER da preskočite kriterijum). U zagradi se nalaze primeri podataka:")
    polaziste = input("Polazište (msu): ")
    odrediste = input("Odredište (bju): ")
    try:
        datum_polaska = input("Datum polaska (2031-03-30 08:46:51): ")
        datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d %H:%M:%S")
    except Exception:
        datum_polaska = None
    try:
        datum_dolaska = input("Datum dolaska (2031-03-30 22:02:51): ")
        datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d %H:%M:%S")
    except Exception:
        datum_dolaska = None
    vreme_poletanja = input("Vreme poletanja (11:10): ")
    vreme_sletanja = input("Vreme sletanja (20:15): ")
    prevoznik = input("Prevoznik (Air Serbia): ")
    filtrirani_letovi = copy.deepcopy(letovi.pretraga_letova(letovi.svi_letovi, konkretni_letovi.svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik))
    print()
    if filtrirani_letovi is None or len(filtrirani_letovi) == 0:
        sistem.error("Nije pronađen nijedan let.")
    else:
        for let in filtrirani_letovi:
            let["sifra_polazisnog_aerodroma"] = letovi.svi_letovi[let["broj_leta"]]["sifra_polazisnog_aerodroma"]
            let["sifra_odredisnog_aerodorma"] = letovi.svi_letovi[let["broj_leta"]]["sifra_odredisnog_aerodorma"]
            let["cena"]                       = letovi.svi_letovi[let["broj_leta"]]["cena"]
            let["prevoznik"]                  = letovi.svi_letovi[let["broj_leta"]]["prevoznik"]
            zauzeto = 0
            ukupno = 0
            for lista in let["zauzetost"]:
                for stanje in lista:
                    if stanje:
                        zauzeto += 1
                    ukupno += 1
            let["zauzetost"] = f"{zauzeto}/{ukupno}"
        print(tabulate(filtrirani_letovi, numalign="left", headers=let_headers))
    sistem.wait_for_continue()


def povezani_letovi(povezani_let):
    sistem.clear()
    print("Sledeći letovi kreću na istom aerodromu na koji sleće prethodni let, i polaze najkasnije 2 sata nakon tog leta:")
    filtrirani_letovi = copy.deepcopy(letovi.povezani_letovi(letovi.svi_letovi, konkretni_letovi.svi_konkretni_letovi, povezani_let))
    print()
    if filtrirani_letovi is None or len(filtrirani_letovi) == 0:
        sistem.error("Nema povezanih letova.")
    else:
        for let in filtrirani_letovi:
            let["sifra_polazisnog_aerodroma"] = letovi.svi_letovi[let["broj_leta"]]["sifra_polazisnog_aerodroma"]
            let["sifra_odredisnog_aerodorma"] = letovi.svi_letovi[let["broj_leta"]]["sifra_odredisnog_aerodorma"]
            let["cena"]                       = letovi.svi_letovi[let["broj_leta"]]["cena"]
            let["prevoznik"]                  = letovi.svi_letovi[let["broj_leta"]]["prevoznik"]
            zauzeto = 0
            ukupno = 0
            for lista in let["zauzetost"]:
                for stanje in lista:
                    if stanje:
                        zauzeto += 1
                    ukupno += 1
            let["zauzetost"] = f"{zauzeto}/{ukupno}"
        print(tabulate(filtrirani_letovi, numalign="left", headers=let_headers))
    sistem.wait_for_continue()

def pretraga_obicnih_letova():
    sistem.clear()
    print("Upišite krijeterijume po kojima želite da pretražite letove (pritisnite ENTER da preskočite kriterijum). U zagradi se nalaze primeri podataka:")
    polaziste = input("Polazište (msu): ")
    odrediste = input("Odredište (bju): ")
    vreme_poletanja = input("Vreme poletanja (11:10): ")
    vreme_sletanja = input("Vreme sletanja (20:15): ")
    prevoznik = input("Prevoznik (Air Serbia): ")
    model = input("ID modela aviona (101): ")
    try:
        cena = input("Cena (150.75): ")
        cena = float(cena)
    except Exception:
        cena = None
    try:
        datum_pocetka_operativnosti = input("Datum početak operativnosti (2031-03-30 08:46:51): ")
        datum_pocetka_operativnosti = datetime.strptime(datum_pocetka_operativnosti, "%Y-%m-%d %H:%M:%S")
    except Exception:
        datum_pocetka_operativnosti = None
    try:
        datum_kraja_operativnosti = input("Datum kraja operativnosti (2031-03-30 22:02:51): ")
        datum_kraja_operativnosti = datetime.strptime(datum_kraja_operativnosti, "%Y-%m-%d %H:%M:%S")
    except Exception:
        datum_kraja_operativnosti = None
    filtrirani_letovi = copy.deepcopy(letovi.pretraga_obicnih_letova(letovi.svi_letovi, polaziste, odrediste, vreme_poletanja, vreme_sletanja, prevoznik, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti))
    print()
    dani_skraceno = ["Pon", "Uto", "Sre", "Čet", "Pet", "Sub", "Ned"]
    if filtrirani_letovi is None or len(filtrirani_letovi) == 0:
        sistem.error("Nije pronađen nijedan let.")
    else:
        for let in filtrirani_letovi:
            del let["model"]
            del let["sletanje_sutra"]
            let["dani"] = ", ".join([dani_skraceno[x] for x in let["dani"]])
        print(tabulate(filtrirani_letovi, numalign="left", headers=let_headers))
    sistem.wait_for_continue()


def prikaz_10_najjeftinijih():
    sistem.clear()
    print("Upišite željeno polazište i odredište (pritisnite ENTER da preskočite kriterijum). U zagradi se nalaze primeri podataka:")
    polaziste = input("Polazište (msu): ")
    odrediste = input("Odredište (bju): ")
    top_10 = copy.deepcopy(letovi.najjeftinijh_10(letovi.svi_letovi, polaziste, odrediste))
    dani_skraceno = ["Pon", "Uto", "Sre", "Čet", "Pet", "Sub", "Ned"]
    print()
    if top_10 is None or len(top_10) == 0:
        sistem.error("Nije pronađen nijedan let.")
    else:
        for let in top_10:
            del let["model"]
            del let["sletanje_sutra"]
            let["dani"] = ", ".join([dani_skraceno[x] for x in let["dani"]])
        print(tabulate(top_10, numalign="left", headers=let_headers))
    sistem.wait_for_continue()

def fleksibilni_polasci():
    sistem.clear()
    print("Upišite krijeterijume po kojima želite da pretražite letove (pritisnite ENTER da preskočite kriterijum). U zagradi se nalaze primeri podataka:")
    polaziste = input("Polazište (msu): ")
    odrediste = input("Odredište (bju): ")
    try:
        datum_polaska = input("Datum polaska (2031-03-30 08:46:51)(obavezno): ")
        datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d %H:%M:%S")
        datum_dolaska = input("Datum dolaska (2031-03-30 22:02:51)(obavezno): ")
        datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d %H:%M:%S")
        broj_fleksibilnih_dana = input("Broj fleksibilnih dana (obavezno): ")
        broj_fleksibilnih_dana = int(broj_fleksibilnih_dana)
        print()
    except Exception:
        print()
        sistem.error("Neispravan unos!")
        sistem.wait_for_continue()
        return
    fleksibilni_letovi = copy.deepcopy(letovi.fleksibilni_polasci(letovi.svi_letovi, konkretni_letovi.svi_konkretni_letovi, polaziste, odrediste, datum_polaska, broj_fleksibilnih_dana, datum_dolaska))

    if fleksibilni_letovi is None or len(fleksibilni_letovi) == 0:
        sistem.error("Nije pronađen nijedan let.")
    else:
        for let in fleksibilni_letovi:
            let["sifra_polazisnog_aerodroma"] = letovi.svi_letovi[let["broj_leta"]]["sifra_polazisnog_aerodroma"]
            let["sifra_odredisnog_aerodorma"] = letovi.svi_letovi[let["broj_leta"]]["sifra_odredisnog_aerodorma"]
            let["cena"]                       = letovi.svi_letovi[let["broj_leta"]]["cena"]
            let["prevoznik"]                  = letovi.svi_letovi[let["broj_leta"]]["prevoznik"]
            zauzeto = 0
            ukupno = 0
            for lista in let["zauzetost"]:
                for stanje in lista:
                    if stanje:
                        zauzeto += 1
                    ukupno += 1
            let["zauzetost"] = f"{zauzeto}/{ukupno}"
        fleksibilni_letovi = sorted(fleksibilni_letovi, key=lambda let: let["cena"], reverse=True)
        print(tabulate(fleksibilni_letovi, numalign="left", headers=let_headers))
    sistem.wait_for_continue()


def kupovina_karata(povezani_let = None):
    while True:
        sistem.print_meni(izbor_konk_leta, short=True)
        odluka = input("Unesite komandu(1-3): ")
        if odluka == '2':
            break
        elif odluka == '1':
            if povezani_let:
                povezani_letovi(povezani_let)
            else:
                pretraga_letova()
        elif odluka == '3':
            return
        else:
            sistem.set_greska("Pogrešan unos. Pokušajte ponovo...")
    print()
    sifra = input("Šifra konkretnog leta: ")
    if not sifra.isdigit() or int(sifra) not in konkretni_letovi.svi_konkretni_letovi:
        sistem.error("Ne postoji konkretan let sa tom šifrom!")
        sistem.wait_for_continue()
        return
    sifra = int(sifra)
    konkretan_let = konkretni_letovi.svi_konkretni_letovi[sifra]
    ima_mesta = karte.da_li_postoji_slobodno_mesto(konkretan_let["zauzetost"])
    if not ima_mesta:
        sistem.error("Na tom letu nema slobodnih mesta.")
        sistem.wait_for_continue()
        return

    za_sebe = input("Da li kupujete kartu za sebe? (Da/Ne): ")
    if za_sebe.lower() == "ne":
        ime, prezime = None, None
        while not ime:
            ime = input("Ime druge osobe (obavezno): ")
        while not prezime:
            prezime = input("Prezime druge osobe (obavezno): ")

    potvrda = input("Da li želite da kupite kartu sa upisanim podacima? (Da/Ne): ")
    if potvrda.lower() == "ne":
        sistem.wait_for_continue()
        return

    global korisnik
    dezurni_prodavac = sistem.get_dezurni_prodavac()
    try:
        if za_sebe.lower() == "ne":
            karta, karte.sve_karte = karte.kupovina_karte(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, sifra,
                                                          [{"ime":ime, "prezime":prezime}], letovi.matrica_zauzetosti(konkretan_let),
                                                          korisnik, prodavac=dezurni_prodavac, datum_prodaje=datetime.now().replace(microsecond=0))
        else:
            karta, karte.sve_karte = karte.kupovina_karte(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, sifra,
                                                          [korisnik], letovi.matrica_zauzetosti(konkretan_let),
                                                          korisnik, prodavac=dezurni_prodavac, datum_prodaje=datetime.now().replace(microsecond=0))
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return

    print("Kupovina uspešna! Da li želite da nastavite sa kupovinom?")
    sistem.print_meni(nastavak_kupovine, short=True, clear_text=False)
    odluka = input("Unesite komandu(1-3): ")
    if odluka == '1':
        jos = "da"
        while jos.lower() == "da":
            ima_mesta = karte.da_li_postoji_slobodno_mesto(konkretan_let["zauzetost"])
            if not ima_mesta:
                sistem.error("Na letu nema više slobodnih mesta.")
                sistem.wait_for_continue()
                return

            ime, prezime = None, None
            while not ime:
                ime = input("Ime druge osobe (obavezno): ")
            while not prezime:
                prezime = input("Prezime druge osobe (obavezno): ")

            potvrda = input("Da li želite da kupite kartu sa upisanim podacima? (Da/Ne): ")
            if potvrda.lower() == "ne":
                sistem.wait_for_continue()
                return

            try:
                karta, karte.sve_karte = karte.kupovina_karte(karte.sve_karte,
                                                              konkretni_letovi.svi_konkretni_letovi, sifra,
                                                              [{"ime": ime, "prezime": prezime}],
                                                              letovi.matrica_zauzetosti(konkretan_let),
                                                              korisnik, prodavac=dezurni_prodavac,
                                                              datum_prodaje=datetime.now().replace(microsecond=0))
            except Exception as e:
                sistem.error(str(e))
                sistem.wait_for_continue(False)
                return

            jos = input("Kupovina uspešna! Da li želite da kupite još karata? (Da/Ne): ")
        return
    elif odluka == '2':
        kupovina_karata(konkretan_let)
        return


def pregled_nerealizovanih_karata():
    print()
    global korisnik
    nerealizovane_karte = copy.deepcopy(karte.pregled_nerealizovanaih_kupljenih_karata(korisnik, karte.sve_karte))
    for karta in nerealizovane_karte:
        del karta["obrisana"]
        karta["kupac"] = karta["kupac"]["korisnicko_ime"]
        karta["prodavac"] = karta["prodavac"]["korisnicko_ime"]
        karta["putnici"] = karta["putnici"][0]["ime"] + " " + karta["putnici"][0]["prezime"]
        karta["status"] = "Nerealizovana"
        konkretan_let = konkretni_letovi.svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
        karta["datum_i_vreme_polaska"] = konkretan_let["datum_i_vreme_polaska"]
        karta["datum_i_vreme_dolaska"] = konkretan_let["datum_i_vreme_dolaska"]
        karta["cena"] = letovi.svi_letovi[konkretan_let["broj_leta"]]["cena"]
    if len(nerealizovane_karte) > 0:
        print(tabulate(nerealizovane_karte, numalign="left", headers=karta_headers))
    else:
        print("Nema nerealizovanih karata.")
    sistem.wait_for_continue()
def check_in():
    global korisnik
    while True:
        sistem.print_meni(izbor_karte, short=True)
        odluka = input("Unesite komandu(1-3): ")
        if odluka == '2':
            break
        elif odluka == '1':
            pretraga_karata(korisnik["korisnicko_ime"])
        elif odluka == '3':
            return
        else:
            sistem.set_greska("Pogrešan unos. Pokušajte ponovo...")
    print()
    broj = input("Broj karte: ")
    if not broj.isdigit() or int(broj) not in karte.sve_karte:
        sistem.error("Ne postoji karta sa tim brojem!")
        sistem.wait_for_continue()
        return
    broj = int(broj)
    karta = karte.sve_karte[broj]
    if karta["kupac"]["korisnicko_ime"] != korisnik["korisnicko_ime"]:
        sistem.error("Nemate dozvolu da prijavite karte koje niste kupili!")
        sistem.wait_for_continue()
        return
    if karta["sediste"] != "??":
        sistem.error("Ta karta je vec prijavljena!")
        sistem.wait_for_continue()
        return

    if "pasos" not in karta["putnici"][0] or not karta["putnici"][0]["pasos"]:
        pasos = None
        while not pasos:
            pasos = input("Nedostaje pasoš: ")
        karta["putnici"][0]["pasos"] = pasos
    if "drzavljanstvo" not in karta["putnici"][0] or not karta["putnici"][0]["drzavljanstvo"]:
        drzavljanstvo = None
        while not drzavljanstvo:
            drzavljanstvo = input("Nedostaje državljanstvo: ")
        karta["putnici"][0]["drzavljanstvo"] = drzavljanstvo
    if "pol" not in karta["putnici"][0] or not karta["putnici"][0]["pol"]:
        pol = None
        while not pol:
            pol = input("Nedostaje pol: ")
        karta["putnici"][0]["pol"] = pol

    zauzetost = letovi.matrica_zauzetosti(konkretni_letovi.svi_konkretni_letovi[karta["sifra_konkretnog_leta"]])
    ispis:str = ""
    for i in range(len(zauzetost)):
        ispis += f"Red {i+1}. "
        for j in range(len(zauzetost[i])):
            if not zauzetost[i][j]:
                ispis += chr(j + ord('A')) + " "
            else:
                ispis += "X "
        ispis += "\n"
    print("Slobodna mesta na letu (X su zauzeta):")
    print(ispis)

    red, pozicija = None, None
    while not red or not red.isdigit():
        red = input("Upisite red (broj): ")
    while not pozicija or not pozicija.isupper():
        pozicija = input("Upišite poziciju (veliko slovo): ")

    try:
        konkretni_let = konkretni_letovi.svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
        konkretni_let, karta = letovi.checkin(karta, letovi.svi_letovi, konkretni_let,  int(red), pozicija)
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return

    print("Prijava uspešna! Da li želite da uradite još prijava?")
    sistem.print_meni(nastavak_prijave, short=True, clear_text=False)
    odluka = input("Unesite komandu(1-2): ")
    if odluka == '1':
        check_in()

def pretraga_karata(kupac = None): # Ako je kupac prosleđen, to znači da prikazujemo sa smanjenim dozvolama
    sistem.clear()
    print("Upišite krijeterijume po kojima želite da pretražite karte (pritisnite ENTER da preskočite kriterijum). U zagradi se nalaze primeri podataka:")
    polaziste = input("Polazište (msu): ")
    odrediste = input("Odredište (bju): ")
    try:
        datum_polaska = input("Datum polaska (2031-03-30 08:46:51): ")
        datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d %H:%M:%S")
    except Exception:
        datum_polaska = None
    try:
        datum_dolaska = input("Datum dolaska (2031-03-30 22:02:51): ")
        datum_dolaska = datetime.strptime(datum_dolaska, "%Y-%m-%d %H:%M:%S")
    except Exception:
        datum_dolaska = None
    korisnicko_ime_putnika = input("Korisničko ime ili ime i prezime putnika: ")
    filtrirane_karte = copy.deepcopy(karte.pretraga_prodatih_karata(karte.sve_karte, letovi.svi_letovi, konkretni_letovi.svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, korisnicko_ime_putnika, kupac))
    print()
    if filtrirane_karte is None or len(filtrirane_karte) == 0:
        sistem.error("Nije pronađena nijedna karta.")
    else:
        for karta in filtrirane_karte:
            if kupac:
                del karta["obrisana"]
            karta["kupac"] = karta["kupac"]["korisnicko_ime"]
            karta["prodavac"] = karta["prodavac"]["korisnicko_ime"]
            karta["putnici"] = karta["putnici"][0]["ime"] + " " + karta["putnici"][0]["prezime"]
            karta["status"] = "Nerealizovana"
            konkretan_let = konkretni_letovi.svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
            karta["datum_i_vreme_polaska"] = konkretan_let["datum_i_vreme_polaska"]
            karta["datum_i_vreme_dolaska"] = konkretan_let["datum_i_vreme_dolaska"]
            karta["cena"] = letovi.svi_letovi[konkretan_let["broj_leta"]]["cena"]
        print(tabulate(filtrirane_karte, numalign="left", headers=karta_headers))
    sistem.wait_for_continue()

def prodaja_karata(povezani_let = None):
    while True:
        sistem.print_meni(izbor_konk_leta, short=True)
        odluka = input("Unesite komandu(1-3): ")
        if odluka == '2':
            break
        elif odluka == '1':
            if povezani_let:
                povezani_letovi(povezani_let)
            else:
                pretraga_letova()
        elif odluka == '3':
            return
        else:
            sistem.set_greska("Pogrešan unos. Pokušajte ponovo...")
    print()
    sifra = input("Šifra konkretnog leta: ")
    if not sifra.isdigit() or int(sifra) not in konkretni_letovi.svi_konkretni_letovi:
        sistem.error("Ne postoji konkretan let sa tom šifrom!")
        sistem.wait_for_continue()
        return
    sifra = int(sifra)
    konkretan_let = konkretni_letovi.svi_konkretni_letovi[sifra]
    ima_mesta = karte.da_li_postoji_slobodno_mesto(konkretan_let["zauzetost"])
    if not ima_mesta:
        sistem.error("Na tom letu nema slobodnih mesta.")
        sistem.wait_for_continue()
        return

    za_reg = input("Da li kupujete kartu za registrovanog korisnika? (Da/Ne): ")
    korisnicko_ime = None
    if za_reg.lower() == "ne":
        ime, prezime = None, None
        while not ime:
            ime = input("Ime osobe (obavezno): ")
        while not prezime:
            prezime = input("Prezime osobe (obavezno): ")
    else:
        while not korisnicko_ime or korisnicko_ime not in korisnici.svi_korisnici:
            korisnicko_ime = input("Korisničko ime (obavezno): ")

    potvrda = input("Da li želite da prodate kartu sa upisanim podacima? (Da/Ne): ")
    if potvrda.lower() == "ne":
        sistem.wait_for_continue()
        return

    global korisnik
    prodavac = korisnik
    if korisnicko_ime:
        korisnik2 = korisnici.svi_korisnici[korisnicko_ime]
    try:
        if za_reg.lower() == "ne":
            karta, karte.sve_karte = karte.kupovina_karte(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, sifra,
                                                          [{"ime": ime, "prezime": prezime}],
                                                          letovi.matrica_zauzetosti(konkretan_let),
                                                          {"ime": ime, "prezime": prezime}, prodavac=prodavac,
                                                          datum_prodaje=datetime.now().replace(microsecond=0))
        else:
            karta, karte.sve_karte = karte.kupovina_karte(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, sifra,
                                                          [korisnik2], letovi.matrica_zauzetosti(konkretan_let),
                                                          korisnik2, prodavac=prodavac,
                                                          datum_prodaje=datetime.now().replace(microsecond=0))
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return

    print("Prodaja uspešna! Da li želite da nastavite sa prodajom?")
    sistem.print_meni(nastavak_prodaje, short=True, clear_text=False)
    odluka = input("Unesite komandu(1-3): ")
    if odluka == '1':
        jos = "da"
        while jos.lower() == "da":
            ima_mesta = karte.da_li_postoji_slobodno_mesto(konkretan_let["zauzetost"])
            if not ima_mesta:
                sistem.error("Na letu nema više slobodnih mesta.")
                sistem.wait_for_continue()
                return

            za_reg = input("Da li kupujete kartu za registrovanog korisnika? (Da/Ne): ")
            korisnicko_ime = None
            if za_reg.lower() == "ne":
                ime, prezime = None, None
                while not ime:
                    ime = input("Ime osobe (obavezno): ")
                while not prezime:
                    prezime = input("Prezime osobe (obavezno): ")
            else:
                while not korisnicko_ime or korisnicko_ime not in korisnici.svi_korisnici:
                    korisnicko_ime = input("Korisničko ime (obavezno): ")

            potvrda = input("Da li želite da kupite kartu sa upisanim podacima? (Da/Ne): ")
            if potvrda.lower() == "ne":
                sistem.wait_for_continue()
                return

            prodavac = korisnik
            if korisnicko_ime:
                korisnik2 = korisnici.svi_korisnici["korisnicko_ime"]

            try:
                if za_reg.lower() == "ne":
                    karta, karte.sve_karte = karte.kupovina_karte(karte.sve_karte,
                                                                  konkretni_letovi.svi_konkretni_letovi, sifra,
                                                                  [{"ime": ime, "prezime": prezime}],
                                                                  letovi.matrica_zauzetosti(konkretan_let),
                                                                  {"ime": ime, "prezime": prezime}, prodavac=prodavac,
                                                                  datum_prodaje=datetime.now().replace(microsecond=0))
                else:
                    karta, karte.sve_karte = karte.kupovina_karte(karte.sve_karte,
                                                                  konkretni_letovi.svi_konkretni_letovi, sifra,
                                                                  [korisnik2], letovi.matrica_zauzetosti(konkretan_let),
                                                                  korisnik2, prodavac=prodavac,
                                                                  datum_prodaje=datetime.now().replace(microsecond=0))
            except Exception as e:
                sistem.error(str(e))
                sistem.wait_for_continue(False)
                return

            jos = input("Prodaja uspešna! Da li želite da prodate još karata? (Da/Ne): ")
        return
    elif odluka == '2':
        prodaja_karata(konkretan_let)
        return

def check_in_prodavac():
    global korisnik
    while True:
        sistem.print_meni(izbor_karte, short=True)
        odluka = input("Unesite komandu(1-3): ")
        if odluka == '2':
            break
        elif odluka == '1':
            pretraga_karata()
        elif odluka == '3':
            return
        else:
            sistem.set_greska("Pogrešan unos. Pokušajte ponovo...")
    print()
    broj = input("Broj karte: ")
    if not broj.isdigit() or int(broj) not in karte.sve_karte:
        sistem.error("Ne postoji karta sa tim brojem!")
        sistem.wait_for_continue()
        return
    broj = int(broj)
    karta = karte.sve_karte[broj]
    if karta["sediste"] != "??":
        sistem.error("Ta karta je vec prijavljena!")
        sistem.wait_for_continue()
        return

    if "pasos" not in karta["putnici"][0] or not karta["putnici"][0]["pasos"]:
        pasos = None
        while not pasos:
            pasos = input("Nedostaje pasoš: ")
        karta["putnici"][0]["pasos"] = pasos
    if "drzavljanstvo" not in karta["putnici"][0] or not karta["putnici"][0]["drzavljanstvo"]:
        drzavljanstvo = None
        while not drzavljanstvo:
            drzavljanstvo = input("Nedostaje državljanstvo: ")
        karta["putnici"][0]["drzavljanstvo"] = drzavljanstvo
    if "pol" not in karta["putnici"][0] or not karta["putnici"][0]["pol"]:
        pol = None
        while not pol:
            pol = input("Nedostaje pol: ")
        karta["putnici"][0]["pol"] = pol

    zauzetost = letovi.matrica_zauzetosti(konkretni_letovi.svi_konkretni_letovi[karta["sifra_konkretnog_leta"]])
    ispis:str = ""
    for i in range(len(zauzetost)):
        ispis += f"Red {i+1}. "
        for j in range(len(zauzetost[i])):
            if not zauzetost[i][j]:
                ispis += chr(j + ord('A')) + " "
            else:
                ispis += "X "
        ispis += "\n"
    print("Slobodna mesta na letu (X su zauzeta):")
    print(ispis)

    red, pozicija = None, None
    while not red or not red.isdigit():
        red = input("Upišite red (broj): ")
    while not pozicija or not pozicija.isupper():
        pozicija = input("Upišite poziciju (veliko slovo): ")

    try:
        konkretni_let = konkretni_letovi.svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
        konkretni_let, karta = letovi.checkin(karta, letovi.svi_letovi, konkretni_let,  int(red), pozicija)
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return

    print("Prijava uspešna! Da li želite da uradite još prijava?")
    sistem.print_meni(nastavak_prijave, short=True, clear_text=False)
    odluka = input("Unesite komandu(1-2): ")
    if odluka == '1':
        check_in()

def izmena_karte():
    while True:
        sistem.print_meni(izbor_karte, short=True)
        odluka = input("Unesite komandu(1-3): ")
        if odluka == '2':
            break
        elif odluka == '1':
            pretraga_karata()
        elif odluka == '3':
            return
        else:
            sistem.set_greska("Pogrešan unos. Pokušajte ponovo...")
    print()
    broj = input("Broj karte: ")
    if not broj.isdigit() or int(broj) not in karte.sve_karte:
        sistem.error("Ne postoji karta sa tim brojem!")
        sistem.wait_for_continue()
        return
    broj = int(broj)
    karta = karte.sve_karte[broj]

    nova_sifra_konkretnog_leta = input("Nova šifra konkretnog leta: ")
    try:
        datum_polaska = input("Datum polaska (2031-03-30 08:46:51): ")
        datum_polaska = datetime.strptime(datum_polaska, "%Y-%m-%d %H:%M:%S")
    except Exception:
        datum_polaska = None
    sediste = input("Novo sedište: ")
    try:
        karte.sve_karte = karte.izmena_karte(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, broj, int(nova_sifra_konkretnog_leta), datum_polaska, sediste)
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return


def brisanje_karte():
    while True:
        sistem.print_meni(izbor_karte, short=True)
        odluka = input("Unesite komandu(1-3): ")
        if odluka == '2':
            break
        elif odluka == '1':
            pretraga_karata()
        elif odluka == '3':
            return
        else:
            sistem.set_greska("Pogrešan unos. Pokušajte ponovo...")
    print()
    broj = input("Broj karte: ")
    if not broj.isdigit() or int(broj) not in karte.sve_karte:
        sistem.error("Ne postoji karta sa tim brojem!")
        sistem.wait_for_continue()
        return
    broj = int(broj)
    karta = karte.sve_karte[broj]

    global korisnik
    try:
        karte.sve_karte = karte.brisanje_karte(korisnik, karte.sve_karte, broj)
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return
    print()
    print("Karta je uspešno označena za brisanje.")
    sistem.wait_for_continue()

def registracija_novog_prodavca():
    print()
    korisnicko_ime = input("Korisničko ime (obavezno): ")
    lozinka = input("Lozinka (obavezno): ")
    ime = input("Ime (obavezno): ")
    prezime = input("Prezime (obavezno): ")
    email = input("Email (obavezno): ")
    telefon = input("Telefon (obavezno): ")
    pasos = input("Pasoš: ")
    drzavljanstvo = input("Državljanstvo: ")
    pol = input("Pol: ")
    try:
        korisnik = korisnici.kreiraj_korisnika(korisnici.svi_korisnici, False, "prodavac", "", korisnicko_ime, lozinka,
                                               ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return
    print()
    print("Prodavac je uspešno registrovan!")
    sistem.wait_for_continue()

def kreiraj_let():
    sistem.clear()
    print("Unesite podatke novog leta (svi podaci su obavezni). U zagradi se nalaze primeri podataka:")
    broj_leta = input("Broj leta (aa11): ")
    id_modela = input("Id modela aviona (101): ")
    if not id_modela.isdigit() or int(id_modela) not in model_aviona.svi_modeli_aviona:
        sistem.error("Model aviona sa tim id ne postoji.")
        sistem.wait_for_continue()
        return
    else:
        model = model_aviona.svi_modeli_aviona[int(id_modela)]
    sifra_polazisnog_aerodroma = input("Šifra polazišnog aerodroma (msu): ")
    sifra_odredisnog_aerodroma = input("Šifra odredišnog aerodroma (bju): ")
    vreme_poletanja = input("Vreme poletanja (11:10): ")
    vreme_sletanja = input("Vreme sletanja (20:15): ")
    sletanje_sutra = input("Sletanje sutra (False): ")
    prevoznik = input("Prevoznik (Air Serbia): ")
    dani = input("Dani ([0,3,4]): ")
    cena = input("Cena (150.75): ")
    datum_pocetka_operativnosti = input("Datum početka operativnosti (2023-06-05 13:17:43): ")
    datum_kraja_operativnosti = input("Datum kraja operativnosti (2023-06-15 13:17:43): ")

    try: #kreiranje_letova će svakako konvertovati podatke u odgovarajući tip, pa ne moramo to da uradimo unapred
        letovi.svi_letovi = letovi.kreiranje_letova(letovi.svi_letovi, broj_leta, sifra_polazisnog_aerodroma,
                                    sifra_odredisnog_aerodroma, vreme_poletanja, vreme_sletanja, sletanje_sutra,
                                    prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)
        konkretni_letovi.svi_konkretni_letovi = konkretni_letovi.kreiranje_konkretnog_leta(konkretni_letovi.svi_konkretni_letovi, letovi.svi_letovi[broj_leta])
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return
    print()
    print("Let je uspešno kreiran!")
    sistem.wait_for_continue()

def izmeni_let():
    while True:
        sistem.print_meni(izbor_leta, short=True)
        odluka = input("Unesite komandu(1-3): ")
        if odluka == '2':
            break
        elif odluka == '1':
            pretraga_obicnih_letova()
        elif odluka == '3':
            return
        else:
            sistem.set_greska("Pogrešan unos. Pokušajte ponovo...")
    print()
    broj = input("Broj leta: ")
    if broj not in letovi.svi_letovi:
        sistem.error("Ne postoji let sa tim brojem!")
        sistem.wait_for_continue()
        return
    let = letovi.svi_letovi[broj]

    sistem.clear()
    print("Unesite podatke novog leta (pritisnite ENTER da preskočite podatak). U zagradi se nalaze primeri podataka:")
    id_modela = input("Id modela aviona (101): ")
    if not id_modela:
        model = let["model"]
    elif not id_modela.isdigit() or int(id_modela) not in model_aviona.svi_modeli_aviona:
        sistem.error("Model aviona sa tim id ne postoji.")
        sistem.wait_for_continue()
        return
    else:
        model = model_aviona.svi_modeli_aviona[int(id_modela)]
    sifra_polazisnog_aerodroma = input("Šifra polazišnog aerodroma (msu): ")
    if not sifra_polazisnog_aerodroma: sifra_polazisnog_aerodroma = let["sifra_polazisnog_aerodroma"]
    sifra_odredisnog_aerodroma = input("Šifra odredišnog aerodroma (bju): ")
    if not sifra_odredisnog_aerodroma: sifra_odredisnog_aerodroma = let["sifra_odredisnog_aerodorma"]
    vreme_poletanja = input("Vreme poletanja (11:10): ")
    if not vreme_poletanja: vreme_poletanja = let["vreme_poletanja"]
    vreme_sletanja = input("Vreme sletanja (20:15): ")
    if not vreme_sletanja: vreme_sletanja = let["vreme_sletanja"]
    sletanje_sutra = input("Sletanje sutra (False): ")
    if not sletanje_sutra: sletanje_sutra = let["sletanje_sutra"]
    prevoznik = input("Prevoznik (Air Serbia): ")
    if not prevoznik: prevoznik = let["prevoznik"]
    dani = input("Dani ([0,3,4]): ")
    if not dani: dani = let["dani"]
    cena = input("Cena (150.75): ")
    if not cena: cena = let["cena"]
    datum_pocetka_operativnosti = input("Datum početka operativnosti (2023-06-05 13:17:43): ")
    if not datum_pocetka_operativnosti: datum_pocetka_operativnosti = let["datum_pocetka_operativnosti"]
    datum_kraja_operativnosti = input("Datum kraja operativnosti (2023-06-15 13:17:43): ")
    if not datum_kraja_operativnosti: datum_kraja_operativnosti = let["datum_kraja_operativnosti"]

    try: #izmena_letova će svakako konvertovati podatke u odgovarajući tip, pa ne moramo to da uradimo unapred
        letovi.svi_letovi = letovi.izmena_letova(letovi.svi_letovi, broj, sifra_polazisnog_aerodroma,
                                    sifra_odredisnog_aerodroma, vreme_poletanja, vreme_sletanja, sletanje_sutra,
                                    prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)
    except Exception as e:
        sistem.error(str(e))
        sistem.wait_for_continue(False)
        return
    print()
    print("Let je uspešno izmenjen!")
    sistem.wait_for_continue()

def brisanje_karata_admin():
    sistem.clear()
    karte_za_brisanje = copy.deepcopy(karte.pretraga_karata_za_brisanje(karte.sve_karte))
    if len(karte_za_brisanje) == 0:
        print("Nema karata za brisanje.")
        sistem.wait_for_continue()
        return

    for karta in karte_za_brisanje:
        karta["kupac"] = karta["kupac"]["korisnicko_ime"]
        karta["prodavac"] = karta["prodavac"]["korisnicko_ime"]
        karta["putnici"] = karta["putnici"][0]["ime"] + " " + karta["putnici"][0]["prezime"]
        if karta["status"] == konstante.STATUS_REALIZOVANA_KARTA:
            karta["status"] = "Realizovana"
        else:
            karta["status"] = "Nerealizovana"
        konkretan_let = konkretni_letovi.svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
        karta["datum_i_vreme_polaska"] = konkretan_let["datum_i_vreme_polaska"]
        karta["datum_i_vreme_dolaska"] = konkretan_let["datum_i_vreme_dolaska"]
        karta["cena"] = letovi.svi_letovi[konkretan_let["broj_leta"]]["cena"]
    print(tabulate(karte_za_brisanje, numalign="left", headers=karta_headers))
    print()
    izbor = input("Da li hoćete da brišete karte (1) ili da poništite brisanje za karte (2): ")
    if izbor == '1':
        koje = input("Koje karte želite da obrišete? Navedite brojeve karata odvojene razmacima ili \"sve\" ako želite da obrišete sve označene karte: ")
        obrisano = ""
        global korisnik
        if koje.lower() == "sve":
            for karta in karte_za_brisanje:
                broj = karta["broj_karte"]
                karte.sve_karte = karte.brisanje_karte(korisnik, karte.sve_karte, broj)
                obrisano += str(broj) + " "
        else:
            koje = koje.split(" ")
            for broj in koje:
                if broj.isdigit() and int(broj) in karte.sve_karte:
                    karte.sve_karte = karte.brisanje_karte(korisnik, karte.sve_karte, int(broj))
                    obrisano += broj + " "
        print()
        if obrisano != "":
            print("Uspešno su obrisane karte: " + obrisano)
        else:
            print("Nijedna karta nije obrisana.")
        sistem.wait_for_continue()
    elif izbor == '2':
        koje = input("Za koje karte želite da poništite brisanje? Navedite brojeve karata odvojene razmacima ili \"sve\" ako želite da poništite sve oznake: ")
        ponisteno = ""
        if koje.lower() == "sve":
            for karta in karte_za_brisanje:
                broj = karta["broj_karte"]
                karte.sve_karte[broj]["obrisana"] = False
                ponisteno += str(broj) + " "
        else:
            koje = koje.split(" ")
            for broj in koje:
                if broj.isdigit() and int(broj) in karte.sve_karte:
                    karte.sve_karte[int(broj)]["obrisana"] = False
                    ponisteno += broj + " "
        print()
        if ponisteno != "":
            print("Uspešno je poništeno brisanje karata: " + ponisteno)
        else:
            print("Brisanje nije poništeno ni za jednu kartu.")
        sistem.wait_for_continue()
    else:
        sistem.wait_for_continue()

def izvestaj():
    while True:
        sistem.print_meni(izbor_izvestaja, short=True)
        odluka = input("Unesite komandu(1-8): ")
        izvestaj = None
        if odluka == '1':
            while True:
                try:
                    dan = input("Dan prodaje (2022-04-15): ")
                    dan = datetime.strptime(dan, "%Y-%m-%d").date()
                    break
                except Exception: pass
            izvestaj = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(karte.sve_karte, dan)
            break
        elif odluka == '2':
            while True:
                try:
                    dan = input("Dan polaska (2022-04-15): ")
                    dan = datetime.strptime(dan, "%Y-%m-%d").date()
                    break
                except Exception: pass
            izvestaj = izvestaji.izvestaj_prodatih_karata_za_dan_polaska(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, dan)
            break
        elif odluka == '3':
            while True:
                try:
                    dan = input("Dan prodaje (2022-04-15): ")
                    dan = datetime.strptime(dan, "%Y-%m-%d").date()
                    break
                except Exception: pass
            prodavac = input("Prodavac (NikolaJ): ")
            izvestaj = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(karte.sve_karte, dan, prodavac)
            break
        elif odluka == '4':
            while True:
                try:
                    dan = input("Dan prodaje (2022-04-15): ")
                    dan = datetime.strptime(dan, "%Y-%m-%d").date()
                    break
                except Exception: pass
            broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, letovi.svi_letovi, dan)
            break
        elif odluka == '5':
            while True:
                try:
                    dan = input("Dan polaska (2022-04-15): ")
                    dan = datetime.strptime(dan, "%Y-%m-%d").date()
                    break
                except Exception: pass
            broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, letovi.svi_letovi, dan)
            break
        elif odluka == '6':
            while True:
                try:
                    dan = input("Dan prodaje (2022-04-15): ")
                    dan = datetime.strptime(dan, "%Y-%m-%d").date()
                    break
                except Exception: pass
            prodavac = input("Prodavac (NikolaJ): ")
            broj, cena = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, letovi.svi_letovi, dan, prodavac)
            break
        elif odluka == '7':
            izvestaj = izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(karte.sve_karte, konkretni_letovi.svi_konkretni_letovi, letovi.svi_letovi)
            break
        elif odluka == '8':
            return
        else:
            sistem.set_greska("Pogrešan unos. Pokušajte ponovo...")
    print()
    if izvestaj is None:
        print(f"Broj prodatih karata je {broj}, a ukupna cena je {cena}.")
    elif type(izvestaj) == list:
        filtrirane_karte = copy.deepcopy(izvestaj)
        if filtrirane_karte is None or len(filtrirane_karte) == 0:
            sistem.error("Nije pronađena nijedna karta.")
        else:
            for karta in filtrirane_karte:
                karta["kupac"] = karta["kupac"]["korisnicko_ime"]
                karta["prodavac"] = karta["prodavac"]["korisnicko_ime"]
                karta["putnici"] = karta["putnici"][0]["ime"] + " " + karta["putnici"][0]["prezime"]
                if karta["status"] == konstante.STATUS_REALIZOVANA_KARTA:
                    karta["status"] = "Realizovana"
                else:
                    karta["status"] = "Nerealizovana"
                konkretan_let = konkretni_letovi.svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
                karta["datum_i_vreme_polaska"] = konkretan_let["datum_i_vreme_polaska"]
                karta["datum_i_vreme_dolaska"] = konkretan_let["datum_i_vreme_dolaska"]
                karta["cena"] = letovi.svi_letovi[konkretan_let["broj_leta"]]["cena"]
            print(tabulate(filtrirane_karte, numalign="left", headers=karta_headers))
    else:
        for ubc in izvestaj.values():
            izraz = "kartu" if ubc[0] == 1 else "karata"
            print(f"Prodavac {ubc[2]['ime']} {ubc[2]['prezime']} je prodao {ubc[0]} {izraz}, sa ukupnom cenom {ubc[1]}.")
    sistem.wait_for_continue()

def log_out():
    return True

def izlazak():
    letovi.sacuvaj_letove("data/letovi.csv", "|", letovi.svi_letovi)
    model_aviona.sacuvaj_modele_aviona("data/modeli_aviona.csv", "|", model_aviona.svi_modeli_aviona)
    aerodromi.sacuvaj_aerodrome("data/aerodromi.csv", "|", aerodromi.svi_aerodromi)
    korisnici.sacuvaj_korisnike("data/korisnici.csv", "|", korisnici.svi_korisnici)
    konkretni_letovi.sacuvaj_kokretan_let("data/konkretni_letovi.csv", "|", konkretni_letovi.svi_konkretni_letovi)
    karte.sacuvaj_karte(karte.sve_karte, "data/karte.csv", "|")
    exit()

glavni_meni = \
    ("Log in", login), ("Register", register), ("Pregled nerealizovanih letova", pregled_nerealizovanih_letova), \
    ("Pretraga letova", pretraga_letova), ("Prikaz 10 najjeftinijih (po opadajućoj ceni)", prikaz_10_najjeftinijih), \
    ("Fleksibilni polasci", fleksibilni_polasci), ("Exit", izlazak)

korisnicki_meni = \
    ("Pregled nerealizovanih letova", pregled_nerealizovanih_letova), ("Pretraga letova", pretraga_letova), \
    ("Prikaz 10 najjeftinijih (po opadajućoj ceni)", prikaz_10_najjeftinijih), \
    ("Fleksibilni polasci", fleksibilni_polasci), ("Kupovina karata", kupovina_karata), \
    ("Pregled nerealizovanih karata", pregled_nerealizovanih_karata), ("Prijava na let (check-in)", check_in), \
    ("Log out",log_out), ("Exit", izlazak)

izbor_konk_leta = ("Pretraži konkretne letove", None), ("Ukucaj traženu šifru konkretnog leta", None), ("Odustani od kupovine", None)
nastavak_kupovine = ("Kupi kartu za saputnika", None), ("Kupi kartu za povezani let", None), ("Ne želim da nastavim sa kupovinom", None)
izbor_karte = ("Pretraži karte", None), ("Ukucaj traženi broj karte", None), ("Odustani od prijave", None)
nastavak_prijave = ("Prijavi saputnika", None), ("Ne želim da nastavim sa prijavama", None)

prodavac_meni =\
    ("Pregled nerealizovanih letova", pregled_nerealizovanih_letova), ("Pretraga letova", pretraga_letova), \
    ("Prikaz 10 najjeftinijih (po opadajućoj ceni)", prikaz_10_najjeftinijih), \
    ("Fleksibilni polasci", fleksibilni_polasci), ("Prodaja karata", prodaja_karata), \
    ("Prijava na let (check-in)", check_in_prodavac), ("Izmena karte", izmena_karte), ("Brisanje karte", brisanje_karte), \
    ("Pretraga prodatih karata", pretraga_karata), ("Log out",log_out), ("Exit", izlazak)

nastavak_prodaje = ("Prodaj kartu za saputnika", None), ("Prodaj kartu za povezani let", None), ("Ne želim da nastavim sa prodajom", None)
izbor_karte_izmena = ("Pretraži karte", None), ("Ukucaj traženi broj karte", None), ("Odustani od izmene", None)

admin_meni = \
    ("Pregled nerealizovanih letova", pregled_nerealizovanih_letova), ("Pretraga letova", pretraga_letova), \
    ("Prikaz 10 najjeftinijih (po opadajućoj ceni)", prikaz_10_najjeftinijih), \
    ("Fleksibilni polasci", fleksibilni_polasci), ("Pretraga prodatih karata", pretraga_karata), \
    ("Registracija novog prodavca", registracija_novog_prodavca), ("Kreiranje letova", kreiraj_let), \
    ("Izmena letova", izmeni_let), ("Brisanje karata", brisanje_karata_admin), ("Izveštaji", izvestaj), ("Log out", log_out), ("Exit", izlazak)

izbor_leta = ("Pretraži letove", None), ("Ukucaj traženi broj leta", None), ("Odustani od izmene", None)
izbor_izvestaja = ("Lista prodatih karata za izabrani dan prodaje", None), ("Lista prodatih karata za izabrani dan polaska", None),\
    ("Lista prodatih karata za izabrani dan prodaje i izabranog prodavca", None), ("Ukupan broj i cena prodatih karata za izabrani dan prodaje", None), \
    ("Ukupan broj i cena prodatih karata za izabrani dan polaska", None), ("Ukupan broj i cena prodatih karata za izabrani dan prodaje i izabranog prodavca", None), \
    ("Ukupan broj i cena prodatih karata u poslednjih 30 dana, po prodavcima", None), ("Odustani od izveštaja", None)

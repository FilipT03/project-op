from datetime import datetime, date, timedelta
"""
Funkcija kao rezultat vraća listu karata prodatih na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    rezultat = []
    if type(dan) == datetime:
        dan = dan.date()
    for karta in sve_karte.values():
        datum = karta["datum_prodaje"]
        if type(datum) == datetime and datum.date() == dan:
            rezultat.append(karta)
        elif type(datum) == date and datum == dan:
            rezultat.append(karta)
    return rezultat


"""
Funkcija kao rezultat vraća listu svih karata čiji je dan polaska leta na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    rezultat = []
    if type(dan) == datetime:
        dan = dan.date()
    for karta in sve_karte.values():
        datum = svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"]
        if type(datum) == datetime and datum.date() == dan:
            rezultat.append(karta)
        elif type(datum) == date and datum == dan:
            rezultat.append(karta)
    return rezultat
"""
Funkcija kao rezultat vraća listu karata koje je na zadati dan prodao zadati prodavac.
"""
def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    #return [karta for karta in sve_karte.values() if karta["datum_prodaje"].date() == dan and karta["prodavac"] == prodavac]
    rezultat = []
    if type(dan) == datetime:
        dan = dan.date()
    for karta in sve_karte.values():
        if type(karta["prodavac"]) == str and karta["prodavac"] != prodavac:
            continue
        elif type(karta["prodavac"]) == dict and karta["prodavac"]["korisnicko_ime"] != prodavac:
            continue
        elif type(karta["prodavac"]) == tuple:
            continue
        datum = karta["datum_prodaje"]
        if type(datum) == datetime and datum.date() == dan:
            rezultat.append(karta)
        elif type(datum) == date and datum == dan:
            rezultat.append(karta)
    return rezultat

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata prodatih na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:
    broj = 0
    cena = 0
    if type(dan) == datetime:
        dan = dan.date()
    for karta in sve_karte.values():
        datum = karta["datum_prodaje"]
        if type(datum) == datetime and datum.date() != dan:
            continue
        elif type(datum) == date and datum != dan:
            continue
        broj += 1
        konkretan_let = svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
        cena += svi_letovi[konkretan_let["broj_leta"]]["cena"]
    return broj, cena

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata čiji je dan polaska leta na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_polaska(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date
) -> tuple:
    broj = 0
    cena = 0
    if type(dan) == datetime:
        dan = dan.date()
    for karta in sve_karte.values():
        datum = svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]["datum_i_vreme_polaska"]
        konkretan_let = svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
        if type(datum) == datetime and datum.date() != dan:
            continue
        elif type(datum) == date and datum != dan:
            continue
        broj += 1
        cena += svi_letovi[konkretan_let["broj_leta"]]["cena"]
    return broj, cena


"""
Funkcija kao rezultat vraća dve vrednosti: broj karata koje je zadati prodavac prodao na zadati dan i njihovu 
ukupnu cenu. Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
    sve_karte: dict,
    konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date,
    prodavac: str
) -> tuple:
    broj = 0
    cena = 0
    if type(dan) == datetime:
        dan = dan.date()
    for karta in sve_karte.values():
        datum = karta["datum_prodaje"]
        if type(datum) == datetime and datum.date() != dan:
            continue
        elif type(datum) == date and datum != dan:
            continue
        if type(karta["prodavac"]) == str and karta["prodavac"] != prodavac:
            continue
        elif type(karta["prodavac"]) == dict and karta["prodavac"]["korisnicko_ime"] != prodavac:
            continue
        broj += 1
        konkretan_let = konkretni_letovi[karta["sifra_konkretnog_leta"]]
        cena += svi_letovi[konkretan_let["broj_leta"]]["cena"]
    return broj, cena


"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""
def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict
) -> dict: #ubc znaci ukupan broj i cena
    rezultat = {}
    for karta in sve_karte.values():
        #if karta["datum_prodaje"] > datetime.now() or karta["datum_prodaje"] + timedelta(days=30) < datetime.now():
        try:
            datum = datetime.strptime(karta["datum_prodaje"],"%d.%m.%Y.").date()
        except ValueError:
            datum = datetime.strptime(karta["datum_prodaje"],"%Y-%m-%d %H:%M:%S").date()
        except TypeError:
            if type(karta["datum_prodaje"]) == datetime:
                datum = karta["datum_prodaje"].date()
            else:
                datum = karta["datum_prodaje"]
        if datum > date.today() or datum + timedelta(days=30) < date.today():
            continue
        if type(karta["prodavac"]) == str:
            key = karta["prodavac"]
        else:
            key = karta["prodavac"]["korisnicko_ime"]
        if key not in rezultat.keys():
            rezultat[key] = [0,0,""]
        konkretan_let = svi_konkretni_letovi[karta["sifra_konkretnog_leta"]]
        rezultat[key][0] += 1
        rezultat[key][1] += svi_letovi[konkretan_let["broj_leta"]]["cena"]
        rezultat[key][2]  = karta["prodavac"]
    return rezultat

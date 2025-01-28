import datetime
from dataclasses import dataclass



@dataclass
class Arbeitszeit:
    arbeitszeit = datetime.datetime

class Arbeitsart:
    name = str
    zeitfaktor = int

class PersDaten:
    name = str
    email = str
    passwort = str
    ort = str
    plz = str
    strasse = str
    hausnummer = str


class Feld:
    groesse = float
    frucht = str
    gps_daten = str

class Fahrzeug:
    name = str
    kategorie = str
    leistung = int
    stunden = float
    gps_daten = str
    frei = bool
    zustand = enumerate
    service = datetime.datetime


class Angestellter:
    arbeitszeit = Arbeitszeit
    persdaten = PersDaten

class Auftrag:
    angestellter = Angestellter
    arbeitsort = Feld
    arbeitsart = Arbeitsart
    zeit = Arbeitsart.zeitfaktor
    fahrzeug = Fahrzeug



from datetime import datetime
from pony.orm import PrimaryKey, Required, Optional, Database, Set


db = Database()
db.bind(provider='sqlite', filename='./databaze.sqlite', create_db=True)



class Uzivatel(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    heslo = Required(str)
    jmeno = Optional(str)
    rezervaces = Set('Rezervace')


class Rezervace(db.Entity):
    id = PrimaryKey(int, auto=True)
    uzivatel = Required(Uzivatel)
    zacatek = Required(datetime)
    konec = Required(datetime)
    sal = Required('Sal')


class Sal(db.Entity):
    id = PrimaryKey(int, auto=True)
    jmeno = Optional(str, unique=True)
    kapacita = Required(int)
    Dostupnost = Optional(bool)
    rezervaces = Set(Rezervace)


db.generate_mapping(create_tables=True)

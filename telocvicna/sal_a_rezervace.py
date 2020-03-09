from datetime import datetime
from pony.orm import db_session, select
from webface.models import Sal, Rezervace, Uzivatel



with db_session:
    uzivatele = select((u.id, u.login) for u in Uzivatel)
    for u in uzivatele:
        print(u[0], u[1])
    
    uzivatele = select(u for u in Uzivatel)
    for u in uzivatele:
        print(u.id, u.login)

    uzivatele = list(uzivatele)

    uid = input('Zadej id uzivatelem, kteremu patri rezervace > ')

    pinec = Sal.get(jmeno='Pinec') or Sal(jmeno='Pinec', kapacita=20)
    volejbal = Sal.get(jmeno='Volejbal') or Sal(jmeno='Volejbal', kapacita=40)

    zacatek = datetime(2020,2,20,8,0)
    konec = datetime(2020,2,20,10,0)

    rezervace1 = Rezervace(uzivatel=Uzivatel[uid], sal=pinec, 
                           zacatek=zacatek, konec=konec)
    rezervace2 = Rezervace(uzivatel=uzivatele[0], sal=volejbal,
                           zacatek=zacatek, konec=konec)


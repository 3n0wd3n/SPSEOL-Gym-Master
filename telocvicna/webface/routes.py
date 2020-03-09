from . import app
from datetime import datetime
from .models import (Uzivatel, Sal, Rezervace)
from flask import render_template, request, redirect, url_for, session, flash
from pony.orm import db_session, select
from werkzeug.security import check_password_hash


@app.route("/", methods=["GET"])
def index():
    with db_session:
        seznam_salu = select((s.id, s.jmeno) for s in Sal)
        objednavky = select((r.sal.jmeno, r.zacatek, r.konec) for r in Rezervace)
        for j, z, k in objednavky:
            print("######", j, z, k )
          
        return render_template("base.html.j2",
                               seznam_salu=list(seznam_salu),
                               objednavky=list(objednavky),
                               str=str,
                               int=int)

@app.route("/objednavka/", methods=["POST"])
def objednavka():
    sal_id = request.form.get('sal_id')
    datum = request.form.get('datum')
    zacatek = request.form.get('zacatek')
    konec = request.form.get('konec')
    if sal_id and datum and zacatek and konec:
        rok, mesic, den = map(int,datum.split('-'))
        z_hodina, z_minuta = map(int,zacatek.split(':'))
        k_hodina, k_minuta = map(int,konec.split(':'))
        zacatek = datetime(rok, mesic, den, z_hodina, z_minuta)
        konec = datetime(rok, mesic, den, k_hodina, k_minuta)
        print(zacatek)
        print(konec)

        if zacatek >= konec:
            flash("Nejdřív začátek potom konec!")
        elif zacatek <= datetime.now():
            flash("V minulosti nelze objendnávat!")
        else:
            with db_session:
                sal = Sal[sal_id]
                objednavky = select((r.id, r.zacatek, r.konec) 
                                    for r in Rezervace if r.sal == sal)
                for r_id, r_zacatek, r_konec in objednavky:
                    print(r_id, r_zacatek, r_konec)



        return redirect(url_for("index"))
    else:
        flash("Vyplň všechna políčka!!!")
        return redirect(url_for("index", sal_id=sal_id,
                                         datum=datum, 
                                         zacatek=zacatek,
                                         konec=konec
                                         ))

@app.route("/login/", methods=["POST"])
def login():
    login = request.form.get("login")
    heslo = request.form.get("heslo")
    print(login)
    if login and heslo:
        with db_session:
            uzivatel = Uzivatel.get(login=login)
            if uzivatel:
                pwhash = uzivatel.heslo
                if check_password_hash(pwhash, heslo):
                    session["login"] = login
    return redirect(url_for("index"))


@app.route("/logout/", methods=["GET"])
def logout():
    session.pop('login', None)
    return redirect(url_for('index'))

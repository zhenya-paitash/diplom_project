from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sqlite3
import os
import database
from datetime import datetime
import random as R

# ======================================================================================================================
app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db_app.db'),
    DEBUG=False,
    SECRET_KEY='diplomproject',
    USERNAME='zhenya',
    PASSWORD='password'))
app.config.from_envvar('settings_app', silent=True)

month = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня',
         '07': 'июля', '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}

# database.update()
# ======================================================================================================================
def connect_db():
    """ Соединяет с указанной базой данных """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """ Создание базы данных """
    with app.app_context():
        db = get_db()
        with app.open_resource('architecture.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """ Если ещё нет соединения с базой данных, открыть новое - для текущего контекста приложения """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """ Закрывает базу данных снова в конце запроса """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def news(news):
    db = get_db()
    if news == "habr":
        what = 10
    else:
        what = 3
    new = db.execute(f'SELECT * FROM {news} ORDER BY RANDOM() LIMIT {what}').fetchall()
    return new


def media(media):
    db = get_db()
    list = db.execute(f'SELECT * FROM {media} ORDER BY RANDOM() LIMIT 20').fetchall()
    return list


# ======================================================================================================================
@app.route("/")
def main_page():
    return render_template("MAIN.html", habr=news("habr"), hinews=news("hinews"), lostfilm=news("lostfilm"))


@app.route("/afisha/", methods=['GET', 'POST'])
def afisha():
    db = get_db()
    today = datetime.now()
    DATE = today.strftime("%d.%m.%Y")
    if request.method == 'POST':  # 2019-09-01
        d = request.form['DATE'].split('-')
        try:
            DATE = f"{d[2]}.{d[1]}.{d[0]}"
        except:
            DATE = today.strftime("%d.%m.%Y")
    cursor = db.execute(f'SELECT * FROM afisha WHERE date="{DATE}"')
    afisha = cursor.fetchall()
    DATE = f"{DATE.split('.')[0]} {month[DATE.split('.')[1]]} {DATE.split('.')[-1]} года"
    return render_template("AFISHA.html", afisha=afisha, DATE=DATE, today=today.strftime("%Y-%m-%d"), habr=news("habr"),
                           hinews=news("hinews"), lostfilm=news("lostfilm"))


@app.route("/films/")
def films():
    return render_template("FILMS.html", films=media('films'), habr=news("habr"),
                           hinews=news("hinews"), lostfilm=news("lostfilm"))


@app.route("/series/")
def series():
    return render_template("SERIES.html", series=media('series'), habr=news("habr"),
                           hinews=news("hinews"), lostfilm=news("lostfilm"))


@app.route("/cartoons/")
def cartoons():
    return render_template("CARTOONS.html", cartoons=media('cartoons'), habr=news("habr"),
                           hinews=news("hinews"), lostfilm=news("lostfilm"))


@app.route("/weather/", methods=['GET', 'POST'])
def weather():
    db = get_db()
    today = datetime.now().strftime("%Y-%m-%d")
    DATE = today
    if request.method == 'POST':
        DATE = request.form['DATE']
        if DATE == '':
            DATE = today
    cursor = db.execute(f'SELECT * FROM weather WHERE date="{DATE}"')
    weather = cursor.fetchall()
    DATE = f"{DATE.split('-')[-1]} {month[DATE.split('-')[1]]} {DATE.split('-')[0]} года"
    return render_template("WEATHER.html", weather=weather, today=today, DATE=DATE,
                           habr=news("habr"), hinews=news("hinews"), lostfilm=news("lostfilm"))


@app.route("/money/", methods=['GET', 'POST'])
def money():
    db = get_db()
    today = datetime.now().strftime("%Y-%m-%d")
    DATE = today
    if request.method == 'POST':
        DATE = request.form['DATE']
        if DATE == '':
            DATE = today
    cursor = db.execute(f'SELECT * FROM money WHERE date="{DATE}"')
    money = cursor.fetchall()
    cursor = db.execute(f'SELECT * FROM money_landmarks')
    landmarks = cursor.fetchall()
    DATE = f"{DATE.split('-')[-1]} {month[DATE.split('-')[1]]} {DATE.split('-')[0]} года"
    return render_template("MONEY.html", money=money, landmarks=landmarks, today=today, DATE=DATE,
                           habr=news("habr"), hinews=news("hinews"), lostfilm=news("lostfilm"))


@app.route("/news/")
def news_page():
    db = get_db()
    one = db.execute(f'SELECT * FROM hinews ORDER BY RANDOM() LIMIT 30').fetchall()
    two = db.execute(f'SELECT * FROM habr ORDER BY RANDOM() LIMIT 30').fetchall()
    three = db.execute(f'SELECT * FROM lostfilm ORDER BY RANDOM() LIMIT 30').fetchall()
    return render_template("NEWS.html", one=one, two=two, three=three, habr=news("habr"), hinews=news("hinews"),
                           lostfilm=news("lostfilm"))


@app.route("/playlist/")
def playlist():
    db = get_db()
    playlist = db.execute(f'SELECT * FROM music ORDER BY RANDOM() LIMIT 15').fetchall()
    return render_template("PLAYLIST.html", playlist=playlist, habr=news("habr"), hinews=news("hinews"),
                           lostfilm=news("lostfilm"))


@app.route("/about/")
def about():
    return render_template("ABOUT.html", habr=news("habr"), hinews=news("hinews"), lostfilm=news("lostfilm"))


@app.route("/contacts/", methods=['GET', 'POST'])
def contacts():
    db = get_db()
    if request.method == 'POST':
        NAME = request.form['NAME']
        MAIL = request.form['MAIL']
        REVIEW = request.form['REVIEW']
        if NAME != '' and MAIL != '' and REVIEW != '':
            db.execute(f'INSERT INTO messages(name, mail, review) VALUES '
                       f'("{NAME}", "{MAIL}", "{REVIEW}")')
            db.commit()
    review = db.execute(f'SELECT * FROM messages ORDER BY id DESC LIMIT 5').fetchall()
    return render_template("CONTACTS.html", review=review, habr=news("habr"), hinews=news("hinews"),
                           lostfilm=news("lostfilm"))


@app.errorhandler(404)
def page_not_found(event):
    return render_template("PAGE_404.html", habr=news("habr"), hinews=news("hinews"), lostfilm=news("lostfilm")), 404



# if __name__ == "__main__":
#     app.run()
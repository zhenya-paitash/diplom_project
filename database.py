import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import timedelta, date, datetime
import threading

"""           ДЛЯ РАБОТЫ СКРИПТА ВРУЧНУЮ - СЛЕДУЕТ РАСКОМЕНТИРОВАТЬ НУЖНЫЕ СТРОКИ ВНИЗУ СКРИПТА !!!       """


def update():  # обновление баз данных
    db_money_update()  # №1
    db_money_landmarks_update()  # №2
    db_weather_update()  # №3
    db_afisha_update()  # №4
    db_media_update("films")  # №5 - films
    db_media_update("series")  # №5 - series
    db_media_update("cartoons")  # №5 - cartoons
    db_lostfilm_update()  # №6
    db_hinews_update()  # №7
    db_habr_update()  # №8
    db_music_update()  # №9


# ======================================================================================================================
# ================================= №1 БАЗА ДАННЫХ money ОБНОВЛЕНИЕ : =================================================
# ======================================================================================================================
def db_money_update():
    """ обновление базы данных валюты """
    print(f"{' ' * 20}1.Проверка базы данных ... №1 MONEY | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect('db_app.db')
    cursor = server.cursor()
    start_date, end_date, delta = date(2019, 9, 1), date.today(), timedelta(days=1)
    while start_date <= end_date:
        time = start_date.strftime("%Y-%m-%d")
        cursor.execute(f"SELECT * FROM money WHERE date = '{time}'")
        result = cursor.fetchall()
        if result == []:  # если [] пустой (такой даты нету) = ДОБАВЛЯЕМ строку в DB
            print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | {time} ")
            url = 'http://www.nbrb.by/API/ExRates/Rates?onDate=' + str(time) + '&Periodicity=0'
            txt = requests.get(url).json()
            Cur_Date = txt[0]['Date'].split('T')[0]
            cursor.execute(f"INSERT INTO money (date) VALUES ('{Cur_Date}')")
            for i in txt:  # 26 повторений для 26 валют
                Cur_Abbreviation = i['Cur_Abbreviation']
                Cur_OfficialRate = i['Cur_OfficialRate']
                inserted = f"UPDATE money SET {Cur_Abbreviation} = '{Cur_OfficialRate}' WHERE date ='{Cur_Date}'"
                cursor.execute(inserted)
        server.commit()
        start_date += delta
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")
    threading.Timer(60, db_money_update).start()


# ======================================================================================================================
# ================================= №2 БАЗА ДАННЫХ money_landmarks ОБНОВЛЕНИЕ : ========================================
# ======================================================================================================================
def db_money_landmarks_update():
    """ обновление базы данных абревиатур валюты """
    print(
        f"{' ' * 20}2.Проверка базы данных ... №2 MONEY_LANDMARKS | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect('db_app.db')
    cursor = server.cursor()
    url = "http://www.nbrb.by/API/ExRates/Rates?Periodicity=0"
    txt = requests.get(url).json()
    for i in txt:
        Cur_ID = i['Cur_ID']
        cursor.execute(f'SELECT * FROM money_landmarks WHERE id="{Cur_ID}"')
        result = cursor.fetchall()  # данные в таблице за данное число
        if result == []:  # если за данное число нет данных - вносим, иначе, обновление не требуется
            print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | {Cur_ID}")
            Cur_Abbreviation = i['Cur_Abbreviation']
            Cur_Scale = i['Cur_Scale']
            Cur_Name = i['Cur_Name']
            cursor.execute(
                f"INSERT INTO money_landmarks (id, scale, abbreviation, name) "
                f"VALUES ('{Cur_ID}', '{Cur_Scale}', '{Cur_Abbreviation}', '{Cur_Name}')")
            server.commit()
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")


# ======================================================================================================================
# ================================= №3 БАЗА ДАННЫХ weather ОБНОВЛЕНИЕ : ===============================================
# ======================================================================================================================
def db_weather_update():
    """ обновление базы данных погоды """
    print(f"{' ' * 20}3.Проверка базы данных ... №3 WEATHER | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect("db_app.db")
    cursor = server.cursor()
    # {{url_for('static',filename='weather/   day-yasno.png    ')}}  -  ссылка на иконку
    icons = {"day": {"ясно": "day-yasno.png",  # иконки погоды
                     "облачно": "day-oblachno.png",
                     "малооблачно": "day-malooblachno.png",
                     "пасмурно": "day-pasmurno.png",
                     "снег": "day-snow.png",
                     "дождь": "day-rain.png"},
             "night": {"ясно": "night-yasno.png",
                       "облачно": "night-oblachno.png",
                       "малооблачно": "night-malooblachno.png",
                       "пасмурно": "night-pasmurno.png",
                       "снег": "night-snow.png",
                       "дождь": "night-rain.png"}}
    start_date, end_date, delta = date(2019, 9, 1), date.today(), timedelta(days=1)
    while start_date <= end_date:
        time = start_date.strftime("%Y-%m-%d")
        cursor.execute(f'SELECT * FROM weather WHERE date="{time}"')
        result = cursor.fetchall()  # данные в таблице за данное число
        if result == []:  # если за данное число нет данных - вносим, иначе, обновление не требуется
            print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | {time}")
            cities = ['minsk', 'gomel', 'brest', 'grodno', 'vitebsk', 'mogilev']  # сразу для всех столиц
            for city in cities:  # 6 повторений для каждой столицы
                url = f"https://meteo.by/{city}/retro/{time}/"
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'lxml')
                get = soup.find("table", class_="t-weather").find_all("tr", class_="time")
                for i in get:
                    temp = str(i.find("td", class_="temp").text).split()
                    day_period = temp[0]
                    temp_min = temp[1]
                    temp_max = temp[-1]
                    description = ' '.join(str(i.find("td", class_="icon").text).split())
                    PNG = description.split()
                    icon = PNG[0] if len(PNG) == 1 else PNG[-1]
                    icon = icons['day'][icon] if day_period == 'утро' or day_period == 'день' else icons['night'][icon]
                    data = i.find_all('td', class_="data")
                    pressure = data[0].text.replace('…', '-')
                    humidity = data[1].text.replace('…', '-')
                    wind_speed = data[-1].text.replace('…', '-')
                    direction_wind = i.find('td', class_="dir").find("span").get('title')
                    pogoda = f'INSERT INTO weather ' \
                        f'(date, city, day_period, temp_min, temp_max, description, ' \
                        f'icon, pressure, humidity, wind_speed, direction_wind) VALUES ' \
                        f'("{time}", "{city}", "{day_period}", "{temp_min}", "{temp_max}","{description}",' \
                        f'"{icon}", "{pressure}", "{humidity}","{wind_speed}","{direction_wind}")'
                    cursor.execute(pogoda)
            server.commit()
        start_date += delta
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")
    threading.Timer(66, db_weather_update).start()


# ======================================================================================================================
# ================================= №4 БАЗА ДАННЫХ afisha ОБНОВЛЕНИЕ : ===============================================
# ======================================================================================================================
def db_afisha_update():
    """ обновление базы данных афиши """
    print(f"{' ' * 20}4.Проверка базы данных ... №4 AFISHA | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect("db_app.db")
    cursor = server.cursor()
    date = (datetime.now()).strftime("%d.%m.%Y")
    cursor.execute(f'SELECT * FROM afisha WHERE date="{date}"')
    result = cursor.fetchall()
    if result == []:
        print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | {date}")
        url = "http://kino.bycard.by/"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'lxml')
        d = soup.find('div', class_="content wrapper clearfix").find_all('div', class_="events_list__row")
        for i in d:
            films_in_row = i.find_all('div', class_="event_item")
            for j in films_in_row:
                name = j .find('div', class_="event_item__name").text
                href = f"http://kino.bycard.by{j.find_all('div', class_='event_item__buy')[0].find('a').get('href')}"
                time = j.find('time', class_="event_item__date").text
                film = BeautifulSoup(requests.get(href).text, 'lxml')
                poster = f"http://kino.bycard.by{film.find('div', class_='poster').find('img').get('src')}"
                try:
                    trailer = film.find('div', class_="poster").find('a').get('href')
                except:
                    trailer = ''
                description = film.find('div', class_="full-description").find_all('p')[-1].text
                film_on_base = f'INSERT INTO afisha ' \
                    f'(date, time, name, description, href, poster, trailer) ' \
                    f'VALUES ' \
                    f'("{date}", "{time}", "{name}", "{description}", "{href}", "{poster}", "{trailer}")'
                cursor.execute(film_on_base)
        server.commit()
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")
    threading.Timer(78, db_afisha_update).start()


# ======================================================================================================================
# ================================= №5 БАЗА ДАННЫХ films, series, cartoons ОБНОВЛЕНИЕ : ===============================
# ======================================================================================================================
def db_media_update(media):
    print(f"{' ' * 20}5.Проверка базы данных ... №5 {media.upper()} | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect("db_app.db")
    cursor = server.cursor()
    # soup = BeautifulSoup(requests.get("https://rezka.ag/films/").text, 'lxml')
    # pages = soup.find('div', class_="b-content__inline_items").find('div', class_="b-navigation").find_all('a')[-2]
    # max_pages = pages.text
    # for page in range(1, int(max_pages) + 1):
    for page in range(1, 2):
        url = f"https://rezka.ag/{str(media)}/page/{page}/"
        txt = BeautifulSoup(requests.get(url).text, 'lxml').find('div', class_="b-content__inline_items").find_all(
            'div', class_="b-content__inline_item")
        for i in txt:
            name = i.find('div', class_="b-content__inline_item-link").find('a').text.replace("\"", "\'").lower()
            cursor.execute(f'SELECT * FROM {media} WHERE NAME="{name}"')
            result = cursor.fetchall()
            if result == []:
                print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | страница: {page}, name: {name}")
                href = i.find('div', class_="b-content__inline_item-cover").find('a').get('href')
                info = BeautifulSoup(requests.get(href).text, 'lxml')
                img = "https://rezka.ag{}".format(
                    info.find('div', class_="b-post__infotable_left").find('div', class_="b-sidecover").find_all('a')[
                        -1].find('img').get('src'))
                try:
                    description = info.find('div', class_="b-post__description").find('div',
                                                                                      class_="b-post__description_text").text.replace(
                        "\"", "\'")
                except:
                    description = ''
                table = info.find('div', class_="b-post__infotable_right").find('table',
                                                                                class_="b-post__info").find_all('tr')
                rate_imdb = ""
                rate_kp = ""
                tagline = ""
                date = ""
                country = ""
                producer = ""
                genre = ""
                age = ""
                time = ""
                actors = ""
                for j in table:
                    if "Рейтинги:" in j.text:
                        if "IMDb" in j.text:
                            rate_imdb = j.find('span', class_="b-post__info_rates imdb").text
                        if "Кинопоиск" in j.text:
                            rate_kp = j.find('span', class_="b-post__info_rates kp").text
                        # rate = j.find_all("td")[-1].text
                    elif "Слоган" in j.text:
                        tagline = j.find_all("td")[-1].text.replace("\"", "\'")
                    elif "Дата выхода:" in j.text:
                        date = j.find_all("td")[-1].text
                        # YEAR = i.find_all("td")[-1].find('a').text.split(' ')[0]
                        # print(YEAR)
                        # print(DATE)
                    elif "Страна" in j.text:
                        country = j.find_all('td')[-1].text
                    elif "Режиссер" in j.text:
                        producer = j.find_all('td')[-1].text
                    elif "Жанр" in j.text:
                        genre = j.find_all('td')[-1].text
                    elif "Возраст" in j.text:
                        age = j.find_all('td')[-1].text
                    elif "Время" in j.text:
                        time = j.find_all('td')[-1].text
                    elif "В ролях актеры" in j.text:
                        actors = j.find_all('td')[-1].text
                film = f'INSERT INTO {media} ' \
                    f'(name,rate_imdb,rate_kp,time,date,country,genre,age,producer,actors,tagline,description,img,href)' \
                    f'VALUES ' \
                    f'("{name}","{rate_imdb}","{rate_kp}","{time}","{date}","{country}","{genre}","{age}",' \
                    f'"{producer}","{actors}","{tagline}","{description}","{img}","{href}")'
                cursor.execute(film)
                server.commit()
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")


# ======================================================================================================================
# ================================= №6 БАЗА ДАННЫХ lostfilm ОБНОВЛЕНИЕ : ==============================================
# ======================================================================================================================
def db_lostfilm_update():
    print(f"{' ' * 20}6.Проверка базы данных ... №6 LOSTFILM | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect("db_app.db")
    cursor = server.cursor()
    # url = 'https://lostfilm.info/news/'
    # soup = BeautifulSoup(requests.get(url).text, 'lxml')
    # max_pages = int(
    #     soup.find('div', class_="grid_9").find('div', class_="paging-container").find_all('a')[-1].get('href').split(
    #         '/')[-2])
    # for page in range(1, max_pages + 1):
    for page in range(1, 2):
        lost = BeautifulSoup(requests.get(f"https://lostfilm.info/news/{page}/").text, 'lxml').find('div',
                                                                                                    class_="grid_9").find_all(
            'div', class_="news-container")
        for i in lost:
            title = i.find('h4', class_="news-header").text.replace("\"", "\'")
            cursor.execute(f'SELECT * FROM lostfilm WHERE title="{title}"')
            result = cursor.fetchall()
            if result == []:
                print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | страница: {page}, news: {title}")
                date = i.find('div', class_="news-date small").text
                img = f"http://lostfilm.info{i.find('img', class_='alignleft').get('src')}"
                href = f"http://lostfilm.info{i.find('a', class_='submenu-btn-nodrop relative').get('href')}"
                news = f'INSERT INTO lostfilm (title,date,img,href) VALUES ("{title}","{date}","{img}","{href}")'
                cursor.execute(news)
        server.commit()
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")
    threading.Timer(3600, db_lostfilm_update).start()


# ======================================================================================================================
# ================================= №7 БАЗА ДАННЫХ hinews ОБНОВЛЕНИЕ : ================================================
# ======================================================================================================================
def db_hinews_update():
    print(f"{' ' * 20}7.Проверка базы данных ... №7 HINEWS | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect("db_app.db")
    cursor = server.cursor()
    for page in range(1, 2):
        hi = BeautifulSoup(requests.get(f"https://hi-news.ru/page/{page}/").text, 'lxml').find('div',
                                                                                               class_="main-section").find(
            'div', class_="roll main-roll").find_all('div', class_='item')
        for i in hi:
            name = i.find('h2').find('a').text.replace("\"", "\'")
            cursor.execute(f'SELECT * FROM hinews WHERE name="{name}"')
            result = cursor.fetchall()
            if result == []:
                print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | страница: {page}, news: {name}")
                text = i.find('div', class_="text").find_all('p')[0].text.replace("\"", "\'")
                img = f"https:{i.find('div', class_='cover-wrap').find('a').find('img').get('src')}"
                href = i.find('h2').find('a').get('href')
                news = f'INSERT INTO hinews (name,text,img,href) VALUES ("{name}","{text}","{img}","{href}")'
                cursor.execute(news)
            server.commit()
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")
    threading.Timer(3700, db_hinews_update).start()


# ======================================================================================================================
# ================================= №8 БАЗА ДАННЫХ habr ОБНОВЛЕНИЕ : ==================================================
# ======================================================================================================================
def db_habr_update():
    print(f"{' ' * 20}8.Проверка базы данных ... №8 HABR | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect("db_app.db")
    cursor = server.cursor()
    # soup = BeautifulSoup(requests.get("https://habr.com/top/monthly/").text, "lxml")
    # pages = soup.find('div', class_="page__footer").find('a',
    #     class_="toggle-menu__item-link toggle-menu__item-link_pagination toggle-menu__item-link_bordered").get('href')
    # total_pages = pages.split('page')[1].split('/')[0]
    # for page in range(1, int(total_pages) + 1):
    for page in range(1, 2):
        soup = BeautifulSoup(requests.get(f"https://habr.com/top/monthly/page{page}/").text, 'lxml')
        habr = soup.find('div', class_="posts_list").find_all('h2', class_="post__title")
        for i in habr:
            name = i.find('a').text.replace("\"", "\'")
            cursor.execute(f'SELECT * FROM habr WHERE name="{name}"')
            result = cursor.fetchall()
            if result == []:
                print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | страница: {page}, news: {name}")
                href = i.find('a').get('href')
                news = f'INSERT INTO habr (name,href) VALUES ("{name}","{href}")'
                cursor.execute(news)
            server.commit()
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")
    threading.Timer(3800, db_habr_update).start()


# ======================================================================================================================
# ================================= №9 БАЗА ДАННЫХ music ОБНОВЛЕНИЕ : =================================================
# ======================================================================================================================
def db_music_update():
    print(f"{' ' * 20}9.Проверка базы данных ... №9 MUSIC | {(datetime.now()).strftime('%H:%M:%S (%d.%m.%Y)')}")
    server = sqlite3.connect("db_app.db")
    cursor = server.cursor()
    f = open('my_playlist.txt', 'r')
    l = [line.strip() for line in f]
    for i in l:
        cursor.execute(f'SELECT * FROM music WHERE href="{i}"')
        result = cursor.fetchall()
        if result == []:
            print(f"{' ' * 22}{'.'*18} НАЙДЕНО ОБНОВЛЕНИЕ | видео: {i}")
            href = f'INSERT INTO music (href) VALUES ("{i}")'
            cursor.execute(href)
        server.commit()
    f.close()
    cursor.close()
    server.close()
    print(f"{' ' * 22}{'=' * 100}")

# ======================================================================================================================
# ==================================== для выполнения вручную (расскоментировать) ======================================
# ======================================================================================================================
# # 1 - №1 БАЗА ДАННЫХ money ОБНОВЛЕНИЕ :
# db_money_update()
#
#
# # 2 - №2 БАЗА ДАННЫХ money_landmarks ОБНОВЛЕНИЕ :
# db_money_landmarks_update()
#
#
# # 3 - №3 БАЗА ДАННЫХ weather ОБНОВЛЕНИЕ :
# db_weather_update()
#
#
# # 4 - №4 БАЗА ДАННЫХ afisha ОБНОВЛЕНИЕ :
# db_afisha_update()
#                                                               # ИНСТРУКЦИЯ : # ДЛЯ ОБНОВЛЕНИЯ Базы Данных ВРУЧНУЮ
#                                                                              # ПРОСТО РАССКОМЕНТИРУЙ НУЖНОЕ ДЕЙСТВИЕ !
# # 5 - №5 БАЗА ДАННЫХ films, series, cartoons ОБНОВЛЕНИЕ :
# db_media_update("films")
# db_media_update("series")
# db_media_update("cartoons")
#
#
# # 6 - №6 БАЗА ДАННЫХ lostfilm ОБНОВЛЕНИЕ :
# db_lostfilm_update()
#
#
# # 7 - №7 БАЗА ДАННЫХ hinews ОБНОВЛЕНИЕ :
# db_hinews_update()
#
#
# # 8 - №8 БАЗА ДАННЫХ habr ОБНОВЛЕНИЕ :
# db_habr_update()
#
#
# # 8 - №9 БАЗА ДАННЫХ music ОБНОВЛЕНИЕ :
# db_music_update()
#
#
# ======================================================================================================================

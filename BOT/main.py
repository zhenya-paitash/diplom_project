import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import random as R
import threading

token = 'thisismytoken'
bot = telebot.TeleBot(token)


# ======================================================================================================================
@bot.message_handler(commands=['start'])
def start(message):
    key = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btnStart = types.KeyboardButton(text="Показать клавиатуру\n🎹")
    btnHelp = types.KeyboardButton(text="Помощь\n🆘")
    btnWiki = types.KeyboardButton(text='Википедия\n📜')
    btnGoroskop = types.KeyboardButton(text='Гороскоп\n♊️')
    btnHdrezka = types.KeyboardButton(text='Медиотека\n🎥')
    btnCoin = types.KeyboardButton(text='Бросить монетку\n🎲')
    btnMagic = types.KeyboardButton(text='Магический шар\n🎱')
    btnTube = types.KeyboardButton(text='Музыка с Youtube\n🎸')
    btnMoney = types.KeyboardButton(text='Курсы валют\n💹')
    btnAnekdot = types.KeyboardButton(text='Анекдот\n😆')
    btnAfisha = types.KeyboardButton(text='Афиша\n🎬')
    btnPogoda = types.KeyboardButton(text='Прогноз погоды\n☂️')
    btnSearch = types.KeyboardButton(text='Поиск фильмов\n📲')
    btnLostfilm = types.KeyboardButton(text='Новости кино\n📰')
    btnHinews = types.KeyboardButton(text='Новости технологий\n📰')
    btnHabr = types.KeyboardButton(text='Новости Habr\n📰')
    btnMem = types.KeyboardButton(text='Мемчики\n🤪')
    btnPlaylist = types.KeyboardButton(text='Плеслист автора\n🎧')
    btnPlaces = types.KeyboardButton(text="Места поблизости\n⛰", request_location=True)
    key.row(btnStart, btnHelp)
    key.row(btnGoroskop, btnHdrezka)
    key.row(btnMoney, btnPogoda)
    key.row(btnAfisha, btnLostfilm)
    key.row(btnHinews, btnHabr)
    key.row(btnWiki, btnSearch)
    key.row(btnCoin, btnMagic)
    key.row(btnTube, btnPlaylist)
    key.row(btnAnekdot, btnMem)
    key.row(btnPlaces)
    bot.send_message(message.chat.id, "Приветствую! Выбери команду:", reply_markup=key)


@bot.message_handler(commands=['help'])
def help(message):
    help = '🆘 Мои команды:\n\n' \
           '◽️/start - приветствие, клавиатура\n' \
           '◽️/help - помощь\n' \
           '◽️/w - значение слов в википедии\n' \
           '◽️/goroskop - гороскоп\n' \
           '◽️/hdrezka - MEDIA контент\n' \
           '◽️/coin - для важных решений\n' \
           '◽️/magic - для ещё более важных решений\n' \
           '◽️/tube - послушай музыку на ютубе\n' \
           '◽️/money - курсы валют\n' \
           '◽️/anekdot - травлю не хуже Петросяна\n' \
           '◽️/afisha - фильмы в прокате\n' \
           '◽️/pogoda - погода в минске\n' \
           '◽️/s - поиск фильмов\n' \
           '◽️/lostfilm - последние новости сериалов\n' \
           '◽️/hinews - хроника из мира высоких технологий\n' \
           '◽️/habr - последние статьи хабр\n' \
           '◽️/mem - случайные мемы\n' \
           '◽️/playlist - плейлисты автора\n' \
           '\n' \
           '🆘 Также я отвечаю на:\n' \
           'Стикеры, Музыку, Войс. Играю в Марко'
    bot.send_message(message.chat.id, help)


@bot.message_handler(commands=['money'])
def money(message):
    url = "http://www.nbrb.by/API/ExRates/Rates?Periodicity=0"
    txt = requests.get(url).json()
    money = []
    for i in txt:
        money.append("{0:<6} 💰 {1:3}{2:>40}\n".format(i['Cur_OfficialRate'],
                                                       i['Cur_Abbreviation'],
                                                       i['Cur_Name']))
    bot.send_message(message.chat.id, ''.join(money))


@bot.message_handler(commands=['anekdot'])
def anekdot(message):
    url = 'https://nekdo.ru/random/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    anekdot = soup.find('div', class_="text").text
    bot.send_message(message.chat.id, anekdot)


@bot.message_handler(commands=['afisha'])
def afisha(message):
    kino = types.InlineKeyboardMarkup()
    html = requests.get('https://afisha.tut.by/place/belarus-kino/').text
    soup = BeautifulSoup(html, 'lxml')
    movie = soup.find('div', class_="events-block js-cut_wrapper").find_all('ul', class_="b-lists list_afisha col-5")
    for i in movie[0:3]:
        into = i.find_all('li')
        for y in into:
            name = y.find('a', class_="name").text
            genre = y.find('div', class_="txt").find('p').text
            title = f'{name} ({genre})'
            ticket = y.find('div', class_="txt").find('a').get('href')
            post = types.InlineKeyboardButton(text=title, url=ticket)
            kino.add(post)
    bot.send_message(message.chat.id, '🎬 Купить билет в кино 🎬', reply_markup=kino)


@bot.message_handler(commands=['pogoda'])
def pogoda(message):
    url = 'http://www.pogoda.by/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    minsk = soup.find('div', class_="middle").find('table').find('tr').text
    now = types.InlineKeyboardMarkup()
    check = types.InlineKeyboardButton(text='🌤 Смотреть подробнее 🌤', url='http://www.pogoda.by/')
    now.add(check)
    bot.send_message(message.chat.id, f'В Минске {minsk}', reply_markup=now)


@bot.message_handler(commands=['lostfilm'])
def lostfilm(message):
    url = 'https://lostfilm.info/news/'
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    lost = soup.find('div', class_="grid_9").find_all('div', class_="news-container")
    news = types.InlineKeyboardMarkup()
    for i in lost:
        title = i.find('h4').text
        link = 'http://lostfilm.info' + i.find('a', class_="submenu-btn-nodrop relative").get('href')
        post = types.InlineKeyboardButton(text=title, url=link)
        news.add(post)
    bot.send_message(message.chat.id, '📰 Новости кино с http://lostfilm.info/news/', reply_markup=news)


@bot.message_handler(commands=['hinews'])
def hinews(message):
    news = types.InlineKeyboardMarkup()
    soup = BeautifulSoup(requests.get('https://hi-news.ru/').text, 'lxml')
    hinews = soup.find('div', class_="roll main-roll").find_all('h2')
    for i in hinews:
        name = i.find('a').text
        href = i.find('a').get('href')
        post = types.InlineKeyboardButton(text=name, url=href)
        news.add(post)
    bot.send_message(message.chat.id, '📰 Последние новости с hi-news.ru', reply_markup=news)


@bot.message_handler(commands=['habr'])
def habr(message):
    habr = types.InlineKeyboardMarkup()
    html = requests.get("https://habr.com/top/monthly/").text
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('div', class_="posts_list").find_all('h2', class_="post__title")
    for i in title:
        name = i.find('a').text
        href = i.find('a').get('href')
        post = types.InlineKeyboardButton(text=name, url=href)
        habr.add(post)
    bot.send_message(message.chat.id, '📰 Последние статьи на habr.com', reply_markup=habr)


@bot.message_handler(commands=['playlist'])
def playlist(message):
    playlist = types.InlineKeyboardMarkup()
    metalcore = types.InlineKeyboardButton(text='metalcore',
                                           url='https://open.spotify.com/playlist/7tcGFiuphmZkicSbxl5eBw')
    synth_pop = types.InlineKeyboardButton(text='synthpop',
                                           url='https://open.spotify.com/playlist/1HfuXDwLtwaJ57MxJbZ3kb')
    rockhit = types.InlineKeyboardButton(text="80's rock hits",
                                           url="https://open.spotify.com/playlist/6MFiuivM0TNNByXeVBUvtz")
    lofi = types.InlineKeyboardButton(text='lofi moodies',
                                           url="https://open.spotify.com/playlist/30yzoQXNvlYsxIK6BcXS9l")
    playlist.add(synth_pop,rockhit,lofi,metalcore)
    bot.send_message(message.chat.id, 'Мой плейлист на Spotify', reply_markup=playlist)


@bot.message_handler(commands=['w'])
@bot.edited_message_handler(commands=['w'])
def wikipedia(message):
    if message.text == '/w' and len(message.text) == 2 or message.text == "Википедия\n📜":
        bot.send_message(message.chat.id, 'Напиши мне термин после /w (например: "/w Углерод")\n'
                                          'и я поищу для тебя его значение на википедии')
    elif '/w' in message.text and len(message.text) > 3:
        txt = str(message.text)[2:]
        url = 'https://ru.wikipedia.org/wiki/'
        linked = url + txt
        html = requests.get(linked).text
        wiki = BeautifulSoup(html, 'lxml').find("div", id="mw-content-text").find('p').text
        wuku = types.InlineKeyboardMarkup()
        link = types.InlineKeyboardButton(text='На википедию 🖥', url=linked)
        wuku.add(link)
        bot.send_message(message.chat.id, wiki, reply_markup=wuku)


@bot.message_handler(commands=['goroskop'])
def goroskop(message):
    keyboard = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text='♈️Овен', callback_data='овен')
    but_2 = types.InlineKeyboardButton(text='♉️Телец', callback_data='телец')
    but_3 = types.InlineKeyboardButton(text='♊️Близнец', callback_data='близнец')
    but_4 = types.InlineKeyboardButton(text='♋️Рак', callback_data='рак')
    but_5 = types.InlineKeyboardButton(text='♌️Лев', callback_data='лев')
    but_6 = types.InlineKeyboardButton(text='♍️Дева', callback_data='дева')
    but_7 = types.InlineKeyboardButton(text='♎️Весы', callback_data='весы')
    but_8 = types.InlineKeyboardButton(text='♏️Скорпион', callback_data='скорпион')
    but_9 = types.InlineKeyboardButton(text='♐️Стрелец', callback_data='стрелец')
    but_10 = types.InlineKeyboardButton(text='♑️Козерог', callback_data='козерог')
    but_11 = types.InlineKeyboardButton(text='♒️Водолей', callback_data='водолей')
    but_12 = types.InlineKeyboardButton(text='♓️Рыбы', callback_data='рыбы')
    keyboard.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8, but_9, but_10, but_11, but_12)
    bot.send_message(message.chat.id, 'Выберите Ваш знак Зодиака:', reply_markup=keyboard)


@bot.message_handler(commands=['coin'])
def coinflip(message):
    coin = R.randrange(101)
    bot.send_message(message.chat.id, '🔸 ОРЁЛ' if coin <= 50 else '♦️РЕШКА')


@bot.message_handler(commands=['magic'])
@bot.edited_message_handler(commands=['magic'])
def magic(message):
    if message.text == '/magic' and len(message.text) == 6 or message.text == "Магический шар\n🎱":
        bot.send_message(message.chat.id, 'Если у Вас возник какой-то серьёзный вопрос, ни в коем случае не пытайтесь '
                                          'решить его самостоятельно! Именно для таких ситуаций и был придуман '
                                          'магический шар. Просто спросите у него интересующий Вас вопрос в формате '
                                          '"/magic стоит ли мне сменить работу?", как он сразу же напишет о Вашей '
                                          'дилемме профессиональной гадалке, чтобы узнать как Вам лучше поступить!')
    else:
        if '?' in message.text:
            magic8 = ['Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да', 'Можешь быть уверен в этом',
                      'Мне кажется — «да»', 'Вероятнее всего', 'Хорошие перспективы', 'Знаки говорят — «да»', 'Да',
                      'Пока не ясно, попробуй снова', 'Спроси позже', 'Лучше не рассказывать',
                      'Сейчас нельзя предсказать', 'Сконцентрируйся и спроси опять', 'Даже не думай',
                      'Мой ответ — «нет»', 'По моим данным — «нет»', 'Перспективы не очень хорошие',
                      'Весьма сомнительно']
            bot.send_message(message.chat.id, R.choice(magic8))
        else:
            bot.send_message(message.chat.id, '🌀 Это точно вопрос?')


@bot.message_handler(commands=['tube'])
def youtube(message):
    f = open('my_playlist.txt', 'r')
    l = [line.strip() for line in f]
    bot.send_message(message.chat.id, R.choice(l))


@bot.message_handler(commands=['hdrezka'])
def rezka(message):
    media_select = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text='Фильмы', callback_data='фильмы')
    but_2 = types.InlineKeyboardButton(text='Сериалы', callback_data='сериалы')
    but_3 = types.InlineKeyboardButton(text='Мультфильмы', callback_data='мультфильмы')
    but_4 = types.InlineKeyboardButton(text='Аниме', callback_data='аниме')
    but_5 = types.InlineKeyboardButton(text='Новинки', callback_data='новинки')
    but_6 = types.InlineKeyboardButton(text='Анонсы', callback_data='анонсы')
    search = types.InlineKeyboardButton(text='Поиск', callback_data='поиск')
    media_select.add(but_1, but_2, but_3, but_4, but_5, but_6, search)
    bot.send_message(message.chat.id, '🎥 Выберите категорию:', reply_markup=media_select)


@bot.message_handler(commands=['s'])
@bot.edited_message_handler(commands=['s'])
def s(message):
    if message.text == '/s' and len(
            message.text) == 2 or message.text == 'поиск' or message.text == "Поиск фильмов\n📲":
        bot.send_message(message.chat.id, 'Напиши мне фильм после /s (например: "/s интерстеллар")\n'
                                          'и я выдам тебе результаты поиска.')
    elif '/s' in message.text and len(message.text) >= 5:
        s = types.InlineKeyboardMarkup()
        url = 'https://rezka.ag/index.php?do=search&subaction=search&q='
        user = message.text[2:]
        html = requests.get(url + user).text
        soup = BeautifulSoup(html, 'lxml')
        prt = soup.find('div', class_="b-content__inline b-content__search_wrapper").find_all('div',
                                                                                              class_="b-content__inline_item-link")
        for i in prt[0:10]:
            name = i.find('a').text
            href = i.find('a').get('href')
            genre = i.find('div').text
            txt = f"{name} ({genre})"
            post = types.InlineKeyboardButton(text=txt, url=href)
            s.add(post)
        bot.send_message(message.chat.id, '📲 Результаты поиска по HDrezka', reply_markup=s)


@bot.message_handler(commands=['mem'])
def mem(message):
    url = 'https://www.anekdot.ru/random/mem/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    img = soup.find('div', class_="col-left col-left-margin").find_all('div', class_="topicbox")
    for i in img:
        try:
            mem = i.find('img').get('src')
            if mem == None:
                continue
            bot.send_photo(message.chat.id, mem)
            break
        except:
            continue


@bot.message_handler(content_types=['sticker'])
def gif(message):
    bot.send_sticker(message.chat.id, 'CAADAgAD9wMAAonq5QfPnExSSdW_zhYE')


@bot.message_handler(content_types=['audio', 'voice'])
def audio(message):
    bot.send_audio(message.chat.id, 'CQADAgAD6QQAAuD0-EmcefSQ_1T4BxYE')


@bot.message_handler(content_types=['location'])
def handle_loc(message):
    map = types.InlineKeyboardMarkup()
    lon, lat = message.location.longitude, message.location.latitude
    url = "https://www.google.com/maps/search/{}/@{},{},15z/data=!3m1!4b1!4m7!2m6!3m5!1z0KDQtdGB0YLQvtGA0LDQvdGL!2sВаше%20местоположение!4m2!1d30.9657495!2d52.4124194"
    magazin = types.InlineKeyboardButton(text='Магазины', url=url.format('магазин', lat, lon))
    apteka = types.InlineKeyboardButton(text='Аптеки', url=url.format('аптека', lat, lon))
    bankomat = types.InlineKeyboardButton(text='Банкоматы', url=url.format('банкомат', lat, lon))
    kafe = types.InlineKeyboardButton(text='Кафе', url=url.format('кафе', lat, lon))
    cinema = types.InlineKeyboardButton(text='Кинотеатры', url=url.format('кинотеатр', lat, lon))
    map.add(magazin, apteka, bankomat, kafe, cinema)
    coord = f"Широта : {lat} , Долгота : {lon}\nРядом с вами находятся:"
    bot.send_message(message.chat.id, coord, reply_markup=map)


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def text(message):
    if message.text == "Показать клавиатуру\n🎹":
        start(message)
    elif message.text == "Помощь\n🆘":
        help(message)
    elif message.text == "Википедия\n📜":
        wikipedia(message)
    elif message.text == "Гороскоп\n♊️":
        goroskop(message)
    elif message.text == "Медиотека\n🎥":
        rezka(message)
    elif message.text == "Бросить монетку\n🎲":
        coinflip(message)
    elif message.text == "Магический шар\n🎱":
        magic(message)
    elif message.text == "Музыка с Youtube\n🎸":
        youtube(message)
    elif message.text == "Курсы валют\n💹":
        money(message)
    elif message.text == "Анекдот\n😆":
        anekdot(message)
    elif message.text == "Афиша\n🎬":
        afisha(message)
    elif message.text == "Прогноз погоды\n☂️":
        pogoda(message)
    elif message.text == "Поиск фильмов\n📲":
        s(message)
    elif message.text == "Новости кино\n📰":
        lostfilm(message)
    elif message.text == "Новости технологий\n📰":
        hinews(message)
    elif message.text == "Новости Habr\n📰":
        habr(message)
    elif message.text == "Мемчики\n🤪":
        mem(message)
    elif message.text == "Плеслист автора\n🎧":
        playlist(message)
    elif message.text == "Места поблизости\n⛰":
        handle_loc(message)
    elif message.text.lower() == 'марко':
        polo = types.InlineKeyboardMarkup()
        marko = types.InlineKeyboardButton(text='ПОЛО', url='https://www.youtube.com/watch?v=KeFyE6-spWM')
        polo.add(marko)
        bot.send_message(message.chat.id, '😁', reply_markup=polo)
    else:
        bot.send_message(message.chat.id, "Извините, нет такой команды!")


@bot.callback_query_handler(func=lambda c: True)
def inline_selected(c):
    zodiac = {"овен": 'aries', "телец": "taurus", "близнец": "gemini", "рак": "cancer", "лев": "leo",
              "дева": "virgo", "весы": "libra", "скорпион": "scorpio", "стрелец": "sagittarius",
              "козерог": "capricorn", "водолей": "aquarius", "рыбы": "pisces"}
    url_list = {'фильмы': 'https://rezka.ag/films/?filter=watching',
                'сериалы': 'https://rezka.ag/series/?filter=watching',
                'мультфильмы': 'https://rezka.ag/cartoons/?filter=watching',
                'аниме': 'https://rezka.ag/animation/?filter=watching',
                'новинки': 'https://rezka.ag/new/?filter=watching',
                'анонсы': 'https://rezka.ag/announce/'}
    if c.data in zodiac:
        url = "http://1001goroskop.ru/?znak="
        html = requests.get(url + zodiac[c.data]).text
        soup = BeautifulSoup(html, 'lxml')
        goroskop = soup.find('table', id="eje_text").find('div', itemprop="description").find('p').text
        bot.send_message(c.message.chat.id, goroskop)
    if c.data == 'поиск':
        link = types.InlineKeyboardMarkup()
        search = types.InlineKeyboardButton(text='Поиск по HDrezka',
                                            url='https://rezka.ag/index.php?do=search&subaction=search&q=python')
        link.add(search)
        bot.send_message(c.message.chat.id, 'Напиши мне фильм после /s (например: "/s интерстеллар")\n'
                                            'и я выдам тебе результаты поиска.', reply_markup=link)
    if c.data in url_list:
        html = requests.get(url_list[c.data]).text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('div', class_="b-content__inline").find_all('div', class_="b-content__inline_item-link")
        medialist = types.InlineKeyboardMarkup()
        for i in content[0:10]:
            name, href = i.text, i.find('a').get('href')
            medialist.add(types.InlineKeyboardButton(text=name, url=href))
        bot.send_message(c.message.chat.id, f'🎞 {c.data} сейчас смотрят', reply_markup=medialist)


def every_minute():
    requests.get('https://www.google.com')
    threading.Timer(60, every_minute).start()


# ======================================================================================================================
if __name__ == '__main__':
    every_minute()
    bot.polling(none_stop=True, interval=0)

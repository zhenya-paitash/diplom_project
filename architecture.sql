CREATE TABLE IF NOT EXISTS money (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	date TEXT,
	AUD REAL, BGN REAL, UAH REAL, DKK REAL,
	USD REAL, EUR REAL, PLN REAL, IRR REAL,
	ISK REAL, JPY REAL, CAD REAL, CNY REAL,
	KWD REAL, MDL REAL, NZD REAL, NOK REAL,
	RUB REAL, XDR REAL, SGD REAL, KGS REAL,
	KZT REAL, TRY REAL, GBP REAL, CZK REAL,
	SEK REAL, CHF REAL);

CREATE TABLE IF NOT EXISTS money_landmarks (
	id INTEGER,
	scale INTEGER,
	abbreviation TEXT,
	name TEXT);

CREATE TABLE IF NOT EXISTS weather (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	date TEXT,
	city TEXT,
	day_period TEXT,
	temp_min TEXT,
	temp_max TEXT,
	description TEXT,
	icon TEXT,
	pressure TEXT,
	humidity TEXT,
	wind_speed TEXT,
	direction_wind TEXT);

CREATE TABLE IF NOT EXISTS afisha (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	date TEXT,
	time TEXT,
	name TEXT,
	description TEXT,
	href TEXT,
	poster TEXT,
	trailer TEXT);

CREATE TABLE IF NOT EXISTS films (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	rate_imdb TEXT,
	rate_kp TEXT,
	time TEXT,
	date TEXT,
	country TEXT,
	genre TEXT,
	age TEXT,
	producer TEXT,
	actors TEXT,
	tagline TEXT,
	description TEXT,
	img TEXT,
	href TEXT);

CREATE TABLE IF NOT EXISTS series (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	rate_imdb TEXT,
	rate_kp TEXT,
	time TEXT,
	date TEXT,
	country TEXT,
	genre TEXT,
	age TEXT,
	producer TEXT,
	actors TEXT,
	tagline TEXT,
	description TEXT,
	img TEXT,
	href TEXT);

CREATE TABLE IF NOT EXISTS cartoons (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	rate_imdb TEXT,
	rate_kp TEXT,
	time TEXT,
	date TEXT,
	country TEXT,
	genre TEXT,
	age TEXT,
	producer TEXT,
	actors TEXT,
	tagline TEXT,
	description TEXT,
	img TEXT,
	href TEXT);

CREATE TABLE IF NOT EXISTS lostfilm (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT,
	date TEXT,
	img TEXT,
	href TEXT);

CREATE TABLE IF NOT EXISTS hinews (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	text TEXT,
	img TEXT,
	href TEXT);

CREATE TABLE IF NOT EXISTS habr (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	href TEXT);

CREATE TABLE IF NOT EXISTS music (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	href TEXT);

CREATE TABLE IF NOT EXISTS messages (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	mail TEXT,
	review TEXT,
	clock TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

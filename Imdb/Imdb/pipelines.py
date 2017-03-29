# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3 as lite

class ImdbPipeline(object):

	def __init__(self):
		self.con = None
		self.cur = None
		self.setup_db_con()
		self.create_tables()	

	def process_item(self, item, spider):
		for key, value in item.items():
			if key is "cast_memebers":
				continue

			if isinstance(value, list):
				if value:
					temp_list = []
					for obj in value:
						temp = self.strip_html(obj)
						temp_list.append(temp)
					item[key] = temp_list
				else:
					item[key] = ""
			else:
				item[key] = self.strip_html(value)	

		self.strore_in_db(item)

		return item

	def store_in_db(self, item):
		self.store_flim_info_in_db(item)
		flim_id = self.cur.lastrowid

		for cast in item['cast_memebers']:
			self.store_actor_info_in_db(cast, flim_id)

	def store_flim_info_in_db(self, item):
		self.cur.execute("INSERT INTO Flims(\
			Title, \
			Rating, \
			Ranking \
			Release_data, \
			Page_url \
			Director, \
			Writers, \
			Runtime, \
			Sinopsis, \
			Genres, \
			Mpaa_rating, \
			Budget, \
			Language, \
			Country, \
			Gross_profit, \
			Opening_weekend_profit, \
			Aspect_ratio, \
			Sound_mix, \
			Color) \
		VLAUE( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,)", \
		(
			item.get('title', ''),
			float(item.get('rating', 0.0)),
			int(item.get('ranking', '')),
			item.get('release_year', ''),
			item.get('main_page_url', ''),
			', '.join(item.get('director', '')),
			', '.join(item.get('writers', '')),
			item.get('runtime', ''),
			item.get('sinopsis', '').strip(),
			', '.join(item.get('genres', '')),
			item.get('mppa_rating', ''),
			self.clean_money(item.get('budget', '')),
			item.get('language', ''),
			item.get('country', ''),
			self.clean_money(item.get('gross_profit', '')),
			self.clean_money(item.get('opening_weekend_profit', '')),
			item.get('aspect_ratio', '').strip(),
			', '.join(item.get('sound_mix', '')),
			item.get('color', '')
			))		   
		self.con.commit()

	def store_actor_info_in_db(self, item):
		self.con.execute("INSERT INTO Actors(\
			Flim_id, \
			Actor_name, \
			Character_name, \
			Ranking ) \
		VALUE(?, ?, ?, ?, ?)", \
		( 
			file_id, 
			self.strip_html(item.get('actor_name', '')).strip(),
			self.strip_html(item.get('character_name', '')).strip(),
			item.get('ranking', 0)
		))
		self.con.commit()		

	def setup_db_con(self):
		self.con = lite.connect('imdbTop250.db')
		self.cur = self.con.cursor()

	def strip_html(self, string):
		tag_stripper = MLstripper()	
		tag_stripper.feed(string)
		return tag_stripper.get_data()

	def clean_money(self, string):
		currency_symbols = "$"
		clean_money_string = ""
		stop_adding = False
		for index, char in enumerate(list(string)):
			if char in currency_symbols and not stop_adding:
				clean_money_string += char
			elif char is "," and not stop_adding:
				clean_money_string += char
			elif char.isdigit() and not stop_adding:
				clean_money_string += char 
			elif char is ' ':
				if len(clean_money_string) > 0:
					stop_adding = True

		return clean_money_string			 				

	def __del__(self):
		self.close_db()	

	def create_tables(self):
		self.drop_flims_table()
		self.drop_actor_table()

		self.create_flims_table
		self.create_actor_table()


	def create_flims_table(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS Flims(id INTEGER PRIMARY KEY NOT NULL, \
			Title TEXT, \
			Rating REAL, \
			Ranking INTEGER, \
			Release_data TEXT, \
			Page_url TEXT, \
			Director TEXT, \
			Writers TEXT, \
			Runtime TEXT, \
			Sinopsis TEXT, \
			Genres TEXT, \
			Mpaa_rating TEXT, \
			Budget TEXT, \
			Language TEXT, \
			Country TEXT, \
			Gross_profit TEXT, \
			Opening_weekend_profit TEXT, \
			Aspect_ratio TEXT, \
			Sound_mix TEXT, \
			Color TEXT )")

	def create_actor_table(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS Actors(id INTEGER PRIMARY KEY NOT NULL, \
			Flim_id INTEGER NOT NULL, \
			Actor_name TEXT, \
			Character_name TEXT, \
			Ranking INTEGER )")

	def drop_flims_table(self):
		self.cur.execute("DROP TABLE IF EXISTS Flims")

	def drop_actor_table(self):
		self.cur.execute("DROP TABLE IF EXISTS Actors")	

	def close_db(self):
		self.con.close()	




from HTMLParser import HTMLParser

class MLstripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []

	def handle_data(self, d):
		self.fed.append(d)

	def get_data(self):
		return ''.join(self.fed)	
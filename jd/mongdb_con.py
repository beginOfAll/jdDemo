from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['jd']


def add_single_url(url_obj):
	db["single_url"].insert_one(url_obj)


def save_multiple(data):
	col = db["multiple_goods"]
	col.insert(data)


def save_single(data):
	col = db['single_good']
	col.insert(data)

import requests
from jd import parse_html, mongdb_con, get_from_db
import csv
import json

'''
multiple_url_list = [
	('GTX1070', r'https://search.jd.com/Search?keyword=1070&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=1070&psort=3&click=0'),
	('DDR4-8G',
	 r'https://search.jd.com/search?keyword=%E5%86%85%E5%AD%98%E6%9D%A1%20ddr4%208g&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=3.def.0.V06&wq=%E5%86%85%E5%AD%98%E6%9D%A1%20dd&ev=210_1558%5E&uc=0#J_searchWrap')
]

single_url_list = [
	('AMD 1600X', 'https://item.jd.com/4802774.html'),
	('AMD 1700', 'https://item.jd.com/3885181.html'),
	('AMD 1700X', 'https://item.jd.com/4466792.html'),
	('Intel i7 7700', 'https://item.jd.com/4132930.html'),
	('Intel i7 7700K', 'https://item.jd.com/4132882.html'),
	('金士顿 8G DDR4', 'https://item.jd.com/2121097.html')
]
'''


def write_to_txt(item, res_dict_list):
	headers = ['time', 'group', 'price', 'name']
	with open('../resultTXT/jd.txt', 'at', encoding="utf-8") as f:
		f.write(item + "\r\n")
		f_csv = csv.DictWriter(f, headers)
		f_csv.writeheader()
		f_csv.writerows(res_dict_list)
		f.write("\r\n")


def get_html(url):
	resp = requests.get(url)
	if resp.headers.get('content-type').find('charset') == -1:
		resp.encoding = resp.apparent_encoding
	return resp.text


def get_json(url):
	sku = url.split('/')[-1].strip(".html")
	price_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + sku
	return json.loads(get_html(price_url))


def run_search():
	single_url_list = get_from_db.get_single_url('')
	for item_name, url in single_url_list:
		json1 = get_json(url)
		res = parse_html.parse_single_json(json1, item_name)
		print(res)
		mongdb_con.save_single(res)
	'''
	multiple_url_list = 
	for item_name, url in multiple_url_list:
		html = get_html(url)
		res = parse_html.parse_multiple(html, group=item_name)
		write_to_txt(item_name, res)
		mongdb_con.save_multiple(res)
	'''


if __name__ == '__main__':
	run_search()

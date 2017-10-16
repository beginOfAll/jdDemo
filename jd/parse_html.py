import re
from collections import OrderedDict

from common import wjz_tools


def parse_multiple(html1, group="noName"):
	result_list = list()

	pat1 = '<ul class="gl-warp clearfix" data-tpl="1".+?<div class="page clearfix">'
	result1 = re.compile(pat1, re.S).findall(html1)
	result1 = result1[0]
	part2 = '<li data-sku=".+?" class="gl-item">.+?</li>'
	goods_list = re.compile(part2, re.S).findall(result1)
	for one in goods_list:
		one_data = OrderedDict()
		one_data["time"] = wjz_tools.get_time1()
		one_data["group"] = group
		# price
		part_price = '<div class="p-price">.+?<div class="p-name p-name-type-2">'
		part_price_i = '<i>(.*?)</i>'
		price = re.compile(part_price, re.S).findall(one)[0]
		one_data["price"] = re.compile(part_price_i, re.S).findall(price)[0]
		# name
		part_name = '<div class="p-name p-name-type-2">.+?<div class="p-commit">'
		name = re.compile(part_name, re.S).findall(one)[0]
		part_name_em = '<em>(.+?)</em>'
		one_data["name"] = re.compile(part_name_em, re.S).findall(name)[0].replace('<font class="skcolor_ljg">',
																				   '').replace('</font>', '')

		result_list.append(one_data)
	return result_list


def parse_single(html1, name):
	result_dict = OrderedDict()
	result_dict["time"] = wjz_tools.get_time1()
	result_dict["name"] = name
	# price
	pat1 = '<div class="summary-price J-summary-price">(.+?)<div class="summary-info J-summary-info clearfix">'
	pat_price = '<span class="price J-p-4802774">(.+?)</span>'
	result1 = re.compile(pat1, re.S).findall(html1)[0]
	result_dict["price"] = re.compile(pat_price, re.S).findall(result1)[0]
	return result_dict


def parse_single_json(json1, name):
	result_dict = OrderedDict()
	result_dict["time"] = wjz_tools.get_time1()
	result_dict["name"] = name
	result_dict["price"] = json1[0]['p']
	return result_dict

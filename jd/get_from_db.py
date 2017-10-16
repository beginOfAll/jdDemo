from jd.mongdb_con import db


def get_by_name(name):
	col = db['single_good']
	# 查询后按时间排序
	data_list = list(col.find({"name": name}, {"time": 1, "price": 1, "_id": 0}).sort([("time", 1)]))
	temp_data = None
	res_list = list()
	for i in data_list:
		if temp_data is None:
			temp_data = i
		else:
			# 过滤同一天的数据
			if i["time"][0:10] == temp_data["time"][0:10]:
				continue
			else:
				temp_data = i
		res_list.append(temp_data)
	return res_list


def get_single_url(user_name):
	cursor = db["single_url"].find({'by': user_name})
	return [(one['name'], one['url']) for one in cursor]

# print(get_by_name('AMD 1600X'))

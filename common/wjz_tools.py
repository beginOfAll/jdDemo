# YYYY-MM-DD HH:MM:SS
def get_time1():
	import time
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# YYYY-MM-DD HH:MM:SS.ssssss
def get_now_time():
	from datetime import datetime
	return datetime.today()

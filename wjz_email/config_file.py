import os
import json
import platform
from werkzeug.utils import secure_filename

if 'Linux' in platform.system():
	base_path = '/home/wjzDemo_config/email/'
	atta_path = base_path + 'atta/'
else:
	base_path = 'C:\\Wangjz\\wjzDemo_config\\email\\'
	atta_path = base_path + 'atta\\'

if not os.path.exists(base_path):
	os.makedirs(base_path)
if not os.path.exists(atta_path):
	os.makedirs(atta_path)


# 参数f
def save_atta(f, username):
	dir_path = atta_path + username + '/'
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	f.save(os.path.join(dir_path, secure_filename(f.filename)))
	return os.path.join(dir_path, secure_filename(f.filename))


def get_config(username):
	config_file_path = base_path + username + '.ini'
	if os.path.isfile(config_file_path):
		with open(config_file_path, 'rt', encoding='utf-8') as f:
			config = json.load(f)
	else:
		config = False
	return config


def save_config(config):
	res = False
	config_file_path = base_path + config['username'] + '.ini'
	with open(config_file_path, 'wt', encoding='utf-8') as f:
		json.dump(config, f)
		res = True
	return res

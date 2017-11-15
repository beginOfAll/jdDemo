from flask import Flask, request, jsonify, render_template, Response, json, Blueprint, redirect, url_for, \
	send_from_directory
from jd import get_from_db, Running, mongdb_con
from common import wjz_tools
from weChat import robot
import base64
from wjz_email import config_file, send_email
from flask_login import (LoginManager, login_required, login_user, current_user, logout_user, UserMixin)

app = Flask(__name__)
# 限制 content 大小，上传文件大小16M
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# user models
class User(UserMixin):
	def __init__(self, id, name, psw):
		self.id = id
		self.name = name
		self.psw = psw


user1 = User('1', 'admin', 'admin')
user2 = User('2', 'wjz', 'wjz12138')
user3 = User('3', 'visitor', '123456')
user_list = [
	user1, user2, user3
]

# flask-login
app.secret_key = 's3cr3t'
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	user = None
	for u in user_list:
		if u.get_id() == user_id:
			user = u
	return user


# login url
auth = Blueprint('auth', __name__)

# small toos url
stools = Blueprint('stools', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		res = False
		name = request.form['username']
		psw = request.form['password']
		for u in user_list:
			if u.name == name and u.psw == psw:
				login_user(u)
				res = True
		return jsonify(res)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))


@app.route('/')
@login_required
def index():
	return render_template('index.html')


@app.route('/wechat/getQR', methods=['POST'])
@login_required
def getQR():
	psw = request.form['password']
	mode = request.form['mode']
	text = request.form['text']
	png = 'data:image/png;base64,'
	if psw == 'wjz':
		png += base64.b64encode(robot.wechat(mode, text)).decode('ascii')
	return Response(png, mimetype='image/png')


@app.route('/send_email/getUser', methods=['POST'])
@login_required
def getUserInfo():
	username = request.form['username']
	if username != '':
		res = config_file.get_config(username)
	else:
		res = False
	return jsonify(res)


@app.route('/send_email/save', methods=['POST'])
@login_required
def saveInfo():
	res = False
	if current_user.id == '3':
		return jsonify("visitor")
	emailData = json.loads(request.form['emailData'])
	try:
		atta1_path = config_file.save_atta(request.files['atta1'], emailData['username'])
	except Exception:
		atta1_path = ''
	try:
		atta2_path = config_file.save_atta(request.files['atta2'], emailData['username'])
	except Exception:
		atta2_path = ''
	try:
		atta3_path = config_file.save_atta(request.files['atta3'], emailData['username'])
	except Exception:
		atta3_path = ''

	if config_file.save_config(emailData):
		emailData['atta1'] = atta1_path
		emailData['atta2'] = atta2_path
		emailData['atta3'] = atta3_path
		res = send_email.new_thread_to_send(emailData)
	return jsonify(res)


@app.route('/jd')
@login_required
def hello_world():
	return render_template('jd.html')


@app.route('/jd/get', methods=['POST'])
@login_required
def get_data():
	name = request.form['name']
	if name != "":
		res = get_from_db.get_by_name(name)
		res_list = list()
		for i in res:
			res_list.append([i["time"], i["price"]])
		return jsonify(res_list)
	else:
		return ""


@app.route('/jd/search')
@login_required
def search_data():
	if current_user.id == '3':
		return jsonify("visitor")
	res = Running.run_search()
	return res


@app.route('/jd/get_single_url')
@login_required
def get_single_url_list():
	d_list = get_from_db.get_single_url("")
	return jsonify(d_list)


@app.route('/jd/add_single_url', methods=['POST'])
@login_required
def add_single():
	if current_user.id == '3':
		return jsonify("visitor")
	url_obj = dict()
	url_obj['by'] = ''
	url_obj['time'] = wjz_tools.get_time1()
	url_obj['name'] = request.form['name']
	url_obj['url'] = request.form['url']
	mongdb_con.add_single_url(url_obj)
	return "success"


@stools.route('/picTotxt', methods=['POST'])
@login_required
def pic_to_txt():
	from wjz_small_tools.pic_to_txt import picToTxt
	if 'pic' not in request.files:
		return jsonify(False)
	f_pic = request.files['pic']
	if f_pic.filename == "":
		return jsonify(False)
	txt_lines = request.form['lines']
	return jsonify(picToTxt(f_pic, int(txt_lines)))


@stools.route('/download/<filename>', methods=['GET'])
@login_required
def download(filename):
	from wjz_small_tools.pic_to_txt import base_path
	return send_from_directory(base_path, filename, as_attachment=True)


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(stools, url_prefix='/stools')
if __name__ == '__main__':
	app.run(debug=True)

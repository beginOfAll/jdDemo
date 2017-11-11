from flask import Flask, request, jsonify, render_template, Response, json
from jd import get_from_db, Running, mongdb_con
from common import wjz_tools
from weChat import robot
import base64
from wjz_email import config_file, send_email

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/wechat/getQR', methods=['POST'])
def getQR():
	psw = request.form['password']
	mode = request.form['mode']
	text = request.form['text']
	png = 'data:image/png;base64,'
	if psw == 'wjz':
		png += base64.b64encode(robot.wechat(mode, text)).decode('ascii')
	return Response(png, mimetype='image/png')


@app.route('/send_email/getUser', methods=['POST'])
def getUserInfo():
	username = request.form['username']
	if username != '':
		res = config_file.get_config(username)
	else:
		res = False
	return jsonify(res)


@app.route('/send_email/save', methods=['POST'])
def saveInfo():
	res = False
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
def hello_world():
	return render_template('jd.html')


@app.route('/jd/get', methods=['POST'])
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
def search_data():
	res = Running.run_search()
	return res


@app.route('/jd/get_single_url')
def get_single_url_list():
	d_list = get_from_db.get_single_url("")
	return jsonify(d_list)


@app.route('/jd/add_single_url', methods=['POST'])
def add_single():
	url_obj = dict()
	url_obj['by'] = ''
	url_obj['time'] = wjz_tools.get_time1()
	url_obj['name'] = request.form['name']
	url_obj['url'] = request.form['url']
	mongdb_con.add_single_url(url_obj)
	return "success"


if __name__ == '__main__':
	app.run(debug=True)

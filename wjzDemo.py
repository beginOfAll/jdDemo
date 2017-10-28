from flask import Flask, request, jsonify, render_template, Response
from jd import get_from_db, Running, mongdb_con
from common import wjz_tools
from weChat import robot
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wechat/getQR', methods=['POST'])
def getQR():
    psw = request.form['password']
    png = 'data:image/png;base64,'
    if psw == 'wjz':
         png += base64.b64encode(robot.wechat()).decode('ascii')
    return Response(png, mimetype='image/png')


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

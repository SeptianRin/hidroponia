import datetime
import time
import os
import re
import bottle
import dataset
import unittest
import simplejson as json
import requests
# import postgress driver
import psycopg2
from bottle import default_app
from boddle import boddle

app = bottle.Bottle()
bottle.TEMPLATE_PATH.insert(0, "./")
# app.config["db"] = dataset.connect("sqlite:///data.db?check_same_thread=False")
if os.environ.get('APP_LOCATION') == 'heroku':
    uri = os.getenv("DATABASE_URL")  # or other relevant config var

    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        app.config["db"] = dataset.connect(uri)
else:
    app.config["db"] = dataset.connect(
        "sqlite:///data.db?check_same_thread=False")

# app.config["db"] = dataset.connect("mysql+pymysql://septianrin:@septianrin.mysql.pythonanywhere-services.com/septianrin$hidroponia")
# app.config["db"] = dataset.connect("mysql+mysqldb://septianrin:hidroponia@septianrin.mysql.pythonanywhere-services.com/septianrin$hidroponia")
app.config["api_key"] = "JtF2aUE5SGHfVJBCG5SH"


@ app.route('/', method=["GET"])
def index():
    dummytank = ""
    logo = "bitmap.png"
    ph = "ph.png"
    thermo = "thermo.png"
    pupuk = "pupuk.png"

    nilaitank = app.config["db"]["data"].all(_limit=1, order_by='-id')
    for point in nilaitank:
        dummytank = point["tinggi"]

    return bottle.template("frontend.html", logo=logo, pupuk=pupuk, thermo=thermo, ph=ph, dummytank=dummytank)


@ app.route('/predict', method=["GET"])
def predict():
    # URL = "http://forecast-that.herokuapp.com/predict/"+str(count)
    URL = "http://forecast-that.herokuapp.com/predict"
    response = requests.get(url=URL)
    return response


@ app.route("/height", method=["GET"])
def thermo():
    logo = 'bitmap.png'
    return bottle.template("views/height.html", logo=logo)


@ app.route("/ph", method=["GET"])
def ph():
    logo = 'bitmap.png'
    return bottle.template("views/ph.html", logo=logo)


@ app.route("/conductivity", method=["GET"])
def fert():
    logo = 'bitmap.png'
    return bottle.template("views/conductivity.html", logo=logo)


@ app.route("/asset/image/<picture>")
def serve_pictures(picture):
    return bottle.static_file(picture, root='static/image')


@ app.route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return bottle.static_file(filename, root='static/css')


@ app.route('/<filename:re:.*\.js>')
def javascripts(filename):
    return bottle.static_file(filename, root='static/js')


@ app.route('/<filename:re:.*\.map>')
def maps(filename):
    return bottle.static_file(filename, root='static/map')


@ app.route('/<filename:re:.*\.woff2>')
def font(filename):
    return bottle.static_file(filename, root='static/fonts')


@ app.route("/api", method=["GET"])
def api():
    response = []
    response.append({
        "Data Frontend": bottle.request.url+"/datafrontend"
    })
    response.append({
        "Lihat Semua Data": bottle.request.url+"/lihatdata"
    })
    response.append({
        "Upload Data": bottle.request.url+"/simpandata?tinggi={nilai}&ec={nilai}&ph={nilai}"
    })
    bottle.response.content_type = "application/json"
    return json.dumps(response)


@ app.route("/api/datafrontend", method=["GET"])
def datafrontend():
    response = []
    datapointsdata = app.config["db"]["data"].all(_limit=1, order_by='-id')
    for point in datapointsdata:
        response.append({
            "date": point["ts"],
            "value": point["tinggi"]
        })
        response.append({
            "date": point["ts"],
            "value": point["ec"]
        })
        response.append({
            "date": point["ts"],
            "value": point["ph"]
        })

    bottle.response.content_type = "application/json"
    return json.dumps(response)


@ app.route("/api/simpandata", method=["GET"])
def simpandata():
    simtinggi = bottle.request.query.tinggi
    simec = bottle.request.query.ec
    simph = bottle.request.query.ph
    status = 400
    ts = int(time.time())  # current timestamp

    def is_number(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return True
    if simtinggi:
        if simec:
            if simph:
                if is_number(simtinggi) and is_number(simec) and is_number(simph):
                    app.config["db"]["data"].insert(
                        dict(ts=ts, tinggi=simtinggi, ec=simec, ph=simph))
                    status = 200
                    return "Nilai tinggi: " + simtinggi + ", Nilai EC: " + simec + ", dan Nilai PH: " + simph
                else:
                    return "Data masukan tidak dalam bentuk digit"
            else:
                return "Data masukan PH tidak ditemukan"
        else:
            return "Data masukan EC tidak ditemukan"
    else:
        return "Data masukan Tinggi Nutrisi tidak ditemukan"


@ app.route("/api/lihatdata", method=["GET"])
def lihatdata():
    responsetinggi = []
    responseec = []
    responseph = []
    responseall = {}
    datapointsall = app.config["db"]["data"].all()

    for data in datapointsall:
        responsetinggi.append({
            "date": datetime.datetime.fromtimestamp(int(data["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": data["tinggi"]
        })

        responseec.append({
            "date": datetime.datetime.fromtimestamp(int(data["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": data["ec"]
        })

        responseph.append({
            "date": datetime.datetime.fromtimestamp(int(data["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": data["ph"]
        })

    responseall.update({"dataTinggi": responsetinggi})
    responseall.update({"dataEC": responseec})
    responseall.update({"dataPH": responseph})

    bottle.response.content_type = "application/json"
    return json.dumps(responseall)


@ app.route("/api/lihatdata/<jumlah>", method=["GET"])
def lihatdata(jumlah):
    responsetinggi = []
    responseec = []
    responseph = []
    responseall = {}
    datapointsall = app.config["db"]["data"].all(_limit=jumlah, order_by="-id")

    for data in datapointsall:
        responsetinggi.append({
            "date": datetime.datetime.fromtimestamp(int(data["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": data["tinggi"]
        })

        responseec.append({
            "date": datetime.datetime.fromtimestamp(int(data["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": data["ec"]
        })

        responseph.append({
            "date": datetime.datetime.fromtimestamp(int(data["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": data["ph"]
        })

    responseall.update({"dataTinggi": responsetinggi})
    responseall.update({"dataEC": responseec})
    responseall.update({"dataPH": responseph})

    bottle.response.content_type = "application/json"
    return json.dumps(responseall)


# uncomment if deploy on heroku
if os.environ.get('APP_LOCATION') == 'heroku':
    bottle.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    bottle.run(app, host='localhost', port=3000, debug=True)
# uncomment if deploy on pythonanywhere
# application = default_app()

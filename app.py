import datetime
import time
import os
import bottle
import dataset
import unittest
import simplejson as json
# import postgress driver
import psycopg2
from bottle import default_app
from boddle import boddle

app = bottle.Bottle()
bottle.TEMPLATE_PATH.insert(0, "./")
# app.config["db"] = dataset.connect("sqlite:///data.db?check_same_thread=False")
if os.environ.get('APP_LOCATION') == 'heroku':
    app.config["db"] = dataset.connect(
        os.environ.get('DATABASE_URL'))
else:
    app.config["db"] = dataset.connect(
        "sqlite:///data.db?check_same_thread=False")

# app.config["db"] = dataset.connect("mysql+pymysql://septianrin:@septianrin.mysql.pythonanywhere-services.com/septianrin$hidroponia")
# app.config["db"] = dataset.connect("mysql+mysqldb://septianrin:hidroponia@septianrin.mysql.pythonanywhere-services.com/septianrin$hidroponia")
app.config["api_key"] = "JtF2aUE5SGHfVJBCG5SH"
statusMode = "otomatis"
manph = 7
mantds = 1000
mansuhu = 30


@ app.route('/', method=["GET"])
def index():
    logo = "bitmap.png"
    ph = "ph.png"
    thermo = "thermo.png"
    pupuk = "pupuk.png"
    return bottle.template("frontend.html", logo=logo, pupuk=pupuk, thermo=thermo, ph=ph)


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
    print()
    return bottle.static_file(picture, root='static/image')


@ app.route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return bottle.static_file(filename, root='static/css')


@ app.route('/asset/js/<filename:re:.*\.js>')
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
    datapointstinggi = app.config["db"]["tinggi"].all(_limit=1, order_by='-id')
    datapointsec = app.config["db"]["ec"].all(_limit=1, order_by='-id')
    datapointsph = app.config["db"]["ph"].all(_limit=1, order_by='-id')

    for point in datapointsph:
        response.append({
            "date": point["ts"],
            "value": point["value"]
        })

    for point in datapointstinggi:
        response.append({
            "date": point["ts"],
            "value": point["value"]
        })
    for point in datapointsec:
        response.append({
            "date": point["ts"],
            "value": point["value"]
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

    if is_number(simtinggi) and is_number(simec) and is_number(simph):
        app.config["db"]["tinggi"].insert(dict(ts=ts, value=simtinggi))
        app.config["db"]["ec"].insert(dict(ts=ts, value=simec))
        app.config["db"]["ph"].insert(dict(ts=ts, value=simph))
        status = 200
        return "The value of tinggi is: " + simtinggi + " and the value of EC is: " + simec + " and the value of ph is: " + simph
    else:
        return "Data masukan tidak memenuhi format masukan"


@ app.route("/api/lihatdata", method=["GET"])
def lihatdata():
    responsetinggi = []
    responseec = []
    responseph = []
    responseall = {}
    datapointstinggi = app.config["db"]["tinggi"].all()
    datapointsec = app.config["db"]["ec"].all()
    datapointsph = app.config["db"]["ph"].all()

    for tinggi in datapointstinggi:
        responsetinggi.append({
            "date": datetime.datetime.fromtimestamp(int(tinggi["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": tinggi["value"]
        })
    for ec in datapointsec:
        responseec.append({
            "date": datetime.datetime.fromtimestamp(int(ec["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": ec["value"]
        })
    for ph in datapointsph:
        responseph.append({
            "date": datetime.datetime.fromtimestamp(int(ph["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": ph["value"]
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

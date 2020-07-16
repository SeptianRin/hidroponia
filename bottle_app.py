
import datetime
import time

import bottle
import dataset
import simplejson as json
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app

app= bottle.Bottle()

bottle.TEMPLATE_PATH.insert(0,"./")

app.config["db"] = dataset.connect("sqlite:///data.db?check_same_thread=False")
#app.config["db"] = dataset.connect("mysql+pymysql://septianrin:@septianrin.mysql.pythonanywhere-services.com/septianrin$hidroponia")
#app.config["db"] = dataset.connect("mysql+mysqldb://septianrin:hidroponia@septianrin.mysql.pythonanywhere-services.com/septianrin$hidroponia")

app.config["api_key"] = "JtF2aUE5SGHfVJBCG5SH"


@app.route('/', method = ["GET"])
def index():
    logo = "bitmap.png"
    ph = "ph.png"
    thermo = "thermo.png"
    pupuk = "pupuk.png"
    return bottle.template("frontend.html",logo=logo,pupuk=pupuk,thermo=thermo,ph=ph)

@app.route("/api",method=["GET","POST"])
def api():
    if bottle.request.method == "POST":
        status = 400
        ts = int(time.time())
        value = bottle.request.body.read()
        api_key = bottle.request.get_header("Api-Key")

        print(">>> {} :: {}".format(value,api_key))

        if api_key == "JtF2aUE5SGHfVJBCG5SH" and value :
            app.config["db"]["point"].insert(dict(ts=ts, value=value))
            status = 200
            return bottle.HTTPResponse(status=status, body="sukses")

    else:
        response = []
        datapoints =app.config["db"]["point"].all()

        for point in datapoints:
            response.append({
                "date": datetime.datetime.fromtimestamp(int(point["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
                "value": point["value"]
            })
        bottle.response.content_type = "application/json"
        return json.dumps(response)

@app.route("/datafrontend",method=["GET"])
def datafrontend():
    response = []
    datapointssuhu = app.config["db"]["suhu"].all(_limit=1,order_by='-id')
    datapointstds = app.config["db"]["tds"].all(_limit=1,order_by='-id')
    datapointsph = app.config["db"]["ph"].all(_limit=1,order_by='-id')

    for point in datapointsph:
        response.append({
            "date": point["ts"],
            "value": point["value"]
            })

    for point in datapointssuhu:
        response.append({
            "date": point["ts"],
            "value": point["value"]
        })
    for point in datapointstds:
        response.append({
            "date": point["ts"],
            "value": point["value"]
            })

    bottle.response.content_type = "application/json"
    return json.dumps(response)

@app.route("/thermo", method=["GET"])
def thermo():
    logo = 'bitmap.png'
    return bottle.template("temp.html", logo =logo)

@app.route("/ph", method=["GET"])
def ph():
    logo = 'bitmap.png'
    return bottle.template("ph.html", logo =logo)

@app.route("/fert", method=["GET"])
def fert():
    logo = 'bitmap.png'
    return bottle.template("fert.html", logo =logo)

@app.route("/asset/image/<picture>")
def serve_pictures(picture):
    print()
    return bottle.static_file(picture, root='./image')

@app.route("/asset/css/<css>")
def serve_css(css):
    return bottle.static_file(css, root='./mysite/css')

@app.route("/simpandata", method=["GET"])
def simpandata():
    suhu = bottle.request.query.field1
    tds = bottle.request.query.field2
    ph = bottle.request.query.field3
    status = 400
    ts = int(time.time()) # current timestamp
    #value = bottle.request.body.read() # data from device
    #api_key = bottle.request.get_header("Api-Key") # api key from header
    # outputs to console recieved data for debug reason
    #print(">>> {} :: {}".format(value, api_key))
    # if api_key is correct and value is present
    # then writes attribute to point table
    if suhu and tds and ph:
        app.config["db"]["suhu"].insert(dict(ts=ts, value=suhu))
        app.config["db"]["tds"].insert(dict(ts=ts, value=tds))
        app.config["db"]["ph"].insert(dict(ts=ts, value=ph))
        status = 200
        return bottle.HTTPResponse(status=status, body="sukses")
    # we only need to return status
    return bottle.HTTPResponse(status=status, body="gagal")
#return "The value of param1 is: " + suhu + " and the value of param2 is: " + tds + " and the value of param 3 is: " + ph #bottle.template("frontend.html")

@app.route("/lihatdata", method=["GET"])
def lihatdata():
    responsesuhu = []
    responsetds = []
    responseph = []
    responseall = []
    datapointssuhu = app.config["db"]["suhu"].all()
    datapointstds = app.config["db"]["tds"].all()
    datapointsph = app.config["db"]["ph"].all()

    for suhu in datapointssuhu:
        responsesuhu.append({
            "date": datetime.datetime.fromtimestamp(int(suhu["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": suhu["value"]
        })
    for tds in datapointstds:
        responsetds.append({
            "date": datetime.datetime.fromtimestamp(int(tds["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
                "value": tds["value"]
            })
    for ph in datapointsph:
        responseph.append({
            "date": datetime.datetime.fromtimestamp(int(ph["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": ph["value"]
        })

    responseall.append(responsesuhu)
    responseall.append(responsetds)
    responseall.append(responseph)

    bottle.response.content_type = "application/json"
    return json.dumps(responseall)

@app.route("/coba", method=["GET"])
def coba():
    responsesuhu = []
    responsetds = []
    responseph = []
    responseall = {}
    datapointssuhu = app.config["db"]["suhu"].all()
    datapointstds = app.config["db"]["tds"].all()
    datapointsph = app.config["db"]["ph"].all()

    for suhu in datapointssuhu:
        responsesuhu.append({
            "date": datetime.datetime.fromtimestamp(int(suhu["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": suhu["value"]
        })
    for tds in datapointstds:
        responsetds.append({
            "date": datetime.datetime.fromtimestamp(int(tds["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
                "value": tds["value"]
            })
    for ph in datapointsph:
        responseph.append({
            "date": datetime.datetime.fromtimestamp(int(ph["ts"])).strftime("%Y-%m-%d %H:%M:%S"),
            "value": ph["value"]
        })

    responseall.update({"dataSuhu":responsesuhu})
    responseall.update({"dataTDS":responsetds})
    responseall.update({"dataPH":responseph})

    bottle.response.content_type = "application/json"
    return json.dumps(responseall)

#uncomment if deploy on
if os.environ.get('APP_LOCATION') == 'heroku':
    bottle.run(app,host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    bottle.run(app,host='localhost', port=3000, debug=True)
#uncomment if deploy on pythonanywhere
#application = default_app()

from autojoin import AutoJoin
from flask import Flask,jsonify
import json
from flask import make_response
from flask import request
import psutil
import os 
import platform

app = Flask(__name__)

@app.route('/')
def home():
	return 'SkyAuto Version 1.0'

@app.route('/system',methods=['get'])
def processSystem():
    cpuInfo = platform.processor()
    systemInfo = platform.system() + " " +platform.release() + " " +platform.version()
    cpuCount = psutil.cpu_count()
    cpuFreq  = psutil.cpu_freq()
    # cpuPercent = psutil.cpu_percent(interval=0.5, percpu=True)
    cpuPercent = f'{round(psutil.cpu_percent(),2)}%'
    memory = psutil.virtual_memory()
    memoryTotal = f'{round(memory.total / 1024**3)}GB'
    memoryAvailable = f'{round(memory.available/1024**3,1)}GB'
    systemInfo = {
        'cpu' : cpuInfo,
        'system':systemInfo,
        'cpuCount' : cpuCount,
        'cpuFreq' : cpuFreq,
        'cpuPercent' :cpuPercent,
        'memoryTotal' : memoryTotal,
        'memoryAvailable' : memoryAvailable
    }
    retData = {"success":"true","data":systemInfo}
    response = make_response(jsonify(retData),201)
    return response

@app.route('/autoload',methods=['post'])
def processAutoLoadPost():
    requestJSON = request.get_json()
    targetURL = requestJSON['url']
    userNick = requestJSON['userNick']
    password = requestJSON['password']
    print(targetURL+" "+userNick+" "+password)

    auto = AutoJoin(targetURL,userNick,password)
    retData = auto.join()    
    response = make_response(jsonify(retData),201)
    return response


@app.route('/autoload',methods=['get'])
def processAutoLoadGetParameters():
    targetURL = request.args.get("url")
    userNick = request.args.get("usernick")
    password = request.args.get("password")
    print(targetURL+" "+userNick+" "+password)

    auto = AutoJoin(targetURL,userNick,password)
    retData = auto.join()    
    response = make_response(jsonify(retData),201)
    return response
    

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)    
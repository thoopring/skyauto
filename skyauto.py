from autojoin import AutoJoin
from flask import Flask,jsonify
import json
from flask import make_response
from flask import request
import psutil
import os 
import platform
import time
from flask import Response

app = Flask(__name__)
joins = []

@app.route('/')
def home():
	return 'SkyAuto Version 1.3'

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

@app.route('/listjoins',methods=['get'])
def listJoins():
    results = []

    for join in joins:
        jd = {
            'userNick' : join.userNick,
            'uniqueID' : join.uniqueID
        }
        results.append(jd)
    
    response = Response(json.dumps(results),  mimetype='application/json')
    return response

@app.route('/killjoin',methods=['get'])
def killJoin():
    userNick = request.args.get("usernick")
    uniqueID = request.args.get("uniqueid")    
    targetIndex = -1
    if userNick!=None:
        for join in joins:
            if join.userNick == userNick:
                join.driver.quit()
                joins.remove(join)                
                retData = {"success":"true","userNick":join.userNick}
                response = make_response(jsonify(retData),201)
                return response
    elif uniqueID!=None:
        for join in joins:
            if join.uniqueID == uniqueID:                
                join.driver.quit()
                joins.remove(join)
                retData = {"success":"true","uniqueID":join.uniqueID}
                response = make_response(jsonify(retData),201)
                return response

    retData = {"success":"false"}
    response = make_response(jsonify(retData),201)
    return response


@app.route('/killalljoins',methods=['get'])
def killAllJoins():
    for join in joins:        
        join.driver.quit()
    joins.clear()
    retData = {"success":"true"}
    response = make_response(jsonify(retData),201)
    return response

@app.route('/killlastjoin',methods=['get'])
def killLastJoin():
    join = joins.pop()
    join.driver.quit()
    retData = {"success":"true"}
    response = make_response(jsonify(retData),201)
    return response

# ????????? join??? ???????????? ?????? 
@app.route('/autojoin',methods=['get'])
def processAutoLoadGetParameters():
    targetURL = request.args.get("url")
    userNick = request.args.get("usernick")
    password = request.args.get("password")
    isCameraUsed = extractBoolean(request.args.get("camera"))
    isMicUsed = extractBoolean(request.args.get("mic"))

    print(targetURL+" "+userNick+" "+password)

    auto = AutoJoin(targetURL,userNick,password,isCameraUsed,isMicUsed)
    retData = auto.join()    
    response = make_response(jsonify(retData),201)
    if retData['success'] == 'true':
        joins.append(auto)
    return response   

# ?????? ?????? join??? ???????????? ?????? 
@app.route('/autojoins',methods=['get'])
def processAutoLoadsGetParameters():
    targetURL = request.args.get("url")
    userNick = request.args.get("usernick")
    password = request.args.get("password")
    isCameraUsed = extractBoolean(request.args.get("camera"))
    isMicUsed = extractBoolean(request.args.get("mic"))
    numberGoal = int(request.args.get("number"))
    number = numberGoal

    print(targetURL+" "+userNick+" "+password)

    # ???????????? ?????? 
    start = time.time()
    limit = 10   # ????????? ????????? ??? ?????? ?????? join ?????? 
    timeoutLimit = number * 20 # ?????? join??? ???????????? ?????? = ????????? join ?????? * 20??? 
    # ????????? join ????????? limit??? ???????????? limit??? ?????? 
    if number>limit:
        number = limit
    
    countSuccess = 0    # ????????? ??????
    elapsed = 0         # ??? ?????? ?????? 
    while(countSuccess<number and elapsed<timeoutLimit):
        userNick = userNick + str(countSuccess+1)
        auto = AutoJoin(targetURL,userNick,password,isCameraUsed,isMicUsed)
        # ret = auto.joinSimul()
        ret = auto.join()
        if ret['success'] == 'true':            
            joins.append(auto)
            countSuccess = countSuccess + 1
        # ?????? ?????? ??????
        current = time.time()
        # ?????? ?????? ?????? 
        elapsed = current - start
        print(f"the number of success = {countSuccess}  time elapsed = {elapsed} ")

    # ????????? ?????? = ????????? ????????? ???????????? ?????? ?????? 
    if countSuccess == number:
        retData = {"success":"true","goal":numberGoal,"sucessCount":countSuccess,"limit":limit,"timeElapsed":elapsed,"timeoutLimit":timeoutLimit}    
    else:
        retData = {"success":"false","goal":numberGoal,"sucessCount":countSuccess,"limit":limit,"timeElapsed":elapsed,"timeoutLimit":timeoutLimit}    
    response = make_response(jsonify(retData),201)
    return response
    

def extractBoolean(rawValue):
    ret = True
    if rawValue==None or rawValue=="":
        return True            
    rawValue = rawValue.lower()
    if rawValue == "true" or rawValue == "on" or rawValue == "1":
        ret = True
    elif rawValue == "false" or rawValue == "off" or rawValue == "0":
        ret = False
    else:
        ret = False
    return ret


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)    
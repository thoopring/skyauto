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
	return 'SkyAuto Version 1.2'

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

@app.route('/autojoin',methods=['post'])
def processAutoLoadPost():
    requestJSON = request.get_json()
    targetURL = requestJSON['url']
    userNick = requestJSON['userNick']
    password = requestJSON['password']
    print(targetURL+" "+userNick+" "+password)

    auto = AutoJoin(targetURL,userNick,password)
    retData = auto.join()    
    response = make_response(jsonify(retData),201)
    if retData['success'] == 'true':
        joins.append(auto)
    return response

# 여러 번의 join을 요청하는 경우 
@app.route('/autojoin',methods=['get'])
def processAutoLoadGetParameters():
    targetURL = request.args.get("url")
    userNick = request.args.get("usernick")
    password = request.args.get("password")
    print(targetURL+" "+userNick+" "+password)

    auto = AutoJoin(targetURL,userNick,password)
    retData = auto.join()    
    response = make_response(jsonify(retData),201)
    if retData['success'] == 'true':
        joins.append(auto)
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
def killJoins():
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
    

# 여러 번의 join을 요청하는 경우 
@app.route('/autojoins',methods=['get'])
def processAutoLoadsGetParameters():
    targetURL = request.args.get("url")
    userNick = request.args.get("usernick")
    password = request.args.get("password")
    numberGoal = int(request.args.get("number"))
    number = numberGoal

    print(targetURL+" "+userNick+" "+password)

    # 시작시점 마킹 
    start = time.time()
    limit = 10   # 한번에 요청할 수 있는 최대 join 개수 
    timeoutLimit = number * 20 # 전체 join에 허용되는 시간 = 요청한 join 갯수 * 20초 
    # 요청한 join 개수가 limit를 넘어가면 limit로 설정 
    if number>limit:
        number = limit
    
    countSuccess = 0    # 성공한 횟수
    elapsed = 0         # 총 경과 시간 
    while(countSuccess<number and elapsed<timeoutLimit):
        userNick = userNick + str(countSuccess+1)
        auto = AutoJoin(targetURL,userNick,password)
        # ret = auto.joinSimul()
        ret = auto.join()
        if ret['success'] == 'true':            
            joins.append(auto)
            countSuccess = countSuccess + 1
        # 현재 시점 마킹
        current = time.time()
        # 경과 시간 계산 
        elapsed = current - start
        print(f"the number of success = {countSuccess}  time elapsed = {elapsed} ")

    # 성공한 갯수 = 요청한 갯수와 일치하면 성공 보고 
    if countSuccess == number:
        retData = {"success":"true","goal":numberGoal,"sucessCount":countSuccess,"limit":limit,"timeElapsed":elapsed,"timeoutLimit":timeoutLimit}    
    else:
        retData = {"success":"false","goal":numberGoal,"sucessCount":countSuccess,"limit":limit,"timeElapsed":elapsed,"timeoutLimit":timeoutLimit}    
    response = make_response(jsonify(retData),201)
    return response
    

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)    
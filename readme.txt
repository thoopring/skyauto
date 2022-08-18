# skyepub inc 
# 18.aug 2022
# skytree created

# system used in test
    windows 11
    amd64 ryzen7 5800
    32gb ram 

# preinstall software
    python 3.10.6 installed by choco
    pip 22.2.2 installed
    pip install selenium==3.141
    pip install flask
    pip install psutil

# copy y4m files to C:\Temp folder from the links below
    https://www.dropbox.com/s/nxoh0h55o7wd6a9/city.y4m?dl=1
    https://www.dropbox.com/s/q2e1lxqed966bjo/stockholm.y4m?dl=1
    https://www.dropbox.com/s/ndbmtqakyaz46eb/students.y4m?dl=1
    https://www.dropbox.com/s/b482w03862mklsd/waterfall.y4m?dl=1

# run skyauto flask app
    python skyauto.py 



# skyauto flask app REST APIs 

/system
    returns system information including cpu,memory or etc. 
    method get
    example
        http://127.0.0.1:5000/system
    result
    {
        "data": {
            "cpu": "AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD",
            "cpuCount": 16,
            "cpuFreq": [
                3401.0,
                0.0,
                3401.0
            ],
            "cpuPercent": "4.7%",
            "memoryAvailable": "21.7GB",
            "memoryTotal": "32GB",
            "system": "Windows 10 10.0.22000"
        },
        "success": "true"
    }

/autoload
    lauches chrome and automate joining process, returns sucess or fail when it is finished or terminated. 
    it uses virtual fake cam to simulate the video conferencing. (no additional virtual cam software needed)
    method get
    params
        url      : the url of video conference server
        usernick : user nickname
        password : room secret password
    example
        http://127.0.0.1:5000/autoload?url=https://meet.uplus.co.kr/login?roomNo=3962&usernick=User&password=1234

    result
        when failed 
            step 1 failed to load the url itself. 
            step 2 failed to goto the device setting scene
            step 3 failed to click on start(시작하기) button 
            {
                "step": "3",
                "success": "false"
            }
        when sucess
            {
                "step": "4",
                "success": "true"
            }


/autoload 
    lauches chrome and automate joining process, returns sucess or fail when it is finished or terminated. 
    it uses virtual fake cam to simulate the video conferencing. (no additional virtual cam software needed)
    method post
    body raw in json
        {
            url: the url of video server
            usernick: the nick of joining publisher 
            password : room password
        }
    result
        when failed 
            step 1 failed to load the url itself. 
            step 2 failed to goto the device setting scene
            step 3 failed to click on start(시작하기) button 
            {
                "step": "3",
                "success": "false"
            }
        when sucess
            {
                "step": "4",
                "success": "true"
            }

# when postman(rest api test tool) is used for test, please import SkyAuto.postman_collection.json file in postman application.  
    postman download
    https://www.postman.com/downloads/  

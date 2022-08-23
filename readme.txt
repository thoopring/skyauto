# skyepub inc 
# 18.aug 2022
# skytree created

# system used in test
    ubuntu 20.04.1 (LST)
    Virtual Machine on Proxmox (Octa Cores, 8Giga RAM)

# preinstall software
    * python 3.10.6 installed by choco
    * pip (22.2.2 installed)
    $ pip install selenium==4.0.0.
    $ pip install flask
    $ pip install psutil
    $ pip install webdriver_manager (unzip it and copy ChromeDriver file onto [appPath])

# copy y4m files to [appPath]/y4m folder from the links below
    video y4m files
    https://www.dropbox.com/s/nxoh0h55o7wd6a9/city.y4m?dl=1
    https://www.dropbox.com/s/q2e1lxqed966bjo/stockholm.y4m?dl=1
    https://www.dropbox.com/s/ndbmtqakyaz46eb/students.y4m?dl=1
    https://www.dropbox.com/s/b482w03862mklsd/waterfall.y4m?dl=1
    audio wav files
    https://www.dropbox.com/s/fqukjal60c7i124/BabyElephantWalk60.wav?dl=1
    https://www.dropbox.com/s/yd9xec6kg8ltda2/PinkPanther60.wav?dl=1
    https://www.dropbox.com/s/gcsiwj56pr3b3xq/CantinaBand60.wav?dl=1
    https://www.dropbox.com/s/c39o4991wbs63k4/StarWars60.wav?dl=1


# run skyauto flask app 
    $ python skyauto.py 
    

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

/autojoin
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


/autojoin 
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

/autojoins
    lauches chrome and automate joining process number of times, returns success or fail when all joings are finished or terminated. 
    it uses virtual fake cam to simulate the video conferencing. (no additional virtual cam software needed)
    method get
    params
        url      : the url of video conference server
        usernick : user nickname
        password : room secret password
        number   : number of joins
    example
        http://127.0.0.1:5000/autojoins?url=https://meet.uplus.co.kr/login?roomNo=3962&usernick=User&password=1234&number=5

    result
        success:true is returned
        {
            "goal": 10,
            "limit": 10,
            "success": "true",
            "sucessCount": 10,
            "timeElapsed": 99.40823459625244,
            "timeoutLimit": 200
        }

        success:false is returned when skyauto failed to make joins to the number requested in time. 
        timeoutLimit = number * 20(seconds)
        {
            "goal": 10,
            "limit": 10,
            "success": "false",
            "sucessCount": 8,
            "timeElapsed": 200.40823459625244,
            "timeoutLimit": 200
        }




/killlastjoin
    termiates the last join and release it. 

    {
        "success": "true"
    }

/killlastjoin
    params
        usernick    : the usernick of join to terminate
        uniqueid    : the unique id of join to kill 

    example 
        http://10.10.10.190:5000/killjoin?uniqueid=62fdaec7-94c1-4dc0-a42b-227d551fb35b
    
    Result 
        {
            "success": "true",
            "uniqueID": "62fdaec7-94c1-4dc0-a42b-227d551fb35b"
        }
        or 

        {
            "success": "true",
            "usernick": "User1"
        }

/killalljoins
    kill all joins 

    example
        http://10.10.10.190:5000/killalljoins

    result  
        {
            "success": "true"
        }


# when postman(rest api test tool) is used for test, please import SkyAuto.postman_collection.json file in postman application.  
    postman download
    https://www.postman.com/downloads/  
# skyepub inc 
# 18.aug~5.sep 2022
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
    $ pip install webdriver_manager 
        (unzip it and copy chromedriver file onto [appPath])

# folder structure. 
    drwxrwxr-x 8 skytree skytree     4096  8월 24 02:59 .git
    -rw-rw-r-- 1 skytree skytree       32  8월 23 21:44 .gitignore
    drwxrwxr-x 2 skytree skytree     4096  8월 23 21:58 __pycache__
    -rw-rw-r-- 1 skytree skytree     7592  8월 23 21:49 autojoin.py
    -rwxr-xr-x 1 skytree skytree 13978368  8월 23 21:49 chromedriver            // webdriver 
    drwxrwxr-x 2 skytree skytree     4096  8월 24 02:49 postman                 
    -rw-rw-r-- 1 skytree skytree     6412  8월 24 02:59 readme.txt
    -rw-rw-r-- 1 skytree skytree     5872  8월 23 21:53 skyauto.py
    drwxrwxr-x 2 skytree skytree     4096  8월 23 21:47 y4m                     // media folder (y4m, wav files)


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

*** Updated ***
/autojoin
    launches chrome and automates joining process, returns sucess or fail when it is finished or terminated. 
    it uses virtual fake cam to simulate the video conferencing. (no additional virtual cam software needed)
    method get
    params
        url     : the url of video conference server
        usernick: user nickname
        password: room secret password
        camera  : on (turn camera on),  off (camera off)    default : on 
        mic     : on (turn mic on),     off (mic off)       default : on  
    example
        http://127.0.0.1:5000/autoload?url=https://meet.uplus.co.kr/login?roomNo=3962&usernick=User&password=1234&camera=on&mic=off 

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

*** Updated ***
/autojoins
    launches chrome and automates joining processes till number of joins, returns success or fail when all joings are finished or terminated. 
    it uses virtual fake cam and mic to simulate the video conferencing. (no additional virtual cam software needed)
    method get
    params
        url     : the url of video conference server
        usernick: user nickname
        password: room secret password
        camera  : on (turn camera on),  off (camera off)    default : on 
        mic     : on (turn mic on),     off (mic off)       default : on  
        number  : number of joins
    example
        http://127.0.0.1:5000/autojoins?url=https://meet.uplus.co.kr/login?roomNo=3962&usernick=User&password=1234&number=5&camera=on&mic=off 

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

/listjoins
    returns the list of joins in json array. 
    example
        http://10.10.10.190:5000/listjoins

    result
        [
            {
                "userNick": "User1",
                "uniqueID": "62fdaec7-94c1-4dc0-a42b-227d551fb35b"
            },
            {
                "userNick": "User2",
                "uniqueID": "76edafc7-88c1-5fcf-d49b-3334551ef4ff"
            }

        ]


# when postman(rest api test tool) is used for test, please import SkyAuto.postman_collection.json file in postman application.  
    postman download
    https://www.postman.com/downloads/  


# SkyAuto RestAPI 동작 확인 
    모두 설치 후 
    https://10.10.10.190:5000/system 를 호출하여 
    시스템 정보의 json값을 반환하는지 확인. 

    만약 값을 반환하지 않으면 
    firewall에서 5000번 포트가 허용되는지 확인할 필요가 있음. 

    $ sudo ufw disable
    혹은 
    $ sudo ufw allow 5000/tcp


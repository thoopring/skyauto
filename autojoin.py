from curses import KEY_ENTER
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import random
import traceback
import os
import uuid

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class AutoJoin:
    def __init__(self,url,userNick,password,isCameraUsed,isMicUsed):
        self.targetURL = url
        self.userNick = userNick
        self.password = password
        self.isCameraUsed = isCameraUsed
        self.isMicUsed = isMicUsed
        self.uniqueID = str(uuid.uuid4())
        self.driver = None

    # 접속 함수 
    def join(self):
        print("autojoin #0")
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--allow-file-access-from-files")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument('window-size=720x480')
        # options.add_experimental_option("detach", True) 

        #TODO: FixMe
        # headless 인 경우 참여하고 있는 사용에 대해서 종료할 수 있는 방법이 없음 (주의!!)
        # AWS Vm 에서는 반드시 headless 만 사용 가능함
        #  --> Webdriver 실행 후 리소스 정리(driver.quit)를 보장해야 함
        options.add_argument('--headless')
        # options.add_argument('--no-sandbox')

        print("autojoin #1")
        # Check y4m file path
        script_path = os.path.dirname(os.path.abspath(__file__))
        y4m_path = os.path.join(script_path, 'y4m')
        # print('Video Data Path:', y4m_path)
        if not os.path.exists(y4m_path):
            print('Error: copy y4m file to [your dir]/webrtc-loadtest/y4m')
            return
        else:
            print(f"y4m_path={y4m_path}")
        
        ri = random.randrange(0, 4)
        if ri == 0:
            options.add_argument('--use-file-for-fake-video-capture=%s' % (os.path.join(y4m_path, 'city.y4m')))
            options.add_argument('--use-file-for-fake-audio-capture=%s' % (os.path.join(y4m_path, 'CantinaBand60.wav')))
        elif ri == 1:
            options.add_argument('--use-file-for-fake-video-capture=%s' % (os.path.join(y4m_path, 'stockholm.y4m')))
            options.add_argument('--use-file-for-fake-audio-capture=%s' % (os.path.join(y4m_path, 'PinkPanther60.wav')))
        elif ri == 2:
            options.add_argument('--use-file-for-fake-video-capture=%s' % (os.path.join(y4m_path, 'students.y4m')))
            options.add_argument('--use-file-for-fake-audio-capture=%s' % (os.path.join(y4m_path, 'StarWars60.wav')))
        elif ri == 3:
            options.add_argument('--use-file-for-fake-video-capture=%s' % (os.path.join(y4m_path, 'students.y4m')))
            options.add_argument('--use-file-for-fake-audio-capture=%s' % (os.path.join(y4m_path, 'BabyElephantWalk60.wav')))
            
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", { \
            "profile.default_content_setting_values.media_stream_mic": 1, 
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1, 
            "profile.default_content_setting_values.notifications": 1 
        })

        print("autojoin #3")

        # Selenium 4.0 - load webdriver
        # self.driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Program Files\ChromeDriver\chromedriver.exe')
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except Exception as e:
            print(e)
            return

        print("autojoin #4")
        # self.driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Program Files\ChromeDriver\chromedriver.exe')

        # 해당 주소로 접속 시도 (새로운 브라우저/새로운 탭에서)
        
        self.driver.get(self.targetURL)
        self.driver.set_window_size(720, 480) 

        # self.driver.implicitly_wait(3)
        # 해당 주소가 로딩되어서 room_id를 id로 가진 element가 발견될때까지 대기한다. 
        # 최대 120초 대기 
        print("autojoin #5")
        try:
            isLoaded = WebDriverWait(self.driver,120).until(
                EC.presence_of_all_elements_located((By.ID,'room_id'))
            )
        except:
            # 만약에 오류가 생기면 드라이버를 중지하고 1단계를 표시하는 실패 정보를 리턴한다. 
            self.driver.quit()
            return {"success":"false","step":"5"}

        # 첫번째 화면에서 입력 요소를 추출 
        userNickInput = self.driver.find_element("xpath","/html/body/div[1]/div[1]/div[1]/div/div[2]/input")
        passwordInput = self.driver.find_element("xpath","/html/body/div[1]/div[1]/div[1]/div/div[3]/input")
        loginButton   = self.driver.find_element("xpath","/html/body/div[1]/div[1]/div[1]/div/div[4]/a")

        # 입력요소에 값을 할당
        userNickInput.send_keys(self.userNick)
        passwordInput.send_keys(self.password)
        loginButton.click()

        print("autojoin #6")
        # 기기설정 화면이 나오고 indicator가 사라질때까지 기다린다. 
        # self.driver.implicitly_wait(time_to_wait=20)        
        # 기기설정 화면이 나올때까지 대기한다. 
        try:
            isLoaded = WebDriverWait(self.driver,120).until(
                EC.presence_of_all_elements_located((By.ID,'lodingEnd'))
            )
        except:
            # 만약에 오류가 생기면 드라이버를 중지하고 단계를 표시하는 실패 정보를 리턴한다. 
            self.driver.quit()
            return {"success":"false","step":"6"}  

        print("autojoin #7")

        # 설정창에서 필요한 경우 카메라와 mic를 off시킨다. 
        try:
            print("autojoin #7-1")
            cameraCheckBox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vediooff"]/label')))
            
            print("autojoin #7-2")
            micCheckBox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mikeoff"]/label')))

            print("autojoin #7-3")
            if not self.isCameraUsed and not cameraCheckBox.is_selected():     
                cameraCheckBox.click()
            
            print("autojoin #7-4")
            if not self.isMicUsed and not micCheckBox.is_selected():
                micCheckBox.click()

        except Exception as e:
            self.driver.quit()
            return {"success":"false","step":"7"}  


        print("autojoin #8")
        # 로딩이 끝난 상태에서 startButton을 찾는다. 
        try:
            startButton   = self.driver.find_element("id","setApply")
            startButton.click() 
        except:
            self.driver.quit()
            return {"success":"false","step":"8"}  
        
        print("autojoin #9")
        return {"success":"true","step":"9"}



    # 접속과 유사한 상황을 시뮬레이션 - 사용하지 말 것 
    def joinSimul(self):
        # 시간을 임의로 지체시킨다. 
        time = random.randrange(1,2)
        sleep(time)        
        # 결과를 임의로 내보낸다. 
        step = random.randrange(1,5)
        result = {}
        if step>=1 and step<=3:
            result = {"success":"false","Step":step}
        elif step==4:
            result = {"success":"true","Step":step}
        return result

        
    def isAlertPresent(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException: 
            print("Alert is not found")
            return False

    def showInfo(self):
        print(self.targetURL)
        print(self.userNick)
        print(self.password)
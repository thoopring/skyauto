from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.options import Options
import random

class AutoJoin:
    def __init__(self,url,userNick,password):
        self.targetURL = url
        self.userNick = userNick
        self.password = password
        self.driver = None

    def join(self):

        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--allow-file-access-from-files")
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument('window-size=720x480')
        options.add_experimental_option("detach", True) 
        
        ri = random.randrange(0,3)
        if ri==0:
            options.add_argument(r"--use-file-for-fake-video-capture=C:\Temp\city.y4m")
        elif ri==1:
            options.add_argument(r"--use-file-for-fake-video-capture=C:\Temp\stockholm.y4m")
        elif ri==2:
            options.add_argument(r"--use-file-for-fake-video-capture=C:\Temp\students.y4m")
        elif ri==3:
            options.add_argument(r"--use-file-for-fake-video-capture=C:\Temp\waterfall.y4m")        
        options.add_argument("--disable-infobars")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", { \
            "profile.default_content_setting_values.media_stream_mic": 1, 
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1, 
            "profile.default_content_setting_values.notifications": 1 
        })
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Program Files\ChromeDriver\chromedriver.exe')

        # 해당 주소로 접속 시도 (새로운 브라우저/새로운 탭에서)
        
        self.driver.get(self.targetURL)
        self.driver.set_window_size(720, 480)

        # self.driver.implicitly_wait(3)
        # 해당 주소가 로딩되어서 room_id를 id로 가진 element가 발견될때까지 대기한다. 
        # 최대 10초 대기 
        try:
            isLoaded = WebDriverWait(self.driver,10).until(
                EC.presence_of_all_elements_located((By.ID,'room_id'))
            )
        except:
            # 만약에 오류가 생기면 드라이버를 중지하고 1단계를 표시하는 실패 정보를 리턴한다. 
            self.driver.quit()
            return {"success":"false","step":"1"}

        # 첫번째 화면에서 입력 요소를 추출 
        userNickInput = self.driver.find_element("xpath","/html/body/div[1]/div[1]/div[1]/div/div[2]/input")
        passwordInput = self.driver.find_element("xpath","/html/body/div[1]/div[1]/div[1]/div/div[3]/input")
        loginButton   = self.driver.find_element("xpath","/html/body/div[1]/div[1]/div[1]/div/div[4]/a")

        # 입력요소에 값을 할당
        userNickInput.send_keys(self.userNick)
        passwordInput.send_keys(self.password)
        loginButton.click()

        # self.driver.implicitly_wait(time_to_wait=20)        
        # 기기설정 화면이 나올때까지 대기한다. 
        try:
            isLoaded = WebDriverWait(self.driver,20).until(
                EC.presence_of_all_elements_located((By.ID,'fileDown'))
            )
        except:
            # 만약에 오류가 생기면 드라이버를 중지하고 1단계를 표시하는 실패 정보를 리턴한다. 
            self.driver.quit()
            return {"success":"false","step":"2"}

        
        # 기기설정에서 startButton을 검색한다. 팝업등으로 만약 못찾을 경우 잠시 후 다시 시도한다. 
        # 최종적으로도 못찾을 경우 3단계 정지 정보를 내보낸다. 
        try:
            startButton   = self.driver.find_element("xpath","/html/body/div[2]/div[5]/div[2]/div[1]/div/a[2]")
            startButton.click()
            self.driver.implicitly_wait(10)
            startButton   = self.driver.find_element("xpath","/html/body/div[2]/div[5]/div[2]/div[1]/div/a[2]")
            startButton.click()
        except Exception:
            self.driver.quit()
            return {"success":"false","step":"3"}

        return {"success":"true","step":"4"}

        
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
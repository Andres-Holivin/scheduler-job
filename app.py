import time
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler
import os


class HcBinus:
    url = "https://hc.binus.edu"

    def __init__(self):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        #                                chrome_options=chrome_options)
        self.driver.get(self.url)
        print("run scheduler")

    def login(self):
        inputUsr = self.driver.find_element(By.ID, 'logonuidfield')
        inputPsr = self.driver.find_element(By.ID, 'logonpassfield')
        inputUsr.send_keys("andres.holivin")
        inputPsr.send_keys("andres12holivin")
        btnLogin = self.driver.find_element(By.NAME, "uidPasswordLogon")
        btnLogin.click()
        time.sleep(25)

    def switch_frame(self):
        self.driver.switch_to.frame("contentAreaFrame")
        self.driver.switch_to.frame("isolatedWorkArea")
        print(str(self.driver.page_source))
        print("switch frame")

    def check_wfh(self):
        wfh = self.driver.find_element(By.ID, "WD4A-lbl").click()
        print("check work from home")
        time.sleep(10)

    def click_clock_in(self):
        clock_in = self.driver.find_element(By.ID, "WD4D").click()
        print(datetime.now())
        print("click clock in")
        time.sleep(10)
        self.driver.close()

    def click_clock_out(self):
        clock_out = self.driver.find_element(By.ID, "WD4E").click()
        print(datetime.now())
        print("click clock out")
        time.sleep(10)
        self.driver.close()


class PushMessageTelegram:
    token = "5266674278:AAErQrTyRuIB--0QNEZKailsLxZJqanuydY"
    chat_id = "2086356774"
    url_telegram = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chat_id + "&text="

    def __init__(self):
        print("init")

    def send(self, msg):
        response = requests.get(self.url_telegram + msg)
        print(response)


if __name__ == "__main__":
    sched = BlockingScheduler()


    @sched.scheduled_job('cron', day_of_week='0-5', hour=11, minute=30)
    def scheduled_job():
        hc = HcBinus()
        hc.login()
        hc.check_wfh()
        hc.click_clock_in()
        msg = PushMessageTelegram()
        msg.send("clock in hc run on : "+str(datetime.now()))

    @sched.scheduled_job('cron', day_of_week='0-5', hour=23, minute=55)
    def scheduled_job():
        hc = HcBinus()

        hc.login()
        hc.switch_frame()
        hc.check_wfh()
        hc.click_clock_out()
        msg = PushMessageTelegram()
        msg.send("clock out hc run on : " + str(datetime.now()))


    sched.start()

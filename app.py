import time
from datetime import datetime
import requests
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler


class HcBinus:
    url = "https://hc.binus.edu"

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.url)
        inputUsr = self.driver.find_element(By.ID, 'logonuidfield')
        inputPsr = self.driver.find_element(By.ID, 'logonpassfield')
        inputUsr.send_keys("andres.holivin")
        inputPsr.send_keys("andres12holivin")
        btnLogin = self.driver.find_element(By.NAME, "uidPasswordLogon")
        btnLogin.click()
        time.sleep(10)

    def check_wfh(self):
        self.driver.switch_to.frame("contentAreaFrame")
        self.driver.switch_to.frame("isolatedWorkArea")
        print("switch frame")
        wfh = self.driver.find_element(By.ID, "WD4A-lbl").click()
        print("check work from home")
        time.sleep(5)
        self.driver.close()

    def click_clock_in(self):
        clock_in = self.driver.find_element(By.ID, "WD4D").click()
        print(datetime.now())
        print("click clock in")

    def click_clock_out(self):
        clock_out = self.driver.find_element(By.ID, "WD4E").click()
        print(datetime.now())
        print("click clock out")


class PushMessageTelegram:
    token = "5266674278:AAErQrTyRuIB--0QNEZKailsLxZJqanuydY"
    chat_id = "2086356774"
    url_telegram = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chat_id + "&text="

    def __init__(self):
        print("init")

    def send(self, msg):
        response = requests.get(self.url_telegram + msg)
        print(response)


class HcSchedule:
    def __init__(self):
        print("do schedule")

    def run_schedule_clock_in(self):
        msg = PushMessageTelegram()
        schedule \
            .every(1).minutes.do(msg.send(str(datetime.now())))


def job():
    print("I'm working...")


def cronjob():
    print("Cron job is running")
    print("Tick! The time is: %s" % datetime.now())

    msg = PushMessageTelegram()
    msg.send("Run schedule on The time is: %s" % datetime.now())


if __name__ == "__main__":
    sched = BlockingScheduler()


    @sched.scheduled_job('interval', minutes=1)
    def timed_job():
        msg = PushMessageTelegram()
        msg.send("this schedule run every minutes on " + str(datetime.now()))


    @sched.scheduled_job('cron', day_of_week='0-6', hour=0, minute=20)
    def scheduled_job():
        msg = PushMessageTelegram()
        msg.send("this schedule run every day on " + str(datetime.now()))


    sched.start()

    # schedule \
    #     .every(1).minutes.do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # hcSchedule = HcSchedule()
    # hcSchedule.run_schedule_clock_in()
    # hc = HcBinus()
    # hc.clock_in()
    # msg = PushMessageTelegram()
    # msg.send("test")

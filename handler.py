import json
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
import requests
import logging
from typing import Union
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TODAY = datetime.date.today()
logging.basicConfig(filename='logger.log',level=logging.WARN)

def hello(event, context):
    is_success = execute()
    if is_success:
        return {"statusCode": 200}
    return {"statusCode": 500}

def execute() -> bool:
    try:
        advancec_decline_ratio = RatioService().get_today_ratio()
        if advancec_decline_ratio.is_valid():
            message = advancec_decline_ratio.generate_message()
            MessageService(message).post()
        return True
    except Exception as e:
        logging.error(e)
        return False

class AdvancedDeclineRatio(object):
    def __init__(self, val) -> None:
        self.val = val

    def is_valid(self) -> bool:
        return self.val

    def generate_message(self) -> str:
        return f"【{TODAY}】\n騰落レシオ(10日平均): {self.val}%"

class RatioService(object):

    def __init__(self) -> None:
        # 独自のrequestsをつくる。今回はヘッドレスなGoogleChromeを利用
        self.requests = RequestService()

    def get_today_ratio(self) -> AdvancedDeclineRatio:
        html = self.requests.get('https://nikkei225jp.com/data/touraku.php')
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select('#datatbl tr')
        return self._find_today_ratio(rows)

    def _find_today_ratio(self, rows) -> AdvancedDeclineRatio:
        # なぜかスクレイピングしたときの日付が1日異なる（18:29現在）ため、比較条件のほうは1日ズラす
        cond = TODAY - datetime.timedelta(days=1) # => datetime.datetime(2019, 7, 23, 1, 59, 33, 338054)# 10時間
        for i in range(1,31):
            columns = rows[i].select('td')
            date_column = datetime.date.fromisoformat(columns[0].text)
            if date_column == cond:
                ratio_of_ten_days_average = columns[8].text
                return AdvancedDeclineRatio(float(ratio_of_ten_days_average))
        return AdvancedDeclineRatio(False)

class RequestService(object):
    def __init__(self) -> None:
        options = Options()
        # バイナリのディレクトリを指定
        options.binary_location = '/usr/bin/google-chrome'
        # Headlessモード、no-sandboxモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        # ブラウザを起動する
        driver = webdriver.Chrome(options=options)
        self.driver = driver

    def get(self, url) -> str:
        self.driver.get(url)

        # HTMLを文字コードをUTF-8に変換してから取得します
        html = self.driver.page_source.encode('utf-8')
        return html


class MessageService(object):
    def __init__(self, message:str) -> None:
        self.message = message

    def post(self):
        json = {
            'text': self.message
        }
        requests.post(os.environ.get("SLACK_INCOMING_WEBHOOK"), json=json)

execute()

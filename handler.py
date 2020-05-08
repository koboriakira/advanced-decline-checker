import json
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import request


def hello(event, context):
    try:
        ratio_service = RatioService()
        ratio_of_ten_days_average = ratio_service.get_today_ratio()
        message_service = MessageService(ratio_of_ten_days_average)
        message_service.post()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

    return {
        "statusCode": 200,
    }


class RatioService(object):

    URL = 'https://nikkeiyosoku.com/up_down_ratio/'
    BUSINESS_DAYS = 10

    def get_today_ratio(self):
        today = date.fromisoformat('2020-05-01')

        # ブラウザのオプションを格納する変数をもらってきます。
        # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
        options = Options()
        options.set_headless(True)

        # ブラウザを起動してアクセスする
        driver = webdriver.Chrome(chrome_options=options)
        driver.get("https://nikkei225jp.com/data/touraku.php")

        # HTMLを文字コードをUTF-8に変換してから取得します
        html = driver.page_source.encode('utf-8')

        # BeautifulSoupで扱えるようにパースします
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select('#datatbl tr')

        for i in range(1, 31):
            row = rows[i]
            columns = row.select('td')
            date_column = date.fromisoformat(columns[0].text)
            if date_column == today:
                ratio_of_ten_days_average = columns[8].text
                return float(ratio_of_ten_days_average)
        return False


class MessageService(object):
    # .envで管理する予定
    SLACK_INCOMING_WEBHOOK = 'dummy'

    def __init__(self, ratio):
        self.ratio = ratio

    def post(self):
        text = f"騰落レシオ(10日平均): {self.ratio}%"
        json = {
            'text': text
        }
        requests.post(SLACK_INCOMING_WEBHOOK, json=json)

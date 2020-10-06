from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # Adds chromedriver binary to path


class RequestService:
    def __init__(self, url) -> None:
        self.driver = _generate_drive(url)

    def get(self) -> str:
        # HTMLを文字コードをUTF-8に変換してから取得します
        html = self.driver.page_source.encode('utf-8')
        return html


def _generate_drive(url: str):
    chromedriver_binary
    options = Options()
    # バイナリのディレクトリを指定
    options.binary_location = '/usr/bin/google-chrome'
    # Headlessモード、no-sandboxモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    # ブラウザを起動する
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

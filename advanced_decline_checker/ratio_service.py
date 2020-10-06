import datetime
from datetime import date
from typing import Optional
from bs4 import BeautifulSoup
from advanced_decline_checker.request_service import RequestService
from advanced_decline_checker.advanced_decline_ratio import AdvancedDeclineRatio

URL = 'https://nikkei225jp.com/data/touraku.php'


class RatioService(object):

    def __init__(self) -> None:
        # 独自のrequestsをつくる。今回はヘッドレスなGoogleChromeを利用
        self.requests = RequestService(URL)

    def get_today_ratio(self) -> Optional[AdvancedDeclineRatio]:
        """
        当日の騰落レシオを取得します。ないときはNoneを返却します
        """
        html = self.requests.get()
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select('#datatbl tr')
        return self._find_today_ratio(rows)

    def _find_today_ratio(self, rows) -> Optional[AdvancedDeclineRatio]:
        # なぜかスクレイピングしたときの日付が1日異なる（18:29現在）ため、比較条件のほうは1日ズラす
        # => datetime.datetime(2019, 7, 23, 1, 59, 33, 338054)# 10時間
        cond: date = datetime.date.today() - datetime.timedelta(days=1)
        for i in range(1, 31):
            columns = rows[i].select('td')
            advancec_decline_ratio: AdvancedDeclineRatio = _create_advanced_decline_ratio(
                columns)
            if advancec_decline_ratio is None:
                continue
            if advancec_decline_ratio.research_date == cond:
                return advancec_decline_ratio
        return None


def _create_advanced_decline_ratio(columns) -> Optional[AdvancedDeclineRatio]:
    research_date: date = datetime.date.fromisoformat(columns[0].text)
    try:
        ratio_of_ten_days_average = float(columns[8].text)
        return AdvancedDeclineRatio(ratio_of_ten_days_average, research_date)
    except ValueError:
        return None

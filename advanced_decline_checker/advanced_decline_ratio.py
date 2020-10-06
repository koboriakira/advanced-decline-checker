from datetime import date as Date


class AdvancedDeclineRatio(object):
    def __init__(self, ratio_of_ten_days_average, research_date: Date) -> None:
        self.ratio_of_ten_days_average = ratio_of_ten_days_average
        self.research_date = research_date

    def generate_message(self) -> str:
        return f"【{self.research_date}】\n騰落レシオ(10日平均): {self.ratio_of_ten_days_average}%"

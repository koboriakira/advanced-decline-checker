import requests
import os


class MessageService(object):
    def __init__(self, message: str) -> None:
        self.message = message

    def post(self):
        print(f'Post Message: {self.message}')
        json = {
            'text': self.message
        }
        url: str = os.environ.get("SLACK_INVESTMENT_WEBHOOK")
        requests.post(url, json=json)

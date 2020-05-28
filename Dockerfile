# docker build -t adv_dev_checker_image .
FROM python:3.7.5-slim

# 必要なパッケージをインストール
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y wget unzip curl
  # gcc

WORKDIR work

# GoogleChorme,Chromedriveと依存パッケージをインストール
# 一度失敗させて、依存関係のあるパッケージを出しておく
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && dpkg -i google-chrome-stable_current_amd64.deb; exit 0

# もう一度。今度はchromedriverも入れる
RUN apt-get update \
  && apt-get -f install -y \
  && dpkg -i google-chrome-stable_current_amd64.deb \
  && curl -O https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip \
  && unzip chromedriver_linux64.zip \
  && mv chromedriver /usr/local/bin/

ADD requirements.txt requirements.txt
ADD handler.py handler.py
ADD .env .env

RUN pip install -r requirements.txt

CMD 'bin/bash'

# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, urllib.error
import yaml
from datetime import datetime as dt

class SlackBot:
    """SlackBot class for KeyaBlog"""


    def __init__(self, token):
        self.token = token
        self.url = "https://slack.com/api/chat.postMessage"


    def post_message(self, entry_info):
        '''Post new entry's infomations'''
        req = urllib.request.Request(self.url)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        params = {'token': self.token, # token
                  'channel': "sandbox", # channel ID
                  'username': entry_info['name'],
                  'icon_url': entry_info['icon'],
                  'attachments': [
                      {
                          "color": "#A1599C",
                          "pretext": "新しい記事読んでね!",
                          "title": entry_info['title'],
                          "title_link": entry_info['url']
                      },
                      {
                          "color": "#43B24B",
                          "text": entry_info['head'],
                          "image_url": entry_info['thum'],
                          "footer": "published on",
                          "ts": dt.strptime(entry_info['update'], '%Y-%m-%dT%H:%M+09:00').timestamp()
                      }
                  ]
        }
        print(params)
        params = urllib.parse.urlencode(params).encode("utf-8")

        with urllib.request.urlopen(req, params) as res:
            data = res.read().decode("utf-8")
            print(data)


if __name__ == "__main__":
    f = open("config.yml", 'r')
    data = yaml.load(f)  # 読み込む
    f.close()
    bot = SlackBot(data["token"])
    bot.post_message("test")

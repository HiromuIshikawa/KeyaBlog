# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime as dt

class UpdateChecker:
    """Set of some method for checking blog update"""


    def __init__(self, domain):
        self.domain = domain


    def latest_entries(self):
        '''Return all member's latest entry'''

        path = "/s/k46o/diary/member/list"
        html = urllib.request.urlopen(self.domain + path).read()
        soup = BeautifulSoup(html, 'lxml')
        new_entry_titles = soup.find('select', class_='js-select').findAll('option')[1:]
        update_list = eval(soup.findAll('script')[2].string.replace('\n','')[19:1558].replace('member','"member"').replace('update','"update"'))

        image_src = soup.find('ul', class_='thumb').findAll('li')
        images = [image.find('img').get('src') for image in image_src]

        latest_entries = []
        for i, entry in enumerate(new_entry_titles):
            d = {}
            tmp = entry.string.split(' | ')
            d["name"] = tmp[0].split('(')[0].replace(" ", "")
            d["title"] = tmp[1]
            d["url"] = self.domain + entry.get('value')
            d["image"] = images[i]
            d.update(update_list[i])
            latest_entries.append(d)

        return latest_entries


    def updated_entries(self, entries):
        '''Return new entries from past check(In the future)'''
        f = open('past_checked.txt','r+')
        past_checked = f.readline()
        print(past_checked)
        past_checked = dt.strptime(past_checked, '%Y-%m-%dT%H:%M+09:00\n')

        now = dt.now().strftime('%Y-%m-%dT%H:%M+09:00')
        f.seek(0)
        f.truncate()
        f.write(now)
        f.close()

        updated = [entry for entry in entries if dt.strptime(entry['update'], '%Y-%m-%dT%H:%M+09:00') > past_checked]

        return updated


if __name__ == "__main__":

    keyaki_checker = UpdateChecker("http://www.keyakizaka46.com")
    latest_entries = keyaki_checker.latest_entries()
    print(latest_entries)

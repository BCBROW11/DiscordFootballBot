from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread
from Helpers.runningback import runningback

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
global runningbacks

class get_rb_stats(Thread):

    def __init__(self):
        self.runningbacks = []
        Thread.__init__(self)

    def run(self):
            while(True):
                try:
                    request = requests.get("https://www.pro-football-reference.com/years/2020/rushing.htm")
                    rb_soup = BeautifulSoup(request.content, 'html.parser')
                    rb_table_div = rb_soup.find("div", id="div_rushing")
                    table = rb_table_div.find("tbody")
                    rb_rows = table.find_all("tr", attrs={"class": None})
                    i = 1
                    for row in rb_rows:
                        stats = row.find_all(attrs={"data-stat":True})
                        str = stats[i].text
                        str = str.replace("*", "")
                        self.runningbacks.append(runningback(str, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+6].text, stats[i+7].text, stats[i+8].text, stats[i+10].text, stats[i+11].text, stats[i+12].text, stats[i+13].text))
                    print("runningbacks update done")
                    time.sleep(43200)
                except Exception:
                    print("Excpetion in rb_stats: \n" + exception)
                    pass

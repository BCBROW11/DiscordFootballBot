from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread
from Helpers.quarterback import quarterback

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
global quarterbacks

class get_qb_stats(Thread):

    def __init__(self):
        self.quarterbacks = []
        Thread.__init__(self)

    def run(self):
            while(True):
                try:
                    request = requests.get("https://www.pro-football-reference.com/years/2020/passing.htm")
                    qb_soup = BeautifulSoup(request.content, 'html.parser')
                    qb_table_div = qb_soup.find("div", id="div_passing")
                    table = qb_table_div.find("tbody")
                    qb_rows = table.find_all("tr", attrs={"class": None})
                    i = 1
                    for row in qb_rows:
                        stats = row.find_all(attrs={"data-stat":True})
                        str = stats[i].text
                        str = str.replace("*", "")
                        self.quarterbacks.append(quarterback(str, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+7].text, stats[i+8].text, stats[i+9].text, stats[i+10].text, stats[i+11].text, stats[i+13].text, stats[i+21].text, stats[i+23].text))
                    print("quarterbacks update done")
                    time.sleep(43200)
                except Exception:
                    print("Excpetion in qb_stats: \n" + exception)
                    pass

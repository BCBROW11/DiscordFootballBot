from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread
from Helpers.receiver import receiver

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
global receivers

class get_wr_stats(Thread):

    def __init__(self):
        self.receivers = []
        Thread.__init__(self)

    def run(self):
            while(True):
                try:

                    request = requests.get("https://www.pro-football-reference.com/years/2020/receiving.htm")
                    wr_soup = BeautifulSoup(request.content, 'html.parser')
                    wr_table_div = wr_soup.find("div", id="div_receiving")
                    table = wr_table_div.find("tbody")
                    wr_rows = table.find_all("tr", attrs={"class": None})
                    i = 1
                    for row in wr_rows:
                        stats = row.find_all(attrs={"data-stat":True})
                        str = stats[i].text
                        str = str.replace("*", "")
                        self.receivers.append(receiver(str, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+6].text, stats[i+7].text, stats[i+8].text, stats[i+9].text, stats[i+10].text, stats[i+11].text, stats[i+12].text, stats[i+13].text, stats[i+14].text, stats[i+16].text, stats[i+17].text))
                    print("receivers update done")
                    time.sleep(43200)
                except Exception:
                    print("Excpetion in wr_stats: \n" + exception)
                    pass

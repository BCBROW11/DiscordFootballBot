from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
global wr_rows

class get_wr_stats(Thread):

    def __init__(self):
        self.wr_rows = None
        Thread.__init__(self)

    def run(self):
        try:
            while(True):
                request = requests.get("https://www.pro-football-reference.com/years/2020/receiving.htm")
                wr_soup = BeautifulSoup(request.content, 'html.parser')
                wr_table_div = wr_soup.find("div", id="div_receiving")
                table = wr_table_div.find("tbody")
                self.wr_rows = table.find_all("tr", attrs={"class": None})
                print("receivers update done")
                time.sleep(43200)
        except Exception:
            print("Excpetion in wr_stats: \n" + exception)

from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
global qb_rows

class get_qb_stats(Thread):

    def __init__(self):
        self.qb_rows = None
        Thread.__init__(self)

    def run(self):
        try:
            while(True):
                request = requests.get("https://www.pro-football-reference.com/years/2020/passing.htm")
                qb_soup = BeautifulSoup(request.content, 'html.parser')
                qb_table_div = qb_soup.find("div", id="div_passing")
                table = qb_table_div.find("tbody")
                self.qb_rows = table.find_all("tr", attrs={"class": None})
                print("quarterbacks update done")
                time.sleep(43200)
        except Exception:
            print("Excpetion in qb_stats: \n" + exception)

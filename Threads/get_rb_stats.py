from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
global rb_rows

class get_rb_stats(Thread):

    def __init__(self):
        self.rb_rows = None
        Thread.__init__(self)

    def run(self):
        while(True):
            request = requests.get("https://www.pro-football-reference.com/years/2020/rushing.htm")
            rb_soup = BeautifulSoup(request.content, 'html.parser')
            rb_table_div = rb_soup.find("div", id="div_rushing")
            table = rb_table_div.find("tbody")
            self.rb_rows = table.find_all("tr", attrs={"class": None})
            print("runningbacks update done")
            time.sleep(43200)

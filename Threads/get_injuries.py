from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread
from Helpers.injury import injury

"""
get_injures is a thread that scrapes pro-football-reference for injury reports once every 12 hours
"""
global injuries

class get_injuries(Thread):

    def __init__(self):
        self.injuries = []
        Thread.__init__(self)

    def run(self):
            while(True):
                try:
                    request = requests.get("https://www.pro-football-reference.com/players/injuries.htm")
                    inj_soup = BeautifulSoup(request.content, 'html.parser')
                    inj_table_div = inj_soup.find("div", id="div_injuries")
                    table = inj_table_div.find("tbody")
                    inj_rows = table.find_all("tr", attrs={"class": None})
                    i = 0
                    for row in inj_rows:
                        stats = row.find_all(attrs={"data-stat":True})
                        self.injuries.append(injury(stats[i].text, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                    print("injury update done")
                    time.sleep(43200)
                except Exception:
                    print("Excpetion in get_team_def: \n" + exception)
                    pass

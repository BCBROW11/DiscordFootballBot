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
        self.injuries = None
        Thread.__init__(self)

    def run(self):
            while(True):
                try:
                    self.injuries = []
                    request = requests.get("https://www.pro-football-reference.com/players/injuries.htm")
                    inj_soup = BeautifulSoup(request.content, 'html.parser')
                    inj_table_div = inj_soup.find("div", id="div_injuries")
                    table = inj_table_div.find("tbody")
                    inj_rows = table.find_all("tr", attrs={"class": None})
                    i = 0
                    for row in inj_rows:
                        stats = row.find_all(attrs={"data-stat":True})
                        if stats[i+1].text.lower() == "gnb":
                            self.injuries.append(injury(stats[i].text, "GB", stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                        if stats[i+1].text.lower() == "sfo":
                            self.injuries.append(injury(stats[i].text, "SF", stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                        if stats[i+1].text.lower() == "kan":
                            self.injuries.append(injury(stats[i].text, "KC", stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                        if stats[i+1].text.lower() == "nor":
                            self.injuries.append(injury(stats[i].text, "NO", stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                        if stats[i+1].text.lower() == "nwe":
                            self.injuries.append(injury(stats[i].text, "NE", stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                        if stats[i+1].text.lower() == "lvr":
                            self.injuries.append(injury(stats[i].text, "LV", stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                        if stats[i+1].text.lower() == "tam":
                            self.injuries.append(injury(stats[i].text, "TB", stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                        else:
                            self.injuries.append(injury(stats[i].text, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+4].text, stats[i+5].text))
                    print("injury update done")
                    time.sleep(43200)
                except Exception:
                    print("Excpetion in get_team_def: \n" + exception)
                    pass

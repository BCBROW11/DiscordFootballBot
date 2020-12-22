from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
global team_def_rows

class get_team_def_stats(Thread):

    def __init__(self):
        self.team_def_rows = None
        Thread.__init__(self)

    def run(self):
        try:
            while(True):
                request = requests.get("https://www.pro-football-reference.com/years/2020/opp.htm")
                team_def_soup = BeautifulSoup(request.content, 'html.parser')
                team_def_table_div = team_def_soup.find("div", id="div_team_stats")
                table = team_def_table_div.find("tbody")
                self.team_def_rows = table.find_all("tr", attrs={"class": None})
                print("team defense update done")
                time.sleep(43200)
        except Exception:
            print("Excpetion in get_team_def: \n" + exception)

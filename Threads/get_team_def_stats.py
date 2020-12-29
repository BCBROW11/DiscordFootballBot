from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread
from Helpers.team_defense import team_defense

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
global defenses

class get_team_def_stats(Thread):

    def __init__(self):
        self.defenses = None
        Thread.__init__(self)

    def run(self):
            while(True):
                try:
                    self.defenses = []
                    request = requests.get("https://www.pro-football-reference.com/years/2020/opp.htm")
                    team_def_soup = BeautifulSoup(request.content, 'html.parser')
                    team_def_table_div = team_def_soup.find("div", id="div_team_stats")
                    table = team_def_table_div.find("tbody")
                    team_def_rows = table.find_all("tr", attrs={"class": None})
                    i = 1
                    for row in team_def_rows:
                        stats = row.find_all(attrs={"data-stat":True})
                        self.defenses.append(team_defense(stats[i].text, stats[i+2].text, stats[i+3].text, stats[i+5].text, stats[i+6].text, stats[i+7].text, stats[i+9].text, stats[i+10].text, stats[i+11].text, stats[i+12].text, stats[i+13].text, stats[i+14].text, stats[i+16].text, stats[i+17].text, stats[i+18].text, stats[i+19].text, stats[i+21].text, stats[i+22].text))
                    print("team defense update done")
                    time.sleep(43200)
                except Exception:
                    print("Excpetion in get_team_def: \n" + exception)
                    pass

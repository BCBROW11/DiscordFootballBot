from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread
from Helpers.defend import defend

"""
get_def_stats is a thread that scrapes pro-football-reference for defensive stats once every 12 hours. This thread takes longer to execute
than the other stat scrapes, and this is why it is separate.
"""
global defends
class get_def_stats(Thread):

    def __init__(self):
        self.defends = None
        Thread.__init__(self)

    def run(self):
            while(True):
                try:
                    self.defends = []
                    request = requests.get("https://www.pro-football-reference.com/years/2020/defense.htm")
                    df_soup = BeautifulSoup(request.content, 'html.parser')
                    df_table_div = df_soup.find("div", id="div_defense")
                    table = df_table_div.find("tbody")
                    df_rows = table.find_all("tr", attrs={"class": None})
                    i = 1
                    for row in df_rows:
                        stats = row.find_all(attrs={"data-stat":True})
                        if stats[i+6].text == "":
                            stats[i+6].insert(0, "0")
                        if stats[i+10].text == "":
                            stats[i+10].insert(0, "0")
                        if stats[i+11].text == "":
                            stats[i+11].insert(0, "0")
                        if stats[i+13].text == "":
                            stats[i+13].insert(0, "0")
                        if stats[i+16].text == "":
                            stats[i+16].insert(0, "0")
                        if stats[i+17].text == "":
                            stats[i+17].insert(0, "0")
                        if stats[i+18].text == "":
                            stats[i+18].insert(0, "0")
                        if stats[i+19].text == "":
                            stats[i+19].insert(0, "0")
                        if stats[i+20].text == "":
                            stats[i+20].insert(0, "0")
                        if stats[i+21].text == "":
                            stats[i+21].insert(0, "0")
                        str = stats[i].text
                        str = str.replace("*", "")
                        self.defends.append(defend(str, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+6].text, stats[i+10].text, stats[i+11].text, stats[i+13].text, stats[i+16].text, stats[i+17].text, stats[i+18].text, stats[i+19].text, stats[i+20].text, stats[i+21].text))
                    print("defense update done")
                    time.sleep(43200)
                except Exception:
                    print("Excpetion in def_stats")
                    pass

from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread

"""
get_def_stats is a thread that scrapes pro-football-reference for defensive stats once every 12 hours. This thread takes longer to execute
than the other stat scrapes, and this is why it is separate.
"""
global nfc_p_rows
class get_def_stats(Thread):

    def __init__(self):
        self.nfc_p_rows = None
        Thread.__init__(self)

    def run(self):
            while(True):
                try:

                    request = requests.get("https://www.pro-football-reference.com/years/2020/index.htm")
                    nfc_p_soup = BeautifulSoup(request.content, 'html.parser')
                    nfc_p_table_div = nfc_p_soup.find("div", id="div_nfc_playoff_standings")
                    table = df_table_div.find("tbody")
                    self.nfc_p_rows = table.find_all("tr", attrs={"class": None})
                    print("defense update done")
                    time.sleep(43200)
                except Exception:
                    print("Excpetion in def_stats")
                    pass

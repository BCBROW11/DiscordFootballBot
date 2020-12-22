from bs4 import BeautifulSoup
import requests
import time


"""
get_def_stats is a thread that scrapes pro-football-reference for defensive stats once every 12 hours. This thread takes longer to execute
than the other stat scrapes, and this is why it is separate.
"""
def get_def_stats():
    while(True):
        request = requests.get("https://www.pro-football-reference.com/years/2020/defense.htm")
        df_soup = BeautifulSoup(request.content, 'html.parser')
        df_table_div = df_soup.find("div", id="div_defense")
        table = df_table_div.find("tbody")
        df_rows = table.find_all("tr", attrs={"class": None})
        print("defense update done")
        time.sleep(43200)

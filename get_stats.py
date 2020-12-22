from bs4 import BeautifulSoup
import requests
import time

"""
get_stats is a thread that scrapes pro-football-reference for stats once every 12 hours
"""
def get_stats():
    while(True):
        request = requests.get("https://www.pro-football-reference.com/years/2020/passing.htm")
        qb_soup = BeautifulSoup(request.content, 'html.parser')
        qb_table_div = qb_soup.find("div", id="div_passing")
        table = qb_table_div.find("tbody")
        global qb_rows
        qb_rows = table.find_all("tr", attrs={"class": None})
        print("quarterbacks update done")
        request = requests.get("https://www.pro-football-reference.com/years/2020/rushing.htm")
        rb_soup = BeautifulSoup(request.content, 'html.parser')
        rb_table_div = rb_soup.find("div", id="div_rushing")
        table = rb_table_div.find("tbody")
        global rb_rows
        rb_rows = table.find_all("tr", attrs={"class": None})
        print("runningbacks update done")
        request = requests.get("https://www.pro-football-reference.com/years/2020/receiving.htm")
        wr_soup = BeautifulSoup(request.content, 'html.parser')
        wr_table_div = wr_soup.find("div", id="div_receiving")
        table = wr_table_div.find("tbody")
        global wr_rows
        wr_rows = table.find_all("tr", attrs={"class": None})
        print("receivers update done")
        request = requests.get("https://www.pro-football-reference.com/years/2020/opp.htm")
        team_def_soup = BeautifulSoup(request.content, 'html.parser')
        team_def_table_div = team_def_soup.find("div", id="div_team_stats")
        table = team_def_table_div.find("tbody")
        global team_def_rows
        team_def_rows = table.find_all("tr", attrs={"class": None})
        print("team defense update done")
        time.sleep(43200)

from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread

"""
get_standings is a thread that scrapes pro-football-reference for standings once every 12 hours
"""
global standingsSoup
class get_standings(Thread):
    def __init__(self):
        self.standingsSoup = None
        Thread.__init__(self)
    def run(self):
        while(True):
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            request = requests.get("https://www.pro-football-reference.com/years/2020/", headers = headers)
            self.standingsSoup = BeautifulSoup(request.content, 'html.parser')
            print("standings update done")
            time.sleep(43200)

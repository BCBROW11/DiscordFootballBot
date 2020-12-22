from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread

"""
get_scores is a thread that queries the scorestrip every 15 seconds to provide live scores
"""
global scoreRequest
class get_scores(Thread):
    def __init__(self):
        self.scoreRequest = None
        Thread.__init__(self)
    def run(self):
        try:
            while(True):
                self.scoreRequest = requests.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
                time.sleep(15)
        except Exception:
            print("Excpetion in get_scores: \n" + exception)

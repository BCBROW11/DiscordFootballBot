from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread
import json

"""
get_scores is a thread that queries the scorestrip every 15 seconds to provide live scores
"""
global json_score
class get_scores(Thread):
    def __init__(self):
        self.json_score = None
        Thread.__init__(self)
    def run(self):
            while(True):
                try:
                    scoreRequest = requests.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
                    str = scoreRequest.text
                    str = str.replace(",,", ",\"\",")
                    str = str.replace(",,", ",\"\",")
                    self.json_score = json.loads(str)
                    time.sleep(15)
                except Exception:
                    print("Excpetion in get_scores: \n" + exception)
                    pass

from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
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
                    self.json_score = None
                    session = requests.Session()
                    retry = Retry(connect=3, backoff_factor=0.5)
                    adapter = HTTPAdapter(max_retries=retry)
                    session.mount('http://', adapter)
                    session.mount('https://', adapter)

                    scoreRequest = session.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
                    str = scoreRequest.text
                    str = str.replace(",,", ",\"\",")
                    str = str.replace(",,", ",\"\",")
                    self.json_score = json.loads(str)
                    time.sleep(15)
                except Exception:
                    print("Excpetion in get_scores: \n" + exception)
                    pass

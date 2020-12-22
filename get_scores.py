from bs4 import BeautifulSoup
import requests
import time

"""
get_scores is a thread that queries the scorestrip every 15 seconds to provide live scores
"""
def get_scores():
    while(True):
        global scoreRequest
        scoreRequest = requests.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
        time.sleep(15)

from bs4 import BeautifulSoup
import requests
import time
import threading
from threading import Thread

"""
get_standings is a thread that scrapes pro-football-reference for standings once every 12 hours
"""
global js
class get_standings(Thread):
    def __init__(self):
        self.js = None
        Thread.__init__(self)
    def run(self):
        try:
            while(True):
                headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
                request = requests.get("https://www.pro-football-reference.com/years/2020/", headers = headers)
                standingsSoup = BeautifulSoup(request.content, 'html.parser')
                self.js = {}
                afce = "AFC East"
                afcw = "AFC West"
                afcn = "AFC North"
                afcs = "AFC South"
                nfce = "NFC East"
                nfcw = "NFC West"
                nfcn = "NFC North"
                nfcs = "NFC South"
                self.js[afce] = []
                self.js[afcw] = []
                self.js[afcn] = []
                self.js[afcs] = []
                self.js[nfce] = []
                self.js[nfcw] = []
                self.js[nfcn] = []
                self.js[nfcs] = []
                for s in standingsSoup.find_all('tr'):
                    tn = s.find(attrs={'data-stat': 'team'})
                    w = s.find(attrs={'data-stat': 'wins'})
                    l = s.find(attrs={'data-stat': 'losses'})
                    t = s.find(attrs={'data-stat': 'ties'})
                    #AFC Teams
                    if tn != None and (tn.text == "Buffalo Bills" or tn.text == "Miami Dolphins" or tn.text == "New England Patriots" or tn.text == "New York Jets"):
                        self.js[afce].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
                    if tn != None and (tn.text == "Pittsburgh Steelers" or tn.text == "Cleveland Browns" or tn.text == "Baltimore Ravens" or tn.text == "Cincinnati Bengals"):
                        self.js[afcn].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
                    if tn != None and (tn.text == "Indianapolis Colts" or tn.text == "Tennessee Titans" or tn.text == "Houston Texans" or tn.text == "Jacksonville Jaguars"):
                        self.js[afcs].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
                    if tn != None and (tn.text == "Kansas City Chiefs" or tn.text == "Las Vegas Raiders" or tn.text == "Denver Broncos" or tn.text == "Los Angeles Chargers"):
                        self.js[afcw].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
                    #NFC Teams
                    if tn != None and (tn.text == "Washington Football Team" or tn.text == "Dallas Cowboys" or tn.text == "New York Giants" or tn.text == "Philadelphia Eagles"):
                        self.js[nfce].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
                    if tn != None and (tn.text == "Green Bay Packers" or tn.text == "Minnesota Vikings" or tn.text == "Detroit Lions" or tn.text == "Chicago Bears"):
                        self.js[nfcn].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
                    if tn != None and (tn.text == "Tampa Bay Buccaneers" or tn.text == "New Orleans Saints" or tn.text == "Atlanta Falcons" or tn.text == "Carolina Panthers"):
                        self.js[nfcs].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
                    if tn != None and (tn.text == "San Francisco 49ers" or tn.text == "Arizona Cardinals" or tn.text == "Seattle Seahawks" or tn.text == "Los Angeles Rams"):
                        self.js[nfcw].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
                print("standings updated")
                time.sleep(43200)
        except Exception:
            print("Excpetion in get_standings: \n" + exception)

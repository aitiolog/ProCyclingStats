# -*- coding: utf-8 -*-
"""
ProCyclingStats - download the race startlist

Author: Klemen Ziberna
"""

#####################################
# GLOBAL VARIABLES

URL_STARTLIST = 'http://www.procyclingstats.com/race.php?id=171047&c=3&code=race-startlist'

#####################################
# LIBRARIES
    
from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

#####################################
# MAIN PROGRAM

# Load webpage
url_startlist = URL_STARTLIST

startlist_page = requests.get(url_startlist)
startlist_bs = bs(startlist_page.content, 'html.parser')

# Obtain list of riders
startlist_riders = []

startlist_riders_find = startlist_bs.findAll("a", { "class" : "rider blue " })


for index in range(0,len(startlist_riders_find)):
    startlist_riders.append({'Name': startlist_riders_find[index].text,
                             'Rider_Url': startlist_riders_find[index]['href']})
    

# -*- coding: utf-8 -*-
"""
ProCyclingStats - download rider statistics

Author: Klemen Ziberna
"""

# Libraries

from bs4 import BeautifulSoup as bs
import requests
import re

# Load webpages

# Interesting pages per rider

url_overview = 'http://www.procyclingstats.com/rider/Christopher_Froome'
url_statistics = 'http://www.procyclingstats.com/rider/Christopher_Froome_Statistics'
url_running_pts_score = 'http://www.procyclingstats.com/rider.php?id=140869&c=3&code=riderstats-general-running-point-score'

#url = 'http://www.procyclingstats.com/rider/Christopher_Froome'
url = 'http://www.procyclingstats.com/rider/Primoz_Roglic'



rider_main_page = requests.get(url)
rider_main_page_soup = bs(rider_main_page.content, 'html.parser')

#print(rider_main_page_soup.prettify())

# Extract rider information

#rider_overview_id

rider_overview_DOB
rider_overview_Nationality

# Rider weight
Weight_find = rider_main_page_soup.find_all(string=re.compile('Weight'))
rider_overview_Weight = \
    str(Weight_find[0].parent.next_sibling.string)
rider_overview_Weight = float(rider_overview_Weight.split('kg', 1)[0])


rider_overview_Height



rider_overview_Team2017

# Points by speciality - One day races
OneDayRaces_find = rider_main_page_soup.find_all(string=re.compile('One day races'))
rider_overview_OneDayRaces = int(OneDayRaces_find[0].parent.previous_sibling.string)

# Points by speciality - GC
GC_find = rider_main_page_soup.find_all(string=re.compile('GC'))
rider_overview_GC = int(GC_find[0].parent.previous_sibling.string)

# Points by speciality - Time trial
TimeTrial_find = rider_main_page_soup.find_all(string=re.compile('Time trial'))
rider_overview_TimeTrial = int(TimeTrial_find[0].parent.previous_sibling.string)

# Points by speciality - Sprint
Sprint_find = rider_main_page_soup.find_all(string=re.compile('Sprint'))
rider_overview_Sprint = int(Sprint_find[0].parent.previous_sibling.string)

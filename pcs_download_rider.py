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

# Rider date of birth (DOB)
DOB_find = rider_main_page_soup.findAll(string=re.compile('Date of birth'))
rider_overview_DOB = \
    DOB_find[0].parent.next_sibling.string \
    + DOB_find[0].parent.next_sibling.next_sibling.string + ' ' \
    + DOB_find[0].parent.next_sibling.next_sibling.next_sibling.string


# Rider nationality
Nationality_find = rider_main_page_soup.findAll(string=re.compile('Nationality'))
rider_overview_Nationality = \
    str(Nationality_find[0].parent.next_sibling.next_sibling.next_sibling.string)

# Rider weight
Weight_find = rider_main_page_soup.find_all(string=re.compile('Weight'))
rider_overview_Weight = \
    str(Weight_find[0].parent.next_sibling.string)
rider_overview_Weight = float(rider_overview_Weight.split('kg', 1)[0])

# Rider height
Height_find = rider_main_page_soup.find_all(string=re.compile('Height'))
rider_overview_Height = \
    str(Height_find[0].parent.next_sibling.string)
rider_overview_Height = float(rider_overview_Height.split('m', 1)[0])

# Rider team
Year_find = rider_main_page_soup.findAll(string=re.compile('2017'))
rider_overview_Team2017 = \
    str(Year_find[0].parent.next_sibling.next_sibling.string)

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



#############################
# Create rider dictionary
rider = {}
rider['DOB'] = rider_overview_DOB
rider['Nationality'] = rider_overview_Nationality
rider['Weight'] = rider_overview_Weight
rider['Height'] = rider_overview_Height
rider['Team2017'] = rider_overview_Team2017
rider['Overview_OneDayRaces'] = rider_overview_OneDayRaces
rider['Overview_GC'] = rider_overview_GC
rider['Overview_TimeTrial'] = rider_overview_TimeTrial
rider['Overview_Sprint'] = rider_overview_Sprint


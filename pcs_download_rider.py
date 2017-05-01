# -*- coding: utf-8 -*-
"""
ProCyclingStats - download rider statistics

Author: Klemen Ziberna
"""

#####################################
# LIBRARIES
    
from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd



#####################################
# FUNCTIONS

def pcs_rider_data(FirstName, LastName):
    "Returns a dictionary of the data obtained from the PCS pages"
    
    # Libraries
    
    from bs4 import BeautifulSoup as bs
    import requests
    import re
    
    # Load webpages
    
    # Interesting pages per rider
    #url_overview = 'http://www.procyclingstats.com/rider/Christopher_Froome'
    #url_statistics = 'http://www.procyclingstats.com/rider/Christopher_Froome_Statistics'
    #url_running_pts_score = 'http://www.procyclingstats.com/rider.php?id=140869&c=3&code=riderstats-general-running-point-score'
    
    base_url = 'http://www.procyclingstats.com/'
    url_overview = base_url + 'rider/' + FirstName + '_' + LastName
    url_statistics = base_url + 'rider/' + FirstName + '_' + LastName + '_Statistics'
    
    
    rider_main_page = requests.get(url_overview)
    rider_main_bs = bs(rider_main_page.content, 'html.parser')
    
    rider_statistics_page = requests.get(url_statistics)
    rider_statistics_bs = bs(rider_statistics_page.content, 'html.parser')
    
    #print(rider_main_bs.prettify())
    
    # Extract rider information
    
    rider = {}
    
    # Rider name
    rider['FirstName'] = FirstName
    rider['LastName'] = LastName
    
    # Rider date of birth (DOB)
    DOB_find = rider_main_bs.findAll(string=re.compile('Date of birth'))
    DOB_string = \
        DOB_find[0].parent.next_sibling.string \
        + DOB_find[0].parent.next_sibling.next_sibling.string \
        + DOB_find[0].parent.next_sibling.next_sibling.next_sibling.string
    
    DOB_string_split = DOB_string.split(' (')
    
    rider['DOB'] = DOB_string_split[0].lstrip()
    rider['Age'] = DOB_string_split[1][:-1]
    
    # Rider nationality
    Nationality_find = rider_main_bs.findAll(string=re.compile('Nationality'))
    rider['Nationality'] = \
        str(Nationality_find[0].parent.next_sibling.next_sibling.next_sibling.string)
    
    # Rider weight
    Weight_find = rider_main_bs.find_all(string=re.compile('Weight'))
    rider_overview_Weight = \
        str(Weight_find[0].parent.next_sibling.string)
    rider['Weight'] = float(rider_overview_Weight.split('kg', 1)[0])
    
    # Rider height
    Height_find = rider_main_bs.find_all(string=re.compile('Height'))
    rider_overview_Height = \
        str(Height_find[0].parent.next_sibling.string)
    rider['Height'] = float(rider_overview_Height.split('m', 1)[0])
    
    # Rider team
    Year_find = rider_main_bs.findAll(string=re.compile('2017'))
    rider['Team2017'] = \
        str(Year_find[0].parent.next_sibling.next_sibling.string)
    
    # Points by speciality - One day races
    OneDayRaces_find = rider_main_bs.find_all(string=re.compile('One day races'))
    rider['Overview_OneDayRaces'] = int(OneDayRaces_find[0].parent.previous_sibling.string)
    
    # Points by speciality - GC
    GC_find = rider_main_bs.find_all(string=re.compile('GC'))
    rider['Overview_GC'] = int(GC_find[0].parent.previous_sibling.string)
    
    # Points by speciality - Time trial
    TimeTrial_find = rider_main_bs.find_all(string=re.compile('Time trial'))
    rider['Overview_TimeTrial'] = int(TimeTrial_find[0].parent.previous_sibling.string)
    
    # Points by speciality - Sprint
    Sprint_find = rider_main_bs.find_all(string=re.compile('Sprint'))
    rider['Overview_Sprint'] = int(Sprint_find[0].parent.previous_sibling.string)
    
    
    
    #############################
    # Rider statistics page
    rider_statistics = {}
    
    statistics_table = rider_statistics_bs.find('table')
    rows = statistics_table.findAll('tr')
    
    for row in rows[1:]:
        cols = row.findAll('td')
        rider_statistics[cols[0].string + ' - Position'] = int(cols[1].string)
        rider_statistics[cols[0].string + ' - Value'] = int(cols[2].string)
    
        
    #############################
    # Rider running point score for the last 12 months
    rider_running_pts = {}
    
    # Find running points link
    Running_pts_find = \
        rider_statistics_bs.find(string=re.compile('Running point score'))
    running_pts_url = base_url + str(Running_pts_find.parent['href'])
    
    # Load page
    rider_running_pts_page = requests.get(running_pts_url)
    rider_running_pts_bs = bs(rider_running_pts_page.content, 'html.parser')
    
    # Obtain values
    
    running_pts_table = rider_running_pts_bs.find('table')
    rows = running_pts_table.findAll('tr')
    
    for row in rows[1:13]: #only for last 12 months
        cols = row.findAll('td')
        rider_running_pts['Running point score - ' + cols[0].string] = \
            int(cols[1].string)
    
    
    #############################
    # Merge dictionaries (without changing the original dictionaries)
    merged_rider = dict(rider)
    merged_rider.update(rider_statistics)
    merged_rider.update(rider_running_pts)
    
    #RETURN
    return merged_rider
    

    

###############
# MAIN PROGRAM

Froome_data = pcs_rider_data('Christopher', 'Froome')
Roglic_data = pcs_rider_data('Primoz', 'Roglic')
Yates_data = pcs_rider_data('Simon', 'Yates')

All_riders_list = [Froome_data, Roglic_data, Yates_data]

# Convert list of dictionaries to pandas dataframe
All_riders_df = pd.DataFrame(All_riders_list)


































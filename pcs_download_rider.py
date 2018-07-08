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
from unidecode import unidecode

from pcs_startlist import pcs_startlist_all_riders

#####################################
# FUNCTIONS

def pcs_rider_data(url_rider_id):
    "Returns a dictionary of the data obtained from the PCS pages"
    
    # Libraries
    
    from bs4 import BeautifulSoup as bs
    import requests
    import re
    
    # Load webpages
    
    # Interesting pages per rider
    url_overview = 'https://www.procyclingstats.com/rider/christopher-froome/'
    url_statistics = 'https://www.procyclingstats.com/rider/christopher-froome/statistics/overview'
    #url_running_pts_score = 'http://www.procyclingstats.com/rider.php?id=140869&c=3&code=riderstats-general-running-point-score'
    #url_rider_id = 'rider.php?id=140869'
    
    base_url = 'http://www.procyclingstats.com/'
    
    #url_overview = base_url + 'rider/' + FirstName + '_' + LastName
    #url_statistics = base_url + 'rider/' + FirstName + '_' + LastName + '_Statistics'
    
    url_overview = base_url + url_rider_id
    url_statistics = base_url + url_rider_id + '/statistics/overview'
    
    rider_main_page = requests.get(url_overview)
    rider_main_bs = \
        bs(rider_main_page.content.decode('utf-8', 'ignore'), 'html.parser')
        
    rider_statistics_page = requests.get(url_statistics)
    rider_statistics_bs = \
        bs(rider_statistics_page.content.decode('utf-8', 'ignore'), 'html.parser')
    
    #print(rider_main_bs.prettify())
    
    # Extract rider information
    
    rider = {}
    
    # Rider name
    #rider['FirstName'] = FirstName
    #rider['LastName'] = LastName
    riderName_find = rider_main_bs.findAll('h1')
    rider['Name'] = riderName_find[0].text.split('»',1)[0]
    rider['Name'] = ' '.join(rider['Name'].split())
    try:
        rider['Name_ASCII'] = unidecode(rider['Name'])
    except:
        rider['Name_ASCII'] = 'Unidecode error'
        
    # Rider PCS link
    rider['PCS_link'] = url_overview
    
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
    try:
        rider_overview_Weight = \
            str(Weight_find[0].parent.next_sibling.string)
        rider['Weight'] = float(rider_overview_Weight.split('kg', 1)[0])
    except IndexError:
        rider['Weight'] = 'NaN'
        
    
    # Rider height
    Height_find = rider_main_bs.find_all(string=re.compile('Height'))
    try:
        rider_overview_Height = \
            str(Height_find[0].parent.next_sibling.string)
        rider['Height'] = float(rider_overview_Height.split('m', 1)[0])
    except IndexError:
        rider['Height'] = 'NaN'
    
    # Rider team
    Year_find = rider_main_bs.findAll(string=re.compile('2018'))
    try:
        rider['Team2018'] = \
            str(Year_find[0].parent.next_sibling.next_sibling.string)
    except:
        rider['Team2018'] = 'Error'
    
    # Points by speciality - One day races
    OneDayRaces_find = rider_main_bs.find_all(string=re.compile('One day races'))
    rider['Overview_OneDayRaces'] = \
            int(OneDayRaces_find[0].parent.parent.previous_sibling.string)
    
    # Points by speciality - GC
    GC_find = rider_main_bs.find_all(string=re.compile('GC'))
    rider['Overview_GC'] = \
            int(GC_find[0].parent.parent.previous_sibling.string)
    
    # Points by speciality - Time trial
    TimeTrial_find = rider_main_bs.find_all(string=re.compile('Time trial'))
    rider['Overview_TimeTrial'] = \
            int(TimeTrial_find[0].parent.parent.previous_sibling.string)
    
    # Points by speciality - Sprint
    Sprint_find = rider_main_bs.find_all(string=re.compile('Sprint'))
    rider['Overview_Sprint'] = \
            int(Sprint_find[0].parent.parent.previous_sibling.string)
    
    
    
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
    
# Reorder dataframe columns
def set_column_sequence(dataframe, seq, front=True):
    '''Takes a dataframe and a subsequence of its columns,
       returns dataframe with seq as first columns if "front" is True,
       and seq as last columns if "front" is False.
    '''
    cols = seq[:] # copy so we don't mutate seq
    for x in dataframe.columns:
        if x not in cols:
            if front: #we want "seq" to be in the front
                #so append current column to the end of the list
                cols.append(x)
            else:
                #we want "seq" to be last, so insert this
                #column in the front of the new column list
                #"cols" we are building:
                cols.insert(0, x)
    return dataframe[cols]
    

###############
# MAIN PROGRAM

# Obtain list of riders from startlist
#Tour2017_startlist_url = 'http://www.procyclingstats.com/race.php?id=171088&c=3&code=race-startlist'
#Tour2017_startlist_riders = pcs_startlist_all_riders(Tour2017_startlist_url)


Tour2018_startlist_url = 'https://www.procyclingstats.com/race/tour-de-france/2018/startlist'
Tour2018_startlist_riders = pcs_startlist_all_riders(Tour2018_startlist_url)


# Obtain riders data
input_startlist_riders = Tour2018_startlist_riders

All_riders_list = []
counter = 1

for item in input_startlist_riders:
    print('Downloading data for: '+ item['Name'] + ' ('
          + str(counter) + '/' + str(len(input_startlist_riders)) + ')')
    rider_data = pcs_rider_data(item['Rider_Url'])
    All_riders_list.append(rider_data)
    counter = counter + 1
    

# Convert list of dictionaries to pandas dataframe
All_riders_df = pd.DataFrame(All_riders_list)


# Reorder the dataframe - those columns first
col_order = ['Name',
             'Name_ASCII',
             'Team2018',
             'Age',
             'Nationality',
             'DOB',
             'Height',
             'Weight',
             'PCS_link'
             ]

ordered_All_riders_df = \
    set_column_sequence(All_riders_df, col_order, front=True)


# Save the dataframe to csv file
print('Saving the output table...')
ordered_All_riders_df.to_csv('All_Riders.csv')




























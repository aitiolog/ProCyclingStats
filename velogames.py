# -*- coding: utf-8 -*-
"""
Velogames - rider selection algorithm

Author: Klemen Ziberna
"""

#####################################
# GLOBAL VARIABLES

FILE_PATH = "insert_path"
HTML_FILE = "Velogames Fantasy Cycling _ Fantasy Giro d Italia 2017.html"



#####################################
# LIBRARIES

from bs4 import BeautifulSoup as bs
import pandas as pd
import os

#####################################
# FUNCTIONS

def get_riders_list(bs_html, name_string):
    """
    Function return a list of dictionaries containing Name and Cost for every
    rider in the Velogames dropdown menu.
    
    Inputs:
    bs_html
    name_string = rider1, rider2, ... , rider9
    """
    
    riders_output = []

    rider_list_find = bs_html.find("select", {"name": name_string})
    rider_list_string = rider_list_find.getText(separator=", ")
    rider_list = rider_list_string.split(',')
    rider_list = rider_list[1:-2] #remove non-rider elements
    
    
    for index in range(0,len(rider_list)):
        rider_name = rider_list[index].split('|')[0].strip()
        rider_cost = int(rider_list[index].split('|')[1])
        riders_output.append({'Name':rider_name,
                              'Cost': rider_cost})
        
    return riders_output
        
    
    
    
#####################################
# MAIN PROGRAM
    
# Open the file
full_path = os.path.join(FILE_PATH, HTML_FILE)
opened_file = open(full_path, encoding='utf-8')
velogames_bs = bs(opened_file, 'html.parser')

# Create a list of riders per selection

rider1_list = get_riders_list(velogames_bs, 'rider1')
rider2_list = get_riders_list(velogames_bs, 'rider2')
rider3_list = get_riders_list(velogames_bs, 'rider3')
rider4_list = get_riders_list(velogames_bs, 'rider4')
rider5_list = get_riders_list(velogames_bs, 'rider5')
rider6_list = get_riders_list(velogames_bs, 'rider6')
rider7_list = get_riders_list(velogames_bs, 'rider7')
rider8_list = get_riders_list(velogames_bs, 'rider8')
rider9_list = get_riders_list(velogames_bs, 'rider9')


# Save the lists in the multiple csv files

rider1_df = pd.DataFrame(rider1_list)
rider2_df = pd.DataFrame(rider2_list)
rider3_df = pd.DataFrame(rider3_list)
rider4_df = pd.DataFrame(rider4_list)
rider5_df = pd.DataFrame(rider5_list)
rider6_df = pd.DataFrame(rider6_list)
rider7_df = pd.DataFrame(rider7_list)
rider8_df = pd.DataFrame(rider8_list)
rider9_df = pd.DataFrame(rider9_list)

rider1_df.to_csv('rider1.csv')
rider2_df.to_csv('rider2.csv')
rider3_df.to_csv('rider3.csv')
rider4_df.to_csv('rider4.csv')
rider5_df.to_csv('rider5.csv')
rider6_df.to_csv('rider6.csv')
rider7_df.to_csv('rider7.csv')
rider8_df.to_csv('rider8.csv')
rider9_df.to_csv('rider9.csv')








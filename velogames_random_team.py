# -*- coding: utf-8 -*-
"""
Velogames - random team generator

Author: Klemen Ziberna
"""

#####################################
# GLOBAL VARIABLES

FILE_PATH = "C:\klemen\Repositories\ProCyclingStats\Analysis_Tables\Riders_Points"
CSV_FILES = ["rider1.csv",
             "rider2.csv",
             "rider3.csv",
             "rider4.csv",
             "rider5.csv",
             "rider6.csv",
             "rider7.csv",
             "rider8.csv",
             "rider9.csv"
             ]

#####################################
# LIBRARIES

import pandas as pd
import os
import chardet
from random import randint
import time

#####################################
# FUNCTIONS

def open_csv_chardet(input_csv_file):
    """
    Function opens the csv file, detects correct encoding, then open
    the same file as pandas df with correct encoding
    """
    with open(input_csv_file, 'rb') as f:
        result = chardet.detect(f.read())  # or readline if the file is large
        
    csv_df = pd.read_csv(input_csv_file, encoding=result['encoding'])
    
    return csv_df

    
def max_category_cost(rider_df, sel_column_name):
    """
    Functions returns dataframe with entries with maxium values per 
    sel_column_name per 'Cost' group
    """

    rider_df_sorted = \
        rider_df.sort_values(by=['Cost', sel_column_name], ascending=False)
    max_sel_category_df = \
        rider_df_sorted.groupby(by='Cost', as_index=False, sort=False).first()
    return max_sel_category_df
    

#####################################
# MAIN PROGRAM


# Open the files
rider1_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[0]))
rider2_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[1]))
rider3_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[2]))
rider4_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[3]))
rider5_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[4]))
rider6_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[5]))
rider7_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[6]))
rider8_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[7]))
rider9_df = open_csv_chardet(os.path.join(FILE_PATH, CSV_FILES[8]))


# Combine all dataframes in a list
riders_list = [rider1_df,
               rider2_df,
               rider3_df,
               rider4_df,
               rider5_df,
               rider6_df,
               rider7_df,
               rider8_df,
               rider9_df,
               ]

# Random rider selection

max_cost = 100


# Step 1: Randomly select first 8 riders with the right cost sum range
counter = 0
print('Finding first 8 riders...')
while True:
    print('Iteration number: ' + str(counter))
    random_number = []
    for i in range(0,9):
        random_number.append(randint(0, len(riders_list[i])-1))
    
    random_riders = []
    for j in range(0,8):
        random_riders.append({'Name': riders_list[j]['Name'][random_number[j]],
                              'Cost': riders_list[j]['Cost'][random_number[j]]})
        
    cost = 0
    for k in range(0,len(random_riders)):
        cost = cost + int(random_riders[k]['Cost'])
    
    if cost <= max_cost-4 and cost >= max_cost-18:
        random_selection_part = random_riders
        break
    
    counter = counter + 1
    
# Step 2: From the right remaining riders(cost sum to be 100) randomly select

print('Finding last rider...')

cost_needed = max_cost - cost
find_riders_cost_df = \
    riders_list[8][riders_list[8]['Cost'] == cost_needed].reset_index()
random_number_last = randint(0, len(find_riders_cost_df)-1)
random_riders.append({'Name': find_riders_cost_df['Name'][random_number_last],
                      'Cost': find_riders_cost_df['Cost'][random_number_last]})

# Print the selection
rider_n = 1
print('---------------------------------')
print('Team of randomly selected riders:')
for item in random_riders:
    print(str(rider_n) + '. ' + item['Name'] + ' - ' + str(item['Cost']))
    rider_n = rider_n + 1



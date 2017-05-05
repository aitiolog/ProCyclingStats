# -*- coding: utf-8 -*-
"""
Velogames - test algorithms - v2

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



# Selection algorithm

# Conditions
sel_category = 'PCS Ranking - Individual - Value'
#sel_category = 'PCS Season - Individual - Value'
#sel_category = 'Form_2month'

max_cost = 100 # max cost
best_combination = {'Value':0,
                    'Combination': "",
                    'Cost': 0} 

                    
                    
                    
# Get dataframe with only riders with max value of the selected category
# grouped by 'Cost'

rider1_best_df = max_category_cost(rider1_df, sel_category)
rider2_best_df = max_category_cost(rider2_df, sel_category)
rider3_best_df = max_category_cost(rider3_df, sel_category)
rider4_best_df = max_category_cost(rider4_df, sel_category)
rider5_best_df = max_category_cost(rider5_df, sel_category)
rider6_best_df = max_category_cost(rider6_df, sel_category)
rider7_best_df = max_category_cost(rider7_df, sel_category)
rider8_best_df = max_category_cost(rider8_df, sel_category)
rider9_best_df = max_category_cost(rider9_df, sel_category)


# Option: dirty way to disable levels (reduce them to one element with lowest
# cost)

#rider5_best_df = rider5_best_df.tail(1).reset_index()
rider6_best_df = rider6_best_df.tail(1).reset_index()
rider7_best_df = rider7_best_df.tail(1).reset_index()
rider8_best_df = rider8_best_df.tail(1).reset_index()
#rider9_best_df = rider9_best_df.tail(1).reset_index()


# Selection algorithm
                    
# Main loop

total_timer_start = time.time() #timing the whole loop
timer_start = time.time() #timing process

for index1 in range(0,len(rider1_best_df)):
    
    #Timing
    #timer_end = time.time()
    #print('Elapsed time: ' + str(round(timer_end - timer_start, 2)) + 's')
    #timer_start = time.time()
    print('Rider1: ' + str(index1))
    current_cost = rider1_best_df['Cost'][index1]
    if current_cost > max_cost - 8*4:
        continue

    
    for index2 in range(0,len(rider2_best_df)):
        #Timing
        timer_end = time.time()
        print('Elapsed time: ' + str(round(timer_end - timer_start, 2)) + 's')
        timer_start = time.time()
        print('-Rider2: ' + str(index2))
        current_cost = rider1_best_df['Cost'][index1] \
                    + rider2_best_df['Cost'][index2]                       

        if current_cost > max_cost - 7*4:
            continue

        
        for index3 in range(0,len(rider3_best_df)):
            print('--Rider3: ' + str(index3))
            current_cost = rider1_best_df['Cost'][index1] \
                        + rider2_best_df['Cost'][index2] \
                        + rider3_best_df['Cost'][index3]
            
            if current_cost > max_cost - 6*4:
                continue
            
            
            for index4 in range(0,len(rider4_best_df)):
                #print('---Rider4: ' + str(index4))
                current_cost = rider1_best_df['Cost'][index1] \
                            + rider2_best_df['Cost'][index2] \
                            + rider3_best_df['Cost'][index3] \
                            + rider4_best_df['Cost'][index4] 
                
                if current_cost > max_cost - 5*4:
                    continue
                
                
                for index5 in range(0,len(rider5_best_df)):
                    #print('----Rider5: ' + str(index5))
                    current_cost = rider1_best_df['Cost'][index1] \
                                + rider2_best_df['Cost'][index2] \
                                + rider3_best_df['Cost'][index3] \
                                + rider4_best_df['Cost'][index4] \
                                + rider5_best_df['Cost'][index5] 
                    
                    if current_cost > max_cost - 4*4:
                        continue
                
                
                    for index6 in range(0,len(rider6_best_df)):
                        #print('-----Rider6: ' + str(index6))
                        current_cost = rider1_best_df['Cost'][index1] \
                                    + rider2_best_df['Cost'][index2] \
                                    + rider3_best_df['Cost'][index3] \
                                    + rider4_best_df['Cost'][index4] \
                                    + rider5_best_df['Cost'][index5] \
                                    + rider6_best_df['Cost'][index6] 
                        
                        if current_cost > max_cost - 3*4:
                            continue
                    
                        
                        for index7 in range(0,len(rider7_best_df)):
                            current_cost = rider1_best_df['Cost'][index1] \
                                        + rider2_best_df['Cost'][index2] \
                                        + rider3_best_df['Cost'][index3] \
                                        + rider4_best_df['Cost'][index4] \
                                        + rider5_best_df['Cost'][index5] \
                                        + rider6_best_df['Cost'][index6] \
                                        + rider7_best_df['Cost'][index7] 
                            
                            if current_cost > max_cost - 2*4:
                                continue
                            
                            
                            for index8 in range(0,len(rider8_best_df)):
                                current_cost = rider1_best_df['Cost'][index1] \
                                            + rider2_best_df['Cost'][index2] \
                                            + rider3_best_df['Cost'][index3] \
                                            + rider4_best_df['Cost'][index4] \
                                            + rider5_best_df['Cost'][index5] \
                                            + rider6_best_df['Cost'][index6] \
                                            + rider7_best_df['Cost'][index7] \
                                            + rider8_best_df['Cost'][index8] 
                                
                                if current_cost > max_cost - 1*4:
                                    continue
                                
                                
                                for index9 in range(0,len(rider9_best_df)):
                                    current_cost = rider1_best_df['Cost'][index1] \
                                                + rider2_best_df['Cost'][index2] \
                                                + rider3_best_df['Cost'][index3] \
                                                + rider4_best_df['Cost'][index4] \
                                                + rider5_best_df['Cost'][index5] \
                                                + rider6_best_df['Cost'][index6] \
                                                + rider7_best_df['Cost'][index7] \
                                                + rider8_best_df['Cost'][index8] \
                                                + rider9_best_df['Cost'][index9] 
                                    
                                    if current_cost > max_cost:
                                        continue
                                  
                                    selection_value = \
                                        rider1_best_df[sel_category][index1] \
                                        + rider2_best_df[sel_category][index2] \
                                        + rider3_best_df[sel_category][index3] \
                                        + rider4_best_df[sel_category][index4] \
                                        + rider5_best_df[sel_category][index5] \
                                        + rider6_best_df[sel_category][index6] \
                                        + rider7_best_df[sel_category][index7] \
                                        + rider8_best_df[sel_category][index8] \
                                        + rider9_best_df[sel_category][index9]
                                    
                                    if selection_value <= best_combination['Value']:
                                        continue
                                        
                                    else:
                                        best_combination['Value'] = float(selection_value)
                                        best_combination['Combination'] = [
                                            rider1_best_df['Name'][index1],
                                            rider2_best_df['Name'][index2],
                                            rider3_best_df['Name'][index3],
                                            rider4_best_df['Name'][index4],
                                            rider5_best_df['Name'][index5],
                                            rider6_best_df['Name'][index6],
                                            rider7_best_df['Name'][index7],
                                            rider8_best_df['Name'][index8],
                                            rider9_best_df['Name'][index9]
                                        ]
                                        best_combination['Cost'] = int(current_cost)
                                        
                                        #print('New best selection found:')
                                        #print(best_combination['Combination'])
                            
        


# End

#Timing
total_timer_end = time.time()
print('Total elapsed time: ' 
      + str(round(total_timer_end - total_timer_start, 2)) + 's')








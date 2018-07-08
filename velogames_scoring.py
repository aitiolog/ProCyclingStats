# -*- coding: utf-8 -*-
"""
Velogames Scoring System

Author: Klemen Ziberna
"""

#####################################
# GLOBAL VARIABLES

FILE_PATH = "C:\klemen\Repositories\ProCyclingStats\Results\Tour_2018"

TEAM_LIST = "Velogames_Tour2018_Teams.csv"

STAGE_NAME = "Stage_2"
STAGE_RESULT = "Tour2018_Results_Stage2.csv"

#####################################
# LIBRARIES

import pandas as pd
import os
import chardet

#####################################
# FUNCTIONS

def open_csv_chardet(input_csv_file):
    """
    Function opens the csv file, detects correct encoding, then open
    the same file as pandas df with correct encoding
    """
    with open(input_csv_file, 'rb') as f:
        result = chardet.detect(f.read())  # or readline if the file is large
        
    csv_df = pd.read_csv(input_csv_file, encoding=result['encoding'], \
                         skipinitialspace=True)
    
    return csv_df


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
    

    
#####################################
# MAIN PROGRAM

# NORMAL STAGE (non-time trial)

# Open the files

team_list_df = open_csv_chardet(os.path.join(FILE_PATH, TEAM_LIST))
result_stage_df = open_csv_chardet(os.path.join(FILE_PATH, STAGE_RESULT))

# Process results
results_df = result_stage_df
results_df.dropna(how="all", inplace=True) #remove empty lines
results_df.reset_index(drop=True, inplace=True) #reset index

# Replace team names (mismatch between Velogames and Cyclingnews)

Team_Name_Replacement = {
    'AG2R La Mondiale': 'AG2R La Mondiale',
    'Astana Pro Team': 'Astana Pro Team',
    'Bahrain-Merida': 'Bahrain Merida Pro Cycling Team',
    'BMC Racing Team': 'BMC Racing Team',
    'Bora-Hansgrohe': 'BORA - hansgrohe',
    'Cofidis, Solutions Credits': 'Cofidis Solutions Crédits',
    'Dimension Data': 'Dimension Data',
    'Direct Energie': 'Direct Energie',
    'EF Education First-Drapac p/b Cannondale': 'EF Education First-Drapac p/b Cannondale',
    'Fortuneo-Samsic': 'Fortuneo - Samsic',
    'Groupama-FDJ': 'Groupama - FDJ',
    'Lotto Soudal': 'Lotto Soudal',
    'Mitchelton-Scott': 'Mitchelton-Scott',
    'Movistar Team': 'Movistar Team',
    'Quick-Step Floors': 'Quick-Step Floors',
    'Katusha-Alpecin': 'Team Katusha - Alpecin',
    'LottoNl-Jumbo': 'Team LottoNL-Jumbo',
    'Team Sky': 'Team Sky',
    'Team Sunweb': 'Team Sunweb',
    'Trek-Segafredo': 'Trek - Segafredo',
    'UAE Team Emirates': 'UAE-Team Emirates',
    'Wanty-Groupe Gobert': 'Wanty - Groupe Gobert'
    }
    
results_df['Team'].replace(Team_Name_Replacement, inplace=True)


# Calculate the score

team_scores = team_list_df.to_dict('records')

#rider_idx = 76

# Main loop for every rider

print('Processing points for ' + STAGE_NAME + ':')

for rider_idx in range(0, len(team_scores)):
    
    print(str(rider_idx+1) + ". " + team_scores[rider_idx]['Team_Name']\
          + ": " + team_scores[rider_idx]['Rider'])
    
    ### 1. Individual points
    
    # Extract individual points part of the results (i.e. not team assist)
    individual_results_df = \
        results_df[results_df['Type'].str.contains('TeamAssist')==False]
    
    
    # Find presence of rider in the results
    rider_find_df = \
        individual_results_df[individual_results_df['Rider'] \
                   .str.contains(team_scores[rider_idx]['Rider'], na=False)]
    
    # Append scores to the dictionary
    extract_df = rider_find_df.loc[:, ['Type', 'Points']]
    extract_dict = extract_df.to_dict('records')
    
    for extract_idx in range(0, len(extract_dict)):    
        team_scores[rider_idx][extract_dict[extract_idx]['Type']] = \
                    extract_dict[extract_idx]['Points']
    
    # Calculate sum of individual points
    individual_sum = extract_df['Points'].sum()
    
    ### 2. Team assist points
    
    # Extract team assist part of the results
    team_results_df = results_df[results_df['Type'].str.contains('TeamAssist')]
    
    # Find presence of the team
    team_find_df = \
        team_results_df[team_results_df['Team'] \
                   .str.contains(team_scores[rider_idx]['Team'], na=False)]

   
    # Exclude points for himself
    team_find_df = team_find_df[team_find_df['Rider']. \
                       str.contains(team_scores[rider_idx]['Rider'], na=False) == False]
    
    # Sum the team assist points
    team_assist_sum = team_find_df['Points'].sum()
    
    # Sum the individual and team assist points
    total_points = individual_sum + team_assist_sum
    
    # Append score to the dictionary
    team_scores[rider_idx]['TeamAssist'] = team_assist_sum
    team_scores[rider_idx]['Stage_Total'] = total_points
    
    
#---------------------------------------
# EXPORT SCORES AND CALCULATE TEAM SCORES

# Convert list of dictionaries to pandas dataframe
team_scores_df = pd.DataFrame(team_scores)

# Reorder the dataframe - those columns first
col_order = ['DS',
             'Team_Name',
             'League',
             'Rider_Position',
             'Class',
             'Rider',
             'Team',
             'Cost',
             'Stage_Total'
             ]

ordered_team_scores_df = \
    set_column_sequence(team_scores_df, col_order, front=True)


# Calculate total points per team
team_sum_df = ordered_team_scores_df.groupby(['League', 'DS', 'Team_Name']).sum()
team_sum_df.sort_values(by='Stage_Total', inplace=True, ascending=False)

# Save the dataframe to csv file
print('Saving the output table...')

team_scores_outName = "Detailed_Points_" + STAGE_NAME + ".csv"
ordered_team_scores_df.to_csv(os.path.join(FILE_PATH, team_scores_outName))

team_sum_outName = "Team_Sum_" + STAGE_NAME + ".csv"
team_sum_df.to_csv(os.path.join(FILE_PATH, team_sum_outName))





                
                            

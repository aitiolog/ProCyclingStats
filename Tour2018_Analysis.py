# -*- coding: utf-8 -*-
"""
Velogames - download team points per stage

Author: Klemen Ziberna
"""


#####################################
# GLOBAL VARIABLES

FILE_PATH = "C:\klemen\Repositories\ProCyclingStats\Results\Tour_2018"
      
    
# Stages
Tour_N_stages = 21
Tour_last_stage = 2          

                  
#####################################
# LIBRARIES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import os
import chardet


#####################################
# FUNCTIONS

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


    
#####################################
# MAIN PROGRAM

# Replace DS names

DS_Name_Replacement = {
    "James Kelly": "James",
    "Simon Moore": "Simon",
    "Pip Nicolson": "Pip",
    "Parag Gajendragadkar": "Parag",
    "Klemen's Intelligent Bot 1": "Bot - PCS Overall",
    "Klemen's Intelligent Bot 2": "Bot - PCS Season",
    "Klemen's Intelligent Bot 3": "Bot - PCS 3 month form",
    "Klemen's Random Bot 1": "Random bot 1",
    "Klemen's Random Bot 2": "Random bot 2",
    "Klemen's Random Bot 3": "Random bot 3"
    }


# Open summary stage results

Tour_last_stage = 2

fileName_base = "Team_Sum_Stage_"

# Generate main tables

team_results_df = [] # League A
bot_results_df = [] # League B

# Main loop to load stage results

for stage_idx in range(0, Tour_last_stage):
    Stage_N = stage_idx + 1
    fileName = fileName_base + str(Stage_N) + ".csv"
    print("Opening: "+ fileName)

    stage_df = open_csv_chardet(os.path.join(FILE_PATH, fileName))
    stage_df['DS'].replace(DS_Name_Replacement, inplace=True)
    
    # Extract stage total score

    A_df = stage_df[stage_df['League'] == "A"]
    B_df = stage_df[stage_df['League'] == "B"]
    
    team_df = A_df.loc[:, ['DS', 'Stage_Total']]
    team_df.set_index('DS', inplace=True)

    bot_df = B_df.loc[:, ['DS', 'Stage_Total']]
    bot_df.set_index('DS', inplace=True)

    # Rename the column to the corresponding stage N
    Stage_N_string = "S" + str(Stage_N)
    team_df.rename(columns={'Stage_Total': Stage_N_string}, inplace=True)
    bot_df.rename(columns={'Stage_Total': Stage_N_string}, inplace=True)

    # Append the table to the main table (or generate a new one)
    
    if stage_idx == 0:
        team_results_df = team_df
        bot_results_df = bot_df
    
    else:
        team_results_df = pd.concat([team_results_df, team_df], axis=1)
        bot_results_df = pd.concat([bot_results_df, bot_df], axis=1)
    
# Create cum sum tables

team_cumsum_df = team_results_df.cumsum(axis=1)
bot_cumsum_df = bot_results_df.cumsum(axis=1)


# Order the tables

team_order = ['Andy',
              'James',
              'Parag',
              'Pedro',
              'Pip',
              'Simon',
              'Toby',
              'Klemen']

bot_order = ['Pip',
             'Bot - PCS Overall',
             'Bot - PCS Season',
             'Bot - PCS 3 month form',
             'Random bot 1',
             'Random bot 2',
             'Random bot 3']


ordered_team_cumsum_df = team_cumsum_df.reindex(team_order)
ordered_bot_cumsum_df = bot_cumsum_df.reindex(bot_order)


#------------------
# PLOTTING

# Transpose tables

team_cum_scores = ordered_team_cumsum_df.transpose()
bot_cum_scores = ordered_bot_cumsum_df.transpose()
                 
# Cumulative stage score plot

stage_labels = list(range(1, Tour_N_stages+1)) + ['End']

team_cum_scores[0:Tour_last_stage].plot(linestyle='-', marker='|', grid=1, \
                                   colormap='Accent')

plt.xlim(0,Tour_last_stage-1)
plt.xticks(list(range(0,Tour_last_stage)), stage_labels)
plt.title('Tour 2018: Cumulative scores')
plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', ncol=1, numpoints=1)
plt.ylabel('Points')
plt.xlabel('Stage')
plt.savefig('team_cum_scores.png', bbox_inches='tight')



bot_cum_scores[0:Tour_last_stage].plot(linestyle='-', marker='|', grid=1, \
                                   colormap='Accent')

plt.xlim(0,Tour_last_stage-1)
plt.xticks(list(range(0,Tour_last_stage)), stage_labels)
plt.title('Tour 2018: Cumulative scores')
plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', ncol=1, numpoints=1)
plt.ylabel('Points')
plt.xlabel('Stage')
plt.savefig('bot_cum_scores.png', bbox_inches='tight')





   
## Create outputs
#team_riders_df = pd.DataFrame(team_riders)
#team_riders_df = set_column_sequence(team_riders_df, col_order, front=True)
#
#result_list_df = pd.DataFrame(result_list)
#
#stage_scores = result_list_df['Stage_Score'].apply(pd.Series).transpose()
#stage_scores.columns = result_list_df['Name']
#stage_scores = set_column_sequence(stage_scores, col_order, front=True)
#
#cum_scores = result_list_df['Cumulative_Score'].apply(pd.Series).transpose()
#cum_scores.columns = result_list_df['Name']
#cum_scores = set_column_sequence(cum_scores, col_order, front=True)
#
#
#bot_result_list_df = pd.DataFrame(bot_result_list)
#
#bot_stage_scores = bot_result_list_df['Stage_Score'].apply(pd.Series).transpose()
#bot_stage_scores.columns = bot_result_list_df['Name']
#bot_stage_scores = set_column_sequence(bot_stage_scores, bot_col_order, front=True)
#
#bot_cum_scores = bot_result_list_df['Cumulative_Score'].apply(pd.Series).transpose()
#bot_cum_scores.columns = bot_result_list_df['Name']
#bot_cum_scores = set_column_sequence(bot_cum_scores, bot_col_order, front=True)
#
#
#
## Stage winners and overall leaders
#winners_df = pd.DataFrame()
#winners_df['Stage_N'] = list(range(1,Tour_N_stages+1))
#winners_df['Stage_Score_Winner'] = stage_scores.idxmax(axis=1)
#winners_df['Stage_Score_Winner_Pts'] = stage_scores.max(axis=1)
#winners_df['Overall_Score_Leader'] = cum_scores.idxmax(axis=1)
#winners_df['Stage_Score_Leader_Pts'] = cum_scores.max(axis=1)
#
#bot_winners_df = pd.DataFrame()
#bot_winners_df['Stage_N'] = list(range(1,Tour_N_stages+1))
#bot_winners_df['Stage_Score_Winner'] = bot_stage_scores.idxmax(axis=1)
#bot_winners_df['Stage_Score_Winner_Pts'] = bot_stage_scores.max(axis=1)
#bot_winners_df['Overall_Score_Leader'] = bot_cum_scores.idxmax(axis=1)
#bot_winners_df['Stage_Score_Leader_Pts'] = bot_cum_scores.max(axis=1)
#
## Save to csv file
#team_riders_df.to_csv('team_riders.csv')
#stage_scores.to_csv('stage_scores.csv')
#cum_scores.to_csv('cum_scores.csv')
#winners_df.to_csv('winners.csv')


# Plot figures

# My colors
# Quick gradient example along the Red/Green dimensions
#my_colors = [(x/10.0, x/20.0, 0.75) for x in range(len(Teams_dict_url))]
#my_bot_colors = [(x/10.0, x/20.0, 0.75) for x in range(len(Bot_Teams_dict_url))]
# Specify this list of colors as the `color` option to `plot`.
#df.plot(kind='bar', color=my_colors)

# Or use colormaps
# http://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Show_colormaps

#Tour_last_stage = 22
stage_labels = list(range(1, Tour_N_stages+1)) + ['End']

# Individual stage score plot
stage_scores[0:Tour_last_stage].plot(linestyle='None', marker='o', grid=1, \
                                     colormap='Accent')
plt.xlim(-1,Tour_last_stage)
plt.xticks(list(range(0,Tour_last_stage)), stage_labels)
plt.title('Tour 2017: Individual stage scores')
plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', ncol=1, numpoints=1)
plt.ylabel('Points')
plt.xlabel('Stage')
plt.savefig('stage_scores.png', bbox_inches='tight')

# Cumulative stage score plot
cum_scores[0:Tour_last_stage].plot(linestyle='-', marker='|', grid=1, \
                                   colormap='Accent')
plt.xlim(0,Tour_last_stage-1)
plt.xticks(list(range(0,Tour_last_stage)), stage_labels)
plt.title('Tour 2017: Cumulative scores')
plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', ncol=1, numpoints=1)
plt.ylabel('Points')
plt.xlabel('Stage')
plt.savefig('cum_scores.png', bbox_inches='tight')

##########################
# Bot plots

# Individual stage score plot
bot_stage_scores[0:Tour_last_stage].plot(linestyle='None', marker='o', grid=1, \
                                         colormap='Accent')
plt.xlim(-1,Tour_last_stage)
plt.xticks(list(range(0,Tour_last_stage)), stage_labels)
plt.title('Tour 2017: Individual stage scores')
plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', ncol=1, numpoints=1)
plt.ylabel('Points')
plt.xlabel('Stage')
plt.savefig('bot_stage_scores.png', bbox_inches='tight')

# Cumulative stage score plot
bot_cum_scores[0:Tour_last_stage].plot(linestyle='-', marker='|', grid=1, \
                                        colormap='Accent')
plt.xlim(0,Tour_last_stage-1)
plt.xticks(list(range(0,Tour_last_stage)), stage_labels)
plt.title('Tour 2017: Cumulative scores')
plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', ncol=1, numpoints=1)
plt.ylabel('Points')
plt.xlabel('Stage')
plt.savefig('bot_cum_scores.png', bbox_inches='tight')


#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#
##########################
# Analysis

team_PCS_scores = pd.DataFrame()
team_PCS_scores['Teams'] = col_order
team_PCS_scores['PCS_Overall'] = [5196, 5884, 6417, 6879, 5851, 5105, 7290] 
team_PCS_scores['PCS_Season'] = [1994, 1966, 2169, 2424, 2678, 2478, 3706]

# Correlation plots

# 1. Cumulative score vs PCS Overall points

figure1 = plt.figure(figsize=(21,8))

for i in range(0,Tour_last_stage):
    print(i)
    plot = plt.subplot(4,6,i+1)
    x_data = team_PCS_scores['PCS_Overall'].tolist()
    y_data = cum_scores.values.tolist()[i]
    
    pearR = np.corrcoef(x_data,y_data)[1,0]
    fit = np.polyfit(x_data, y_data, 1)
    fit_fn = np.poly1d(fit) 
    
    plt.scatter(x_data, y_data)
    plt.plot(x_data, fit_fn(x_data), 'r')
    
    plot.tick_params(axis='both', which='major', labelsize=8)
    plot.locator_params(axis='y', nbins=5)
    plot.locator_params(axis='x', nbins=5)
    
    plt.title('Tour 2017 - After Stage ' + str(i+1), fontsize=10)
    plt.ylabel('Velogames Points', fontsize=8)
    plt.xlabel('PCS Overall Points', fontsize=8)
    
figure1.suptitle('Correlation of Velogames Points and PCS Overall Points', fontsize=14)
figure1.subplots_adjust(hspace=0.5, wspace=0.4)    

plt.savefig('cum_scores_PCS_Overall_correlation.png', bbox_inches='tight')



# 2. Cumulative score vs PCS Season points

figure2 = plt.figure(figsize=(21,8))

for i in range(0,Tour_last_stage):
    print(i)
    plot = plt.subplot(4,6,i+1)
    x_data = team_PCS_scores['PCS_Season'].tolist()
    y_data = cum_scores.values.tolist()[i]
    
    pearR = np.corrcoef(x_data,y_data)[1,0]
    fit = np.polyfit(x_data, y_data, 1)
    fit_fn = np.poly1d(fit) 
    
    plt.scatter(x_data, y_data)
    plt.plot(x_data, fit_fn(x_data), 'r')
    
    plot.tick_params(axis='both', which='major', labelsize=8)
    plot.locator_params(axis='y', nbins=5)
    #plot.locator_params(axis='x', nbins=4)
    
    plt.title('Tour 2017 - After Stage ' + str(i+1), fontsize=10)
    plt.ylabel('Velogames Points', fontsize=8)
    plt.xlabel('PCS Season Points', fontsize=8)
    
figure2.suptitle('Correlation of Velogames Points and PCS Season Points', fontsize=14)
figure2.subplots_adjust(hspace=0.5, wspace=0.4)    

plt.savefig('cum_scores_PCS_Season_correlation.png', bbox_inches='tight')




#####################
# Fun statistics

# Number of stage points wins
stage_score_winners = winners_df['Stage_Score_Winner'].value_counts()
overall_score_leaders = winners_df['Overall_Score_Leader'].value_counts()

# Max stage points
max_stage_points = {}
max_stage_pts_index = winners_df['Stage_Score_Winner_Pts'].idxmax()
max_stage_points['Name'] = \
    winners_df['Stage_Score_Winner'][max_stage_pts_index]
max_stage_points['Max_Pts'] = \
    int(winners_df['Stage_Score_Winner_Pts'][max_stage_pts_index])
max_stage_points['Stage'] = \
    int(winners_df['Stage_N'][max_stage_pts_index])

# Stage score statistics
stage_scores_only = stage_scores[0:21] 
stage_score_stats = pd.DataFrame()
stage_score_stats['Mean'] = stage_scores_only.mean()
stage_score_stats['Std'] = stage_scores_only.std()
stage_score_stats['CV'] = ss.variation(stage_scores_only)

# The most constant performance
# --> lowest STD/CV of stage scores

lowest_CV = stage_score_stats.loc[stage_score_stats['CV'].idxmin()]
lowest_STD = stage_score_stats.loc[stage_score_stats['Std'].idxmin()]

# Highest volatility
# --> highest STD/CV of stage scores

highest_CV = stage_score_stats.loc[stage_score_stats['CV'].idxmax()]
highest_STD = stage_score_stats.loc[stage_score_stats['Std'].idxmax()]






















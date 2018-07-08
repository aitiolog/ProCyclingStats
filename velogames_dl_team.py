# -*- coding: utf-8 -*-
"""
Velogames - download team points per stage

Author: Klemen Ziberna
"""


#####################################
# GLOBAL VARIABLES

# Template url
#overall_url = "https://www.velogames.com/giro-ditalia/2017/teamroster.php?tid=590be698bbe75142"
#stage_url = "https://www.velogames.com/giro-ditalia/2017/teamroster.php?tid=590be698bbe75142&ga=13&st=1"

BASE_URL = "https://www.velogames.com/tour-de-france/2017/teamroster.php"

Teams_dict_url = {
                  'Klemen': 'tid=595791a64d5cc777',
                  'Pip': 'tid=5956aeab738c2733',
                  'Simon': 'tid=5956903f270ec458',
                  'Andy': 'tid=5956ce75217cb253',
                  'James': 'tid=594f7ee477e96144',
                  'Pete': 'tid=59552b0e46832762',
                  'Chris': 'tid=5957092dbb091231',
                  'Parag': 'tid=5953ef20898f8367',
                  'Toby': 'tid=59523f13f3409947'
                  }

Bot_Teams_dict_url = {
                  'Klemen': 'tid=595791a64d5cc777',
                  'Klemen 2nd team': 'tid=5957970351477660',
                  'Bot - PCS Overall': 'tid=595789193712f314',
                  'Bot - PCS Season': 'tid=59578c2ee3edb408',
                  'Bot - PCS 2m form': 'tid=59578e3aeb051285',
                  'Random bot 1': 'tid=59579a75efa76904',
                  'Random bot 2': 'tid=59579afb22bb6890',
                  'Random bot 3': 'tid=59579b85604ac598'
                  }

                  
# Stages
Tour_N_stages = 21
Tour_last_stage = 22          

                  
#####################################
# LIBRARIES

from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss

#####################################
# FUNCTIONS
 
def get_stage_score(main_page_url, team_id, stage_N):
    # Load page
    stage_url = main_page_url + "?" + team_id + "&st=" + str(stage_N)
    stage_page = requests.get(stage_url)
    stage_page_bs = \
        bs(stage_page.content.decode('utf-8', 'ignore'), 'html.parser')
        
    # Extract stage score
    stage_find_string = 'Stage ' + str(stage_N) + ' Score:'
    stage_score_find = stage_page_bs.find(string=re.compile(stage_find_string))
    stage_score = stage_score_find.next_sibling.string
    
    return int(stage_score)

    
def get_end_tour_score(main_page_url, team_id, N_all_stages):
    # Load page
    end_tour_url = main_page_url + "?" + team_id + "&st=" + str(N_all_stages+1)
    end_tour_page = requests.get(end_tour_url)
    end_tour_page_bs = \
        bs(end_tour_page.content.decode('utf-8', 'ignore'), 'html.parser')
        
    # Extract end tour score
    end_tour_find_string = 'End-Of-Tour Score:'
    end_tour_find = end_tour_page_bs.find(string=re.compile(end_tour_find_string))
    end_tour_score = end_tour_find.next_sibling.string
    
    return int(end_tour_score)
  
    
def get_team_riders(main_page_url, team_id):
        
    # Load page
    team_url = main_page_url + "?" + team_id
    team_page = requests.get(team_url)
    team_page_bs = \
        bs(team_page.content.decode('utf-8', 'ignore'), 'html.parser')
    
    # Find riders' names
    team_riders_find = \
        team_page_bs.findAll('a', href = re.compile('riderprofile.php?'))
    
    team_riders = []
    for item in team_riders_find:
        team_riders.append(item.text)
    
    return team_riders


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

# Dowload a list of riders for every team

team_riders = {}

for item in Teams_dict_url:
    print('Dowloading riders for: ' + item)
    team_riders[item] = get_team_riders(BASE_URL, Teams_dict_url[item])

bot_team_riders = {}

for item in Bot_Teams_dict_url:
    print('Dowloading riders for: ' + item)
    bot_team_riders[item] = get_team_riders(BASE_URL, Bot_Teams_dict_url[item])
    

# Download scores

#Tour_N_stages = 21

# Get scores for every team

result_list = []

for item in Teams_dict_url:
    print('Dowloading data for: ' + item)
    team_dict_out = {}
    stage_score_list = []
    team_dict_out['Name'] = item
    
    # Stage results
    for n in range(0,Tour_N_stages):
        print('Stage number: ' + str(n+1))
        stage_score_list.insert(n, \
                                get_stage_score(BASE_URL, \
                                                Teams_dict_url[item], n+1))
    
    # End-of-tour score
    stage_score_list.append(get_end_tour_score(BASE_URL, \
                                               Teams_dict_url[item], \
                                               Tour_N_stages))
        
    team_dict_out['Stage_Score'] = stage_score_list
    team_dict_out['Cumulative_Score'] = np.cumsum(stage_score_list).tolist()
    team_dict_out['Stage_N'] = list(range(1,Tour_N_stages+1))
    team_dict_out['Stage_N'].append('End')
    
    result_list.append(team_dict_out)

    
# Man vs machine
bot_result_list = []

for item in Bot_Teams_dict_url:
    print('Dowloading data for: ' + item)
    bot_team_dict_out = {}
    bot_stage_score_list = []
    bot_team_dict_out['Name'] = item
    
    # Stage results
    for n in range(0,Tour_N_stages):
        print('Stage number: ' + str(n+1))
        bot_stage_score_list.insert(n, \
                                get_stage_score(BASE_URL, \
                                                Bot_Teams_dict_url[item], n+1))
    
    # End-of-tour score
    bot_stage_score_list.append(get_end_tour_score(BASE_URL, \
                                               Bot_Teams_dict_url[item], \
                                               Tour_N_stages))
    
    bot_team_dict_out['Stage_Score'] = bot_stage_score_list
    bot_team_dict_out['Cumulative_Score'] = np.cumsum(bot_stage_score_list).tolist()
    bot_team_dict_out['Stage_N'] = list(range(1,Tour_N_stages+1))
    bot_team_dict_out['Stage_N'].append('End')
    
    bot_result_list.append(bot_team_dict_out)

    
# Column order
col_order = ['Pip',
             'Simon',
             'Andy',
             'James',
             'Pete',
             'Chris',
             'Toby',
             'Parag',
             'Klemen']
    
bot_col_order = ['Bot - PCS Overall',
                 'Bot - PCS Season',
                 'Bot - PCS 2m form',
                 'Random bot 1',
                 'Random bot 2',
                 'Random bot 3',
                 'Klemen 2nd team',
                 'Klemen']
                 
             
# Create outputs
team_riders_df = pd.DataFrame(team_riders)
team_riders_df = set_column_sequence(team_riders_df, col_order, front=True)

result_list_df = pd.DataFrame(result_list)

stage_scores = result_list_df['Stage_Score'].apply(pd.Series).transpose()
stage_scores.columns = result_list_df['Name']
stage_scores = set_column_sequence(stage_scores, col_order, front=True)

cum_scores = result_list_df['Cumulative_Score'].apply(pd.Series).transpose()
cum_scores.columns = result_list_df['Name']
cum_scores = set_column_sequence(cum_scores, col_order, front=True)


bot_result_list_df = pd.DataFrame(bot_result_list)

bot_stage_scores = bot_result_list_df['Stage_Score'].apply(pd.Series).transpose()
bot_stage_scores.columns = bot_result_list_df['Name']
bot_stage_scores = set_column_sequence(bot_stage_scores, bot_col_order, front=True)

bot_cum_scores = bot_result_list_df['Cumulative_Score'].apply(pd.Series).transpose()
bot_cum_scores.columns = bot_result_list_df['Name']
bot_cum_scores = set_column_sequence(bot_cum_scores, bot_col_order, front=True)



# Stage winners and overall leaders
winners_df = pd.DataFrame()
winners_df['Stage_N'] = list(range(1,Tour_N_stages+1))
winners_df['Stage_Score_Winner'] = stage_scores.idxmax(axis=1)
winners_df['Stage_Score_Winner_Pts'] = stage_scores.max(axis=1)
winners_df['Overall_Score_Leader'] = cum_scores.idxmax(axis=1)
winners_df['Stage_Score_Leader_Pts'] = cum_scores.max(axis=1)

bot_winners_df = pd.DataFrame()
bot_winners_df['Stage_N'] = list(range(1,Tour_N_stages+1))
bot_winners_df['Stage_Score_Winner'] = bot_stage_scores.idxmax(axis=1)
bot_winners_df['Stage_Score_Winner_Pts'] = bot_stage_scores.max(axis=1)
bot_winners_df['Overall_Score_Leader'] = bot_cum_scores.idxmax(axis=1)
bot_winners_df['Stage_Score_Leader_Pts'] = bot_cum_scores.max(axis=1)

# Save to csv file
team_riders_df.to_csv('team_riders.csv')
stage_scores.to_csv('stage_scores.csv')
cum_scores.to_csv('cum_scores.csv')
winners_df.to_csv('winners.csv')


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






















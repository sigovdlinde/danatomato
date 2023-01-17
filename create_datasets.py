import pickle

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

import plotly.graph_objects as go

import pandas as pd

from datetime import datetime, timedelta

weight = ["Heavyweight", "Light Heavyweight", "Middleweight", "Welterweight", "Lightweight", "Featherweight", 
          "Bantamweight", "Flyweight", "Women's Bantamweight", "Women's Strawweight", "Women's Flyweight", 
          "Women's Featherweight", "Open Weight", "Super Heavyweight", "Catch Weight"]

def open_data(name):
    with open(name, "rb") as fp:
        return pickle.load(fp)

def save_data(data, name):
    with open(name, "wb") as fp:
        pickle.dump(data, fp)

def convert_date(date):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = date.split(' ')[0]
    month = months.index(month) + 1
    
    day = int(date.split(',')[0].split(' ')[1])
    year = int(date.split(', ')[1])
    date = datetime(year, month, day)
    return date

def all_fighter_names(data):
    all_names = []
    for event in data:
        for fight in event[0]:
            if fight[0][0] not in all_names:
                all_names.append(fight[0][0])
                
            if fight[1][0] not in all_names:
                all_names.append(fight[1][0])
    return all_names

def all_referee_names(data):
    all_names = []
    for event in data:
        for fight in event[0]:
            if fight[2][4] not in all_names:
                all_names.append(fight[2][4])
    
    return all_names

def fighter_data(data, name):
    # count = ["Winlose Score","Finish Score", "Finish Rate", ko, submission, decision, wins, losses, draws, knockdowns, 
    #          takedowns landed, takedowns attempted, reversals, submission attempted, control time, weight]
    count = [0 for i in range(16)]
    # Strikes = [Significant Strikes, Attempted Strikes, Accuracy, Head, Body, Leg, Distance, Clinch, Ground]
    strikes = [0 for i in range(9)]
    count[14] = timedelta()
    count[15] = 'Unspecified'
    
    all_data = []

    
    for event in data:
        for fight in event[0]:
            winner = fight[2][0]

            fighters = [fight[0][0], fight[1][0]]
            if name in fighters:
                index = fighters.index(name)
                
                if fight[index][1] != []:
                    total = fight[index][1][0]
                    
                    if fight[2][1] == 'KO/TKO':
                        count[2] += 1
                    elif fight[2][1] == 'Submission':
                        count[2] += 1
                    else:
                        count[2] -= 1

                    count[9] += total[0]
                    count[10] += total[1][0]
                    count[11] += total[1][0]
                    count[12] += total[2]
                    count[13] += total[3]
                    
                    if total[4] != '--':
                        time = datetime.strptime(total[4], '%M:%S').time()
                    else:
                        time = datetime.strptime('00:00', '%M:%S').time()
                    
                    delta = timedelta(minutes=time.minute, seconds=time.second)
                    count[14] += delta
                    
                    for w in weight[::-1]:
                        if w in fight[2][5]:
                            count[15] = w
                            break
                            
                    if count[15] not in weight:
                        count[15] = 'Unspecified'
                    
                    # Total, First, etc = [Significant Strikes, Head, Body, Leg, Distance, Clinch, Ground]
                        # Everything = [Landed, Attempted]
                    strike_list = [item for sublist in fight[index][2][0] for item in sublist]
                    strikes[0] += strike_list[0]
                    strikes[1] += strike_list[1]
                    if strikes[0] != 0 and strikes[1] != 0:
                        strikes[2] = round(strikes[0]/strikes[1] * 100, 2)
                        
                    strikes[3] += strike_list[2]
                    strikes[4] += strike_list[4]
                    strikes[5] += strike_list[6]
                    strikes[6] += strike_list[8]
                    strikes[7] += strike_list[10]
                    strikes[8] += strike_list[12]

                if fight[winner][0] == name:
                    count[0] += 1
                    count[6] += 1

                    if fight[2][1] == 'KO/TKO':
                        count[3] += 1
                        count[1] += 1
                    elif fight[2][1] == 'Submission':
                        count[4] += 1
                        count[1] += 1
                    else:
                        count[5] += 1
                        count[1] -= 1

                elif winner == 2:
                    count[8] += 1
                else:
                    count[0] -= 1
                    count[7] += 1
                
                data = [name, convert_date(event[1])] + count + strikes
                all_data.append(data)
                
    
    return all_data

def fighter_data_per_fight(data, name):
# win = 0 for win, 1 for loss, 2 for other.
# ["Name", "Date", "Opponent", "Weight", "Win", "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", 
#  "Submission Attempted", "Control Time", "Significant Strikes", "Attempted Strikes", "Accuracy", 
#  "Head", "Body", "Leg", "Distance", "Clinch", "Ground"]
    all_data = []
    # Opponent", "Weight", "Method", "Win"
    general_info = []
    # "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", "Submission Attempted", "Control Time"
    other = []
    # "Significant Strikes", "Attempted Strikes", "Accuracy", "Head", "Body", "Leg", "Distance", "Clinch", "Ground"
    strikes = []

    
    for event in data:
        for fight in event[0]:
            winner = fight[2][0]

            fighters = [fight[0][0], fight[1][0]]
            general_info = []
            other = []
            strikes = []
            if name in fighters:
                index = fighters.index(name)
                fighters.remove(name)
                
                general_info.append(fighters[0])
                
                for w in weight[::-1]:
                    if w in fight[2][5]:
                        general_info.append(w)
                        break
                
                
                if fight[index][1] != []:
                    other.append(fight[index][1][0][0])
                    other.append(fight[index][1][0][1][0])
                    other.append(fight[index][1][0][1][1])
                    other.append(fight[index][1][0][2])
                    other.append(fight[index][1][0][3])
                    
                    if fight[index][1][0][4] != '--':
                        time = datetime.strptime(fight[index][1][0][4], '%M:%S').time()
                    else:
                        time = datetime.strptime('00:00', '%M:%S').time()
                    
                    delta = timedelta(minutes=time.minute, seconds=time.second)
                    
                    if delta == None:
                        print(name, delta)
                    
                    other.append(delta)
                    
                    strike_list = [item for sublist in fight[index][2][0] for item in sublist]
                    
                    strikes.append(strike_list[0])
                    strikes.append(strike_list[1])
                    if strikes[0] != 0 and strikes[1] != 0:
                        strikes.append(round(strikes[0]/strikes[1] * 100, 2))
                    else:
                        strikes.append(0)
                        
                    strikes.append(strike_list[2])
                    strikes.append(strike_list[4])
                    strikes.append(strike_list[6])
                    strikes.append(strike_list[8])
                    strikes.append(strike_list[10])
                    strikes.append(strike_list[12])
                    
                    general_info.append(fight[2][1])
  
                if fight[winner][0] == name:
                    general_info.append(0)
                elif winner == 2:
                    general_info.append(2)
                else:
                    general_info.append(1)
                
                # Details
                general_info.append(fight[2][7].replace('.', '  '))
                
                data = [name, convert_date(event[1])] + general_info + other + strikes
                all_data.append(data)
                
    
    return all_data

def referee_data(data, name):
    # count = [ko, submission, decision, finish score, weight]
    count = [0 for i in range(5)]
    count[4] = 'Unspecified'
    all_data = []
    
    for event in data:
        for fight in event[0]:
            if name == fight[2][4]:
                
                for w in weight[::-1]:
                    if w in fight[2][5]:
                        count[4] = w
                        break

                if count[4] not in weight:
                    count[4] = 'Unspecified'
                    
                if fight[2][1] == 'KO/TKO':
                    count[0] += 1
                    count[3] += 1
                elif fight[2][1] == 'Submission':
                    count[1] += 1
                    count[3] += 1
                else:
                    count[2] += 1
                    count[3] -= 1
            
                data = [name, convert_date(event[1])] + count
                all_data.append(data)
    
    return all_data

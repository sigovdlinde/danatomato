import pickle

from datetime import datetime

def open_data(name):
    with open(name, "rb") as fp:
        return pickle.load(fp)

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

def fighter_data(data, name, value):
    all_data = []
    winlose = 0
    # ko not implemented
    ko = 0
    decision = 0
    submission = 0
    finish = 0
    
    for event in data:
        for fight in event[0]:
            winner = fight[2][0]

            if name in (fight[0][0], fight[1][0]):
                if fight[winner][0] == name:
                    winlose += 1

                    if fight[2][1] == 'KO/TKO':
                        ko += 1
                        finish += 1
                    elif fight[2][1] == 'Submission':
                        submission += 1
                        finish += 1
                    else:
                        decision += 1
                        finish -= 1

                elif winner == 2:
                    continue
                else:
                    winlose -= 1
            
                date = convert_date(event[1])
                data = [name, date, ko, submission, decision, winlose, finish]
                all_data.append([name, date, data[value]])
    
    return all_data

def bar_data(data, group):
    # [name, ko, submission, decision, finish]
    if group == 'Fighters':
        return []
    else:
        all_r_names = all_referee_names(data)
        all_data = [[all_r_names[i], 0, 0, 0, 0] for i in range(len(all_r_names))]
        
        for event in data:
            for fight in event[0]:
                name_index = all_r_names.index(fight[2][4])
                    
                if fight[2][1] == 'KO/TKO':
                    all_data[name_index][1] += 1
                    all_data[name_index][4] += 1
                elif fight[2][1] == 'Submission':
                    all_data[name_index][2] += 1
                    all_data[name_index][4] += 1
                else:
                    all_data[name_index][3] += 1
                    all_data[name_index][4] -= 1
                    

    return all_data
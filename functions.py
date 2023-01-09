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

def fighter_data(data, name):
    # strikes moet nog
    # count = [winlose, ko, submission, decision, finish score, wins, losses, draws, knockdowns, 
    #          takedowns landed, takedowns attempted, reversals, submission attempted, control time]
    count = [0 for i in range(14)]
    count[13] = datetime.strptime('00:00', '%M:%S').time()
    all_data = []
    
    for event in data:
        for fight in event[0]:
            winner = fight[2][0]

            fighters = [fight[0][0], fight[1][0]]
            if name in fighters:
                index = fighters.index(name)

                # ["Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", "Submission Attempted", "Control Time"]
                if fight[index][1] != []:
                    total = fight[index][1][0]

                    count[8] += total[0]
                    count[9] += total[1][0]
                    count[10] += total[1][0]
                    count[11] += total[2]
                    count[12] += total[3]

                    if total[4] != '--':
                        time = datetime.strptime(total[4], '%M:%S').time()
                    else:
                        time = datetime.strptime('00:00', '%M:%S').time()

                    count[13]= datetime.combine(datetime.now(), time)

                if fight[winner][0] == name:
                    count[0] += 1
                    count[5] += 1

                    if fight[2][1] == 'KO/TKO':
                        count[1] += 1
                        count[4] += 1
                    elif fight[2][1] == 'Submission':
                        count[2] += 1
                        count[4] += 1
                    else:
                        count[3] += 1
                        count[4] -= 1

                elif winner == 2:
                    count[7] += 1
                else:
                    count[0] -= 1
                    count[6] += 1
            
                data = [convert_date(event[1])] + count
                all_data.append(data)
    
    return [name, all_data]

def referee_data(data, name):
    all_data = []
    # ko not implemented
    ko = 0
    decision = 0
    submission = 0
    finish = 0
    
    for event in data:
        for fight in event[0]:
            if name == fight[2][4]:
                if fight[2][1] == 'KO/TKO':
                    ko += 1
                    finish += 1
                elif fight[2][1] == 'Submission':
                    submission += 1
                    finish += 1
                else:
                    decision += 1
                    finish -= 1
            
                date = convert_date(event[1])
                data = [date, ko, submission, decision, finish]
                all_data.append(data)
    
    return [name, all_data]

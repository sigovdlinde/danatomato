import time
import pickle

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from bs4 import BeautifulSoup

from create_datasets import *

def get_soup(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    re = session.get(url)
    
    return BeautifulSoup(re.text, features='html.parser')

def get_event_urls():
	soup = get_soup('http://ufcstats.com/statistics/events/completed?page=all')

	url_list = []
	for event in soup.find_all('a', {'class': 'b-link b-link_style_black'}):
	    event_url = event.get('href')
	    url_list.append(event_url)

	return url_list

def get_fight_urls_from_event(soup):
    url_list = []
    for fight in soup.find_all('a', {'b-flag b-flag_style_green'}):
        fight_url = fight.get('href')
        url_list.append(fight_url)
    return url_list

# Determine if winner is in left or right column.
# 0 is left, 1 is right, 2 is no contest or draw.
def get_winner_from_fight(soup):
    win_lose = soup.find('div', {'class': 'b-fight-details'}).find_all('i')
    
    if 'b-fight-details__person-status_style_green' in win_lose[0].get('class'):
        winner = 0
    elif 'b-fight-details__person-status_style_green' in win_lose[1].get('class'):
        winner = 1
    else:
        winner = 2
        
    result = soup.find('div', {'class': 'b-fight-details__content'})
    method = result.find('i', {'style': 'font-style: normal'}).get_text(strip=True)
    rnd = result.find('i', {'class': 'b-fight-details__text-item'}).get_text(strip=True).split(':')[1]
    time = result.find_all('i', {'class': 'b-fight-details__text-item'})[1].get_text(strip=True).split(':', 1)[1]
    referee = result.find_all('i', {'class': 'b-fight-details__text-item'})[3].get_text(strip=True).split(':')[1]
    weight = soup.find('div', {'class': 'b-fight-details__fight-head'}).get_text(strip=True)
    
    bonus = soup.find('div', {'class': 'b-fight-details__fight-head'}).find('img')
    if bonus:
        if 'belt' not in bonus:
            bonus = 1
        else:
            bonus = 0
    else:
        bonus = 0
    
    details = result.find_all('p', {'class': 'b-fight-details__text'})[1].get_text(strip=True).split(':', 1)[1]
    
    result = [winner, method, rnd, time, referee, weight, bonus, details]
    
    return result

def get_totals(results):
    for j in [6, 4, 3, 2, 0]:
        del results[j]

    stats = [[], []]
    for j, result in enumerate(results):
        stat = result.find_all('p')

        if j in [0, 2, 3]:
            stats[0].append(int(stat[0].get_text(strip=True)))
            stats[1].append(int(stat[1].get_text(strip=True)))
        elif j == 1:
            stats[0].append([int(x) for x in stat[0].get_text().split(' of ')])
            stats[1].append([int(x) for x in stat[1].get_text().split(' of ')])
        else:
            stats[0].append(stat[0].get_text(strip=True))
            stats[1].append(stat[1].get_text(strip=True))   
    
    return stats

def get_strikes(results):
    for j in [2, 0]:
        del results[j]

    stats = [[], []]
    for result in results:
        stat = result.find_all('p')
        stats[0].append([int(x) for x in stat[0].get_text().split(' of ')])
        stats[1].append([int(x) for x in stat[1].get_text().split(' of ')])
    
    return stats

def get_fighter_stats_from_fight(soup):
    totals = [[], []]
    strikes = [[], []]
    soup = soup.find_all('table')
    
    for i, section in enumerate(soup):
        section = section.find_all('tr',{'class': 'b-fight-details__table-row'})[1:]
        
        for all_results in section:
            results = all_results.find_all('td',{'class': 'b-fight-details__table-col'})
            
            if i <= 1:
                stats = get_totals(results)
                totals[0].append(stats[0])
                totals[1].append(stats[1])
            else:
                stats = get_strikes(results)
                strikes[0].append(stats[0])
                strikes[1].append(stats[1])       
    
    return totals, strikes

def get_fight_data(soup):
    name = [x.get_text() for x in soup.find_all('a', {'class': 'b-fight-details__person-link'})]
    totals, strikes = get_fighter_stats_from_fight(soup)
    result = get_winner_from_fight(soup)
    
    data = [[name[0], totals[0], strikes[0]], [name[1], totals[1], strikes[1]], result]

    return data

def get_all_fight_data(number_of_new_events, all_fight_data = []):
	event_urls = [get_event_urls()[:number_of_new_events]]

	for event_url in event_urls:
	    event_data = []
	    event_soup = get_soup(event_url)
	    fight_urls = get_fight_urls_from_event(event_soup)
	    
	    event_date_location = event_soup.find_all('li', {'class': 'b-list__box-list-item'})
	    event_date = event_date_location[0].get_text(strip=True).split(':', 1)[1]
	    event_location = event_date_location[1].get_text(strip=True).split(':', 1)[1]
	    
	    print(event_soup.find('span', {'class': 'b-content__title-highlight'}).get_text(strip=True), ' #', event_urls.index(event_url))
	    
	    fights = []
	    for fight_url in fight_urls:
	        fight_soup = get_soup(fight_url)
	        fight_data = get_fight_data(fight_soup)
	        fights.append(fight_data)
	        
	        print(fight_data[0][0], 'vs', fight_data[1][0])
	    
	    event_data.append(fights)
	    event_data.append(event_date)
	    event_data.append(event_location)
	    
	    all_fight_data.append(event_data)

	    time.sleep(5)
	    save_data(all_fight_data, 'all_fight_data')

	return all_fight_data

if __name__ == '__main__':
    previous_data = open_data('all_fight_data')
    number_of_new_events = (len(get_event_urls()) - len(previous_data))

    print('Number of new events: ', number_of_new_events)

    if number_of_new_events > 0:
        all_fight_data = get_all_fight_data(number_of_new_events, previous_data)

        all_f_names = all_fighter_names(all_fight_data)
        all_f_data = [fighter_data(all_fight_data, name) for name in all_f_names]
        all_f_data = [item for sublist in all_f_data for item in sublist]

        all_r_names = all_referee_names(all_fight_data)
        all_r_data = [referee_data(all_fight_data, name) for name in all_r_names]
        all_r_data = [item for sublist in all_r_data for item in sublist]

        all_f_data_per_fight = [fighter_data_per_fight(all_fight_data, name) for name in all_f_names]
        all_f_data_per_fight = [item for sublist in all_f_data_per_fight for item in sublist]

        save_data(all_f_data, 'all_f_data')
        save_data(all_f_data_per_fight, 'all_f_data_pf')
        save_data(all_r_data, 'all_r_data')
    else:
        print('Data is up-to-date.')





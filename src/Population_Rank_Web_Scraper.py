"""This file uses a table from WorldPopulationReview to gather a state's population rank.

Exports:
    dictionary_of_population_ranks: a dictionary that maps each U.S. state to its population rank
    backup_dictionary_used: a boolean that indicates if the backup dictionary is in use

Use Cases:
    dictionary_of_population_ranks["California"] == 1
"""

import requests
import bs4
import States_and_State_Capitals_Reader

#this dictionary maps a state to its population
dictionary_of_population_ranks = {}

#intialize request
URL = "https://worldpopulationreview.com/states"
URL_page_request = requests.get(URL)
URL_page_text = URL_page_request.text

soup = bs4.BeautifulSoup(URL_page_text, "html.parser")

#attempt to find the data on the website
try: 
    #locate the desired table using its html tag and class
    #this returns a list, so access the first element
    desired_table = soup.find_all("table")[0]

    table_rows = desired_table.find_all("tr")

    #because the table includes Puerto Rico and DC, track if they have been parsed and manually adjust all ranks in response
    adjustment_factor = 0

    for row in table_rows:
        table_cells = row.find_all("td")
        list_of_table_cells = [cell.text.strip() for cell in table_cells] #convert a row's contents into a list after cleaning it with .strip()

        #ignore empty lists
        if len(list_of_table_cells) == 0:
            continue

        #ignore states that aren't one of the original 50, but update the adjustment factor as those entries mess up the ranking of the table
        if list_of_table_cells[1] not in States_and_State_Capitals_Reader.list_of_state_names:
            adjustment_factor += 1
            continue

        #pull useful information from row
        state = list_of_table_cells[1]
        population_rank = int(list_of_table_cells[0]) - adjustment_factor
        dictionary_of_population_ranks[state] = population_rank

        #indicate that a backup dictionary was not used (used for the GUI)
        backup_dictionary_used = False

#if the table search fails for any reason, use a backup dictionary that contains the table's information from 9:04 p.m. Central Time on January 21st, 2021
except:
    dictionary_of_population_ranks = {'California': 1, 'Texas': 2, 'Florida': 3, 'New York': 4, 'Pennsylvania': 5,
        'Illinois': 6, 'Ohio': 7, 'Georgia': 8, 'North Carolina': 9, 'Michigan': 10,
        'New Jersey': 11, 'Virginia': 12, 'Washington': 13, 'Arizona': 14, 'Tennessee': 15,
        'Massachusetts': 16, 'Indiana': 17, 'Missouri': 18, 'Maryland': 19, 'Colorado': 20,
        'Wisconsin': 21, 'Minnesota': 22, 'South Carolina': 23, 'Alabama': 24, 'Louisiana': 25,
        'Kentucky': 26, 'Oregon': 27, 'Oklahoma': 28, 'Connecticut': 29, 'Utah': 30,
        'Nevada': 31, 'Iowa': 32, 'Arkansas': 33, 'Mississippi': 34, 'Kansas': 35,
        'New Mexico': 36, 'Nebraska': 37, 'Idaho': 38, 'West Virginia': 39, 'Hawaii': 40,
        'New Hampshire': 41, 'Maine': 42, 'Montana': 43, 'Rhode Island': 44, 'Delaware': 45,
        'South Dakota': 46, 'North Dakota': 47, 'Alaska': 48, 'Vermont': 49, 'Wyoming': 50
    }

    #indicate that the backup dictionary was used (used for the GUI)
    backup_dictionary_used = True
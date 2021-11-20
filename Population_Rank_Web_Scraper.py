import requests
from bs4 import BeautifulSoup
from States_and_State_Capitals_Reader import list_of_state_names


#the purpose of this file is to create a dictionary mapping different state names to their population rank
#population ranks will be web scraped from a wikipedia table
dictionary_of_population_ranks = {}


#initialize request
wikipedia_url = "https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population"
wikipedia_page_request = requests.get(wikipedia_url)
wikipedia_page_text = wikipedia_page_request.text

soup = BeautifulSoup(wikipedia_page_text, "html.parser")

#DESIRED_CAPTION is used to identify the desired table on the page
DESIRED_CAPTION = "Population of states, territories, divisions and regions\n[12]"

#find every table on the page
all_tables = soup.find_all("table")

#find the desired table
for table in all_tables:
    caption = table.find("caption")

    #do not consider tables with no captions
    if caption == [] or caption == None:
        continue

    #if a table has a caption, get the caption's text and strip it of leading spaces and new lines
    caption_text = caption.get_text()
    stripped_caption_text = caption_text.rstrip()

    #if this caption is the caption I am looking for, then it is the correct table
    if stripped_caption_text == DESIRED_CAPTION:
        desired_table = table

#if the search for the table works, create a dictionary with up to date information
try:
    table_rows = desired_table.find_all("tr")
    #for each row, create a list containing each cell's content as a string
    for row in table_rows:
        table_cells = row.find_all("td")
        list_of_table_cells = [cell.text.strip() for cell in table_cells]

        #only continue if the list is not empty
        if len(list_of_table_cells) == 0:
            continue

        #if the first cell in the row is one of the 50 states, then extract the data needed to add a key-value pair to the dictionary
        if list_of_table_cells[0] in list_of_state_names:
            state = list_of_table_cells[0]
            population_rank = int(list_of_table_cells[1])
            dictionary_of_population_ranks[state] = population_rank

#if the search for the table fails, use a backup dictionary that contains information from 7:05 pm on November 19th, 2021
except:
    dictionary_of_population_ranks = {
        'Massachusetts': 15, 'Connecticut': 29, 'New Hampshire': 41, 'Maine': 42, 'Rhode Island': 43, 
        'Vermont': 49, 'New York': 4, 'Pennsylvania': 5, 'New Jersey': 11, 'Florida': 3, 
        'Georgia': 8, 'North Carolina': 9, 'Virginia': 12, 'Maryland': 18, 'South Carolina': 23, 
        'West Virginia': 39, 'Delaware': 45, 'Tennessee': 16, 'Alabama': 24, 'Kentucky': 26, 
        'Mississippi': 34, 'Texas': 2, 'Louisiana': 25, 'Oklahoma': 28, 'Arkansas': 33, 
        'Illinois': 6, 'Ohio': 7, 'Michigan': 10, 'Indiana': 17, 'Wisconsin': 20, 
        'Missouri': 19, 'Minnesota': 22, 'Iowa': 31, 'Kansas': 35, 'Nebraska': 37, 
        'South Dakota': 46, 'North Dakota': 47, 'Arizona': 14, 'Colorado': 21, 'Utah': 30, 
        'Nevada': 32, 'New Mexico': 36, 'Idaho': 38, 'Montana': 44, 'Wyoming': 50, 
        'California': 1, 'Washington': 13, 'Oregon': 27, 'Hawaii': 40, 'Alaska': 48
    }

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


#find every table on the page
all_tables = soup.find_all("table")

#filter the tables to only those that contain captions
tables_with_captions = [table for table in all_tables if table.caption is not None]
# print(len(tables_with_captions))

#find the desired table
#this step requires developer to manually determine which table to access 
#in this case, there is only 1 table in the list to choose from
#if there were more / if the page were to change, change the index 
desire_tabled = tables_with_captions[0]

#find all the rows in the table
table_rows = desire_tabled.find_all("tr")


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
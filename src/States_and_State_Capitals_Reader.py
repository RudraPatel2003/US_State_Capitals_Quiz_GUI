"""This file reads a .csv file that lists each of the 50 U.S. states and their capital to create many useful data structures.

Exports:
    list_of_state_names: a list that contains each of the 50 U.S. states
    list_of_state_capitals: a list that contains each of the 50 U.S. state capitals
    dictionary_of_states: dict that maps each state capital to its state
    dictionary_of_state_capitals: a dict that maps each state to its state capital

Use Cases:
    dictionary_of_states["Nashville"] == Tennessee
    dictionary_of_state_capitals["Tennessee"] == Nashville
"""

import csv

list_of_state_names = []
list_of_state_capitals = []
dictionary_of_states = {}
dictionary_of_state_capitals = {}

CSV_FILE_NAME = "src/States_and_State_Capitals_Table.csv"

#read file
with open(CSV_FILE_NAME, "r") as csv_file:
    csv_reader = csv.reader(csv_file)

    #skip first row because it contains headers
    next(csv_reader)

    #extract data from rows
    for row in csv_reader:
        state = row[0]
        capital = row[1]
        list_of_state_names.append(state)
        list_of_state_capitals.append(capital)
        dictionary_of_state_capitals[state] = capital
        dictionary_of_states[capital] = state
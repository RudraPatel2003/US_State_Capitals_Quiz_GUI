import csv


#the purpose of this file is to read the .csv file in order to create a list of state names and a dictionary mapping state names to their capitals
list_of_state_names = []
dictionary_of_state_capitals = {}
dictionary_of_states = {}
list_of_state_capitals = []


#file name
csv_file_name = "States_and_State_Capitals_Table.csv"


#read file
with open(csv_file_name, "r") as csv_file:
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
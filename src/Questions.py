"""This file creates the list of questions regarding the 50 U.S. states.

Exports:
    Question: a class that every question for the test is an instance of.
    list_of_questions: a list that contains all possible questions that can be asked in the test
"""

import States_and_State_Capitals_Reader
import Population_Rank_Web_Scraper

list_of_questions = []

class Question:
    """This class introduces a template for quiz questions.
    
    Attributes:
        state: the name of the state the question is about
        capital: the state's capital
        population_rank: what population rank the state holds in comparison to other states
        weight: how many points the state is worth
    """
    def __init__(self, state: str, capital: str, population_rank: int, weight: int):
        "initializes the Question class"
        self.state = state
        self.capital = capital
        self.population_rank = population_rank
        self.weight = weight

    def create_question_text(self, question_number: int) -> str:
        """returns the question text that the user sees during the quiz.
        
        Arguments:
            question_number: the question's position in the quiz (counting from 1)
        """
        return f"Question {question_number}: What is the capital of {self.state}?"

    def create_population_rank_and_weight_text(self) -> str:
        """returns information about state's population rank and its point value."""
        #there are different conditions for different grammars
        #TODO replace with match-case when Python 3.10 releases to improve readability

        #1-10 award a single point, and 1-3 have unique grammars
        if self.population_rank == 1:
            return f"{self.state} is the most populous state in the US and is worth {self.weight} point."
        elif self.population_rank == 2:
            return f"{self.state} is the {self.population_rank}nd most populous state in the US and is worth {self.weight} point."
        elif self.population_rank == 3:
            return f"{self.state} is the {self.population_rank}rd most populous state in the US and is worth {self.weight} point."
        elif 4 <= self.population_rank <= 10:
            return f"{self.state} is the {self.population_rank}th most populous state in the US and is worth {self.weight} point."

        #11-20 all have consistent grammar
        elif 11 <= self.population_rank <= 20:
            return f"{self.state} is the {self.population_rank}th most populous state in the US and is worth {self.weight} points."

        #21, 31, 41
        elif self.population_rank % 10 == 1:
            return f"{self.state} is the {self.population_rank}st most populous state in the US and is worth {self.weight} points."

        #22, 32, 42
        elif self.population_rank % 10 == 2:
            return f"{self.state} is the {self.population_rank}nd most populous state in the US and is worth {self.weight} points."

        #23, 33, 43
        elif self.population_rank % 10 == 3:
            return f"{self.state} is the {self.population_rank}rd most populous state in the US and is worth {self.weight} points."
        
        #all other numbers between 21-49 that are consistent
        elif 21 <= self.population_rank <= 49:
            return f"{self.state} is the {self.population_rank}th most populous state in the US and is worth {self.weight} points."
        
        #50 has unique grammar
        else:
            return f"{self.state} is the least populous state in the US and is worth {self.weight} points."


def calculate_weight(population_rank: int) -> int:
    """calculates how many points a question is worth
    
    Arguments:
        population_rank: what population rank the state holds in comparison to other states

    Returns:
        an integer 1 through 5 (inclusive)
    """
    if 1 <= population_rank <= 10:
        return 1
    elif 11 <= population_rank <= 20:
        return 2
    elif 21 <= population_rank <= 30:
        return 3
    elif 31 <= population_rank <= 40:
        return 4
    elif 41 <= population_rank <= 50:
        return 5


#create the list of 50 Question instances, each about one state
for i in States_and_State_Capitals_Reader.list_of_state_names:
    state = i
    capital = States_and_State_Capitals_Reader.dictionary_of_state_capitals[state]
    population_rank = Population_Rank_Web_Scraper.dictionary_of_population_ranks[state]
    weight = calculate_weight(population_rank)
    temporary_instance = Question(state, capital, population_rank, weight)
    list_of_questions.append(temporary_instance)
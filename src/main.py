"""This file is the main file of the project and carries out the quiz through a tkinter GUI.

There are 3 stages to the quiz defined by 3 classes
Stage 1: SetupScreen
Stage 2: QuizScren
Stage 3: Final Screen
"""
import tkinter as tk
import Questions
import Population_Rank_Web_Scraper
import States_and_State_Capitals_Reader
import time
import random

class SetupScreen:
    """the first stage of the quiz, where the user is asked for the amount of questions they want
    
    Attributes:
        root: the GUI window
    """
    def __init__(self, root):
        """initialize the setup screen"""
        #reference the GUI window
        self.root = root

        #track if the button in the GUI has been pressed
        self.button_pressed = tk.BooleanVar(self.root)
        self.button_pressed.set("False")

        #ask the user for how many questions they want, storing the value as a variable
        self.number_of_questions = self.prompt_number_of_questions()


    def prompt_number_of_questions(self):
        """asks the user for how many questions they want"""
        #keep looping until an appropriate response is given
        while True:
            self.create_setup_widgets()
            self.display_setup_widgets()

            #wait until the button is pressed, as that changes the value of button_pressed from False to True
            self.button_pressed.set(False)
            self.root.wait_variable(self.button_pressed)
            
            #user input is a string, so convert to an int
            #exceptions are handled by displaying a message and waiting 3 seconds before the screen is refreshed (a new loop)
            #the GUI must update before sleeping or the error and wait labels will not appear
            try:
                question_amount = int(self.question_amount_entry.get())
            except ValueError:
                self.error_message_label.configure(text = "The input must be an integer!")
                self.wait_message_label.configure(text = "Please wait 3 seconds to try again...")
                self.root.update()
                time.sleep(3)
            except Exception:
                self.error_message_label.configure(text = "An unexpected error occured.")
                self.wait_message_label.configure(text = "Please wait 3 seconds to try again...")
                self.root.update()
                time.sleep(3)
            
            #if there is no exception, check if the input is a valid number 1-50
            #if it is not, then display a manual error message with the procedure from before
            #if the input is valid, then return the value for use in the next function
            else:
                if question_amount < 1:
                    self.error_message_label.configure(text = "The input is too low!")
                    self.wait_message_label.configure(text = "Please wait 3 seconds to try again...")
                    self.root.update()
                    time.sleep(3)
                elif question_amount > 50:
                    self.error_message_label.configure(text = "The input is too high!")
                    self.wait_message_label.configure(text = "Please wait 3 seconds to try again...")
                    self.root.update()
                    time.sleep(3)
                else:
                    return question_amount
            
            #no matter what, delete all of the widgets on the screen so that they can be rebuilt in the next loop or QuizScreen
            finally:
                self.destroy_setup_widgets()


    def create_setup_widgets(self):
        """defines the widgets used for the setup screen"""
        self.question_amount_label = tk.Label(self.root, text = "How many questions would you like to be asked about US State Capitals?")
        self.instructions_label = tk.Label(self.root, text = "Enter a number 1-50 (inclusive):")
        self.question_amount_entry = tk.Entry(self.root)
        self.question_amount_entry_submit_button = tk.Button(self.root, text = "Submit", command = self.track_button_press)
        self.error_message_label = tk.Label(self.root, text = "")
        self.wait_message_label = tk.Label(self.root, text = "")
        self.backup_dictionary_message_label = tk.Label(self.root, text = "Could not retreive population rank data; backup dictionary in use")


    def display_setup_widgets(self):
        """displays the widgets used for the setup screen"""
        self.question_amount_label.pack()
        self.instructions_label.pack()
        self.question_amount_entry.pack()
        self.question_amount_entry_submit_button.pack()
        self.error_message_label.pack()
        self.wait_message_label.pack()
        
        #displays message indicating if backup dictionary is in use
        if Population_Rank_Web_Scraper.backup_dictionary_used:
            self.backup_dictionary_message_label.pack()


    def destroy_setup_widgets(self):
        """removes all of the widgets used for the setup screen"""
        self.question_amount_label.destroy()
        self.instructions_label.destroy()
        self.question_amount_entry.destroy()
        self.question_amount_entry_submit_button.destroy()
        self.error_message_label.destroy()
        self.wait_message_label.destroy()
        self.backup_dictionary_message_label.destroy()


    def track_button_press(self):
        """accessed by buttons; sets the button_pressed attribute to True"""
        self.button_pressed.set("True")


    


class QuizScreen:
    """The second stage of the quiz, where the quiz is conducted
    
    Attributes:
        root: the GUI window
        number_of_questions: the number of questions that the quiz will contain
    """
    def __init__(self, root, number_of_questions: int):
        """initializes the quiz"""
        #reference the GUI window
        self.root = root

        #track if the button in the GUI has been pressed
        self.button_pressed = tk.BooleanVar(self.root)
        self.button_pressed.set("False")

        #take in the number of questions the user wanted from SetupScreen
        self.number_of_questions = number_of_questions

        #generate the number of random questions required
        self.list_of_random_questions, self.maximum_points = self.generate_random_questions(self.number_of_questions)

        #conduct the quiz, returning the number of questions correct and total points earned
        self.number_correct, self.points_earned = self.US_State_Capitals_Quiz_GUI(self.list_of_random_questions)


    def US_State_Capitals_Quiz_GUI(self, list_of_random_questions: list[Questions.Question]) -> tuple[int, int]:
        #set number_correct and points to 0
        self.number_correct = 0
        self.points_earned = 0
        question_number = 1

        #begin iterating through each question
        for question in list_of_random_questions:
            self.create_quiz_widgets()

            #input the correct question information into the widgets
            question_text = question.create_question_text(question_number)
            population_rank_and_weight_text = question.create_population_rank_and_weight_text()
            self.display_question_info(question_text, population_rank_and_weight_text)

            self.display_quiz_widgets()

            #wait for the button to be pressed
            self.root.wait_variable(self.button_pressed)
            self.button_pressed.set(False)
            
            #once the button is pressed, pull the text in the entry box
            user_answer = self.user_entry.get()

            #evaluate the user's answer and update number correct and points
            if user_answer == question.capital:
                correct = True
                self.number_correct += 1
                self.points_earned += question.weight
            else:
                correct = False

            #display ongoing accuracy and points
            self.display_number_correct_and_points(question, correct, user_answer, self.number_correct, self.points_earned)

            #increase the question number
            question_number += 1

            #wait 3 seconds for the next question, updating the GUI before the sleep command so that it shows up
            self.wait_label.configure(text = "Please wait 3 seconds...")
            self.root.update()
            time.sleep(3)

            #remove all of the widgets on the screen so that they can be built again in the next loop
            self.destroy_quiz_widgets()

        return self.number_correct, self.points_earned


    def generate_random_questions(self, number_of_questions: int) -> tuple[list[Questions.Question], int]:
        """generates a list of random questions for the quiz
        
        Arguments:
            number_of_questions: the number of questions that the quiz will contain
        
        Returns:
            list_of_random_questions: the list of questions that the quiz will run through
            maximum_points: the maximum number of points that can be earned if all questions are answered correctly
        """
        list_of_random_questions = random.sample(Questions.list_of_questions, number_of_questions)
        maximum_points = sum([question.weight for question in list_of_random_questions])
        return list_of_random_questions, maximum_points


    def display_question_info(self, question_text: str, population_rank_and_weight_text: str):
        """shows the appropriate question information on the quiz screen

        Arguments:
            question_text: the text displaying the actual question
            population_rank_and_weight_text: the text containing each state's population rank and point value
        """
        self.question_label.configure(text = question_text)
        self.population_rank_and_weight_label.configure(text = population_rank_and_weight_text)


    def display_number_correct_and_points(self, question: Questions.Question, correct: bool, user_answer: str, ongoing_accuracy: int, ongoing_points: int):
        """after a question is answered, show if they got it right or not (and if they were thinking of a different state) and the ongoing accuracy and points
        
        Arguments:
            question: the Question instance
            correct: if the user got the answer correct or not
            user_answer: the user's answer to the question
            ongoing_accuracy: the number of questions the user has answered so far
            ongoing_points: the number of questions the user has earned so far
        """
        #if they got the question right, congratulate them
        if correct:
            self.message_label.configure(text = "Correct!")

            #display ongoing accuracy and points
            self.number_correct_label.configure(text = f"Number Correct: {ongoing_accuracy}/{self.number_of_questions}")
            self.points_label.configure(text = f"Points Earned: {ongoing_points}/{self.maximum_points}")
            return

        #if they got it wrong, check if their answer is a different state's capital
        list_of_other_state_capitals = [i for i in States_and_State_Capitals_Reader.list_of_state_capitals if i != question.capital]
        if user_answer in list_of_other_state_capitals:
            #if it is a different state capital, tell them what the capital is and teach say what state they were thinking of
            self.message_label.configure(text = f"Incorrect. The answer is {question.capital}. {user_answer} is actually the capital of {States_and_State_Capitals_Reader.dictionary_of_states[user_answer]}.")

            #display ongoing accuracy and points
            self.number_correct_label.configure(text = f"Number Correct: {ongoing_accuracy}/{self.number_of_questions}")
            self.points_label.configure(text = f"Points Earned: {ongoing_points}/{self.maximum_points}")
            return
        
        #if they got it wrong and it is not a different capital, teach them the correct state
        else:
            #display question outcome and teach correct capital
            self.message_label.configure(text = f"Incorrect. The answer is {question.capital}.")

            #display ongoing accuracy and points
            self.number_correct_label.configure(text = f"Number Correct: {ongoing_accuracy}/{self.number_of_questions}")
            self.points_label.configure(text = f"Points Earned: {ongoing_points}/{self.maximum_points}")
            return

        
    def create_quiz_widgets(self):
        """defines the widgets used for the quiz screen"""
        self.question_label = tk.Label(self.root, text = "")
        self.population_rank_and_weight_label = tk.Label(self.root, text = "")
        self.user_entry = tk.Entry(self.root)
        self.check_answer_button = tk.Button(self.root, text = "Check Answer", command = self.track_button_press)
        self.message_label = tk.Label(self.root, text = "")
        self.number_correct_label = tk.Label(self.root, text = "")
        self.points_label = tk.Label(self.root, text = "")
        self.wait_label = tk.Label(self.root, text = "")


    def display_quiz_widgets(self):
        """displays the widgets used for the quiz screen"""
        self.question_label.pack()
        self.population_rank_and_weight_label.pack()
        self.user_entry.pack()
        self.check_answer_button.pack()
        self.message_label.pack()
        self.number_correct_label.pack()
        self.points_label.pack()
        self.wait_label.pack()
    

    def destroy_quiz_widgets(self):
        """removes all of the widgets used for the quiz screen"""
        self.question_label.destroy()
        self.population_rank_and_weight_label.destroy()
        self.user_entry.destroy()
        self.check_answer_button.destroy()
        self.message_label.destroy()
        self.number_correct_label.destroy()
        self.points_label.destroy()
        self.wait_label.destroy()


    def track_button_press(self):
        """accessed by buttons; sets the button_pressed attribute to True"""
        self.button_pressed.set(True)


class FinalScreen:
    """the final screen where the user can see how they did
    
    Attributes:
        root: the GUI window
        number_correct: the number of questions the user got correct
        number_of_questions: the number of questions asked
        points_eanred: the number of points the user earned
        maximum_points: the maximum number of points that can be earned if all questions are answered correctly
    """
    def __init__(self, root, number_correct, number_of_questions, points_earned, maximum_points):
        "initializes the final screen"
        #reference the GUI window
        self.root = root

        #record accuracy and points
        self.number_correct = number_correct
        self.number_of_questions = number_of_questions
        self.points_earned = points_earned
        self.maximum_points = maximum_points

        #display how the user did
        self.display_totals()
    

    def display_totals(self):
        """creates the final screen"""
        self.create_final_widgets()
        self.display_final_widgets()

    
    def create_final_widgets(self):
        """defines the widgets used for the final screen"""
        self.thank_you_message_label = tk.Label(self.root, text = "Thank you! You have completed the US State Capitals Quiz!")
        self.number_correct_label = tk.Label(self.root, text = f"Total Number Correct: {self.number_correct}/{self.number_of_questions}")
        self.points_earned_label = tk.Label(self.root, text = f"Total Points Earned: {self.points_earned}/{self.maximum_points}")
        self.exit_button = tk.Button(self.root, text = "Exit", command = self.close_final_window)


    def display_final_widgets(self):
        """displays the widgets used for the final screen"""
        self.thank_you_message_label.pack()
        self.number_correct_label.pack()
        self.points_earned_label.pack()
        self.exit_button.pack()


    def close_final_window(self):
        """closes the GUI"""
        self.root.destroy()


if __name__ == "__main__":
    #create GUI window and rename it
    root = tk.Tk()
    root.title("US State Capitals Quiz GUI")
    
    #resize and center the screen (https://www.pythontutorial.net/tkinter/tkinter-window/ for explanation)
    window_width = 600
    window_height = 200

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    centerpoint_x = int(screen_width / 2 - window_width / 2)
    centerpoint_y = int(screen_height / 2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{centerpoint_x}+{centerpoint_y}')

    #ask for the number of questions
    setup = SetupScreen(root)

    #conduct the quiz
    quiz = QuizScreen(root, setup.number_of_questions)

    #display results with information from previous step
    final_screen = FinalScreen(root, quiz.number_correct, quiz.number_of_questions, quiz.points_earned, quiz.maximum_points)

    #make GUI work
    root.mainloop()
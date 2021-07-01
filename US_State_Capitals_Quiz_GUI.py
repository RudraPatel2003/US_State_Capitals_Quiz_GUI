import tkinter as tk
from Questions import Question, list_of_questions
import time
import random

#the purpose of this file is to create a GUI where the quiz on US State Capitals can be conducted

class SetupScreen:
    """the first stage of the quiz, where the user is asked for the amount of questions they want"""
    def __init__(self, root):
        #reference the GUI window
        self.root = root

        #create an attribute that determines if a button in the GUI has been pressed or not and initially set it to False
        #this is set as an attribute because it is modified by different methods
        self.button_pressed = tk.BooleanVar(self.root)
        self.button_pressed.set("False")

        #ask the user for how many questions they want, storing the value as a variable
        self.number_of_questions = self.prompt_number_of_questions()


    def create_setup_widgets(self):
        """defines the widgets used for the setup screen"""
        self.question_amount_label = tk.Label(self.root, text = "How many questions would you like to be asked about US State Capitals?")
        self.instructions_label = tk.Label(self.root, text = "Enter a number 1-50 (inclusive):")
        self.question_amount_entry = tk.Entry(self.root)
        self.question_amount_entry_submit_button = tk.Button(self.root, text = "Submit", command = self.track_button_press)
        self.error_message_label = tk.Label(self.root, text = "")
        self.wait_message_label = tk.Label(self.root, text = "")


    def display_setup_widgets(self):
        """displays the widgets used for the setup screen"""
        self.question_amount_label.pack()
        self.instructions_label.pack()
        self.question_amount_entry.pack()
        self.question_amount_entry_submit_button.pack()
        self.error_message_label.pack()
        self.wait_message_label.pack()


    def destroy_setup_widgets(self):
        """removes all of the widgets used for the setup screen"""
        self.question_amount_label.destroy()
        self.instructions_label.destroy()
        self.question_amount_entry.destroy()
        self.question_amount_entry_submit_button.destroy()
        self.error_message_label.destroy()
        self.wait_message_label.destroy()


    def track_button_press(self):
        """accessed by buttons; sets the button_pressed attribute to True"""
        self.button_pressed.set("True")


    def prompt_number_of_questions(self):
        """asks the user for how many questions they want"""
        #keep looping until an appropriate response is given
        while True:
            #create and display widgets that determine question amount
            self.create_setup_widgets()
            self.display_setup_widgets()

            #reset the button_pressed variable to False
            self.button_pressed.set(False)

            #wait until the button is pressed, as that changes the value of button_pressed from False to True
            self.root.wait_variable(self.button_pressed)
            
            #pull the data that the user has entered into the entry box, converting it into an integer
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


class QuizScreen:
    """The second stage of the quiz, where the quiz is conducted"""
    def __init__(self, root, number_of_questions):
        #reference the GUI window
        self.root = root

        #create an attribute that determines if a button in the GUI has been pressed or not and initially set it to False
        #this is set as an attribute because it is modified by different methods
        self.button_pressed = tk.BooleanVar(self.root)
        self.button_pressed.set("False")

        #take in the number of questions the user wanted from SetupScreen
        self.number_of_questions = number_of_questions

        #generate the number of random questions required
        self.list_of_random_questions, self.maximum_points = self.generate_random_questions(self.number_of_questions)

        #conduct the quiz, returning the number of questions correct and total points earned
        self.number_correct, self.points_earned = self.US_State_Capitals_Quiz_GUI(self.list_of_random_questions)


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

    def generate_random_questions(self, number_of_questions):
        """generates a list of random questions for the quiz"""
        list_of_random_questions = random.sample(list_of_questions, number_of_questions)
        maximum_points = sum([question.weight for question in list_of_random_questions])
        return list_of_random_questions, maximum_points


    def display_question_info(self, question_text, population_rank_and_weight_text):
        """shows the appropriate question information on the quiz screen"""
        self.question_label.configure(text = question_text)
        self.population_rank_and_weight_label.configure(text = population_rank_and_weight_text)


    def display_number_correct_and_points(self, question, correct, ongoing_accuracy, ongoing_points):
        """after a question is answered, show if they got it right or not and the ongoing accuracy and points"""
        if correct:
            #display question outcome
            self.message_label.configure(text = "Correct!")

            #display ongoing accuracy and points
            self.number_correct_label.configure(text = f"Number Correct: {ongoing_accuracy}/{self.number_of_questions}")
            self.points_label.configure(text = f"Points Earned: {ongoing_points}/{self.maximum_points}")
        else:
            #display question outcome and teach correct capital
            self.message_label.configure(text = f"Incorrect. The answer is {question.capital}.")

            #display ongoing accuracy and points
            self.number_correct_label.configure(text = f"Number Correct: {ongoing_accuracy}/{self.number_of_questions}")
            self.points_label.configure(text = f"Points Earned: {ongoing_points}/{self.maximum_points}")


    def track_button_press(self):
        """accessed by buttons; sets the button_pressed attribute to True"""
        self.button_pressed.set(True)


    def US_State_Capitals_Quiz_GUI(self, list_of_random_questions):
        #set number_correct and points to 0
        self.number_correct = 0
        self.points_earned = 0
        question_number = 1

        #begin iterating through each question
        for question in list_of_random_questions:
            #create the widgets
            self.create_quiz_widgets()

            #input the correct question information into the widgets
            question_text = question.create_question_text(question_number)
            population_rank_and_weight_text = question.create_population_rank_and_weight_text()
            self.display_question_info(question_text, population_rank_and_weight_text)

            #display the widgets
            self.display_quiz_widgets()

            #set the button_pressed variable to False
            self.button_pressed.set(False)

            #wait for the button to be pressed
            self.root.wait_variable(self.button_pressed)

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
            self.display_number_correct_and_points(question, correct, self.number_correct, self.points_earned)

            #increase the question number
            question_number += 1

            #wait 3 seconds for the next question, updating the GUI before the sleep command so that it shows up
            self.wait_label.configure(text = "Please wait 3 seconds...")
            self.root.update()
            time.sleep(3)

            #remove all of the widgets on the screen so that they can be built again in the next loop
            self.destroy_quiz_widgets()

        return self.number_correct, self.points_earned
            

class FinalScreen:
    """the final screen where the user can see how they did"""
    def __init__(self, root, number_correct, number_of_questions, points_earned, maximum_points):
        #reference the GUI window
        self.root = root

        #record accuracy and points
        self.number_correct = number_correct
        self.number_of_questions = number_of_questions
        self.points_earned = points_earned
        self.maximum_points = maximum_points

        #display how the user did
        self.display_totals()
    

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


    def display_totals(self):
        """creates the final screen"""
        self.create_final_widgets()
        self.display_final_widgets()

        
if __name__ == "__main__":
    #create GUI window and rename it
    root = tk.Tk()
    root.title("US State Capitals Quiz GUI")

    #ask for the number of questions
    setup = SetupScreen(root)

    #conduct the quiz
    quiz = QuizScreen(root, setup.number_of_questions)

    #display results with information from previous step
    final_screen = FinalScreen(root, quiz.number_correct, quiz.number_of_questions, quiz.points_earned, quiz.maximum_points)

    #make GUI work
    root.mainloop()
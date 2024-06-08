import PySimpleGUI as sg
import random
import time


# Set default font size
sg.set_options(font=("Helvetica", 20))
background_color = "#0091D5"
score = 0 
correct_feedback_phrase = ["That's correct", "Good Job!", "Perfect answer", "Very Good!", "That's Cool!"]
incorrect_feedback_phrase = ["That's Wrong!", "Incorrect!!", "Make it right next time!"]
feedback_text_color = ""
start_time = time.time()
time_spent = 0
right_answer = 0 
wrong_answer = 0 


def generate_question(operation):
    """Generates a math question based on the operation."""

    if operation == "Add":
      num1 = int(random.randint(10, 99))
      num2 = int(random.randint(7, 15))
      num2 = abs(10 - (num1 - num2)) + num2
      return f"{num1} + {num2} = ", num1 + num2
    elif operation == "Subtract":
      num1 = int(random.randint(10, 100))
      num2 = int(random.randint(10, num1-10))
      return f"{num1} - {num2} =", num1 - num2
    elif operation == "Multiplication":
      num1 = int(random.randint(3, 10))
      num2 = int(random.randint(2,10))        
      return f"{num1} * {num2} =", num1 * num2
    elif operation == "Division":
      num1 = int(random.randint(3, 100))
      num2 = random.randint(1, 10)  # Ensure no division by zero
      return f"{num1} / {num2} =", num1 / num2

def check_answer(question, answer):
    """Checks if the user's answer is correct."""

    correct_answer = question.split("=")[0].strip()
    print("INside the Check_ANSWER BLOCK:")
    print("question =====>", question)
    print('question.split("=")[0].strip():  ', question.split("=")[0].strip())
    print("correct_answer =>", correct_answer)
    print("correct_answer type =>", type(correct_answer))
    print("float(answer) =>", float(answer))
    return float(answer) == correct_answer

def calculate_time_spent(start_time):
  """Calculates the time spent since the start time and returns it in mm:ss format."""

  # Get the current time in seconds
  current_time = time.time()

  # Calculate the time difference in seconds
  time_spent = current_time - start_time

  # Convert seconds to minutes and seconds (discarding milliseconds)
  minutes = int(time_spent // 60)
  seconds = int(time_spent % 60)

  # Format the output string in mm:ss format
  output_string = f"{minutes:02d}:{seconds:02d}"

  return output_string

# Layout for the operation selection screen
operation_layout = [
    [sg.Text("What do you want to practice, Aarav?",  background_color=background_color)],
    [sg.Radio("Addition", "OPERATION", key="Add",  background_color=background_color)],
    [sg.Radio("Subtraction", "OPERATION", key="Subtract",  background_color=background_color)],
    [sg.Radio("Multiplication", "OPERATION", key="Multiplication",  background_color=background_color)],
    [sg.Radio("Division", "OPERATION", key="Division",  background_color=background_color)],
    [sg.Button("Start Practice")]
]

# Layout for the question screen
question_layout = [
    [sg.Text(f"\tCorrect Answer:{right_answer}\tWrong Answer:{wrong_answer}", key="score", justification='right', font=("Helvetica", 14), text_color="black", background_color=background_color)],
    [sg.HorizontalSeparator()], 
    [sg.Text("", key="question",  background_color=background_color), sg.InputText(key="answer", size=(4, 1), focus=True , **{"enable_events": True})],
    [sg.Text("", key="timer", font=("Lucida Console", 14), text_color="black", background_color=background_color)],  # Timer text
    [sg.Text("", key="nothing", text_color="Red",  background_color=background_color)],
    [sg.Button("Submit Answer")],
    [sg.HorizontalSeparator()],
    [sg.Text("", key="feedback", font=("Tahoma", 14), text_color="black",  background_color=background_color)]
]


# Create the windows
operation_window = sg.Window("Math Practice", operation_layout,  background_color=background_color)
question_window = None

while True:
    event, values = operation_window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "Start Practice":
        selected_operation = None
        for operation in ['Add', 'Subtract', 'Multiplication', 'Division']:
            if values[operation]:
                selected_operation = operation
                break
        operation_window.close() # Close the Main Options Window

        if selected_operation:
            question, correct_answer = generate_question(selected_operation)

            if question_window:
                question_window.close()
            
            question_window = sg.Window("Math Practice", question_layout,  background_color=background_color, finalize=True,  size=(450,300))
            question_window["question"].update(question)
         
            while True:
                q_event, q_values = question_window.read()
                if q_event == sg.WIN_CLOSED:
                    break
                time_spent = calculate_time_spent(start_time)
                question_window["timer"].update(f"Time spent: {time_spent}")

                if q_event == "Submit Answer" or q_values["answer"].endswith("\n") :
                    
                    try:
                        user_answer = int(q_values["answer"].strip())
                    except ValueError:
                        print("Encountered Value Error")
                        user_answer = None 
                    
                    print("QUESTION correct_answer", correct_answer, type(correct_answer))
                    print("QUESTION user_answer", user_answer, type(user_answer))
                    feedback_text = ""
                    feedback_text_color = "Red"

                    print("90: user_answer = {} | correct_answer = {} | question ={}".format(user_answer, correct_answer, question))

                    if user_answer == correct_answer:
                      feedback_text = "\t" + correct_feedback_phrase[int(random.randint(1,len(correct_feedback_phrase)-1))]
                      feedback_text_color = "Green"
                      score = score + 1
                      right_answer +=1 
                    else:
                      feedback_text = "\t" + incorrect_feedback_phrase[int(random.randint(1,len(incorrect_feedback_phrase)-1))]
                      feedback_text_color = "Red"
                      wrong_answer += 1

                    question_window["feedback"].update(feedback_text)
                    question, correct_answer = generate_question(selected_operation)
                    question_window["question"].update(question)
                    create_question_window = False
                    question_window["answer"].update("")
                    question_window["score"].update(f"\tCorrect Answer:{right_answer}\tWrong Answer:{wrong_answer}")
                    question_window["answer"].set_focus() 
                    feedback_text = ""

            question_window.close()

operation_window.close()

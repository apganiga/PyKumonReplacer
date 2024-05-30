import PySimpleGUI as sg

# Define the layout
layout = [
    [sg.Text("Enter your text:")],
    [sg.InputText(key="-INPUT-")],  # Assign a key for easy access
    [sg.Submit(button_text="Submit")],
]

# Create the window
window = sg.Window("Input Box Example", layout)

# Event loop
while True:
    event, values = window.read()

    # Check for closing the window or pressing ESC
    if event == sg.WIN_CLOSED:
        break

    # Get the input text
    input_text = values["-INPUT-"]

    # Check if submit button was clicked or Enter key was pressed
    if event == "Submit" or input_text.endswith("\n"):
        # Process the input text (replace with your desired action)
        print(f"You entered: {input_text}")

window.close()

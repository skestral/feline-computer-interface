####################################################################################################
# Program Graphical User Interface
# This file contains the necessary elements to set up and control the UI screens with tkinter
####################################################################################################
import tkinter as tk
from tkinter import ttk

###################
# Main Screen
# this function creates the home screen of the UI with buttons to setup, view logs, export, and quit
###################
def setup_screen(app):
    app.clear_screen() # always start by clearing!
# Window title
    label = tk.Label(app.root, text="Feline Computer Interface", font=("Arial", 20))
    label.pack(pady=20)

# Create buttons to get to other screens
    setup_btn = tk.Button(app.root, text="Setup Session", command=app.setup_session_screen)
    setup_btn.pack(pady=10)

    access_data_btn = tk.Button(app.root, text="Access Data", command=app.access_data_screen)
    access_data_btn.pack(pady=10)

    export_btn = tk.Button(app.root, text="Export Data to CSV", command=app.export_to_csv)
    export_btn.pack(pady=10)

    exit_btn = tk.Button(app.root, text="Exit", command=app.root.quit)
    exit_btn.pack(pady=10)

###################
# Setup Session Screen
# this function creates the session options screen from Main Screen -> Setup -> Run Session
###################
def setup_session_screen(app):
    app.clear_screen() # always start by clearing!

#Window title
    label = tk.Label(app.root, text="Setup Session", font=("Arial", 20))
    label.pack(pady=20)

#Drop down menu to select how long images will stay on screen
    # section label
    interval_label = tk.Label(app.root, text="Select interval (seconds):", font=("Arial", 12))
    interval_label.pack(pady=10)
    # make the drop down menu
    app.interval_var = tk.StringVar()
    app.interval_dropdown = ttk.Combobox(app.root, textvariable=app.interval_var)
    app.interval_dropdown['values'] = [i for i in range(1, 121)]
    app.interval_dropdown.current(4)  # Default to 5 seconds (index 4 since it starts from 0...)
    app.interval_dropdown.pack(pady=10)

# Radio button to pick which API to call from
    animal_label = tk.Label(app.root, text="Select animal type:", font=("Arial", 12))
    animal_label.pack(pady=10)
    # allow user to pick either or both, loop thru options etc
    app.animal_var = tk.StringVar(value="cat")
    animals = [("Cat Images", "cat"), ("Dog Images", "dog"), ("Mixed Images", "mixed")]
    for text, value in animals:
        tk.Radiobutton(app.root, text=text, variable=app.animal_var, value=value).pack(pady=5)

# Start and back buttons
    start_btn = tk.Button(app.root, text="Start Session", command=app.start_session)
    start_btn.pack(pady=10)

    back_btn = tk.Button(app.root, text="Back", command=lambda: setup_screen(app))
    back_btn.pack(pady=10)

###################
# View logs Screen
# this function creates the screen to view the current log. this will display the session_log.txt contents
###################
def access_data_screen(app):
    app.clear_screen() # clear the screen...
#Window label
    label = tk.Label(app.root, text="Access Data", font=("Arial", 20))
    label.pack(pady=20)
#Create a text box to display log contents
    data_text = tk.Text(app.root, height=20, width=100)
    data_text.pack(pady=10)
    #grab the data to display as a string object
    data_text.insert(tk.END, "\n".join(app.session_data)) 
#Back button
    back_btn = tk.Button(app.root, text="Back", command=lambda: setup_screen(app))
    back_btn.pack(pady=10)
    


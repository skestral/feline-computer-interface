####################################################################################################
# catlogger
# catlogger.py is where the core program lives
####################################################################################################

import tkinter as tk
from tkinter import messagebox, filedialog
from ui import setup_screen, setup_session_screen, access_data_screen
from cat_dog_generator import fetch_image_url
import csv
from auth import CAT_API_KEY, DOG_API_KEY  # Import the API keys
from io import BytesIO
from PIL import Image, ImageTk
import requests
import time

###################
# Create CatLoggerApp Class
# Contains core programming as class to call
###################
class CatloggerApp:
    #Create a subclass for managing session data
    class SessionData:
        def __init__(self):
            self.data = []
        # add a new line for logging
        def add_entry(self, entry):
            self.data.append(entry)
        # clear data as called
        def clear(self):
            self.data.clear()

# Setup default values / variables for us to play with
    def __init__(self, root):
        self.root = root
        self.root.title("Feline computer Interface")
        self.root.geometry("800x600")  # basic default window size
        self.session_data = self.SessionData()  # store data
        self.current_stimuli = ["", ""]  # set up to store the two displayed images
        self.api_key = {"cat": CAT_API_KEY, "dog": DOG_API_KEY}  #api keys..
        self.interval = 5000  # set default interval that is populated in the drop down
        self.animal_choice = "cat"  # set the default radio button option
        self.after_id = None
        self.session_count = 0  #keep track of sessions, starts at 0
        self.current_session = ""  #current session starts blank
        self.treat_dispensed = False  # track if a treat was dispensed for our imaginary dispenser and imagionary cat in our imaginary experiment
        self.data_saved = True  # tried setting a flag to manage if data is saved... but its not fully flushed out
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # what to do on close
    # series of function calls to load screens
    def setup_ui(self):
        setup_screen(self)
    def setup_session_screen(self):
        setup_session_screen(self)
    def access_data_screen(self):
        access_data_screen(self)

# function that handles running of a session. displaying images, logging keys, etc
    def start_session(self):
        self.clear_screen()

        # import the user defined time interval
        try:
            self.interval = int(self.interval_var.get()) * 1000  #time is in ms
        except ValueError:
            self.interval = 5000  # set a default just in case an error happens

        # import the user defined API / animal choice
        self.animal_choice = self.animal_var.get()

        # Set up logging
        self.session_count += 1 # increment session count
        self.current_session = f"Session_{self.session_count}" # name of session as session_#
        self.session_data.add_entry(f"Starting {self.current_session} with {self.animal_choice} images at interval {self.interval // 1000} seconds.") # log start of session with some metadata

        #set up grid for session screen layout. two images side by side, buttons under, then log window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        # image placement
        self.stimuli_frame = tk.Frame(self.root)
        self.stimuli_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.stimuli_frame.grid_rowconfigure(0, weight=1)
        self.stimuli_frame.grid_columnconfigure(0, weight=1)
        self.stimuli_frame.grid_columnconfigure(1, weight=1)
        self.stimuli_image_labels = [tk.Label(self.stimuli_frame), tk.Label(self.stimuli_frame)]
        for i in range(2):
            self.stimuli_image_labels[i].grid(row=0, column=i, padx=20, pady=10, sticky="nsew")

        # create buttons on session screen
        self.create_buttons()

        # end button
        end_btn = tk.Button(self.root, text="End Session", command=self.end_session)
        end_btn.grid(row=2, column=0, columnspan=2, pady=20)

        # logging window
        self.log_area = tk.Text(self.root, height=5, width=90)
        self.log_area.grid(row=3, column=0, columnspan=2, pady=10)

        # finally call to display images... stimuli = images in this instance
        self.display_stimuli()

        # start logging feline based key presses
        self.root.bind("<KeyPress>", self.key_press)

    ###################
    # Session Buttons
    # this function creates the buttons that are under each image on screen. These are intended to
    # correlate with a button color or shape for the cat to press during testing. By default we will bind
    # them to A and L keys
    ###################
    def create_buttons(self):
        button_font = ("Arial", 24)

        green_triangle = tk.Button(self.root, text="▲", fg="green", command=lambda: self.key_press("a", 0),
                                   width=5, height=2, font=button_font)
        green_triangle.grid(row=1, column=0, pady=10, sticky="s")

        red_circle = tk.Button(self.root, text="●", fg="red", command=lambda: self.key_press("l", 1),
                               width=5, height=2, font=button_font)
        red_circle.grid(row=1, column=1, pady=10, sticky="s")

    ###################
    # Display Stimuli Images
    # This function will call the images, set their sizes pretending to by dynamic in sizing, and also
    # have some pre-built functionality for an imaginary treat dispenser.
    ###################
    def display_stimuli(self):
        self.treat_dispensed = False  # set treat flag at the load of new images... one treat per round is available!

        max_image_height = self.root.winfo_height() * 0.7  # set images to 70% of current window height
        # image sizes will refresh with each new round, not dynamically!

        # for each image (2 max) grab images and place them as an appropriate size
        for i in range(2):
            image_url = fetch_image_url(self.animal_choice, self.api_key)
            if image_url:
                self.current_stimuli[i] = image_url
                response = requests.get(image_url)
                image_data = Image.open(BytesIO(response.content))

                # figure out what size to make the image, width edition
                base_width = self.root.winfo_width() // 2 - 40 #half window size accounting for padding
                w_percent = (base_width / float(image_data.size[0]))
                h_size = int((float(image_data.size[1]) * float(w_percent)))

                # figure out what size to make the image, height edition
                if h_size > max_image_height:
                    h_size = int(max_image_height)
                    base_width = int((max_image_height / float(image_data.size[1])) * float(image_data.size[0]))
                # resize as needed
                image_data = image_data.resize((base_width, h_size), Image.LANCZOS)

                # add labels with padding and framing info
                image = ImageTk.PhotoImage(image_data)
                self.stimuli_image_labels[i].config(image=image)
                self.stimuli_image_labels[i].image = image

        # log that the images were changed
        self.log_area.insert(tk.END, f"Images cycled at {time.strftime('%H:%M:%S')}\n")
        self.log_area.see(tk.END)
        #set up next round of images
        self.after_id = self.root.after(self.interval,
                                        self.display_stimuli)

    ###################
    # Key Press Handling
    # This function handles the key logging.
    ###################
    def key_press(self, event, index=None):
        treat_dispensed = False
        if index is not None:
            key = event
            stimuli = self.current_stimuli[index] # grab current image to match with key presses
            treat_dispensed = self.trigger_arduino_treat() # calls the empty / placeholder function that would be used to actually dispense a treat
        else:
            key = event.keysym #key press event
            # we only want to care about the A and L keys
            if key == 'a':
                stimuli = self.current_stimuli[0]
                treat_dispensed = self.trigger_arduino_treat()  # only dispense treats on A or L
            elif key == 'l': 
                stimuli = self.current_stimuli[1]
                treat_dispensed = self.trigger_arduino_treat() # only dispense treats on A or L
            else:
                stimuli = "N/A" # don't dispense a treat on any other action
        # log what key was pressed and other metadata -> Log all keys not just A or L
        log_entry = f"{self.current_session}, Key: {key}, Stimuli: {stimuli}, Treat: {treat_dispensed}, Time: {time.strftime('%H:%M:%S')}" 
        self.session_data.add_entry(log_entry) 
        self.log_area.insert(tk.END, log_entry + "\n")
        self.log_area.see(tk.END)
        self.data_saved = False  # set the data saved flag to false since we just made ne data

    ###################
    # Trigger Arduino Treat Dispenser
    # This provides the framework to expand for triggering a hardware device to dispense a treat
    ###################
    def trigger_arduino_treat(self):
        if not self.treat_dispensed: # check if a treat has been given or not
            self.treat_dispensed = True 
            ######                                                                  ######
            ###### insert new code here to trigger arduino or other treat dispenser ######
            ######                                                                  ######
            self.log_area.insert(tk.END, "Treat dispensed!\n")  # log that a treat was dispensed
            self.log_area.see(tk.END)
            return True
        return False

    ###################
    # End session
    # this function handles saving the data and closing tasks before returning to the main screen
    ###################
    def end_session(self):
        self.root.unbind("<KeyPress>")
        if self.after_id:
            self.root.after_cancel(self.after_id)  #stop next task
        self.session_data.add_entry(f"Ending {self.current_session}")  # display status
        self.log_area.insert(tk.END, f"Ending {self.current_session}\n")
        self.save_data() #save data
        setup_screen(self) # return to main screen
        
        
    ###################
    # Save data
    # this function will save data to the session_log.txt... different from the export to csv!
    # this file will always be overwritten and is what is used to display the log in the GUI
    ###################
    def save_data(self):
        try:
            with open("session_log.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(self.session_data.data))
            messagebox.showinfo("Session Ended",
                                "Session data ready to save.")
            self.export_to_csv()
            self.data_saved = True  # Mark data as saved
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session data: {e}")

    ###################
    # Export to CSV
    # this function will grab current data then map to a structure to export as a CSV file for better session
    # data management. This will only happen when a user presses the button on the main screen
    ###################
    def export_to_csv(self):
        try:
            #open the save dialog box to pick a location for saving, set to csv file
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path: # if a file path was selected...
                with open(file_path, "w", newline='', encoding="utf-8") as csvfile:
                    csvwriter = csv.writer(csvfile) # start making the csv
                    csvwriter.writerow(["Session", "Timestamp", "Key Pressed", "Stimuli", "Treat Dispensed"]) # make columns
                    # identify which parts of the string belong in which column then send to csvwriter
                    for entry in self.session_data.data: 
                        parts = entry.split(", ")
                        if len(parts) == 5:  
                            session = parts[0]
                            timestamp = parts[4].split(": ")[1]
                            key = parts[1].split(": ")[1]
                            stimuli = parts[2].split(": ")[1]
                            treat_dispensed = parts[3].split(": ")[1]
                            csvwriter.writerow([session, timestamp, key, stimuli, treat_dispensed])
                        else:
                            csvwriter.writerow([parts[0], "", "", "", ""])
                messagebox.showinfo("Export Successful", "Data exported to CSV successfully.")  #let the user know the data was saved
                self.data_saved = True  #update the save data flag
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data to CSV: {e}")  #handle an unexpected error or cancel

    # clear screen function loops through and removes widgets
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # conditional to decide if an unsaved data window should be displayed before closing the window
    def on_closing(self):
        if not self.data_saved:
            if messagebox.askyesno("Unsaved Data", "You have unsaved data. Do you want to save before exiting?"):
                self.save_data()
        self.root.destroy()
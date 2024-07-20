####################################################################################################
# Feline Computer Interface
# Main file for jumping off 
# catlogger.py - primary functions of the program with logging
# ui.py - handles generating the GUI
# cat_dog_generator.py - handles API calls
# auth.py - stores API keys... for storing keys directly or redirecting to .env
# env.example - example format for .env file 
# requirements.txt - built requirements doc using pipreqs for ease of deployment on SOEC (someone else's computer)
####################################################################################################

import tkinter as tk
from catlogger import CatloggerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = CatloggerApp(root)
    root.mainloop()

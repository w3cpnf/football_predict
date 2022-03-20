import os
os.chdir('D:/Projects/Football/Database/DQ_Code')

import tkinter as tk
#import pandas as pd

import PL_DQ_Club_Queries as db
#define dashboard method and size/height
root = tk.Tk(className = "DQ check for club level, referees and trainer")
canvas = tk.Canvas(root, height = 900, width = 1200)
canvas.pack()



def matchdays_check():
    db.check_matchdays()
    
def clubs_check():
    db.check_clubs()      
    db.check_clubs_home_id()
    
def duplicates_check_staging():
    db.check_duplicates_staging()   
    
def duplicates_check_data():
    db.check_duplicates_data()   

def check_duplicates_features():
    db.check_duplicates_features()   

#headline
headliner_label = tk.Label(root, text = 'DQ Checks', font=('calibre', 14, 'bold')) 
headliner_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.1) 

#Nbr of Matchdays
button_plan = tk.Button(root, text = 'Nbr of Matchdays',command = matchdays_check)
button_plan.pack()
button_plan.place(relx = 0.1, rely = 0.25, relwidth = 0.16, relheight = 0.05)

#Nbr of Clubs
button_results = tk.Button(root, text = 'Nbr of Clubs',command = clubs_check)
button_results.pack()
button_results.place(relx = 0.3, rely = 0.25, relwidth = 0.16, relheight = 0.05)

#Duplicates
button_dup_staging = tk.Button(root, text = 'Duplicates Staging',command = duplicates_check_staging)
button_dup_staging.pack()
button_dup_staging.place(relx = 0.5, rely = 0.25, relwidth = 0.16, relheight = 0.05)

button_dup_data = tk.Button(root, text = 'Duplicates Data',command = duplicates_check_data)
button_dup_data.pack()
button_dup_data.place(relx = 0.7, rely = 0.25, relwidth = 0.16, relheight = 0.05)

button_dup_features = tk.Button(root, text = 'Duplicates Features',command = check_duplicates_features)
button_dup_features.pack()
button_dup_features.place(relx = 0.1, rely = 0.4, relwidth = 0.16, relheight = 0.05)

root.mainloop()
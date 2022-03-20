import os
os.chdir('D:/Projects/Football/Prediction_Code')

import tkinter as tk
from pandastable import Table
#import pandas as pd

import My_Tools_Prediction as t


#define dashboard method and size/height
root = tk.Tk(className = "Prediction Algorithm")
canvas = tk.Canvas(root, height = 900, width = 1200)
canvas.pack()

#define buttons, entries and labels    
saison_label = tk.Label(root, text = 'Season', font=('calibre', 10, 'bold')) 
saison_label.place(relx = 0, rely = 0.06, relwidth = 0.1, relheight = 0.1) 
entry_saison = tk.Entry()
entry_saison.place(relx = 0.1, rely = 0.1, relwidth = 0.05, relheight = 0.02)

spieltag_label = tk.Label(root, text = 'Matchday', font=('calibre', 10, 'bold'))
spieltag_label.place(relx = 0.15, rely = 0.06, relwidth = 0.1, relheight = 0.1) 
entry_spieltag = tk.Entry()
entry_spieltag.place(relx = 0.25, rely = 0.1, relwidth = 0.05, relheight = 0.02)




def get_relevant_gameday():

    season = entry_saison.get()
    gameday = int(entry_spieltag.get())
    df = t.get_relevant_gameday(gameday, season)
    frame = tk.Frame(root)
    frame.pack()
    frame.place(relx = 0.5, rely = 0.5)
    pt = Table(frame, dataframe = df, width = 500, height = 50, showtoolbar=True, showstatusbar=True)
    pt.show()
    


#headline
headliner_label = tk.Label(root, text = 'Schedule', font=('calibre', 14, 'bold')) 
headliner_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.1) 

#random_forest miner
button_gameday= tk.Button(root, text = 'Get schedule of gameday',command = get_relevant_gameday)
button_gameday.pack()
button_gameday.place(relx = 0.01, rely = 0.4, relwidth = 0.25, relheight = 0.05)



root.mainloop()



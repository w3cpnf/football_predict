import os
os.chdir('D:/Projects/Football/Prediction_Code')

import tkinter as tk
import pandas as pd
from pandastable import Table
#import pandas as pd

import My_Tools_Prediction as t
import Get_Logistic_Regression as lr

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

vereins_id_label = tk.Label(root, text = 'Club ID', font=('calibre', 10, 'bold'))
vereins_id_label.place(relx = 0.3, rely = 0.06, relwidth = 0.1, relheight = 0.1) 
entry_vereins_id = tk.Entry()
entry_vereins_id.place(relx = 0.4, rely = 0.1, relwidth = 0.05, relheight = 0.02)

test_length_label = tk.Label(root, text = 'Proba Threshold For Length', font=('calibre', 10, 'bold'))
test_length_label.place(relx = 0.5, rely = 0.02, relwidth = 0.2, relheight = 0.1) 

test_length_label_1 = tk.Label(root, text = 'Length 1', font=('calibre', 10, 'bold'))
test_length_label_1.place(relx = 0.5, rely = 0.1, relwidth = 0.2, relheight = 0.1) 
entry_test_length_1 = tk.Entry()
entry_test_length_1.place(relx = 0.65, rely = 0.14, relwidth = 0.04, relheight = 0.02)

test_length_label_2 = tk.Label(root, text = 'Length 2', font=('calibre', 10, 'bold'))
test_length_label_2.place(relx = 0.7, rely = 0.1, relwidth = 0.2, relheight = 0.1) 
entry_test_length_2 = tk.Entry()
entry_test_length_2.place(relx = 0.85, rely = 0.14, relwidth = 0.05, relheight = 0.02)

test_length_label_3 = tk.Label(root, text = 'Length 3', font=('calibre', 10, 'bold'))
test_length_label_3.place(relx = 0.5, rely = 0.18, relwidth = 0.2, relheight = 0.1) 
entry_test_length_3 = tk.Entry()
entry_test_length_3.place(relx = 0.65, rely = 0.22, relwidth = 0.04, relheight = 0.02)

features_label = tk.Label(root, text = 'Features', font=('calibre', 10, 'bold'))
features_label.place(relx = -0.05, rely = 0.12, relwidth = 0.2, relheight = 0.1) 
entry_features = tk.Entry()
entry_features.place(relx = 0.1, rely = 0.16, relwidth = 0.2, relheight = 0.02)

def get_relevant_gameday():
    #define global dataframe (can be used in other functions)
    #season = entry_saison.get()
    gameday = int(entry_spieltag.get())
    df = t.get_relevant_gameday(gameday)
    frame = tk.Frame(root)
    frame.pack()
    frame.place(relx = 0.5, rely = 0.5)
    pt = Table(frame, dataframe = df, width = 500, height = 50, showtoolbar=True, showstatusbar=True)
    pt.show()
    
 
    
def get_log_reg_miner():
    vereins_id = int(entry_vereins_id.get())
    threshold_1 = float(entry_test_length_1.get())
    threshold_2 = float(entry_test_length_2.get())
    threshold_3 = float(entry_test_length_3.get())
    
    global df_miner_logreg
    df_miner_logreg = pd.DataFrame()   
    
    df = lr.log_reg_miner(vereins_id, threshold_1, threshold_2, threshold_3)
    df_miner_logreg = df_miner_logreg.append(df)
    
    frame = tk.Frame(root)
    frame.pack()
    frame.place(relx = 0.5, rely = 0.5)
    pt = Table(frame, dataframe = df_miner_logreg, width = 500, height = 50, showtoolbar=True, showstatusbar=True)
    pt.show()
    print("done")   
    
def get_log_reg_prediction():
    spieltag = int(entry_spieltag.get())
    vereins_id = int(entry_vereins_id.get())
    features = str(entry_features.get())
    saison = entry_saison.get()
    lr.log_reg(vereins_id, saison, spieltag, features)
    print("done")   
    
    
#headline
headliner_label = tk.Label(root, text = 'Prediction Algorithm', font=('calibre', 14, 'bold')) 
headliner_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.1) 

#random_forest miner
button_gameday= tk.Button(root, text = 'Get schedule of gameday',command = get_relevant_gameday)
button_gameday.pack()
button_gameday.place(relx = 0.01, rely = 0.4, relwidth = 0.25, relheight = 0.05)


#logReg Miner
button_log_reg_miner = tk.Button(root, text = 'Get best features for logistic regression',command = get_log_reg_miner)
button_log_reg_miner.pack()
button_log_reg_miner.place(relx = 0.01, rely = 0.5, relwidth = 0.25, relheight = 0.05)

#logReg
button_log_reg = tk.Button(root, text = 'Prediction based on logistic regression',command = get_log_reg_prediction)
button_log_reg.pack()
button_log_reg.place(relx = 0.01, rely = 0.55, relwidth = 0.25, relheight = 0.05)
root.mainloop()



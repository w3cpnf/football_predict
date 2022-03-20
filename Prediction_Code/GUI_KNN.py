import os
os.chdir('D:/Projects/Football/Prediction_Code')

import tkinter as tk
import pandas as pd
from pandastable import Table
#import pandas as pd

import Get_KNN_Predictions as knn
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

vereins_id_label = tk.Label(root, text = 'Club ID', font=('calibre', 10, 'bold'))
vereins_id_label.place(relx = 0.3, rely = 0.06, relwidth = 0.1, relheight = 0.1) 
entry_vereins_id = tk.Entry()
entry_vereins_id.place(relx = 0.4, rely = 0.1, relwidth = 0.05, relheight = 0.02)

test_length_label = tk.Label(root, text = 'Proba Threshold For Length', font=('calibre', 10, 'bold'))
test_length_label.place(relx = 0.5, rely = 0.02, relwidth = 0.2, relheight = 0.1) 

test_length_label_1 = tk.Label(root, text = 'Threshold for 10', font=('calibre', 10, 'bold'))
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

n_neighbors_label = tk.Label(root, text = 'N neighbors', font=('calibre', 10, 'bold'))
n_neighbors_label.place(relx = -0.05, rely = 0.18, relwidth = 0.2, relheight = 0.1) 
entry_n_neighbors = tk.Entry()
entry_n_neighbors.place(relx = 0.1, rely = 0.22, relwidth = 0.05, relheight = 0.02)

metric_label = tk.Label(root, text = 'Metric', font=('calibre', 10, 'bold'))
metric_label.place(relx =  -0.05, rely = 0.24, relwidth = 0.2, relheight = 0.1) 
entry_metric = tk.Entry()
entry_metric.place(relx = 0.1, rely = 0.28, relwidth = 0.04, relheight = 0.02)

p_label = tk.Label(root, text = 'Power Parameter', font=('calibre', 10, 'bold'))
p_label.place(relx = 0.15, rely = 0.18, relwidth = 0.2, relheight = 0.1) 
entry_p = tk.Entry()
entry_p.place(relx = 0.32, rely = 0.22, relwidth = 0.04, relheight = 0.02)


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
    

   
def get_knn_miner():
    vereins_id = int(entry_vereins_id.get())
    threshold_1 = float(entry_test_length_1.get())
    threshold_2 = float(entry_test_length_2.get())
    threshold_3 = float(entry_test_length_3.get())
    global df_miner_knn
    df_miner_knn = pd.DataFrame()   
    
    df = knn.knn_prediction_miner(vereins_id, threshold_1, threshold_2, threshold_3)
    df_miner_knn = df_miner_knn.append(df)
    
    frame = tk.Frame(root)
    frame.pack()
    frame.place(relx = 0.5, rely = 0.5)
    pt = Table(frame, dataframe = df_miner_knn, width = 500, height = 50, showtoolbar=True, showstatusbar=True)
    pt.show()
    print("done")   
    
    
def get_knn_prediction():
    
    spieltag = int(entry_spieltag.get())
    vereins_id = int(entry_vereins_id.get())
    saison = entry_saison.get()
    features = entry_features.get()
    n = int(entry_n_neighbors.get())
    m = entry_metric.get()
    p = int(entry_p.get())
    
    knn.knn(vereins_id, saison, spieltag, features, n, m, p)
    print("done")    
    

    
    
#headline
headliner_label = tk.Label(root, text = 'KNN Prediction', font=('calibre', 14, 'bold')) 
headliner_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.1) 

#random_forest miner
button_gameday= tk.Button(root, text = 'Get schedule of gameday',command = get_relevant_gameday)
button_gameday.pack()
button_gameday.place(relx = 0.01, rely = 0.4, relwidth = 0.25, relheight = 0.05)


#knn miner
button_knn_miner = tk.Button(root, text = 'Get best features for KNN ',command = get_knn_miner)
button_knn_miner.pack()
button_knn_miner.place(relx = 0.01, rely = 0.5, relwidth = 0.25, relheight = 0.05)

#knn
button_knn = tk.Button(root, text = 'Prediction based on knn regression',command = get_knn_prediction)
button_knn.pack()
button_knn.place(relx = 0.01, rely = 0.55, relwidth = 0.25, relheight = 0.05)


root.mainloop()





import os
os.chdir('D:/Projects/Football/Database/DQ_Code')

import tkinter as tk
#import pandas as pd

import DQ_Prediction as dq

#define dashboard method and size/height
root = tk.Tk(className = "DQ check used queries as prediction base")
canvas = tk.Canvas(root, height = 900, width = 1200)
canvas.pack()


def data_set_check_used():
    dq.check_data_set_used()
    
def data_set_check_all():
    dq.check_data_set_possible()
    
def data_set_check_used_pl():
    dq.check_data_set_used_pl()    

#headline
headliner_label = tk.Label(root, text = 'DQ check used queries as prediction base', font=('calibre', 14, 'bold')) 
headliner_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.1) 

#gameplan
button_check1 = tk.Button(root, text = 'Query Check Use',command = data_set_check_used)
button_check1.pack()
button_check1.place(relx = 0.1, rely = 0.25, relwidth = 0.16, relheight = 0.05)

button_check2 = tk.Button(root, text = 'Query Check All',command = data_set_check_all)
button_check2.pack()
button_check2.place(relx = 0.3, rely = 0.25, relwidth = 0.16, relheight = 0.05)

#gameplan
button_check3 = tk.Button(root, text = 'Query Check Use PL',command = data_set_check_used_pl)
button_check3.pack()
button_check3.place(relx = 0.5, rely = 0.25, relwidth = 0.16, relheight = 0.05)

root.mainloop()
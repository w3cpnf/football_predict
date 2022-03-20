import os
os.chdir('D:/Projects/Football/Database/DQ_Code')


import DQ_Prediction_Queries as db



def check_data_set_used():
    
    f1 = db.get_data_db(2)
    df_spieltag = f1.get_data()
    print(df_spieltag)
    
    f2 = db.get_data_db(3)
    df_all = f2.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            nbr_duplicates = len(df_s) - len(df_s.drop_duplicates())
            print(nbr_duplicates)
            print("duplicates in saison")
            print(s)      
            
    f3 = db.get_data_db(1)
    df_nbr = f3.get_data()
     
    
    #print(df_spieltag['Spieltag'])
    
    if len(df_nbr)==0:
        print(" ")
        print('Nbr of clubs for all matchdays is correct')
    else:
        
        print(df_nbr)
        
    print("done")

def check_data_set_used_pl():
    
    f1 = db.get_data_db(8)
    df_spieltag = f1.get_data()
    print(df_spieltag)
    
    f2 = db.get_data_db(9)
    df_all = f2.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            nbr_duplicates = len(df_s) - len(df_s.drop_duplicates())
            print(nbr_duplicates)
            print("duplicates in saison")
            print(s)      
            
    f3 = db.get_data_db(7)
    df_nbr = f3.get_data()
     
    
    #print(df_spieltag['Spieltag'])
    
    if len(df_nbr)==0:
        print(" ")
        print('Nbr of clubs for all matchdays is correct')
    else:
        
        print(df_nbr)
        
    print("done")
    
def check_data_set_possible():
    
    f1 = db.get_data_db(5)
    df_spieltag = f1.get_data()
    print(df_spieltag)
    
    f2 = db.get_data_db(6)
    df_all = f2.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            nbr_duplicates = len(df_s) - len(df_s.drop_duplicates())
            print(nbr_duplicates)
            print("duplicates in saison")
            print(s)      
            
    f3 = db.get_data_db(4)
    df_nbr = f3.get_data()
     
    
    #print(df_spieltag['Spieltag'])
    
    if len(df_nbr)==0:
        print(" ")
        print('Nbr of clubs for all matchdays is correct')
    else:
        
        print(df_nbr)
        
    print("done")
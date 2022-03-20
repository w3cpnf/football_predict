import os
os.chdir('D:/Projects/Football/Database/DQ_Code')

import DQ_Player_Queries as db



def check_kader():
    
    f1 = db.get_data_db(1)
    df_spieltag = f1.get_data()
    
    f2 = db.get_data_db(2)
    df_nbr = f2.get_data()
    
    print("Nbr of clubs per Saison and transfer window: ")
    if len(df_nbr)==0:
        print(" ")
        print("No Team with critical low player number in team")
        print(" ")
    else:
        print(df_nbr)
        print("Nbr of player within a season with a critical nbr within a team: ")
    
    if len(df_spieltag)==0:
        print(" ")
        print("Nbr of clubs per Saison is fine")
        print(" ")
    else:
        print(df_spieltag)
        
    f4 = db.get_data_db(4)
    df_nbr_clubs = f4.get_data()
    
    if len(df_nbr_clubs)==0:
        print(" ")
        print("Correct Nbr of Teams per Saison")
        print(" ")
    else:
        print(df_nbr_clubs)
        print("Nbr of Teams within a season is not correct: ")
        
    f3 = db.get_data_db(3)
    df_all = f3.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)  
       
            
def check_master_player_config():
    
    f1 = db.get_data_db(5)
    df_spieltag = f1.get_data()
    
    f2 = db.get_data_db(6)
    df_nbr = f2.get_data()
    
    print("Nbr of clubs per Saison and transfer window: ")
    print(df_nbr)
    print("Nbr of player within a season with a critical nbr within a team: ")

    if len(df_spieltag)==0:
        print(" ")
        print("All fine")
    else:
        print(df_spieltag)
        
    f3 = db.get_data_db(7)
    df_all = f3.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)               
            
def check_url():
    
    f1 = db.get_data_db(8)
    df_spieltag = f1.get_data()
    
    f2 = db.get_data_db(9)
    df_nbr = f2.get_data()
    
    print("Nbr of clubs per Season: ")
    print(df_spieltag)
    
    print("Nbr of player within a season with a critical nbr within a team: ")

    if len(df_nbr)==0:
        print("**************")
        print("All fine")
    else:
        print(df_nbr)
        
    f3 = db.get_data_db(10)
    df_all = f3.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)          


            
def check_master_player():
       
    f3 = db.get_data_db(11)
    df = f3.get_data() 

    if len(df.drop_duplicates('Spieler'))==len(df):
        print("No duplicates in the table master_player")
    else:
        print("duplicates Spieler_ID")

def check_age_worth():
    
    f1 = db.get_data_db(12)
    df_spieltag = f1.get_data()
    
    print("Nbr of clubs per Saison: ")
    print(df_spieltag)
    print("***************")
    print("Nbr of player within a season with a critical nbr within a team: ")
    
    f2 = db.get_data_db(43)
    df_nbr_clubs = f2.get_data()
    
    if len(df_nbr_clubs)==0:
        print("***************")
        print("All fine")
        
    else:
        print(df_nbr_clubs)  
        
    print("***************")      
    f3 = db.get_data_db(13)
    df_nbr_players = f3.get_data()      
    print("***************")
    print("Critical numbers of players in matchday")
    print(df_nbr_players)

    f4 = db.get_data_db(14)
    df_all = f4.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)      
            
    print("done")
            
def player_mapping_config_duplicate_check():

    f1 = db.get_data_db(10)
    df_mapping = f1.get_data()
    
    df_spieler = df_mapping[['Spieler', 'Spieler_ID']].drop_duplicates()
    
    spieler_id = df_spieler.drop_duplicates('Spieler')
    print("***************")    
    if len(spieler_id[spieler_id.duplicated('Spieler_ID')])==0:
        print(" ")
        print('No Player with a double ID in the mapping')
    else:
        print("Player with double ID in the Mapping:")
        print(spieler_id[spieler_id.duplicated('Spieler_ID')])
        
    print("***************")        
    spieler = df_spieler.drop_duplicates('Spieler_ID')
    if len(spieler[spieler.duplicated('Spieler')])==0:  
        print(" ")
        print('No Id with a double ID in the mapping')    
    else:
        print(spieler[spieler.duplicated('Spieler')])  
        
    if len(df_mapping)==len(df_mapping.drop_duplicates()):
        print(" ")
        print("No Duplicated Values in the mapping")
        
        
def check_player_staging_daten():
    
    f1 = db.get_data_db(16)
    df_nbr = f1.get_data()
    print("***************")  
    print("Nbr of matchdays per Saison: ")
    print(df_nbr)
    print("***************")  
    f2 = db.get_data_db(17)
    df = f2.get_data()
    if len(df)==0:
        print(" ")
        print("No critical nbr of players within a team")
    else:
        print(df)
    print("***************")  
    f4 = db.get_data_db(18)
    df_nbr_clubs = f4.get_data()  
    
    if len(df_nbr_clubs)==0:
        print(" ")
        print("Correct Nbr of Teams per Season and Matchday")
        print(" ")
    else:
        print(df_nbr_clubs)
        print("Nbr of Teams within a season is not correct: ")
        
    f3 = db.get_data_db(15)
    df_all = f3.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)  
  
    
def check_player_data_daten():
    
    f1 = db.get_data_db(20)
    df_nbr = f1.get_data()
    print("***************")  
    print("Nbr of matchdays per Saison: ")
    print(df_nbr)
    print("***************")  
    f2 = db.get_data_db(21)
    df = f2.get_data()
    if len(df)==0:
        print(" ")
        print("No critical nbr of players within a team")
    else:
        print(df)
    print("***************")  
    f4 = db.get_data_db(22)
    df_nbr_clubs = f4.get_data()  
    
    if len(df_nbr_clubs)==0:
        print(" ")
        print("Correct Nbr of Teams per Season and Matchday")
        print(" ")
    else:
        print(df_nbr_clubs)
        print("Nbr of Teams within a season is not correct: ")
        
    f3 = db.get_data_db(19)
    df_all = f3.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)
        
def check_kicker_daten():
    
    f1 = db.get_data_db(27)
    df_nbr = f1.get_data()
    print("Number of Teams per Season:")
    print("")
    print(df_nbr)
    print(" ")
    
    f2 = db.get_data_db(28)
    df_player = f2.get_data()
    print(" ")
    print("Nbr of Players with critical number of players for a matchday: ")
    print(df_player)
    print(" ")
    
    f3 = db.get_data_db(30)
    df_critical = f3.get_data()    
    if len(df_critical)==0:
        print(" ")
        print("All Fine")
        print(" ")
    else:
        print(df_critical)   
        print(" ")
        
    f5 = db.get_data_db(31)
    df_matchdays = f5.get_data()  
    print("Nbr Matchdays per Season: ")
    print(" ")
    print(df_matchdays)
    print(" ")
    
    f4 = db.get_data_db(29)
    df_all = f4.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)
        
def player_kader_duplicate_check():

    f1 = db.get_data_db(3)
    df_kader = f1.get_data()
    
    df_spieler = df_kader[['Spieler', 'Spieler_ID']].drop_duplicates()

    spieler_id = df_spieler.drop_duplicates('Spieler')
    if len(spieler_id[spieler_id.duplicated('Spieler_ID')])==0:
        print(" ")
        print('No Player with a double ID in the kader')
    else:
        print("Problem with")
        print(spieler_id[spieler_id.duplicated('Spieler_ID')])
    
    spieler = df_spieler.drop_duplicates('Spieler_ID')
    if len(spieler[spieler.duplicated('Spieler')])==0:  
        print(" ")
        print('No Id with a double ID in the kader')    
    else:
        print("Problem with")
        print(spieler[spieler.duplicated('Spieler')])  
        
    if len(df_kader)==len(df_kader.drop_duplicates()):
        print(" ")
        print("No Duplicated Values in the Kader")    
  
    
    
    
def player_staging_daten_duplicate_check():

    f1 = db.get_data_db(15)
    df_daten = f1.get_data()
    
    spieler_id = df_daten.drop_duplicates('Spieler')
    if len(spieler_id[spieler_id.duplicated('Spieler_ID')])==0:
        print(" ")
        print('No Player with a double ID in the data table')
    else:
        print(spieler_id[spieler_id.duplicated('Spieler_ID')])
    
    spieler = df_daten.drop_duplicates('Spieler_ID')
    if len(spieler[spieler.duplicated('Spieler')])==0:  
        print(" ")
        print('No Id with a double ID in the data table')    
    else:
        print(spieler[spieler.duplicated('Spieler')])  
        
    if len(df_daten)==len(df_daten.drop_duplicates()):
        print(" ")
        print("No Duplicated Values in the data table")          
    
    
    
def kicker_duplicate_check():

    f = db.get_data_db(40)
    df = f.get_data()
    print(df['Saison'].drop_duplicates())
    saisons = df['Saison'].drop_duplicates()
    
    for s in saisons:
        df_daten = df[df['Saison']==s]
            
        if len(df_daten)==len(df_daten.drop_duplicates()):
            print(" ")
            print("No Duplicated Values in the data table for saison " +str(s))   
            
            

def check_perf_daten():
    
    f1 = db.get_data_db(32)
    df_nbr = f1.get_data()
    print("Number of Teams per Season:")
    print("")
    print(df_nbr)
    print(" ")
    
    f2 = db.get_data_db(25)
    df_player = f2.get_data()
    print(" ")
    print("Nbr of Players with critical number of players for a matchday: ")
    print(df_player)
    print(" ")
    
    f3 = db.get_data_db(24)
    df_critical = f3.get_data()    
    if len(df_critical)==0:
        print(" ")
        print("All Fine")
        print(" ")
    else:
        print(df_critical)   
        print(" ")
        
    f5 = db.get_data_db(23)
    df_matchdays = f5.get_data()  
    print("Nbr Matchdays per Season: ")
    print(" ")
    print(df_matchdays)
    print(" ")
    
    f4 = db.get_data_db(26)
    df_all = f4.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)


def check_startelf_daten():
    
    f1 = db.get_data_db(33)
    df_nbr = f1.get_data()
    print("Number of Teams per Season:")
    print("")
    print(df_nbr)
    print(" ")
    
    f2 = db.get_data_db(34)
    df_player = f2.get_data()
    print(" ")
    print("Nbr of Players with critical number of players for a matchday: ")
    print(df_player)
    print(" ")
    
    f3 = db.get_data_db(36)
    df_critical = f3.get_data()    
    if len(df_critical)==0:
        print(" ")
        print("All Fine")
        print(" ")
    else:
        print(df_critical)   
        print(" ")
        
    f5 = db.get_data_db(37)
    df_matchdays = f5.get_data()  
    print("Nbr Matchdays per Season: ")
    print(" ")
    print(df_matchdays)
    print(" ")
    
    f4 = db.get_data_db(35)
    df_all = f4.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)
            
            
def check_injuries_daten():
    
    f1 = db.get_data_db(38)
    df_matchdays = f1.get_data()  
    print("Nbr Matchdays per Season: ")
    print(" ")
    print(df_matchdays)
    print(" ")

    f2 = db.get_data_db(41)
    df_date = f2.get_data()    
    if len(df_date)==0:
        print(" ")
        print("Dates and Matchdays are all fitting")
        print(" ")
    else:
        print(df_date)   
        print(" ")
    
    f3 = db.get_data_db(42)
    df_player = f3.get_data()
    print(" ")
    print("Nbr of Players with critical number of players for a matchday: ")
    print(df_player)
    print(" ")
    
    f4 = db.get_data_db(40)
    df_teams = f4.get_data()
    print(" ")
    print("Nbr of Teams within a season: ")
    print(df_teams)
    print(" ")        

    
    f5 = db.get_data_db(39)
    df_all = f5.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)
            
def check_injuries_staging():
    
    f1 = db.get_data_db(44)
    df_matchdays = f1.get_data()  
    print("Nbr injured players per Season: ")
    print(" ")
    print(df_matchdays)
    print(" ")
    
    f5 = db.get_data_db(45)
    df_all = f5.get_data() 
    saisons = df_all['Saison'].drop_duplicates()    
    for s in saisons:
        df_s = df_all[df_all['Saison']==s]
        if len(df_s.drop_duplicates())==len(df_s):
            print("No duplicates in saison ")
            print(s)
        else:
            print("duplicates in saison")
            print(s)
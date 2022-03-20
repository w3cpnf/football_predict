import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
import My_Tools as t

#import other files 
import Read_Load_Database as db


def getNewPlayer(df):
    
    dfPlayerID = df[['Spieler']] 
    f = t.unify_letters(dfPlayerID, 1)
    dfPlayerID = f.replace_letters()
    dfPlayerID = dfPlayerID.drop_duplicates()
    
    df_id = db.get_table('master_spieler_id')
    player_missing = t.get_new_player(dfPlayerID, df_id)  
    player_missing['Spieler_ID'] = range(df_id.tail(1).iloc[0,0]+1,df_id.tail(1).iloc[0,0]+len(player_missing)+1)
    player_missing = player_missing[['Spieler_ID', 'Spieler']]
        
    return player_missing

dfSquadBundesliga = db.get_table('bl1_staging_squad_api')
dfSquadBundesliga['Spieler'] = dfSquadBundesliga['player.firstname']+ " " + dfSquadBundesliga['player.lastname']
f = t.unify_letters(dfSquadBundesliga, 1)
dfPlayerID = f.replace_letters()
dfPlayerID = dfPlayerID[['Spieler', 'player.id', 'player.name', 'player.firstname', 'player.lastname']]

dfPlayerID = dfPlayerID.rename(columns = {'player.id':'Spieler_ID_Api', 'player.name':'Name', 'player.firstname':'Vorname',
                          'player.lastname':'Nachname'}) 
dfPlayerID = dfPlayerID.drop_duplicates()
dfPlayerID['Spieler_ID'] = range(1, len(dfPlayerID)+1)

db.upload_local_data_to_database(dfPlayerID, "master_spieler_api")
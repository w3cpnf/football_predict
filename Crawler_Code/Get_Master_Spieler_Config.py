import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

import Read_Load_Database as db
import pandas as pd


def get_player_config(c, saison, transferfenster):

    f3 = db.get_data_db(7)
    df_mapping_transfermarkt = f3.get_data()   
    df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
    v1 = df_mapping_transfermarkt['Vereins_ID'].iloc[c-1]
    v2 = df_mapping_transfermarkt['Verein'].iloc[c-1]
    print(v2)
    
    f_k =db.get_data_db(12)
    df_kader = f_k.get_data()
    
    df_kader = df_kader[df_kader['Vereins_ID']==v1]
    df_kader = df_kader[df_kader['Saison']==saison]
    df_kader = df_kader[df_kader['Transferfenster']==transferfenster]
    df_kader = df_kader[['Saison', 'Verein', 'Spieler', 'Spieler_ID', 'Vereins_ID']]
    
    df_complete = pd.DataFrame()
    
    if transferfenster == 1:
        for i in range(1,18):
            df_kader = df_kader.assign(Spieltag = i)
            df_complete = df_complete.append(df_kader)

    if transferfenster == 2:
        for i in range(18,35):
            df_kader = df_kader.assign(Spieltag = i)
            df_complete = df_complete.append(df_kader)
            
    return df_complete
#df = get_player_config(10, '2019/20', 2)
#db.upload_local_data_to_database(df, 'bl1_master_spieler_config')
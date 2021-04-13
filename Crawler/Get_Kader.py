import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
#import other files 
import My_Tools as t
import Read_Load_Database as db


def get_kader(c, saison):
    
    
    df_complete = pd.DataFrame()
    f3 = db.get_data_db(7)
    df = f3.get_data()
    df = df[df['Saison']==saison]
    l_verein_transfermakrt = df['Verein_Transfermarkt']
    id_transfermakrt = df['ID_Transfermarkt']
    l_Verein = df['Verein']
    id_Verein = df['Vereins_ID']

    v1 = l_verein_transfermakrt.iloc[c-1]
    v2 = id_transfermakrt.iloc[c-1]
    v3 = l_Verein.iloc[c-1]
    v4 = id_Verein.iloc[c-1]
    transfermarkt_saison = saison[0:4]
    
    url = 'https://www.transfermarkt.de/'+str(v1)+'/startseite/verein/'+str(v2)+'/saison_id/'+str(transfermarkt_saison)
   
   #https://www.transfermarkt.de/borussia-dortmund/startseite/verein/16?saison_id=2015 
   
    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    driver.get(url)
    
    time.sleep(5)
    
    player_o = WebDriverWait(driver,10).until(t.find_player_1) 
    player_e = WebDriverWait(driver,10).until(t.find_player_2)  
    
    player_1 = t.get_list(player_o)
    player_2 = t.get_list(player_e)

    
    if v4 != 4:# and v4 != 3: #v4 != 4 and:

        df_player_1 = pd.DataFrame(player_1)
        df_player_1 = df_player_1[0].str.split('\n', expand = True)
        df_player_1[1] = df_player_1[1].astype(str)
        indexNames = df_player_1[df_player_1[1]=='None'].index
        df_player_1.drop(indexNames, inplace=True)
        df_player_1[3] = df_player_1[3].map(str) + df_player_1[4].map(str) 
        df_player_1[3] = df_player_1[3].str.split('€', expand = True)
        df_player_1 = df_player_1.drop(columns = [0,4], axis = 1)
        df_1 = df_player_1[[1,2]]
        df_2 = df_player_1[3].str.split('(', expand = True)
        df_3 = df_2[[0]]
        df_4 = df_2[1].str.split(')', expand = True)
        df_2 = df_4[[0]]
        df_5 = df_4[[1]]
        df_all_1 = pd.concat([df_1, df_2, df_3, df_5], axis = 1)
        df_all_1.columns = ['Spieler', 'Position', 'Alter', 'Geburtstag', 'Wert']
        
          
        df_player_2 = pd.DataFrame(player_2)
        df_player_2 = df_player_2[0].str.split('\n', expand = True)
        df_player_2[1] = df_player_2[1].astype(str)
        indexNames = df_player_2[df_player_2[1]=='None'].index
        df_player_2.drop(indexNames, inplace=True)
        df_player_2[3] = df_player_2[3].map(str) + df_player_2[4].map(str) 
        df_player_2[3] = df_player_2[3].str.split('€', expand = True)
        df_player_2 = df_player_2.drop(columns = [0,4], axis = 1)
        df_1 = df_player_2[[1,2]]
        df_2 = df_player_2[3].str.split('(', expand = True)
        df_3 = df_2[[0]]
        df_4 = df_2[1].str.split(')', expand = True)
        df_2 = df_4[[0]]
        df_5 = df_4[[1]]
        df_all_2 = pd.concat([df_1, df_2, df_3, df_5], axis = 1)
        df_all_2.columns = ['Spieler', 'Position', 'Alter', 'Geburtstag', 'Wert']
        
        df_all = pd.concat([df_all_1, df_all_2], axis = 0, ignore_index = True)
        df_all = df_all.assign(Vereins_ID = v4, Verein = v3)
    
        df_complete = df_complete.append(df_all)
        driver.quit()

    else:
   
        df_player_1 = pd.DataFrame(player_1)
        df_player_1 = df_player_1[0].str.split('\n', expand = True)
        df_player_1[1] = df_player_1[1].astype(str)
        indexNames = df_player_1[df_player_1[1]=='None'].index
        df_player_1.drop(indexNames, inplace=True)
        #df_player_1[3] = df_player_1[3].map(str) + df_player_1[4].map(str) 
        df_player_1[3] = df_player_1[3].str.split('€', expand = True)
        df_player_1 = df_player_1.drop(columns = [0], axis = 1)

        df_1 = df_player_1[[1,2]]
        df_2 = df_player_1[3].str.split('(', expand = True)
        df_3 = df_2[[0]]
        df_4 = df_2[1].str.split(')', expand = True)
        df_2 = df_4[[0]]
        df_5 = df_4[[1]]
        df_all_1 = pd.concat([df_1, df_2, df_3, df_5], axis = 1)
        df_all_1.columns = ['Spieler', 'Position', 'Alter', 'Geburtstag', 'Wert']

          
        df_player_2 = pd.DataFrame(player_2)
        df_player_2 = df_player_2[0].str.split('\n', expand = True)
        df_player_2[1] = df_player_2[1].astype(str)
        indexNames = df_player_2[df_player_2[1]=='None'].index
        df_player_2.drop(indexNames, inplace=True)
        #df_player_2[3] = df_player_2[3].map(str) + df_player_2[4].map(str) 
        df_player_2[3] = df_player_2[3].str.split('€', expand = True)
        df_player_2 = df_player_2.drop(columns = [0], axis = 1)
        df_1 = df_player_2[[1,2]]
        df_2 = df_player_2[3].str.split('(', expand = True)
        df_3 = df_2[[0]]
        df_4 = df_2[1].str.split(')', expand = True)
        df_2 = df_4[[0]]
        df_5 = df_4[[1]]
        df_all_2 = pd.concat([df_1, df_2, df_3, df_5], axis = 1)
        df_all_2.columns = ['Spieler', 'Position', 'Alter', 'Geburtstag', 'Wert']
        
        df_all = pd.concat([df_all_1, df_all_2], axis = 0, ignore_index = True)
        df_all = df_all.assign(Vereins_ID = v4, Verein = v3)
    
        df_complete = df_complete.append(df_all)
        driver.quit()
        
    f_l = t.unify_letters(df_complete, 1)
    df_complete = f_l.replace_letters()

    df_complete['Spieler'] = df_complete['Spieler'].str.replace("*","")
    df_complete['Spieler'] = df_complete['Spieler'].str.replace(".","")
    df_complete['Wert'] = df_complete['Wert'].str.strip()
    df_complete['Spieler'] = df_complete['Spieler'].str.strip()
    df_complete = df_complete.replace({'Jan-Ingwer Callsen-Bracker':'J. Callsen-Bracker', 'Cedrick Makiadi':'Cedric Makiadi', 'Pierre-Emerick Aubameyang':'P. Aubameyang', 'Anderson':'Bamba Anderson',
                             'Roberto Firmino':'R. Barbosa de Oliveira', 'Ja-Cheol Koo':'Ja-cheol Koo', 'Klaas Jan Huntelaar':'Klaas-Jan Huntelaar', 
                             'Eric Maxim Choupo-Moting':'E. Choupo-Moting', 'Luiz Gustavo':'Luiz Gustavo Dias','Marcelo':'M. Guedes Filho', 'Zoltan Stieber':'Stiebi',
                             'Per Ciljan Skjelbred':'Per Skjelbred', 'Jairo':'Jairo Samperio', 'Rafa Lopez':'Rafael Lopez', 'Pierre-Emile Höjbjerg':'Pierre-Emile Hojbjerg',
                             'Mats Möller Daehli':'Mats Möller Dæhli', 'Baard Finne':'Bard Finne', 'Joao Pereira':'J. da Silva Pereira', 'Serey Die':'Geoffroy Serey Die',
                             'Tolga Cigerci':'Tolga Ciğerci', 'Jose Manuel Reina':'Jose Reina'})
    
    df_complete = df_complete.drop_duplicates()
    #df_complete = df_complete[df_complete['Geburtstag']!='k. A.']
    # ind_1 = df_complete[df_complete['Spieler']=='Gonzalo Castro'].index
    # ind_2 = df_complete[df_complete['Spieler']=='Karim Bellarabi'].index
    # ind_3 = df_complete[df_complete['Spieler']=='Ömer Toprak'].index
    #ind_4 = df_complete[df_complete['Spieler']=='Hakan Calhanoglu'].index
    ind_5 = df_complete[df_complete['Spieler']=='Daniel Thur'].index
    ind_6 = df_complete[df_complete['Spieler']=='Johannes Wolff'].index
    ind_7 = df_complete[df_complete['Spieler']=='Liam Fisch'].index
    
    # df_complete.iloc[ind_1, 4]='14,00 Mio.'
    # df_complete.iloc[ind_2, 4]='8,00 Mio.'
    # df_complete.iloc[ind_3, 4]='18,00 Mio.'
    # df_complete.iloc[ind_4, 4]='18,00 Mio.'
    df_complete.iloc[ind_5, 3]='28.04.1998'
    df_complete.iloc[ind_6, 3]='10.07.1998'
    df_complete.iloc[ind_7, 3]='23.11.1998'
    
    df_complete = df_complete[df_complete['Wert']!='None']
    df_complete = df_complete[df_complete['Wert']!='']
    df_complete = df_complete[df_complete['Spieler']!='nan']
    print("Crawled Team")
    
    return df_complete



def get_new_player(df):
   
    f1 = db.get_data_db(1)
    df_id = f1.get_data()
    
    if len(df_id)>0:
    
        player_missing = t.get_new_player(df, df_id)  
        player_missing['Spieler_ID'] = range(df_id.tail(1).iloc[0,0]+1,df_id.tail(1).iloc[0,0]+len(player_missing)+1)
        player_missing = player_missing[['Spieler_ID', 'Spieler']]
        
    else:
        
        df['Spieler_ID'] = range(len(df))
        df['Spieler_ID'] = df['Spieler_ID'].add(1)
        df = df[['Spieler', 'Spieler_ID']]
        player_missing = df

        
    player_missing = player_missing[['Spieler_ID', 'Spieler']]
    player_missing = player_missing.dropna()
    player_missing = player_missing[player_missing['Spieler']!='nan']
    
    print(player_missing)
    return player_missing


    
def get_kader_club(df, saison, transferfenster):
    
    if transferfenster != 1 and transferfenster != 2:
        print("wrong timewindow parameter")
    
    c1 = len(df)

    f_new = db.get_data_db(1)
    df_id = f_new.get_data()
    f2 =  db.get_data_db(3)
    df_vereins_id = f2.get_data()
    
    df = df.merge(df_vereins_id, on = ['Verein', 'Vereins_ID'], how = 'inner')
    df = df.merge(df_id, on = 'Spieler', how = 'inner')
    c2 = len(df)
    
    if c1 != c2:
        print("Problem with join")
        print(c1)
        print(c2)
    df = df.assign(Saison = saison, Transferfenster = transferfenster)
    df = df[['Vereins_ID', 'Verein', 'Spieler_ID', 'Spieler', 'Position', 'Transferfenster', 'Saison']]
    
    return df


def get_Wert_Alter(df, saison, c):
        
    f_new = db.get_data_db(12)
    df_kader = f_new.get_data()
    
    f3 = db.get_data_db(7)
    df_mapping_transfermarkt = f3.get_data()   

    df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
    v1 = df_mapping_transfermarkt['Vereins_ID'].iloc[c-1]
    df_kader = df_kader[df_kader['Saison']==saison]
    df_kader = df_kader[df_kader['Vereins_ID']==v1]
    df_id = df_kader[['Spieler', 'Spieler_ID']]
    
    
    c1 = len(df)
    df = df.merge(df_id, on = 'Spieler', how = 'inner')
    c2 = len(df)
    
    if abs(c1 - c2)>4:
        print("problem with join")
    df['Wert'] = df['Wert'].str.strip()   
    df = df[df['Wert']!='']
    df = df[df['Wert']!='-']
    df = df[df['Wert']!='-  None']
    
    df_1 = df['Wert'].str.split(' ', expand = True)

    df_1[0] = df_1[0].str.replace(",",".").astype(float) 
 
    df_1['Multiplicator'] = np.where(df_1[1]=='Mio.', 1, 0.001)
    df_1 = df_1.assign(Spielerwert_Million = lambda x: x[0]*x['Multiplicator'])
    df_1 = df_1.drop([0,1,'Multiplicator'], axis = 1)

    df_t = pd.concat([df, df_1], axis = 1)
    
    f3 = db.get_data_db(2)
    df_datum = f3.get_data()
    df_datum = df_datum[df_datum['Saison']==saison]
    df_all = pd.DataFrame()
    print(df_t['Geburtstag'])
    df_t['Geburtstag'] = pd.to_datetime(df_t['Geburtstag'])

    
    for s in df_datum['Spieltag']: 
        df = df_datum[df_datum['Spieltag']==s]
        df_1 = df_t
        df_1 = df_1.assign(Spieltag = df['Spieltag'].iloc[0])
        df_1 = df_1.assign(Jahr = df['Jahr'].iloc[0])
        df_1 = df_1.assign(Saison = df['Saison'].iloc[0])
        df_1 = df_1.assign(Datum = df['Datum'].iloc[0])
        
        sp_ids = df_1['Spieler_ID'].drop_duplicates()
        
        for sid in sp_ids:
            df_2 = df_1[df_1['Spieler_ID']==sid]
            date = df_2['Datum'].iloc[0]
            geburtstag = df_2['Geburtstag'].iloc[0]
            alter = date.year - geburtstag.year - ((date.month, geburtstag.day) < (date.month, date.day))
            df_2 = df_2.assign(Spieler_Alter = alter)
            df_all = df_all.append(df_2)
    df_all.index = range(len(df_all)) 
    df_all['Spieler_Alter'] = pd.to_numeric(df_all['Spieler_Alter'])

    df_all = df_all.drop_duplicates() 
    df_all = df_all.dropna()
    
    df_all = df_all[['Spieltag', 'Spieler_ID', 'Spieler', 'Verein', 'Vereins_ID', 'Geburtstag', 'Spieler_Alter', 'Spielerwert_Million', 'Jahr', 'Saison']]
   
    #df_all['Geburtstag'] = df_all['Geburtstag'].to_string()
    #print(type(df_all['Geburtstag']))
    print("Worth, Age calculations are done")
    return df_all





#df = get_player_age_worth()
#get_new_player(df)
#db.upload_local_db_data(df, 20)






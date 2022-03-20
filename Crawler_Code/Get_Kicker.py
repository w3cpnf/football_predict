import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time

#import other files 
import My_Tools as t
import Read_Load_Database as db



        
def get_kicker(spieltag, saison, c):
        
    s1 = saison[0:4]+'-'+saison[5:7]
    
    f1 = db.get_data_db(7)
    df_mapping_transfermarkt = f1.get_data()
    df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
    id_Verein = df_mapping_transfermarkt['Vereins_ID']
    v1 = id_Verein.iloc[c-1]

    spiele_plan = db.get_data_db(2)
    df = spiele_plan.get_data()
    df = df[df['Saison']==saison]
    df = df[df['Spieltag']==spieltag]   
    
    mapping_kicker = db.get_data_db(16)
    df_mapping_kicker = mapping_kicker.get_data()

    df_mapping_kicker = df_mapping_kicker[df_mapping_kicker['Saison']==saison]
    df_mapping_kicker = df_mapping_kicker[df_mapping_kicker['Vereins_ID']==v1]
    
    v = df_mapping_kicker['Webpage'].iloc[0]
    verein = df_mapping_kicker['Verein'].iloc[0]

 
    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    url = 'https://www.kicker.de/1-bundesliga/'+str(v)+'/topspieler-spieltag/'+str(s1)+'/'+str(spieltag)

    driver.get(url)

    time.sleep(5)
    name = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__index kick__table--ranking__index--teamplayer']")    
    position = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__number kick__respt-m-w-100']")
    note = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__master kick__respt-m-w-65 kick__table--ranking__mark']")
               
    f1 = t.get_df(name)
    f2 = t.get_df(position)
    f3 = t.get_df(note)

    df_name = f1.df()           
    df_position = f2.df()
    df_note = f3.df()
    
    driver.quit()   
    
    df_name = df_name.fillna('')
    df_name['Spieler'] = df_name[1] + ' ' + df_name[0]
    df_name = df_name.drop([0,1], axis = 1)
    df_position.columns = ['Position']
    df_note.columns = ['Note']
    
    df_all  = pd.concat([df_name, df_position, df_note], axis = 1)

    f4 = t.unify_letters(df_all,1)
    df_all = f4.replace_letters()
    df_all = t.replace_kicker_names(df_all)
    df_all = df_all.assign(Spieltag = spieltag)

    f6 = db.get_data_db(9)
    df_spieler_config = f6.get_data()
    df_spieler_config = df_spieler_config[df_spieler_config['Saison']==saison]
    df_spieler_config = df_spieler_config[df_spieler_config['Vereins_ID']==v1]
    df_spieler_config = df_spieler_config[df_spieler_config['Spieltag']==spieltag]
    print(df_all)
    df_a = df_all.merge(df_spieler_config, on = ['Spieler', 'Spieltag'], how = 'inner')
    
    df_a['Note'] = df_a['Note'].str.replace(",",".").astype(float)  
    df_a = df_a.assign(Verein = verein)

    df_a = df_a[['Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein', 'Spieltag', 'Position', 'Note', 'Saison']]
    df_a = df_a.drop_duplicates()
    
    mistake = t.get_outer_on_player(df_a, df_spieler_config)

    if len(df_a)==len(df_all):
        print('Everthing fine')
    else:
        print(mistake)
        print(str(v))
        
    return df_a 
    
#df = get_kicker(2, '2018/19', 3)
#db.upload_local_data_to_database(df, 'bl1_data_spieler_kicker_position')
#db.upload_local_db_data(df, 9)


def get_kicker_all(saison, c):
    
    df_complete = pd.DataFrame()
    
    for spieltag in range(1,35):
        
        s1 = saison[0:4]+'-'+saison[5:7]
        
        f1 = db.get_data_db(7)
        df_mapping_transfermarkt = f1.get_data()
        #print(df_mapping_transfermarkt)
        df_mapping_transfermarkt = df_mapping_transfermarkt[df_mapping_transfermarkt['Saison']==saison]
        id_Verein = df_mapping_transfermarkt['Vereins_ID']
        v1 = id_Verein.iloc[c-1]
    
        spiele_plan = db.get_data_db(2)
        df = spiele_plan.get_data()
        df = df[df['Saison']==saison]
        df = df[df['Spieltag']==spieltag]   
        #print(df)
        mapping_kicker = db.get_data_db(16)
        df_mapping_kicker = mapping_kicker.get_data()
        #print(df_mapping_kicker)
        df_mapping_kicker = df_mapping_kicker[df_mapping_kicker['Saison']==saison]
        df_mapping_kicker = df_mapping_kicker[df_mapping_kicker['Vereins_ID']==v1]
        
        v = df_mapping_kicker['Webpage'].iloc[0]
        verein = df_mapping_kicker['Verein'].iloc[0]
    
     
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        url = 'https://www.kicker.de/1-bundesliga/'+str(v)+'/topspieler-spieltag/'+str(s1)+'/'+str(spieltag)
    
        driver.get(url)
    
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        name = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__index kick__table--ranking__index--teamplayer']")    
        position = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__number kick__respt-m-w-100']")
        note = driver.find_elements_by_xpath("//td[@class='kick__table--ranking__master kick__respt-m-w-65 kick__table--ranking__mark']")
                   
        f1 = t.get_df(name)
        f2 = t.get_df(position)
        f3 = t.get_df(note)
    
        df_name = f1.df()           
        df_position = f2.df()
        df_note = f3.df()
        
        driver.quit()   
        
        df_name = df_name.fillna('')
        df_name['Spieler'] = df_name[1] + ' ' + df_name[0]
        df_name = df_name.drop([0,1], axis = 1)
        df_position.columns = ['Position']
        df_note.columns = ['Note']
        
        df_all  = pd.concat([df_name, df_position, df_note], axis = 1)
    
        f4 = t.unify_letters(df_all,1)
        df_all = f4.replace_letters()
        df_all = t.replace_kicker_names(df_all)
        df_all = df_all.assign(Spieltag = spieltag)
    
        f6 = db.get_data_db(9)
        df_spieler_config = f6.get_data()
        df_spieler_config = df_spieler_config[df_spieler_config['Saison']==saison]
        df_spieler_config = df_spieler_config[df_spieler_config['Vereins_ID']==v1]
        df_spieler_config = df_spieler_config[df_spieler_config['Spieltag']==spieltag]
        print(df_all)
        df_a = df_all.merge(df_spieler_config, on = ['Spieler', 'Spieltag'], how = 'inner')
        
        df_a['Note'] = df_a['Note'].str.replace(",",".").astype(float)  
        df_a = df_a.assign(Verein = verein)
    
        df_a = df_a[['Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein', 'Spieltag', 'Position', 'Note', 'Saison']]
        df_a = df_a.drop_duplicates()
        
        mistake = t.get_outer_on_player(df_a, df_spieler_config)
        print(df_a.merge(df_spieler_config, on = ['Spieler'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']['Spieler'])
        if len(df_a)==len(df_all):
            print('Everthing fine')
        else:
            print(mistake)
            print(str(v))
        
        df_complete = df_complete.append(df_a)
        
    return df_complete 


#df = get_kicker_all('2020/21', 18)
#df = df.assign(Jahr = 2015, Woche = 1)
#df = df.drop(['Woche','Jahr'], axis = 1)
#db.upload_local_data_to_database(df, 'bl1_data_spieler_kicker_position')
#db.upload_local_db_data(df, 9)
# f = db.get_data_db(19)
# df = f.get_data()
# df = df[df['Saison']=='2019/20']
# df = df.drop_duplicates()
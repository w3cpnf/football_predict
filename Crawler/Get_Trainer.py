import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time


import My_Tools as t
import Read_Load_Database as db




def get_trainer():
    
    f = db.get_data_db(25)
    df = f.get_data()  
    
    list_trainer = df['Webpage']
    list_verein = df['Verein']
    list_verein_id = df['Vereins_ID']
    
    all_length = len(list_trainer)
    df_all = pd.DataFrame()
    
    for i in range(all_length):
        
        v_t = list_trainer[i]
        v = list_verein[i]
        v_id = list_verein_id[i]
        
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get(v_t)
        time.sleep(5)
    
        table = driver.find_elements_by_xpath("//table[@class='standard_tabelle']")
        f_t = t.get_df(table)
        df_table = f_t.df().T
        driver.quit()
        
        df_table = df_table[0].str.split(' ', expand = True)
        df_table['Von'] = pd.to_datetime(df_table[0].iloc[1:], dayfirst=True, infer_datetime_format=True)
        df_table['Bis'] = pd.to_datetime(df_table[2].iloc[1:], dayfirst=True, infer_datetime_format=True)
        df_table['Trainer'] = df_table[3].iloc[1:] +' '+ df_table[4].iloc[1:]
        df_table['Geburtstag'] = df_table[5].iloc[1:]
        df_trainer = df_table[['Trainer', 'Von', 'Bis', 'Geburtstag']].dropna()
        df_trainer = df_trainer[df_trainer['Bis']>'2019-08-01']
        df_trainer = df_trainer.assign(Vereins_ID = v_id, Verein = v)
        df_all = df_all.append(df_trainer)
        
    f_replace = t.unify_letters(df_all, 2)
    df_all = f_replace.replace_letters()
    
    return df_all



def new_trainer(df):

    f3 = db.get_data_db(17)   
    df_tid = f3.get_data()

    f_replace = t.unify_letters(df, 2)
    df_trainer = f_replace.replace_letters()

    df_new_trainer = df_trainer.merge(df_tid, on = ['Trainer'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only'][['Trainer']].drop_duplicates()
    df_new_trainer['Trainer_ID'] = range(df_tid.tail(1).iloc[0,0]+1,df_tid.tail(1).iloc[0,0]+len(df_new_trainer)+1)
    df_new_trainer = df_new_trainer[['Trainer_ID', 'Trainer']]
    
    return df_new_trainer
    
 
    
def get_plan(df, spieltag):
    
  
    f2 = db.get_data_db(2)
    df_spielplan = f2.get_data()
    
    f1 = db.get_data_db(17)
    df_trainer_id = f1.get_data()
    
    df_t = df.merge(df_trainer_id, on = 'Trainer', how = 'inner')

    
    df_all = pd.DataFrame()
    trainer = df_t['Trainer_ID'].drop_duplicates()

    
    for trai in trainer:
        df_i = df_t[df_t['Trainer_ID']==trai]
        vereine = df_i['Vereins_ID'].drop_duplicates()
        for v in vereine:
            df_vt = df_i[df_i['Vereins_ID']==v]
            bis = df_vt['Bis'].iloc[0]
            von = df_vt['Von'].iloc[0]
            
            df_splan_verein = df_spielplan[df_spielplan['Vereins_ID']==v]
        
            df_spam = df_splan_verein[df_splan_verein['Datum']>=von]
            df_spam = df_spam[df_spam['Datum']<=bis]
            df_ready = df_spam.merge(df_vt, on = ['Vereins_ID', 'Verein'], how = 'inner')
            df_all = df_all.append(df_ready)
        
    df_all = df_all.sort_values(by = ['Vereins_ID', 'Saison', 'Spieltag'])
    df_all = df_all[['Trainer_ID', 'Trainer', 'Vereins_ID', 'Verein', 'Von', 'Bis', 'Saison', 'Spieltag', 'Jahr', 'Geburtstag']]
    df_all = df_all[df_all['Spieltag']==spieltag]
    df_all = df_all.drop_duplicates()
    print(df_all)
    return df_all




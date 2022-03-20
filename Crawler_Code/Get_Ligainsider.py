import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 

#import other files 
import My_Tools as t 
import Read_Load_Database as db

# always recent gameday
#perf_url = 'https://www.ligainsider.de/bundesliga/noten/spieltag/saison-2014-2015/419/'



def get_perf_index(spieltag, url, saison):
      
    driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//span[@id="cmpbntyestxt"]'))).click()
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    player = driver.find_elements_by_xpath("//td[@class='text-left']")
    time.sleep(5)
    info = driver.find_elements_by_xpath("//td[@class='text-right']")
    time.sleep(5)
    note = driver.find_elements_by_xpath("//td[@class='text-right sorting_1']")
    
    
    f1 = t.get_df(player)
    f2 = t.get_df(info)
    f3 = t.get_df(note)
    
    df_player = f1.df()
    df_info = f2.df() 
    df_note = f3.df() 
    driver.quit()
    
    df_note.columns = ['Note_Spieltag']
    
    
    df_p = t.columns(df_player, 1)
    df_i = t.columns(df_info, 2)
    
    df_all = pd.concat([df_p, df_note, df_i], axis = 1) 
    df_all = df_all.assign(Spieltag = spieltag)
    
    f4 = t.unify_letters(df_all, 1)
    df_all = f4.replace_letters()
    df_all = t.change_name_ligainsider(df_all)
    df_all = t.get_numbers(df_all)
    df_all['Spieler'] = df_all['Spieler'].str.strip()
    df_all['Verein'] = df_all['Verein'].str.strip()
    
    f5 = db.get_data_db(49)
    df_spieler_id = f5.get_data()  
    df_spieler_id = df_spieler_id[df_spieler_id['Saison']==saison]
    df_spieler_id = df_spieler_id[df_spieler_id['Spieltag']==spieltag]
    df_spieler_id['Spieler'] = df_spieler_id['Spieler'].str.strip()   
    
    df_n = df_all.merge(df_spieler_id, on = ['Spieler', 'Verein', 'Spieltag'], how = 'inner')
    df_not = df_all.merge(df_n, on = ['Spieler', 'Spieltag'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    print(df_not)
    
    df_n = df_n[['Spieler_ID', 'Spieler','Vereins_ID', 'Verein', 'Spieltag', 'Position', 'Note_Spieltag', 'Pkt_Spieltag',
                 'Min_Spieltag','Durchschnitt_Note', 'Durchschnitt_Pos_Pkt', 'Saison']]
            
    return df_n 
    

#df = get_perf_index(1, perf_url, '2014/15')

#db.upload_local_data_to_database(df, 'bl1_data_spieler_performance')
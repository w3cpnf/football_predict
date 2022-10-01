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


def replace_player_name(df):
    df = df.replace({'Jacob Laursen':'Jacob Barrett Laursen', 'Evan Ndicka ':'Evan N\'Dicka', 'Josip Brekalo':'Josip Brekalo',
                     'Gian-Luca Itter':'Luca Itter', 'Hee-chan Hwang':'Hee-chan Hwang', 'Hans Nunoo Sarpei':'Nunoo Sarpei',
                     'Armel Bella-Kotchap':'Armel Bella Kotchap', 'N. Sarenren Bazee':'Noah Joel Sarenren Bazee', 
                     'Manu Kone':'Kouadio Kone', 'Adam Matuschyk':'Adam Matuszczyk', 'Sebastian Prödl':'Sebastian Prödl'})
    return df

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
    
    #f5 = db.get_data_db(49)
    #df_spieler_id = f5.get_data()  
    df_spieler_id = db.get_table('bl1_staging_spieler_kader')
    
    
    df_spieler_id = df_spieler_id[df_spieler_id['Saison']==saison]
    #df_spieler_id = df_spieler_id[df_spieler_id['Spieltag']==spieltag]
    df_spieler_id['Spieler'] = df_spieler_id['Spieler'].str.strip()   
    df_spieler_id = df_spieler_id[['Vereins_ID', 'Verein', 'Spieler', 'Spieler_ID', 'Saison']]
    
    df_all = df_all.replace({'Mönchengladbach':'Borussia Mönchengladbach', 'TSG Hoffenheim':'TSG 1899 Hoffenheim'
                                      ,'Greuther Fürth':'SpVgg Greuther Fürth'})
    df_all['Spieler'] =  df_all['Spieler'].str.strip()
    df_all = replace_player_name(df_all)

    df_n = df_all.merge(df_spieler_id, on = ['Spieler', 'Verein'], how = 'inner')
    df_not = df_all.merge(df_n, on = ['Spieler', 'Spieltag'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    print(df_not)
    
    df_n = df_n[['Spieler_ID', 'Spieler','Vereins_ID', 'Verein', 'Spieltag', 'Position', 'Note_Spieltag', 'Pkt_Spieltag',
                 'Min_Spieltag','Durchschnitt_Note', 'Durchschnitt_Pos_Pkt', 'Saison']]
    
    print(spieltag)
    print("is done")
            
    return df_n 
    
perf_url = 'https://www.ligainsider.de/bundesliga/noten/spieltag/saison-2014-2015/593/'
spieltag = 2
saison = '2014/15'
df = get_perf_index(spieltag, perf_url, saison)
#df_1 = df[df['Spieler_ID']==460]
#df_2 = df[df['Spieler_ID']==379]
#df_2 = df_2.drop_duplicates()
#db.upload_local_data_to_database(df_2, 'bl1_data_spieler_performance')
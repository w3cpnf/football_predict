import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
from selenium import webdriver
import time
import numpy as np
import pandas as pd

import My_Tools as t
import Read_Load_Database as db


# driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
# driver.get('https://www.transfermarkt.de/1-bundesliga/startseite/wettbewerb/L1')
# all_info = driver.find_elements_by_xpath("//div[@class='responsive-table']") 
# all_info = all_info[0].text
# index_home = all_info.find("FC Bayern München")
# index_ende_home = all_info.find("FC Bayern München")+len("FC Bayern München")
# clubUrlHome = all_info[index_home:index_ende_home]

#df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Kadergröße', 'Kaderwert_Million', 'Kaderwert_Per_Spieler_Million','Saison']]
class club_value:
    
    def __init__(self, spieltag, saison):
        self.spieltag = spieltag
        self.saison = saison
        
      
    def get_club_value(self):
        
        s = self.spieltag
        saison = self.saison
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get('https://www.transfermarkt.de/1-bundesliga/startseite/wettbewerb/L1')
        time.sleep(5)
  
        verein = driver.find_elements_by_xpath("//td[@class='hauptlink no-border-links']") 
        #verein = driver.find_elements_by_xpath("//td[@class='hauptlink no-border-links hide-for-small hide-for-pad']")
        kader = driver.find_elements_by_xpath("//td[@class='zentriert']") 
        #wert = driver.find_elements_by_xpath("//td[@class='rechts hide-for-small hide-for-pad']") 
        wert = driver.find_elements_by_xpath("//td[@class='rechts']") 

        f1 = t.get_df(kader)
        f2 = t.get_df(verein) 
        f3 = t.get_df(wert)

        df_kader = f1.df()
        df_verein = f2.df()
        df_wert = f3.df()

        df_verein[0] = df_verein[0].str.strip()

        df_wert = df_wert.iloc[2:38]
        df_wert = t.columns(df_wert, 9)
        df_wert.index = range(len(df_wert))       
        print(df_wert)
        df_1 = df_wert['Kaderwert'].str.split(' ', expand = True)
        df_2 = df_wert['WertPerSpieler'].str.split(' ', expand = True)
        df_1[0] = df_1[0].str.replace(",",".").astype(float) 
        df_2[0] = df_2[0].str.replace(",",".").astype(float) 
        df_1['Multiplicator'] = np.where(df_1[1]=='Mio.', 1, 1000)
        df_2['Multiplicator'] = np.where(df_2[1]=='Mio.', 1, 0.1)
        df_1 = df_1.assign(Kaderwert_Million = lambda x: x[0]*x['Multiplicator'])
        df_2 = df_2.assign(Kaderwert_Per_Spieler_Million = lambda x: x[0]*x['Multiplicator'])
        df_1 = df_1.drop([0,1,2,'Multiplicator'], axis = 1)
        df_2 = df_2.drop([0,1,2,'Multiplicator'], axis = 1)
        df = pd.concat([df_1, df_2], axis = 1)
        

        df_verein[0] = df_verein[df_verein[0].astype(bool)]
        df_verein = df_verein.dropna()
        df_verein.index = range(len(df_verein))
        df_verein = df_verein.iloc[0:18,:]
        df_verein.columns = ['Verein']
        
        df_kader = df_kader.iloc[3:57]
        df_kader = t.columns(df_kader, 11)
        #df_kader[0] = df_kader[0][df_kader[0] != '26.05.2021']
        #df_kader[0] = df_kader[0][df_kader[0] != '29.05.2021']
        df_kader = df_kader[['Kadergröße']]
        #df_kader = df_kader[~df_kader[0].str.contains("-")]
        #df_kader[0] = df_kader[df_kader[0].astype(bool)]
        print(df_kader)
        df_kader = df_kader.dropna()
        
        df_kader = df_kader.astype(int)
        print(df_kader)
        #df_kader = df_kader[df_kader[0]>11]
        #df_kader = df_kader[df_kader[0]<40]
        df_kader.index = range(len(df_kader))
        df_kader = df_kader.iloc[0:18,:]
        #df_kader.columns = ['Kadergröße']
        print(df_kader)
        driver.quit()

        df_all = pd.concat([df_kader, df_verein, df], axis = 1)
        
        df_all = df_all.rename({'FC Schalke 04': 'FC Schalke', '1.FSV Mainz 05': '1.FSV Mainz'})
        

        df_all = df_all.dropna()
        df_all = df_all.replace({'Bor. Dortmund': 'Borussia Dortmund', 'Bay. Leverkusen': 'Bayer 04 Leverkusen', 'SC Freiburg':'Sport-Club Freiburg',
                                    'F. Düsseldorf':'Fortuna Düsseldorf', 'Union Berlin':'1. FC Union Berlin', 'Bayern München':'FC Bayern München', 
                                    'SC Paderborn':'SC Paderborn 07', '1.FSV Mainz':'1. FSV Mainz 05', 'FC Schalke':'FC Schalke 04', 'TSG Hoffenheim':'TSG 1899 Hoffenheim',
                                    'E. Frankfurt':'Eintracht Frankfurt', 'Werder Bremen':'SV Werder Bremen', '1.FC Köln':'1. FC Köln',                    
                                    'Bor. M\'gladbach':'Borussia Mönchengladbach', 'RasenBallsport Leipzig':'RB Leipzig', 
                                    '1.FSV Mainz 05':'1. FSV Mainz 05', '1.FC Union Berlin':'1. FC Union Berlin', 
                                    'Arminia Bielefeld':'DSC Arminia Bielefeld'})
        df_id = db.get_table('master_vereins_id') 

        print(df_all)
        df_all = df_all.merge(df_id, on = 'Verein', how = 'inner')
        
        df_plan = db.get_table('bl1_data_vereine_spielplan') 
        df_plan = df_plan[df_plan['Saison']==saison]
        df_plan = df_plan[df_plan['Spieltag']==s]
        
        df_all = df_all.merge(df_plan, on = ['Verein', 'Vereins_ID'], how = 'inner')

        df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Kadergröße', 'Kaderwert_Million', 'Kaderwert_Per_Spieler_Million','Saison']]
        df_all = df_all.drop_duplicates()
        return df_all
        

#f = club_value(21, '2021/22')
#df = f.get_club_value()
#db.upload_local_data_to_database(df, 'bl1_data_vereine_kader_wert')

class club_value_premier_league:
    
    def __init__(self, spieltag, saison):
        self.spieltag = spieltag
        self.saison = saison
        
      
    def get_club_value(self):
        
        s = self.spieltag
        saison = self.saison
        driver = webdriver.Firefox(executable_path=r'D:\Projects\Football\Database\Crawler_Code\Webdrivers\geckodriver')
        driver.get('https://www.transfermarkt.de/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2021')
        time.sleep(5)
  
        verein = driver.find_elements_by_xpath("//td[@class='hauptlink no-border-links']") 
        #verein = driver.find_elements_by_xpath("//td[@class='hauptlink no-border-links hide-for-small hide-for-pad']")
        kader = driver.find_elements_by_xpath("//td[@class='zentriert']") 
        #wert = driver.find_elements_by_xpath("//td[@class='rechts hide-for-small hide-for-pad']") 
        wert = driver.find_elements_by_xpath("//td[@class='rechts']") 


        f1 = t.get_df(kader)
        f2 = t.get_df(verein) 
        f3 = t.get_df(wert)

        df_kader = f1.df()
        df_verein = f2.df()
        df_wert = f3.df()

        df_wert = df_wert.iloc[2:42]
        df_wert = t.columns(df_wert, 9)
        df_wert.index = range(len(df_wert))   

 
        #print(df_wert)
        df_1 = df_wert['Kaderwert'].str.split(' ', expand = True)
        df_2 = df_wert['WertPerSpieler'].str.split(' ', expand = True)
        df_1[0] = df_1[0].str.replace(",",".").astype(float) 
        df_2[0] = df_2[0].str.replace(",",".").astype(float) 
        df_1['Multiplicator'] = np.where(df_1[1]=='Mio.', 1, 1000)
        df_2['Multiplicator'] = np.where(df_2[1]=='Mio.', 1, 1000)
        df_1 = df_1.assign(Kaderwert_Million = lambda x: x[0]*x['Multiplicator'])
        df_2 = df_2.assign(Kaderwert_Per_Spieler_Million = lambda x: x[0]*x['Multiplicator'])
        df_1 = df_1.drop([0,1,2,'Multiplicator'], axis = 1)
        df_2 = df_2.drop([0,1,2,'Multiplicator'], axis = 1)
        df = pd.concat([df_1, df_2], axis = 1)


        df_verein[0] = df_verein[df_verein[0].astype(bool)]
        df_verein = df_verein.dropna()
        df_verein.index = range(len(df_verein))
        df_verein = df_verein.iloc[0:20,:]
        df_verein.columns = ['Verein']
        df_verein['Verein'] = df_verein['Verein'].str.strip()
        print(df_verein)
        #print(df_kader)
        df_kader = df_kader.iloc[3:63]
        print(df_kader)
        df_kader = t.columns(df_kader, 11)
        #df_kader[0] = df_kader[0][df_kader[0] != '26.05.2021']
        #df_kader[0] = df_kader[0][df_kader[0] != '29.05.2021']
        df_kader = df_kader[['Kadergröße']]
        #df_kader = df_kader[~df_kader[0].str.contains("-")]
        #df_kader[0] = df_kader[df_kader[0].astype(bool)]
        
        #print(df_kader)
        df_kader = df_kader.dropna()

        df_kader = df_kader.astype(int)

        df_kader.index = range(len(df_kader))
        df_kader = df_kader.iloc[0:20,:]
        df_kader.columns = ['Kadergröße']

        driver.quit()

        df_all = pd.concat([df_kader, df_verein, df], axis = 1)
       
        #df_all = df_all.rename({'FC Schalke 04': 'FC Schalke', '1.FSV Mainz 05': '1.FSV Mainz'})


        df_all = df_all.dropna()
        

        df_id = db.get_table('master_vereins_id') 
        df_all = df_all.merge(df_id, on = 'Verein', how = 'inner')
        
        df_plan = db.get_table('pl_data_vereine_spielplan') 
        df_plan = df_plan[df_plan['Saison']==saison]
        df_plan = df_plan[df_plan['Spieltag']==s]
        
        df_all = df_all.merge(df_plan, on = ['Verein', 'Vereins_ID'], how = 'inner')

        df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Kadergröße', 'Kaderwert_Million', 'Kaderwert_Per_Spieler_Million', 'Saison']]
        df_all = df_all.drop_duplicates()
        
        return df_all




#f = club_value_premier_league(24, '2021/22')
#df = f.get_club_value()
#db.upload_local_data_to_database(df, 'pl_data_vereine_kader_wert')

#df = df.drop('Spieltag', axis = 1)
#df_all = pd.DataFrame()
#for i in range(8,18):
#    df = df.assign(Spieltag = i)
#    df_all = df_all.append(df)
#df_all = df_all[['Spieltag', 'Vereins_ID', 'Verein', 'Kadergröße', 'Kaderwert_Million', 'Kaderwert_Per_Spieler_Million', 'Saison']]


#db.upload_local_data_to_database(df_all, 'pl_data_vereine_kader_wert')

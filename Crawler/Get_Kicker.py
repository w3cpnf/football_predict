import os
os.chdir('D:/Projects/Football/Database/Crawler_Code')

#packages and modules
import pandas as pd
from selenium import webdriver
import time

#import other files 
import My_Tools as t
import Read_Load_Database as db


class kicker:
    
    def __init__(self, spieltag, saison, saison_1, c, transferfenster):
        
        self.spieltag = spieltag
        self.saison = saison
        self.saison_1 = saison_1
        self.c = c
        self.transferfenster = transferfenster
        
    def get_kicker(self):
        
        spieltag = self.spieltag
        saison = self.saison
        saison_1 = self.saison_1
        transferfenster = self.transferfenster
        c = self.c
        
        f1 = db.get_data_db(7)
        df_mapping_transfermarkt = f1.get_data()
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

 
        driver = webdriver.Firefox(executable_path=r'D:\Crawling\geckodriver')
        url = 'https://www.kicker.de/1-bundesliga/'+str(v)+'/topspieler-spieltag/'+str(saison_1)+'/'+str(spieltag)
        print(url)
        driver.get(url)
        #https://www.kicker.de/bundesliga/borussia-dortmund/topspieler-spieltag/2020-21/1
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
        print(df_all)
        f4 = t.unify_letters(df_all,1)
        df_all = f4.replace_letters()
        df_all['Spieler'] = df_all['Spieler'].str.strip()
        df_all = df_all.replace({'Jan-Ingwer Callsen-Bracker':'J. Callsen-Bracker', 'Cedrick Makiadi':'Cedric Makiadi', 
                                 'Pierre-Emerick Aubameyang':'P. Aubameyang', 'Anderson':'Bamba Anderson',
                                 'Roberto Firmino':'R. Barbosa de Oliveira', 'Ja-Cheol Koo':'Ja-cheol Koo', 
                                 'Klaas Jan Huntelaar':'Klaas-Jan Huntelaar', 'Eric Maxim Choupo-Moting':'E. Choupo-Moting', 
                                 'Luiz Gustavo':'Luiz Gustavo Dias','Marcelo':'M. Guedes Filho', 'Zoltan Stieber':'Stiebi',
                                 'Per Ciljan Skjelbred':'Per Skjelbred', 'Jairo':'Jairo Samperio', 'Rafa Lopez':'Rafael Lopez', 
                                 'Pierre-Emile Höjbjerg':'Pierre-Emile Hojbjerg', 'Mats Möller Daehli':'Mats Möller Dæhli', 
                                 'Baard Finne':'Bard Finne', 'Joao Pereira':'J. da Silva Pereira', 'Serey Die':'Geoffroy Serey Die',
                                 'Tolga Cigerci':'Tolga Ciğerci', 'Jose Manuel Reina':'Jose Reina', 'Douglas Costa':'Douglas Costa de Souza',
                                 'Konstantinos Stafylidis':'Konstantinos Stafylidis', 'Serey Die':'Geoffroy Serey Die',
                                 'Artem Fedetskyy':'Artem Fedetskyi', 'Naby Keita':'Naby Keïta', 'Bojan':'Bojan Krkic', 
                                 'Andrey Yarmolenko':'Andriy Yarmolenko','Noah Joel Sarenren Bazee':'Noah Sarenren Bazee', 
                                 'Ville Matti Steinmann':'Matti Steinmann', 'Louis Jordan Beyer' :'Jordan Beyer','Kunde':'Pierre Kunde Malong',
                                 'Aaron':'Aaron Martin', 'Yannik Keitel':'Yannik Keitel .','Samuel Kari Fridjonsson':'Samuel Fridjonsson', 
                                 'Florian Wirtz':'Florian Wirtz .', 'Mathias Jörgensen':'Zanka', 'Chang-Hoon Kwon':'Chang-hoon Kwon',
                                 'Heung-Min Son':'Heung-min Son', })
        

        kader = db.get_data_db(12)
        df_kader = kader.get_data()
        df_kader = df_kader[df_kader['Saison']==saison]
        df_kader = df_kader[df_kader['Vereins_ID']==v1]
        df_kader = df_kader[df_kader['Transferfenster']==transferfenster]
        df_kader = df_kader[['Spieler', 'Spieler_ID']]

        df_a = df_all.merge(df_kader, on = 'Spieler', how = 'inner')

        df_a['Note'] = df_a['Note'].str.replace(",",".").astype(float)  
        df_a = df_a.assign(Verein = verein)

        df_a = df_a.merge(df, on = 'Verein', how = 'inner')
        #print(df_a.columns)
        df_a = df_a[['Spieler_ID', 'Spieler', 'Vereins_ID', 'Verein', 'Spieltag', 'Position', 'Note', 'Jahr', 'Woche', 'Saison']]
        df_a = df_a.drop_duplicates()
        
        mistake = t.get_outer_on_player(df_a, df_kader)
        
        if len(df_a)==len(df_all):
            print('Everthing fine')
        else:
            print(mistake)
            print(str(v))
            
        f6 = db.get_data_db(19)
        df_v = f6.get_data()
    
        df_v = df_v[df_v['Saison']==saison]
        df_v = df_v[df_v['Vereins_ID']==v1]
        df_v = df_v[df_v['Spieltag']==spieltag]
        
        
        df_rest = df_a.merge(df_v, on = ['Spieler', 'Spieler_ID',  'Vereins_ID', 'Verein', 'Saison', 'Spieltag', 'Position', 'Note',
                                         'Jahr', 'Woche', 'Saison'], how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
        #print(df_rest)
        df_rest = df_rest.drop('_merge', axis = 1)
        print(df_a.columns)
        return df_a 
    
#f = kicker(34, '2014/15', '2014-15', 5, 2)
#df = f.get_kicker()
#db.upload_local_db_data(df, 9)
#df.drop_duplicates()
#['Spieler']
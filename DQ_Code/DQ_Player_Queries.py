import os
os.chdir('D:/Projects/Football/Database/DQ_Code')

import pandas as pd
import mysql
import mysql.connector

today = pd.Timestamp.date(pd.Timestamp.today())

class get_data_db:
    
    def __init__(self, case):
        self.case = case
        
    def get_data(self):
        
        case = self.case
         
        if case == 1:
            query = '''select 
                        	saison, 
                        	Transferfenster, 
                        	count(distinct Vereins_ID)
                        from 
                        	bl1_staging_spieler_kader
                        group by 
                        	saison, Transferfenster
                        having count(distinct Vereins_ID) != 18
                        order by 
                        	saison
                        ;'''  
        if case == 2:
            query = '''select 
                        	saison, 
                        	Transferfenster, 
                        	Vereins_ID,
                        	count(distinct(Spieler_ID))    
                        from 
                        	bl1_staging_spieler_kader
                        group by 
                        	saison, Transferfenster, Vereins_ID
                        having
                        	count(distinct(Spieler_ID))<22
                        order by 
                        	saison
                        ;'''  
                                                
        if case == 3:     
            query = '''select* from bl1_staging_spieler_kader;'''      

        if case == 4:     
            query = '''select 
                        	saison, 
                        	Transferfenster, 
                        	count(distinct(Vereins_ID))    
                        from 
                        	bl1_staging_spieler_kader
                        group by 
                        	saison, Transferfenster
                        having
                        	count(distinct(Vereins_ID))!=18
                        order by 
                        	saison;'''      

        if case == 5:
            query = '''select 
                        	saison,
                        	spieltag,
                        	count(distinct vereins_id) as Clubs_Nbr
                        from 
                        	bl1_master_spieler_config
                        group by 
                        	saison, spieltag
                        having 
                        	count(distinct vereins_id) != 18
                        order by 
                        	saison, spieltag;''' 
        if case == 6:
            query = '''select 
                        	saison, 
                            count(distinct(spieltag))
                        from 
                        	bl1_master_spieler_config
                        group by 
                        	saison
                        order by 
                        	saison;'''  
                           

        if case == 7:
            query = '''select * from bl1_master_spieler_config;'''    
                         
        if case == 8:
            query = '''select 
                        	saison,
                        	count(distinct vereins_id) as Clubs_Nbr
                        from 
                        	bl1_mapping_ligainsider
                        group by 
                        	saison
                        ;'''  
                    
        if case == 9:
            query = '''select 
                        	saison, 
                        	Verein, 
                        	Vereins_ID, count(distinct Spieler_ID) as Player_Nbr
                        from 
                        	bl1_mapping_ligainsider
                        group by 
                        	saison, Verein, Vereins_ID
                        having 
                        	count(distinct Spieler_ID)<22
                        or 
                        	count(distinct Spieler_ID)>40
                        ;''' 
                        
        if case == 10:
            query = '''select * from bl1_master_spieler_config;'''  
                           
        if case == 11:
            query = '''select * from master_spieler_id;'''  
            
        if case == 12:
            query = '''select 
                        	saison,
                        	count(distinct vereins_id) as Clubs_Nbr
                        from 
                        	bl1_data_spieler_wert_alter
                        group by 
                        	saison
                        ;'''  
        if case == 13:
            query = '''select 
                        	saison, 
                        	Verein, 
                            spieltag,
                        	Vereins_ID, count(distinct Spieler_ID) as Player_Nbr
                        from 
                        	bl1_data_spieler_wert_alter
                        group by 
                        	saison, Verein, Vereins_ID, spieltag
                        having 
                        	count(distinct Spieler_ID)<23
                        or 
                        	count(distinct Spieler_ID)>40
                        ;'''   
                        
        if case == 14:
            query = '''select* from bl1_data_spieler_wert_alter;'''        
                         
            
        if case == 15:     
            query = '''select* from bl1_staging_spieler_daten;'''  
            

        if case == 16:     
            query = '''select 
                        	saison,
                        	count(distinct spieltag)
                        from 
                        	bl1_staging_spieler_daten
                        group by 
                        	saison
                        ;'''  

        if case == 17:     
            query = '''select 
                        	saison, 
                            spieltag,
                        	Verein, 
                        	Vereins_ID, count(distinct Spieler_ID) as Player_Nbr
                        from 
                        	bl1_staging_spieler_daten
                        group by 
                        	saison, Verein, Vereins_ID, spieltag
                        having 
                        	count(distinct Spieler_ID)<15
                        or 
                        	count(distinct Spieler_ID)>40;'''
        if case == 18:     
            query = '''select 
                        	saison,
                            spieltag,
                        	count(distinct vereins_id) as Clubs_Nbr
                        from 
                        	bl1_staging_spieler_daten
                        group by 
                        	saison, spieltag
                        having Clubs_Nbr != 18
                        ;'''
                                                    
        if case == 19:     
            query = '''select* from bl1_data_spieler_daten;'''  
            

        if case == 20:     
            query = '''select 
                        	saison,
                        	count(distinct spieltag)
                        from 
                        	bl1_data_spieler_daten
                        group by 
                        	saison
                        ;'''  

        if case == 21:     
            query = '''select 
                        	saison, 
                            spieltag,
                        	Verein, 
                        	Vereins_ID, count(distinct Spieler_ID) as Player_Nbr
                        from 
                        	bl1_data_spieler_daten
                        group by 
                        	saison, Verein, Vereins_ID, spieltag
                        having 
                        	count(distinct Spieler_ID)<15
                        or 
                        	count(distinct Spieler_ID)>40;'''
        if case == 22:     
            query = '''select 
                        	saison,
                            spieltag,
                        	count(distinct vereins_id) as Clubs_Nbr
                        from 
                        	bl1_data_spieler_daten
                        group by 
                        	saison, spieltag
                        having Clubs_Nbr != 18
                        ;'''  
                        
        if case == 23:     
            query = '''select 
                        	saison,
                        	count(distinct spieltag)
                        from 
                        	bl1_data_spieler_performance
                        group by 
                        	saison
                        ;'''       
                        
        if case == 24:     
            query = '''select 
                        	saison,
                            spieltag,
                        	count(distinct vereins_id) as Clubs_Nbr
                        from 
                        	bl1_data_spieler_performance
                        group by 
                        	saison, spieltag
                        having Clubs_Nbr != 18
                        ;'''
                        
        if case == 25:     
            query = '''select 
                        	saison, 
                        	spieltag,
                        	Verein, 
                        	Vereins_ID, count(distinct Spieler_ID) as Player_Nbr
                        from 
                        	bl1_data_spieler_performance
                        group by 
                        	saison, Verein, Vereins_ID, spieltag
                        having 
                        	count(distinct Spieler_ID)<9
                        or 
                        	count(distinct Spieler_ID)>40
                        ;''' 
                        
        if case == 26:     
            query = '''select * from bl1_data_spieler_performance;'''          
                
        if case == 27:     
            query = '''select saison, count(distinct(vereins_id))
                        from bl1_data_spieler_kicker_position
                        group by saison;'''  
        if case == 28:     
            query = '''select saison, spieltag, vereins_id, count(distinct(spieler_id))
                        from bl1_data_spieler_kicker_position
                        group by saison, spieltag, vereins_id
                        having count(distinct(spieler_id)) <9;''' 
                        
        if case == 29:
            query = '''select* from bl1_data_spieler_kicker_position;'''   
            
        if case == 30:
            query = '''select saison, spieltag, count(distinct(vereins_id))
                        from bl1_data_spieler_kicker_position
                        group by saison, spieltag
                        having count(distinct(vereins_id)) != 18;'''

        if case == 31:
            query = '''select saison, count(distinct(Spieltag))
                        from bl1_data_spieler_kicker_position
                        group by saison;''' 
                        
        if case == 32:     
            query = '''select saison, count(distinct(vereins_id))
                        from bl1_data_spieler_performance
                        group by saison;'''  
                        
        if case == 33:     
            query = '''select saison, count(distinct(vereins_id))
                        from bl1_data_spieler_startelf_system
                        group by saison;'''  
        if case == 34:     
            query = '''select saison, spieltag, vereins_id, count(distinct(spieler_id))
                        from bl1_data_spieler_startelf_system
                        group by saison, spieltag, vereins_id
                        having count(distinct(spieler_id)) <9;''' 
                        
        if case == 35:
            query = '''select* from bl1_data_spieler_startelf_system;'''   
            
        if case == 36:
            query = '''select saison, spieltag, count(distinct(vereins_id))
                        from bl1_data_spieler_startelf_system
                        group by saison, spieltag
                        having count(distinct(vereins_id)) != 18;'''

        if case == 37:
            query = '''select saison, count(distinct(Spieltag))
                        from bl1_data_spieler_startelf_system
                        group by saison;''' 
        if case == 38:     
            query = '''select 
                        	saison,
                        	count(distinct Spieltag) 
                        from 
                        	bl1_data_spieler_verletzt
                        group by 
                        	saison;''' 
                        
        if case == 39:
            query = '''select* from bl1_data_spieler_verletzt;'''   
            
        if case == 40:
            query = '''select 
                        	saison,
                        	count(distinct vereins_id) as Clubs_Nbr
                        from 
                        	bl1_data_spieler_verletzt
                        group by 
                        	saison;'''

        if case == 41:
            query = '''select *
                        from bl1_data_spieler_verletzt
                        where datum > Bis or datum < Von;''' 
        if case == 42:
            query = '''select 
                        	saison,
                            spieltag,
                            count(distinct(Spieler_ID)) as injured_players
                        from 
                        	bl1_data_spieler_verletzt
                        group by 
                        	saison, Spieltag
                        having 
                        	count(distinct(Spieler_ID)) < 60 
                        or 
                        	count(distinct(Spieler_ID)) > 160 ;''' 
        if case == 43:
            query = '''select saison, spieltag, count(distinct(vereins_id))
                        from bl1_data_spieler_startelf_system
                        group by saison, spieltag
                        having count(distinct(vereins_id)) != 18;'''
                        
        if case == 44:     
            query = '''select 
                        	saison,
                            count(distinct(Spieler_ID)) as injured_players
                        from 
                        	bl1_staging_spieler_verletzt
                        group by 
                        	saison;''' 
                        
        if case == 45:
            query = '''select* from bl1_staging_spieler_verletzt;'''   
                        
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd="Teleshop,1871",
            database = 'bl1_daten'
        )
        
        df = pd.read_sql(query, con = mydb)
            
        return df 
    

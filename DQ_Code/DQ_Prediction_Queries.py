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
                        	e.Saison,
                        	e.Spieltag, 
                        	count(distinct(e.Heimmannschaft_ID)), 
                            count(distinct(e.Auswärtsmannschaft_ID))
                        from 
                        	bl1_staging_ergebnisse e
                        inner join 
                        	bl1_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
                        inner join 
                        	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
                        inner join 
                        	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
                        inner join 
                        	bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
                        left outer join 
                        	master_system ms on ms.System = vss1.Spiel_System
                        left outer join 
                        	master_system ms1 on ms1.System = vss2.Spiel_System
                        inner join 
                        	bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
                        inner join 
                        	bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
                        group by 
                            e.Saison, e.Spieltag
                        having 
                        	count(distinct(e.Heimmannschaft_ID)) != 9
                        or 
                        	count(distinct(e.Heimmannschaft_ID)) != count(distinct(e.Auswärtsmannschaft_ID))
                        order by 
                        	e.Saison, e.Spieltag
                        ;'''  
                    
        if case == 2:
            query = '''select 
                        	e.Saison,
                        	count(distinct(e.Spieltag))
                        from 
                        	bl1_staging_ergebnisse e
                        inner join 
                        	bl1_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
                        inner join 
                        	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
                        inner join 
                        	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
                        inner join 
                        	bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
                        left outer join 
                        	master_system ms on ms.System = vss1.Spiel_System
                        left outer join 
                        	master_system ms1 on ms1.System = vss2.Spiel_System
                        inner join 
                        	bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
                        inner join 
                        	bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
                        group by 
                        	saison
                        order by 
                        	e.Saison, e.Spieltag
                        ;'''  
                        
        if case == 3:
            query = '''
                        select 
                        	e.Saison,
                        	e.Spieltag,
                        	e.Heimmannschaft_ID,
                        	e.Auswärtsmannschaft_ID
                        from 
                        	bl1_staging_ergebnisse e
                        inner join 
                        	bl1_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
                        inner join 
                        	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
                        inner join 
                        	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
                        inner join 
                        	bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
                        left outer join 
                        	master_system ms on ms.System = vss1.Spiel_System
                        left outer join 
                        	master_system ms1 on ms1.System = vss2.Spiel_System
                        inner join 
                        	bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
                        inner join 
                        	bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
                        order by 
                        	e.Saison, e.Spieltag

                        ;'''  
        if case == 4:
            query = '''select 
                        	e.Saison,
                        	e.Spieltag, 
                        	count(distinct(e.Heimmannschaft_ID)), 
                            count(distinct(e.Auswärtsmannschaft_ID))
                        from 
                        	bl1_staging_ergebnisse e
                        inner join 
                        	bl1_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
                        inner join 
                        	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
                        inner join 
                        	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
                        inner join 
                        	bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
                        left outer join 
                        	master_system ms on ms.System = vss1.Spiel_System
                        left outer join 
                        	master_system ms1 on ms1.System = vss2.Spiel_System
                        inner join 
                        	bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
                        inner join 
                        	bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
                        group by
                        	Saison, Spieltag
                        having 
                        	e.Saison >= '2014/15' 
                        and 
                        	count(distinct(e.Heimmannschaft_ID)) != 9
                        or 
                        	count(distinct(e.Heimmannschaft_ID)) != count(distinct(e.Auswärtsmannschaft_ID))
                        order by 
                        	e.Saison, e.Spieltag
                        ;'''  
                    
        if case == 5:
            query = '''select 
                        	e.Saison,
                        	count(distinct(e.Spieltag))
                        from 
                        	bl1_staging_ergebnisse e
                        inner join 
                        	bl1_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
                        inner join 
                        	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
                        inner join 
                        	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
                        inner join 
                        	bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
                        left outer join 
                        	master_system ms on ms.System = vss1.Spiel_System
                        left outer join 
                        	master_system ms1 on ms1.System = vss2.Spiel_System
                        inner join 
                        	bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
                        inner join 
                        	bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
                        group by 
                        	e.Saison
                        having
                        	e.Saison >= '2014/15'
                        order by 
                        	e.Saison, e.Spieltag
                        ;'''  
                        
        if case == 6:
            query = '''select 
                        	e.Saison,
                        	e.Spieltag,
                            e.Heimmannschaft_ID,
                            e.Auswärtsmannschaft_ID
                        from 
                        	bl1_staging_ergebnisse e
                        inner join 
                        	bl1_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
                        inner join 
                        	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
                        inner join 
                        	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
                        inner join 
                        	bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
                        left outer join 
                        	master_system ms on ms.System = vss1.Spiel_System
                        left outer join 
                        	master_system ms1 on ms1.System = vss2.Spiel_System
                        inner join 
                        	bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
                        inner join 
                        	bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
                        group by 
                        	e.Saison
                        having
                        	e.Saison >= '2014/15'
                        order by 
                        	e.Saison, e.Spieltag

                        ;'''   
        if case == 7:
            query = '''	
                        select                      
            				e.Saison,
            				e.Spieltag, 
            				count(distinct(e.Heimmannschaft_ID)), 
            				count(distinct(e.Auswärtsmannschaft_ID))
            			from 
            				pl_staging_ergebnisse e
            			inner join 
            				pl_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
            			inner join 
            				pl_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
            			inner join 
            				pl_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
            			inner join 
            				pl_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
            			inner join 
            				pl_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
            			inner join 
            				pl_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
            			inner join 
            				pl_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            			inner join 
            				pl_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
            			inner join 
            				pl_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
            			inner join 
            				pl_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
            			inner join 
            				pl_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
            			inner join 
            				pl_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
            			left outer join 
            				master_system ms on ms.System = vss1.Spiel_System
            			left outer join 
            				master_system ms1 on ms1.System = vss2.Spiel_System
            			inner join 
            				pl_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
            			inner join 
            				pl_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
            			group by 
            				e.Saison, e.Spieltag
            			having 
            				count(distinct(e.Heimmannschaft_ID)) != 10
            			or 
            				count(distinct(e.Heimmannschaft_ID)) != count(distinct(e.Auswärtsmannschaft_ID))
            			order by 
            				e.Saison, e.Spieltag

                        ;'''  
        if case == 8:
            query = '''				
                        select                      
                            e.Saison,
                            count(distinct(e.Spieltag))
            			from 
            				pl_staging_ergebnisse e
            			inner join 
            				pl_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
            			inner join 
            				pl_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
            			inner join 
            				pl_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
            			inner join 
            				pl_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
            			inner join 
            				pl_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
            			inner join 
            				pl_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
            			inner join 
            				pl_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            			inner join 
            				pl_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
            			inner join 
            				pl_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
            			inner join 
            				pl_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
            			inner join 
            				pl_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
            			inner join 
            				pl_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
            			left outer join 
            				master_system ms on ms.System = vss1.Spiel_System
            			left outer join 
            				master_system ms1 on ms1.System = vss2.Spiel_System
            			inner join 
            				pl_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
            			inner join 
            				pl_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
            			group by 
            				e.Saison
            			order by 
            				e.Saison

                        ;'''         
        if case == 9:
            query = '''				
                        select 
                        	e.Saison,
                        	e.Spieltag,
                        	e.Heimmannschaft_ID,
                        	e.Auswärtsmannschaft_ID
            			from 
            				pl_staging_ergebnisse e
            			inner join 
            				pl_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Spieltag = k.Spieltag
            			inner join 
            				pl_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Spieltag = kw.Spieltag
            			inner join 
            				pl_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Spieltag = kw1.Spieltag
            			inner join 
            				pl_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Spieltag = ff.Spieltag
            			inner join 
            				pl_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Spieltag = ff2.Spieltag
            			inner join 
            				pl_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Spieltag = ts.Spieltag
            			inner join 
            				pl_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            			inner join 
            				pl_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
            			inner join 
            				pl_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
            			inner join 
            				pl_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  and e.Saison = o.Saison and e.Spieltag = o.Spieltag
            			inner join 
            				pl_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  and e.Saison = vss1.Saison and e.Spieltag = vss1.Spieltag
            			inner join 
            				pl_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID  and e.Saison = vss2.Saison and e.Spieltag = vss2.Spieltag
            			left outer join 
            				master_system ms on ms.System = vss1.Spiel_System
            			left outer join 
            				master_system ms1 on ms1.System = vss2.Spiel_System
            			inner join 
            				pl_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
            			inner join 
            				pl_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
            			order by 
            				e.Saison, e.Spieltag

                        ;'''                                    
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd="Teleshop,1871",
            database = 'bl1_daten'
        )
        
        df = pd.read_sql(query, con = mydb)
            
        return df 
    
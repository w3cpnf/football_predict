import os
os.chdir('D:/Projects/Football/Prediction_Code')


import pandas as pd
#import mysql
import mysql.connector 


class get_data_db:
    
    def __init__(self, case):
        self.case = case
        
    def get_data(self):
        
        case = self.case
                        
        if case == 1:
                        query = ''' 

                                SELECT 
                                	s.Saison AS Saison,
                                	s.Spieltag AS Spieltag,
                                	s.Heimmannschaft_ID AS Heimmannschaft_ID,
                                	s.Heimmannschaft AS Heimmannschaft,
                                	s.Auswärtsmannschaft_ID AS Gegner_ID,
                                	s.Auswärtsmannschaft AS Gegner,
                                	(kw.Kaderwert_Million - kw1.Kaderwert_Million) AS Kaderwert_Differenz,
                                	(kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million) AS Kaderwert_Per_Spieler_Differenz,
                                	(ff.Abwehr - ff2.Abwehr) AS Abwehrdifferenz,
                                	(ff.Gesamt - ff2.Gesamt) AS Gesamtdiffferenz,
                                	(ff.Angriff - ff2.Angriff) AS Angriffdifferenz,
                                	(ff.Mittelfeld - ff2.Mittelfeld) AS Mittelfelddifferenz,
                                	(ff.Angriff - ff2.Abwehr) AS Heimangriff_Abwehr_Differenz,
                                	(ff2.Angriff - ff.Abwehr) AS Auswärtsangriff_Abwehr_Differenz,
                                	ts.Trainer_ID AS Trainer_ID,
                                	ts1.Trainer_ID AS Gegner_Trainer_ID,
                                	f.L1_Forecast AS L1,
                                	f.L2_Forecast AS L2,
                                	f.L3_Forecast AS L3,
                                	f.L4_Forecast AS L4,
                                	f.L5_Forecast AS L5,
                                	fa.L1_Forecast as GegnerL1,
                                	fa.L2_Forecast as GegnerL2,
                                	fa.L3_Forecast as GegnerL3,
                                	fa.L4_Forecast as GegnerL4,
                                	fa.L5_Forecast as GegnerL5
                                FROM
                                	bl1_staging_vereine_kommende_spieltag s
                                	JOIN bl1_data_vereine_kader_wert kw ON s.Heimmannschaft_ID = kw.Vereins_ID
                                		AND s.Saison =  kw.Saison 
                                		AND s.Spieltag = kw.Spieltag
                                	JOIN bl1_data_vereine_kader_wert kw1 ON s.Auswärtsmannschaft_ID = kw1.Vereins_ID
                                		AND s.Saison =  kw1.Saison
                                		AND s.Spieltag = kw1.Spieltag
                                	JOIN bl1_staging_vereine_fifa_features ff ON s.Heimmannschaft_ID = ff.Vereins_ID
                                		AND s.Saison = ff.Saison 
                                		AND s.Spieltag = ff.Spieltag
                                	JOIN bl1_staging_vereine_fifa_features ff2 ON s.Auswärtsmannschaft_ID = ff2.Vereins_ID
                                		AND s.Saison = ff2.Saison
                                		AND s.Spieltag = ff2.Spieltag
                                	JOIN bl1_data_trainer_spiele ts ON s.Heimmannschaft_ID = ts.Vereins_ID
                                		AND s.Saison = ts.Saison
                                		AND s.Spieltag = ts.Spieltag
                                	JOIN bl1_data_trainer_spiele ts1 ON s.Auswärtsmannschaft_ID = ts1.Vereins_ID
                                		AND s.Saison = ts1.Saison
                                		AND s.Spieltag = ts1.Spieltag
                                	JOIN bl1_features_forecast_club_form f ON s.Heimmannschaft_ID = f.Vereins_ID
                                		AND s.Saison = f.Saison
                                		AND s.Spieltag = f.Spieltag
                                	JOIN bl1_features_forecast_club_form fa ON s.Heimmannschaft_ID = fa.Vereins_ID
                                		AND s.Saison = fa.Saison
                                		AND s.Spieltag = fa.Spieltag
;'''
        if case == 2:
            query = '''
                    SELECT 
                    	s.Saison AS Saison,
                    	s.Spieltag AS Spieltag,
                    	s.Heimmannschaft_ID AS Heimmannschaft_ID,
                    	s.Auswärtsmannschaft_ID AS Gegner_ID,
                    	o.B365H,
                    	o.B365A,
                    	o.B365D,
                    	ms.System_ID as HeimSystem,
                    	ms1.System_ID as AuswärtsSystem,
                    	cl1.Shot_Feature as Home_Shot_Feature,
                    	cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                    	cl1.Fouls_Feature as Home_Fouls_Feature,
                    	cl1.Corner_Feature as Home_Corner_Feature,
                    	cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                    	cl1.Redcard_Feature as Home_Redcard_Feature,
                    	cl2.Shot_Feature as Away_Shot_Feature,
                    	cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                    	cl2.Fouls_Feature as Away_Fouls_Feature,
                    	cl2.Corner_Feature as Away_Corner_Feature,
                    	cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                    	cl2.Redcard_Feature as Away_Redcard_Feature,
                    	ste1.Spieler_1,
                    	ste1.Spieler_2,
                    	ste1.Spieler_3,
                    	ste1.Spieler_4,
                    	ste1.Spieler_5,
                    	ste1.Spieler_6,
                    	ste1.Spieler_7,
                    	ste1.Spieler_8,
                    	ste1.Spieler_9,
                    	ste1.Spieler_10,
                    	ste1.Spieler_11,
                    	ste2.Spieler_1 as Gegner_Spieler_1,
                    	ste2.Spieler_2 as Gegner_Spieler_2,
                    	ste2.Spieler_3 as Gegner_Spieler_3,
                    	ste2.Spieler_4 as Gegner_Spieler_4,
                    	ste2.Spieler_5 as Gegner_Spieler_5,
                    	ste2.Spieler_6 as Gegner_Spieler_6,
                    	ste2.Spieler_7 as Gegner_Spieler_7,
                    	ste2.Spieler_8 as Gegner_Spieler_8,
                    	ste2.Spieler_9 as Gegner_Spieler_9,
                    	ste2.Spieler_10 as Gegner_Spieler_10,
                    	ste2.Spieler_11 as Gegner_Spieler_11
                    FROM
                    	bl1_staging_vereine_kommende_spieltag s
                    	JOIN bl1_features_odds o ON s.Heimmannschaft_ID = o.Heimmannschaft_ID
                    		AND s.Saison = o.Saison
                    		AND s.Spieltag = o.Spieltag
                    	JOIN bl1_data_vereine_spielsystem vss1 on s.Heimmannschaft_ID = vss1.Vereins_ID  
                    		and s.Saison = vss1.Saison 
                    		and s.Spieltag = vss1.Spieltag
                    	JOIN bl1_data_vereine_spielsystem vss2 on s.Auswärtsmannschaft_ID = vss2.Vereins_ID  
                    		and s.Saison = vss2.Saison 
                    		and s.Spieltag = vss2.Spieltag
                    	left outer join 
                    		master_system ms on ms.System = vss1.Spiel_System
                    	left outer join 
                        	master_system ms1 on ms1.System = vss2.Spiel_System
                    	inner join 
                    		bl1_features_forecast_club_data cl1 on s.Heimmannschaft_ID = cl1.Vereins_ID  and s.Saison = cl1.Saison and s.Spieltag = cl1.Spieltag
                    	inner join 
                    		bl1_features_forecast_club_data cl2 on s.Auswärtsmannschaft_ID = cl2.Vereins_ID  and s.Saison = cl2.Saison and s.Spieltag = cl2.Spieltag
                    	inner join 
                    		bl1_features_startelf ste1 on s.Heimmannschaft_ID = ste1.Vereins_ID  and s.Saison = ste1.Saison and s.Spieltag = ste1.Spieltag
                    	inner join 
                        	bl1_features_startelf ste2 on s.Auswärtsmannschaft_ID = ste2.Vereins_ID  and s.Saison = ste2.Saison and s.Spieltag = ste2.Spieltag;''' 
                        
        if case == 4:
            query = '''select* from bl1_staging_vereine_kommende_spieltag;'''
            
        if case == 5:
            query = '''select 
                        	e.Saison,
                        	e.Spieltag, 
                        	e.Heimmannschaft_ID, 
                        	e.Auswärtsmannschaft_ID as Gegner_ID, 
                            k.Tore,
                            k.Gegentore,
                        	k.Spiel_Ausgang, 
                        	kw.Kaderwert_Million - kw1.Kaderwert_Million as Kaderwert_Differenz,
                        	kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million as Kaderwert_Per_Spieler_Differenz,
                        	ff.Abwehr - ff2.Abwehr as Abwehrdifferenz,
                        	ff.Gesamt - ff2.Gesamt as Gesamtdiffferenz,
                        	ff.Angriff - ff2.Angriff as Angriffdifferenz,
                        	ff.Mittelfeld - ff2.Mittelfeld as Mittelfelddifferenz,
                        	ff.Angriff - ff2.Abwehr as Heimangriff_Abwehr_Differenz, 
                        	ff2.Angriff - ff.Abwehr as Auswärtsangriff_Abwehr_Differenz,
                        	ts.Trainer_ID,
                        	ts1.Trainer_ID as Gegner_Trainer_ID,
                        	f.L1,
                        	f.L2,
                        	f.L3,
                        	f.L4,
                        	f.L5,
                        	fa.L1 as GegnerL1,
                        	fa.L2 as GegnerL2,
                        	fa.L3 as GegnerL3,
                        	fa.L4 as GegnerL4,
                        	fa.L5 as GegnerL5,
                        	odds.B365H,
                        	odds.B365D,
                        	odds.B365A,
                            ms.System_ID as Home_System,
                            ms1.System_ID as Away_System
                        from 
                        	bl1_staging_ergebnisse e
                        inner join 
                        	bl1_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID and e.Saison = k.Saison and e.Jahr = k.Jahr  and e.Spieltag = k.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID  and e.Saison = kw.Saison and e.Jahr = kw.Jahr and e.Spieltag = kw.Spieltag
                        inner join 
                        	bl1_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID  and e.Saison = kw1.Saison and e.Jahr = kw1.Jahr and e.Spieltag = kw1.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID  and e.Saison = ff.Saison and e.Jahr = ff.Jahr and e.Spieltag = ff.Spieltag
                        inner join 
                        	bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID  and e.Saison = ff2.Saison and e.Jahr = ff2.Jahr and e.Spieltag = ff2.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID  and e.Saison = ts.Saison and e.Jahr = ts.Jahr and e.Spieltag = ts.Spieltag
                        inner join 
                        	bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID  and e.Saison = ts1.Saison and e.Jahr = ts1.Jahr and e.Spieltag = ts1.Spieltag
                        inner join 
                        	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Jahr = f.Jahr and e.Spieltag = f.Spieltag
                        inner join 
                        	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Jahr = fa.Jahr and e.Spieltag = fa.Spieltag
                        inner join 
                        	bl1_data_vereine_bookmaker_odds odds on e.Heimmannschaft_ID = odds.Heimmannschaft_ID  and e.Saison = odds.Saison and e.Spieltag = odds.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem ss on e.Heimmannschaft_ID = ss.Vereins_ID  and e.Saison = ss.Saison and e.Spieltag = ss.Spieltag
                        inner join 
                        	bl1_data_vereine_spielsystem ss1 on e.Auswärtsmannschaft_ID = ss1.Vereins_ID  and e.Saison = ss1.Saison and e.Spieltag = ss1.Spieltag
                        left outer join 
                        	master_system ms on ms.System = ss.Spiel_System
                        left outer join 
                        	master_system ms1 on ms1.System = ss1.Spiel_System
                        order by 
                        	e.Saison, e.Spieltag;'''
        if case == 6:
            query = '''
                        select
                        	s.Saison AS Saison,
                        	s.Spieltag AS Spieltag,
                        	s.Heimmannschaft_ID AS Heimmannschaft_ID,
                        	s.Heimmannschaft AS Heimmannschaft,
                        	s.Auswärtsmannschaft_ID AS Gegner_ID,
                        	s.Auswärtsmannschaft AS Gegner,
                        	(kw.Kaderwert_Million - kw1.Kaderwert_Million) AS Kaderwert_Differenz,
                        	(kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million) AS Kaderwert_Per_Spieler_Differenz,
                        	(ff.Abwehr - ff2.Abwehr) AS Abwehrdifferenz,
                        	(ff.Gesamt - ff2.Gesamt) AS Gesamtdiffferenz,
                        	(ff.Angriff - ff2.Angriff) AS Angriffdifferenz,
                        	(ff.Mittelfeld - ff2.Mittelfeld) AS Mittelfelddifferenz,
                        	(ff.Angriff - ff2.Abwehr) AS Heimangriff_Abwehr_Differenz,
                        	(ff2.Angriff - ff.Abwehr) AS Auswärtsangriff_Abwehr_Differenz,
                        	ts.Trainer_ID AS Trainer_ID,
                        	ts1.Trainer_ID AS Gegner_Trainer_ID,
                        	f.L1_Forecast AS L1,
                        	f.L2_Forecast AS L2,
                        	f.L3_Forecast AS L3,
                        	f.L4_Forecast AS L4,
                        	f.L5_Forecast AS L5,
                        	fa.L1_Forecast as GegnerL1,
                        	fa.L2_Forecast as GegnerL2,
                        	fa.L3_Forecast as GegnerL3,
                        	fa.L4_Forecast as GegnerL4,
                        	fa.L5_Forecast as GegnerL5,
                            ek.Tore as Heimtore
                        FROM
                        bl1_staging_vereine_kommende_spieltag s
                        JOIN bl1_data_vereine_kader_wert kw ON s.Heimmannschaft_ID = kw.Vereins_ID
                        	AND s.Saison =  kw.Saison 
                        	AND s.Spieltag = kw.Spieltag
                        JOIN bl1_data_vereine_kader_wert kw1 ON s.Auswärtsmannschaft_ID = kw1.Vereins_ID
                        	AND s.Saison =  kw1.Saison
                        	AND s.Spieltag = kw1.Spieltag
                        JOIN bl1_staging_vereine_fifa_features ff ON s.Heimmannschaft_ID = ff.Vereins_ID
                        	AND s.Saison = ff.Saison 
                        	AND s.Spieltag = ff.Spieltag
                        JOIN bl1_staging_vereine_fifa_features ff2 ON s.Auswärtsmannschaft_ID = ff2.Vereins_ID
                        	AND s.Saison = ff2.Saison
                        	AND s.Spieltag = ff2.Spieltag
                        JOIN bl1_data_trainer_spiele ts ON s.Heimmannschaft_ID = ts.Vereins_ID
                        	AND s.Saison = ts.Saison
                        	AND s.Spieltag = ts.Spieltag
                        JOIN bl1_data_trainer_spiele ts1 ON s.Auswärtsmannschaft_ID = ts1.Vereins_ID
                        	AND s.Saison = ts1.Saison
                        	AND s.Spieltag = ts1.Spieltag
                        JOIN bl1_features_forecast_club_form f ON s.Heimmannschaft_ID = f.Vereins_ID
                        	AND s.Saison = f.Saison
                        	AND s.Spieltag = f.Spieltag
                        JOIN bl1_features_forecast_club_form fa ON s.Heimmannschaft_ID = fa.Vereins_ID
                        	AND s.Saison = fa.Saison
                        	AND s.Spieltag = fa.Spieltag
                        JOIN bl1_data_ergebnisse_kategorisiert ek ON s.Heimmannschaft_ID = ek.Vereins_ID
                        	AND s.Saison = ek.Saison
                        	AND (s.Spieltag-1) = ek.Spieltag

;'''  
        if case == 7:
            query = '''                    
                        select
                        	e.Saison,
                        	e.Spieltag, 
                        	e.Heimmannschaft,
                        	e.Heimmannschaft_ID, 
                        	e.Auswärtsmannschaft as Gegner, 
                        	e.Auswärtsmannschaft_ID as Gegner_ID, 
                        	k.Spiel_Ausgang, 
                        	kw.Kaderwert_Million - kw1.Kaderwert_Million as Kaderwert_Differenz,
                        	kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million as Kaderwert_Per_Spieler_Differenz,
                        	ff.Abwehr - ff2.Abwehr as Abwehrdifferenz,
                        	ff.Gesamt - ff2.Gesamt as Gesamtdiffferenz,
                        	ff.Angriff - ff2.Angriff as Angriffdifferenz,
                        	ff.Mittelfeld - ff2.Mittelfeld as Mittelfelddifferenz,
                        	ff.Angriff - ff2.Abwehr as Heimangriff_Abwehr_Differenz, 
                        	ff2.Angriff - ff.Abwehr as Auswärtsangriff_Abwehr_Differenz,
                        	ts.Trainer,
                        	ts.Trainer_ID,
                        	ts1.Trainer_ID as Gegner_Trainer_ID,
                        	f.L1,
                        	f.L2,
                        	f.L3,
                        	f.L4,
                        	f.L5,
                        	fa.L1 as GegnerL1,
                        	fa.L2 as GegnerL2,
                        	fa.L3 as GegnerL3,
                        	fa.L4 as GegnerL4,
                        	fa.L5 as GegnerL5,
                        	o.B365H,
                        	o.B365D,
                        	o.B365A,
                        	ms.System_ID as HeimSystem,
                        	ms1.System_ID as AuswärtsSystem,
                            cl1.Shot_Feature as Home_Shot_Feature,
                            cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                            cl1.Fouls_Feature as Home_Fouls_Feature,
                            cl1.Corner_Feature as Home_Corner_Feature,
                            cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                            cl1.Redcard_Feature as Home_Redcard_Feature,
                        	cl2.Shot_Feature as Away_Shot_Feature,
                            cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                            cl2.Fouls_Feature as Away_Fouls_Feature,
                            cl2.Corner_Feature as Away_Corner_Feature,
                            cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                            cl2.Redcard_Feature as Away_Redcard_Feature
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
                            e.saison, e.Spieltag;'''  

        if case == 8:
            query = '''                    
            select
                        	e.Saison,
                        	e.Spieltag, 
                        	e.Heimmannschaft,
                        	e.Heimmannschaft_ID, 
                        	e.Auswärtsmannschaft as Gegner, 
                        	e.Auswärtsmannschaft_ID as Gegner_ID, 
                        	k.Spiel_Ausgang, 
                        	kw.Kaderwert_Million - kw1.Kaderwert_Million as Kaderwert_Differenz,
                        	kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million as Kaderwert_Per_Spieler_Differenz,
                        	ff.Abwehr - ff2.Abwehr as Abwehrdifferenz,
                        	ff.Gesamt - ff2.Gesamt as Gesamtdiffferenz,
                        	ff.Angriff - ff2.Angriff as Angriffdifferenz,
                        	ff.Mittelfeld - ff2.Mittelfeld as Mittelfelddifferenz,
                        	ff.Angriff - ff2.Abwehr as Heimangriff_Abwehr_Differenz, 
                        	ff2.Angriff - ff.Abwehr as Auswärtsangriff_Abwehr_Differenz,
                        	ts.Trainer,
                        	ts.Trainer_ID,
                        	ts1.Trainer_ID as Gegner_Trainer_ID,
                        	f.L1,
                        	f.L2,
                        	f.L3,
                        	f.L4,
                        	f.L5,
                        	fa.L1 as GegnerL1,
                        	fa.L2 as GegnerL2,
                        	fa.L3 as GegnerL3,
                        	fa.L4 as GegnerL4,
                        	fa.L5 as GegnerL5,
                        	o.B365H,
                        	o.B365D,
                        	o.B365A,
                            ms.System_ID as HeimSystem,
                            ms1.System_ID as AuswärtsSystem,
                            cl1.Shot_Feature as Home_Shot_Feature,
                            cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                            cl1.Fouls_Feature as Home_Fouls_Feature,
                            cl1.Corner_Feature as Home_Corner_Feature,
                            cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                            cl1.Redcard_Feature as Home_Redcard_Feature,
                        	cl2.Shot_Feature as Away_Shot_Feature,
                            cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                            cl2.Fouls_Feature as Away_Fouls_Feature,
                            cl2.Corner_Feature as Away_Corner_Feature,
                            cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                            cl2.Redcard_Feature as Away_Redcard_Feature
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
                        	e.Saison, e.Spieltag;'''  
        if case == 9:
            query = '''                    
            SELECT 
            	s.Saison AS Saison,
            	s.Spieltag AS Spieltag,
            	s.Heimmannschaft_ID AS Heimmannschaft_ID,
            	s.Heimmannschaft AS Heimmannschaft,
            	s.Auswärtsmannschaft_ID AS Gegner_ID,
            	s.Auswärtsmannschaft AS Gegner,
            	(kw.Kaderwert_Million - kw1.Kaderwert_Million) AS Kaderwert_Differenz,
            	(kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million) AS Kaderwert_Per_Spieler_Differenz,
            	(ff.Abwehr - ff2.Abwehr) AS Abwehrdifferenz,
            	(ff.Gesamt - ff2.Gesamt) AS Gesamtdiffferenz,
            	(ff.Angriff - ff2.Angriff) AS Angriffdifferenz,
            	(ff.Mittelfeld - ff2.Mittelfeld) AS Mittelfelddifferenz,
            	(ff.Angriff - ff2.Abwehr) AS Heimangriff_Abwehr_Differenz,
            	(ff2.Angriff - ff.Abwehr) AS Auswärtsangriff_Abwehr_Differenz,
            	ts.Trainer_ID AS Trainer_ID,
            	ts1.Trainer_ID AS Gegner_Trainer_ID,
            	f.L1_Forecast AS L1,
            	f.L2_Forecast AS L2,
            	f.L3_Forecast AS L3,
            	f.L4_Forecast AS L4,
            	f.L5_Forecast AS L5,
            	fa.L1_Forecast as GegnerL1,
            	fa.L2_Forecast as GegnerL2,
            	fa.L3_Forecast as GegnerL3,
            	fa.L4_Forecast as GegnerL4,
            	fa.L5_Forecast as GegnerL5,
            	o.B365H,
            	o.B365A,
            	o.B365D,
            	ms.System_ID as HeimSystem,
            	ms1.System_ID as AuswärtsSystem,
                cl1.Shot_Feature as Home_Shot_Feature,
                cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                cl1.Fouls_Feature as Home_Fouls_Feature,
                cl1.Corner_Feature as Home_Corner_Feature,
                cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                cl1.Redcard_Feature as Home_Redcard_Feature,
            	cl2.Shot_Feature as Away_Shot_Feature,
                cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                cl2.Fouls_Feature as Away_Fouls_Feature,
                cl2.Corner_Feature as Away_Corner_Feature,
                cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                cl2.Redcard_Feature as Away_Redcard_Feature
            FROM
            	pl_staging_vereine_kommende_spieltag s
            	JOIN pl_data_vereine_kader_wert kw ON s.Heimmannschaft_ID = kw.Vereins_ID
            		AND s.Saison =  kw.Saison 
            		AND s.Spieltag = kw.Spieltag
            	JOIN pl_data_vereine_kader_wert kw1 ON s.Auswärtsmannschaft_ID = kw1.Vereins_ID
            		AND s.Saison =  kw1.Saison
            		AND s.Spieltag = kw1.Spieltag
            	JOIN pl_staging_vereine_fifa_features ff ON s.Heimmannschaft_ID = ff.Vereins_ID
            		AND s.Saison = ff.Saison 
            		AND s.Spieltag = ff.Spieltag
            	JOIN pl_staging_vereine_fifa_features ff2 ON s.Auswärtsmannschaft_ID = ff2.Vereins_ID
            		AND s.Saison = ff2.Saison
            		AND s.Spieltag = ff2.Spieltag
            	JOIN pl_data_trainer_spiele ts ON s.Heimmannschaft_ID = ts.Vereins_ID
            		AND s.Saison = ts.Saison
            		AND s.Spieltag = ts.Spieltag
            	JOIN pl_data_trainer_spiele ts1 ON s.Auswärtsmannschaft_ID = ts1.Vereins_ID
            		AND s.Saison = ts1.Saison
            		AND s.Spieltag = ts1.Spieltag
            	JOIN pl_features_forecast_club_form f ON s.Heimmannschaft_ID = f.Vereins_ID
            		AND s.Saison = f.Saison
            		AND s.Spieltag = f.Spieltag
            	JOIN pl_features_forecast_club_form fa ON s.Heimmannschaft_ID = fa.Vereins_ID
            		AND s.Saison = fa.Saison
            		AND s.Spieltag = fa.Spieltag
            	JOIN pl_features_odds o ON s.Heimmannschaft_ID = o.Heimmannschaft_ID
            		AND s.Saison = o.Saison
            		AND s.Spieltag = o.Spieltag
            	JOIN pl_data_vereine_spielsystem vss1 on s.Heimmannschaft_ID = vss1.Vereins_ID  
            		and s.Saison = vss1.Saison 
            		and s.Spieltag = vss1.Spieltag
            	JOIN pl_data_vereine_spielsystem vss2 on s.Auswärtsmannschaft_ID = vss2.Vereins_ID  
            		and s.Saison = vss2.Saison 
            		and s.Spieltag = vss2.Spieltag
            	left outer join 
            		master_system ms on ms.System = vss1.Spiel_System
            	left outer join 
            		master_system ms1 on ms1.System = vss2.Spiel_System
            	inner join 
            		pl_features_forecast_club_data cl1 on s.Heimmannschaft_ID = cl1.Vereins_ID  and s.Saison = cl1.Saison and s.Spieltag = cl1.Spieltag
            	inner join 
            		pl_features_forecast_club_data cl2 on s.Auswärtsmannschaft_ID = cl2.Vereins_ID  and s.Saison = cl2.Saison and s.Spieltag = cl2.Spieltag
            	order by 
            		s.saison, s.spieltag
        ;'''        
                      
        if case == 10:
            query = '''                    
			select
            	e.Saison,
            	e.Spieltag, 
            	e.Heimmannschaft,
            	e.Heimmannschaft_ID, 
            	e.Auswärtsmannschaft as Gegner, 
            	e.Auswärtsmannschaft_ID as Gegner_ID, 
            	k.Spiel_Ausgang, 
            	kw.Kaderwert_Million - kw1.Kaderwert_Million as Kaderwert_Differenz,
            	kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million as Kaderwert_Per_Spieler_Differenz,
            	ff.Abwehr - ff2.Abwehr as Abwehrdifferenz,
            	ff.Gesamt - ff2.Gesamt as Gesamtdiffferenz,
            	ff.Angriff - ff2.Angriff as Angriffdifferenz,
            	ff.Mittelfeld - ff2.Mittelfeld as Mittelfelddifferenz,
            	ff.Angriff - ff2.Abwehr as Heimangriff_Abwehr_Differenz, 
            	ff2.Angriff - ff.Abwehr as Auswärtsangriff_Abwehr_Differenz,
            	ts.Trainer,
            	ts.Trainer_ID,
            	ts1.Trainer_ID as Gegner_Trainer_ID,
            	f.L1,
            	f.L2,
            	f.L3,
            	f.L4,
            	f.L5,
            	fa.L1 as GegnerL1,
            	fa.L2 as GegnerL2,
            	fa.L3 as GegnerL3,
            	fa.L4 as GegnerL4,
            	fa.L5 as GegnerL5,
            	o.B365H,
            	o.B365D,
            	o.B365A,
                cl1.Shot_Feature as Home_Shot_Feature,
                cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                cl1.Fouls_Feature as Home_Fouls_Feature,
                cl1.Corner_Feature as Home_Corner_Feature,
                cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                cl1.Redcard_Feature as Home_Redcard_Feature,
            	cl2.Shot_Feature as Away_Shot_Feature,
                cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                cl2.Fouls_Feature as Away_Fouls_Feature,
                cl2.Corner_Feature as Away_Corner_Feature,
                cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                cl2.Redcard_Feature as Away_Redcard_Feature
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
            	bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  and e.Saison = cl1.Saison and e.Spieltag = cl1.Spieltag
            inner join 
            	bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID  and e.Saison = cl2.Saison and e.Spieltag = cl2.Spieltag
            order by 
            	e.Saison, e.Spieltag
                            ;'''    
        if case == 11:
                        query = ''' 
                               SELECT 
                                	s.Saison AS Saison,
                                	s.Spieltag AS Spieltag,
                                	s.Heimmannschaft_ID AS Heimmannschaft_ID,
                                	s.Heimmannschaft AS Heimmannschaft,
                                	s.Auswärtsmannschaft_ID AS Gegner_ID,
                                	s.Auswärtsmannschaft AS Gegner,
                                	(kw.Kaderwert_Million - kw1.Kaderwert_Million) AS Kaderwert_Differenz,
                                	(kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million) AS Kaderwert_Per_Spieler_Differenz,
                                	(ff.Abwehr - ff2.Abwehr) AS Abwehrdifferenz,
                                	(ff.Gesamt - ff2.Gesamt) AS Gesamtdiffferenz,
                                	(ff.Angriff - ff2.Angriff) AS Angriffdifferenz,
                                	(ff.Mittelfeld - ff2.Mittelfeld) AS Mittelfelddifferenz,
                                	(ff.Angriff - ff2.Abwehr) AS Heimangriff_Abwehr_Differenz,
                                	(ff2.Angriff - ff.Abwehr) AS Auswärtsangriff_Abwehr_Differenz,
                                	ts.Trainer_ID AS Trainer_ID,
                                	ts1.Trainer_ID AS Gegner_Trainer_ID,
                                	f.L1_Forecast AS L1,
                                	f.L2_Forecast AS L2,
                                	f.L3_Forecast AS L3,
                                	f.L4_Forecast AS L4,
                                	f.L5_Forecast AS L5,
                                	fa.L1_Forecast as GegnerL1,
                                	fa.L2_Forecast as GegnerL2,
                                	fa.L3_Forecast as GegnerL3,
                                	fa.L4_Forecast as GegnerL4,
                                	fa.L5_Forecast as GegnerL5,
                                	o.B365H,
                                	o.B365A,
                                	o.B365D
                                    #cl1.Shot_Feature as Home_Shot_Feature,
                                    #cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                                    #cl1.Fouls_Feature as Home_Fouls_Feature,
                                    #cl1.Corner_Feature as Home_Corner_Feature,
                                    #cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                                    #cl1.Redcard_Feature as Home_Redcard_Feature,
                                	#cl2.Shot_Feature as Away_Shot_Feature,
                                    #cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                                    #cl2.Fouls_Feature as Away_Fouls_Feature,
                                    #cl2.Corner_Feature as Away_Corner_Feature,
                                    #cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                                    #cl2.Redcard_Feature as Away_Redcard_Feature
                                FROM
                                	bl1_staging_vereine_kommende_spieltag s
                                	JOIN bl1_data_vereine_kader_wert kw ON s.Heimmannschaft_ID = kw.Vereins_ID
                                		AND s.Saison =  kw.Saison 
                                		AND s.Spieltag = kw.Spieltag
                                	JOIN bl1_data_vereine_kader_wert kw1 ON s.Auswärtsmannschaft_ID = kw1.Vereins_ID
                                		AND s.Saison =  kw1.Saison
                                		AND s.Spieltag = kw1.Spieltag
                                	JOIN bl1_staging_vereine_fifa_features ff ON s.Heimmannschaft_ID = ff.Vereins_ID
                                		AND s.Saison = ff.Saison 
                                		AND s.Spieltag = ff.Spieltag
                                	JOIN bl1_staging_vereine_fifa_features ff2 ON s.Auswärtsmannschaft_ID = ff2.Vereins_ID
                                		AND s.Saison = ff2.Saison
                                		AND s.Spieltag = ff2.Spieltag
                                	JOIN bl1_data_trainer_spiele ts ON s.Heimmannschaft_ID = ts.Vereins_ID
                                		AND s.Saison = ts.Saison
                                		AND s.Spieltag = ts.Spieltag
                                	JOIN bl1_data_trainer_spiele ts1 ON s.Auswärtsmannschaft_ID = ts1.Vereins_ID
                                		AND s.Saison = ts1.Saison
                                		AND s.Spieltag = ts1.Spieltag
                                	JOIN bl1_features_forecast_club_form f ON s.Heimmannschaft_ID = f.Vereins_ID
                                		AND s.Saison = f.Saison
                                		AND s.Spieltag = f.Spieltag
                                	JOIN bl1_features_forecast_club_form fa ON s.Heimmannschaft_ID = fa.Vereins_ID
                                		AND s.Saison = fa.Saison
                                		AND s.Spieltag = fa.Spieltag
                                	JOIN bl1_features_odds o ON s.Heimmannschaft_ID = o.Heimmannschaft_ID
                                		AND s.Saison = o.Saison
                                		AND s.Spieltag = o.Spieltag
                                    #inner join 
                                    #    bl1_features_forecast_club_data cl1 on s.Heimmannschaft_ID = cl1.Vereins_ID  and s.Saison = cl1.Saison and s.Spieltag = cl1.Spieltag
                                    #inner join 
                                    #    bl1_features_forecast_club_data cl2 on s.Auswärtsmannschaft_ID = cl2.Vereins_ID  and s.Saison = cl2.Saison and s.Spieltag = cl2.Spieltag
;'''

        if case == 12:
                        query = ''' 
                                select
                                	e.Saison,
                                	e.Spieltag, 
                                	e.Heimmannschaft,
                                	e.Heimmannschaft_ID, 
                                	e.Auswärtsmannschaft_ID as Gegner_ID, 
                                	k.Spiel_Ausgang, 
                                	kw.Kaderwert_Million - kw1.Kaderwert_Million as Kaderwert_Differenz,
                                	kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million as Kaderwert_Per_Spieler_Differenz,
                                	ff.Abwehr - ff2.Abwehr as Abwehrdifferenz,
                                	ff.Gesamt - ff2.Gesamt as Gesamtdiffferenz,
                                	ff.Angriff - ff2.Angriff as Angriffdifferenz,
                                	ff.Mittelfeld - ff2.Mittelfeld as Mittelfelddifferenz,
                                	ff.Angriff - ff2.Abwehr as Heimangriff_Abwehr_Differenz, 
                                	ff2.Angriff - ff.Abwehr as Auswärtsangriff_Abwehr_Differenz,
                                	ts.Trainer,
                                	ts.Trainer_ID,
                                	ts1.Trainer_ID as Gegner_Trainer_ID,
                                	f.L1,
                                	f.L2,
                                	f.L3,
                                	f.L4,
                                	f.L5,
                                	fa.L1 as GegnerL1,
                                	fa.L2 as GegnerL2,
                                	fa.L3 as GegnerL3,
                                	fa.L4 as GegnerL4,
                                	fa.L5 as GegnerL5
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
;'''


        if case == 13:
                        query = ''' 
                            select
                            	e.Saison,
                            	e.Spieltag, 
                            	e.Heimmannschaft,
                            	e.Heimmannschaft_ID, 
                            	e.Auswärtsmannschaft_ID as Gegner_ID, 
                            	o.B365H,
                            	o.B365D,
                            	o.B365A,
                            	ms.System_ID as HeimSystem,
                            	ms1.System_ID as AuswärtsSystem,
                            	cl1.Shot_Feature as Home_Shot_Feature,
                            	cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                            	cl1.Fouls_Feature as Home_Fouls_Feature,
                            	cl1.Corner_Feature as Home_Corner_Feature,
                            	cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                            	cl1.Redcard_Feature as Home_Redcard_Feature,
                            	cl2.Shot_Feature as Away_Shot_Feature,
                            	cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                            	cl2.Fouls_Feature as Away_Fouls_Feature,
                            	cl2.Corner_Feature as Away_Corner_Feature,
                            	cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                            	cl2.Redcard_Feature as Away_Redcard_Feature,
                                ste1.Spieler_1,
                                ste1.Spieler_2,
                                ste1.Spieler_3,
                                ste1.Spieler_4,
                                ste1.Spieler_5,
                                ste1.Spieler_6,
                                ste1.Spieler_7,
                                ste1.Spieler_8,
                                ste1.Spieler_9,
                                ste1.Spieler_10,
                                ste1.Spieler_11,
                                ste2.Spieler_1 as Gegner_Spieler_1,
                                ste2.Spieler_2 as Gegner_Spieler_2,
                                ste2.Spieler_3 as Gegner_Spieler_3,
                                ste2.Spieler_4 as Gegner_Spieler_4,
                                ste2.Spieler_5 as Gegner_Spieler_5,
                                ste2.Spieler_6 as Gegner_Spieler_6,
                                ste2.Spieler_7 as Gegner_Spieler_7,
                                ste2.Spieler_8 as Gegner_Spieler_8,
                                ste2.Spieler_9 as Gegner_Spieler_9,
                                ste2.Spieler_10 as Gegner_Spieler_10,
                                ste2.Spieler_11 as Gegner_Spieler_11
                            from 
                            	bl1_staging_ergebnisse e
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
                            inner join 
                            	bl1_features_startelf ste1 on e.Heimmannschaft_ID = ste1.Vereins_ID  and e.Saison = ste1.Saison and e.Spieltag = ste1.Spieltag
                            inner join 
                            	bl1_features_startelf ste2 on e.Auswärtsmannschaft_ID = ste2.Vereins_ID  and e.Saison = ste2.Saison and e.Spieltag = ste2.Spieltag
;'''

        if case == 14:
            query = '''                    
            SELECT 
            	s.Saison AS Saison,
            	s.Spieltag AS Spieltag,
            	s.Heimmannschaft_ID AS Heimmannschaft_ID,
            	s.Heimmannschaft AS Heimmannschaft,
            	s.Auswärtsmannschaft_ID AS Gegner_ID,
            	s.Auswärtsmannschaft AS Gegner,
            	(kw.Kaderwert_Million - kw1.Kaderwert_Million) AS Kaderwert_Differenz,
            	(kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million) AS Kaderwert_Per_Spieler_Differenz,
            	(ff.Abwehr - ff2.Abwehr) AS Abwehrdifferenz,
            	(ff.Gesamt - ff2.Gesamt) AS Gesamtdiffferenz,
            	(ff.Angriff - ff2.Angriff) AS Angriffdifferenz,
            	(ff.Mittelfeld - ff2.Mittelfeld) AS Mittelfelddifferenz,
            	(ff.Angriff - ff2.Abwehr) AS Heimangriff_Abwehr_Differenz,
            	(ff2.Angriff - ff.Abwehr) AS Auswärtsangriff_Abwehr_Differenz,
            	ts.Trainer_ID AS Trainer_ID,
            	ts1.Trainer_ID AS Gegner_Trainer_ID,
            	f.L1_Forecast AS L1,
            	f.L2_Forecast AS L2,
            	f.L3_Forecast AS L3,
            	f.L4_Forecast AS L4,
            	f.L5_Forecast AS L5,
            	fa.L1_Forecast as GegnerL1,
            	fa.L2_Forecast as GegnerL2,
            	fa.L3_Forecast as GegnerL3,
            	fa.L4_Forecast as GegnerL4,
            	fa.L5_Forecast as GegnerL5,
            	o.B365H,
            	o.B365A,
            	o.B365D,
                cl1.Shot_Feature as Home_Shot_Feature,
                cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                cl1.Fouls_Feature as Home_Fouls_Feature,
                cl1.Corner_Feature as Home_Corner_Feature,
                cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                cl1.Redcard_Feature as Home_Redcard_Feature,
            	cl2.Shot_Feature as Away_Shot_Feature,
                cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                cl2.Fouls_Feature as Away_Fouls_Feature,
                cl2.Corner_Feature as Away_Corner_Feature,
                cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                cl2.Redcard_Feature as Away_Redcard_Feature
            FROM
            	pl_staging_vereine_kommende_spieltag s
            	JOIN pl_data_vereine_kader_wert kw ON s.Heimmannschaft_ID = kw.Vereins_ID
            		AND s.Saison =  kw.Saison 
            		AND s.Spieltag = kw.Spieltag
            	JOIN pl_data_vereine_kader_wert kw1 ON s.Auswärtsmannschaft_ID = kw1.Vereins_ID
            		AND s.Saison =  kw1.Saison
            		AND s.Spieltag = kw1.Spieltag
            	JOIN pl_staging_vereine_fifa_features ff ON s.Heimmannschaft_ID = ff.Vereins_ID
            		AND s.Saison = ff.Saison 
            		AND s.Spieltag = ff.Spieltag
            	JOIN pl_staging_vereine_fifa_features ff2 ON s.Auswärtsmannschaft_ID = ff2.Vereins_ID
            		AND s.Saison = ff2.Saison
            		AND s.Spieltag = ff2.Spieltag
            	JOIN pl_data_trainer_spiele ts ON s.Heimmannschaft_ID = ts.Vereins_ID
            		AND s.Saison = ts.Saison
            		AND s.Spieltag = ts.Spieltag
            	JOIN pl_data_trainer_spiele ts1 ON s.Auswärtsmannschaft_ID = ts1.Vereins_ID
            		AND s.Saison = ts1.Saison
            		AND s.Spieltag = ts1.Spieltag
            	JOIN pl_features_forecast_club_form f ON s.Heimmannschaft_ID = f.Vereins_ID
            		AND s.Saison = f.Saison
            		AND s.Spieltag = f.Spieltag
            	JOIN pl_features_forecast_club_form fa ON s.Heimmannschaft_ID = fa.Vereins_ID
            		AND s.Saison = fa.Saison
            		AND s.Spieltag = fa.Spieltag
            	JOIN pl_features_odds o ON s.Heimmannschaft_ID = o.Heimmannschaft_ID
            		AND s.Saison = o.Saison
            		AND s.Spieltag = o.Spieltag
            	inner join 
            		pl_features_forecast_club_data cl1 on s.Heimmannschaft_ID = cl1.Vereins_ID  and s.Saison = cl1.Saison and s.Spieltag = cl1.Spieltag
            	inner join 
            		pl_features_forecast_club_data cl2 on s.Auswärtsmannschaft_ID = cl2.Vereins_ID  and s.Saison = cl2.Saison and s.Spieltag = cl2.Spieltag
            	order by 
            		s.saison, s.spieltag
        ;'''        
        if case == 15:
                        query = ''' 
                                select
                                	e.Saison,
                                	e.Spieltag, 
                                	e.Heimmannschaft_ID, 
                                	e.Auswärtsmannschaft_ID as Gegner_ID, 
                                	k.Spiel_Ausgang, 
                                	kw.Kaderwert_Million - kw1.Kaderwert_Million as Kaderwert_Differenz,
                                	kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million as Kaderwert_Per_Spieler_Differenz,
                                	ff.Abwehr - ff2.Abwehr as Abwehrdifferenz,
                                	ff.Gesamt - ff2.Gesamt as Gesamtdiffferenz,
                                	ff.Angriff - ff2.Angriff as Angriffdifferenz,
                                	ff.Mittelfeld - ff2.Mittelfeld as Mittelfelddifferenz,
                                	ff.Angriff - ff2.Abwehr as Heimangriff_Abwehr_Differenz, 
                                	ff2.Angriff - ff.Abwehr as Auswärtsangriff_Abwehr_Differenz,
                                	f.L1,
                                	f.L2,
                                	f.L3,
                                	f.L4,
                                	f.L5,
                                	fa.L1 as GegnerL1,
                                	fa.L2 as GegnerL2,
                                	fa.L3 as GegnerL3,
                                	fa.L4 as GegnerL4,
                                	fa.L5 as GegnerL5
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
                                	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID  and e.Saison = f.Saison and e.Spieltag = f.Spieltag
                                inner join 
                                	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  and e.Saison = fa.Saison and e.Spieltag = fa.Spieltag
;'''


        if case == 16:
                        query = ''' 
                            select
                            	e.Saison,
                            	e.Spieltag, 
                            	e.Heimmannschaft_ID, 
                            	e.Auswärtsmannschaft_ID as Gegner_ID, 
                            	o.B365H,
                            	o.B365D,
                            	o.B365A,
                            	ms.System_ID as HeimSystem,
                            	ms1.System_ID as AuswärtsSystem,
                            	cl1.Shot_Feature as Home_Shot_Feature,
                            	cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                            	cl1.Fouls_Feature as Home_Fouls_Feature,
                            	cl1.Corner_Feature as Home_Corner_Feature,
                            	cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                            	cl2.Shot_Feature as Away_Shot_Feature,
                            	cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                            	cl2.Fouls_Feature as Away_Fouls_Feature,
                            	cl2.Corner_Feature as Away_Corner_Feature,
                            	cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                            	cl2.Redcard_Feature as Away_Redcard_Feature
                            from 
                            	bl1_staging_ergebnisse e
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
;'''
        if case == 17:
                        query = ''' 

                                SELECT 
                                	s.Saison AS Saison,
                                	s.Spieltag AS Spieltag,
                                	s.Heimmannschaft_ID AS Heimmannschaft_ID,
                                	s.Heimmannschaft AS Heimmannschaft,
                                	s.Auswärtsmannschaft_ID AS Gegner_ID,
                                	s.Auswärtsmannschaft AS Gegner,
                                	(kw.Kaderwert_Million - kw1.Kaderwert_Million) AS Kaderwert_Differenz,
                                	(kw.Kaderwert_Per_Spieler_Million - kw1.Kaderwert_Per_Spieler_Million) AS Kaderwert_Per_Spieler_Differenz,
                                	(ff.Abwehr - ff2.Abwehr) AS Abwehrdifferenz,
                                	(ff.Gesamt - ff2.Gesamt) AS Gesamtdiffferenz,
                                	(ff.Angriff - ff2.Angriff) AS Angriffdifferenz,
                                	(ff.Mittelfeld - ff2.Mittelfeld) AS Mittelfelddifferenz,
                                	(ff.Angriff - ff2.Abwehr) AS Heimangriff_Abwehr_Differenz,
                                	(ff2.Angriff - ff.Abwehr) AS Auswärtsangriff_Abwehr_Differenz,
                                	f.L1_Forecast AS L1,
                                	f.L2_Forecast AS L2,
                                	f.L3_Forecast AS L3,
                                	f.L4_Forecast AS L4,
                                	f.L5_Forecast AS L5,
                                	fa.L1_Forecast as GegnerL1,
                                	fa.L2_Forecast as GegnerL2,
                                	fa.L3_Forecast as GegnerL3,
                                	fa.L4_Forecast as GegnerL4,
                                	fa.L5_Forecast as GegnerL5
                                FROM
                                	bl1_staging_vereine_kommende_spieltag s
                                	JOIN bl1_data_vereine_kader_wert kw ON s.Heimmannschaft_ID = kw.Vereins_ID
                                		AND s.Saison =  kw.Saison 
                                		AND s.Spieltag = kw.Spieltag
                                	JOIN bl1_data_vereine_kader_wert kw1 ON s.Auswärtsmannschaft_ID = kw1.Vereins_ID
                                		AND s.Saison =  kw1.Saison
                                		AND s.Spieltag = kw1.Spieltag
                                	JOIN bl1_staging_vereine_fifa_features ff ON s.Heimmannschaft_ID = ff.Vereins_ID
                                		AND s.Saison = ff.Saison 
                                		AND s.Spieltag = ff.Spieltag
                                	JOIN bl1_staging_vereine_fifa_features ff2 ON s.Auswärtsmannschaft_ID = ff2.Vereins_ID
                                		AND s.Saison = ff2.Saison
                                		AND s.Spieltag = ff2.Spieltag
                                	JOIN bl1_features_forecast_club_form f ON s.Heimmannschaft_ID = f.Vereins_ID
                                		AND s.Saison = f.Saison
                                		AND s.Spieltag = f.Spieltag
                                	JOIN bl1_features_forecast_club_form fa ON s.Heimmannschaft_ID = fa.Vereins_ID
                                		AND s.Saison = fa.Saison
                                		AND s.Spieltag = fa.Spieltag
;'''
        if case == 18:
            query = '''
                    SELECT 
                    	s.Saison AS Saison,
                    	s.Spieltag AS Spieltag,
                    	s.Heimmannschaft_ID AS Heimmannschaft_ID,
                    	s.Auswärtsmannschaft_ID AS Gegner_ID,
                    	o.B365H,
                    	o.B365A,
                    	o.B365D,
                    	ms.System_ID as HeimSystem,
                    	ms1.System_ID as AuswärtsSystem,
                    	cl1.Shot_Feature as Home_Shot_Feature,
                    	cl1.Shot_On_Goal_Feature as Home_Shot_On_Goal_Feature,
                    	cl1.Fouls_Feature as Home_Fouls_Feature,
                    	cl1.Corner_Feature as Home_Corner_Feature,
                    	cl1.Yellowcard_Feature as Home_Yellowcard_Feature,
                    	cl1.Redcard_Feature as Home_Redcard_Feature,
                    	cl2.Shot_Feature as Away_Shot_Feature,
                    	cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
                    	cl2.Fouls_Feature as Away_Fouls_Feature,
                    	cl2.Corner_Feature as Away_Corner_Feature,
                    	cl2.Yellowcard_Feature as Away_Yellowcard_Feature,
                    	cl2.Redcard_Feature as Away_Redcard_Feature
                    FROM
                    	bl1_staging_vereine_kommende_spieltag s
                    	JOIN bl1_features_odds o ON s.Heimmannschaft_ID = o.Heimmannschaft_ID
                    		AND s.Saison = o.Saison
                    		AND s.Spieltag = o.Spieltag
                    	JOIN bl1_data_vereine_spielsystem vss1 on s.Heimmannschaft_ID = vss1.Vereins_ID  
                    		and s.Saison = vss1.Saison 
                    		and s.Spieltag = vss1.Spieltag
                    	JOIN bl1_data_vereine_spielsystem vss2 on s.Auswärtsmannschaft_ID = vss2.Vereins_ID  
                    		and s.Saison = vss2.Saison 
                    		and s.Spieltag = vss2.Spieltag
                    	left outer join 
                    		master_system ms on ms.System = vss1.Spiel_System
                    	left outer join 
                        	master_system ms1 on ms1.System = vss2.Spiel_System
                    	inner join 
                    		bl1_features_forecast_club_data cl1 on s.Heimmannschaft_ID = cl1.Vereins_ID  and s.Saison = cl1.Saison and s.Spieltag = cl1.Spieltag
                    	inner join 
                    		bl1_features_forecast_club_data cl2 on s.Auswärtsmannschaft_ID = cl2.Vereins_ID  and s.Saison = cl2.Saison and s.Spieltag = cl2.Spieltag
;''' 
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd="...",
            database = '....'
        )
        
        df = pd.read_sql(query, con = mydb)
            
        return df 
    
    







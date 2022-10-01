from django.db import models
from django.db import connection 
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score, precision_score
from keras.utils import np_utils
from numpy.random import seed
import tensorflow as tf
from tensorflow.keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SequentialFeatureSelector as SFS
from numpy import array
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from numpy import random
import numpy as np
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS
from sklearn.ensemble import GradientBoostingClassifier

def get_data(case):

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
            	fa.L5_Forecast as GegnerL5,
                o.Statistic_Feature as Statistic,
                sch.Schiedsrichter_ID
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
                join bl1_feature_opponent_statistic o on s.Heimmannschaft_ID = o.Vereins_ID  
    			    and s.Auswärtsmannschaft_ID = o.Gegner_ID  
                    and s.Saison = o.Saison 
                    and s.Spieltag = o.Spieltag
				join bl1_data_schiedsrichter_spiele sch on s.Heimmannschaft_ID = sch.Heimmannschaft_ID  
					and s.Auswärtsmannschaft_ID = sch.Auswärtsmannschaft_ID  
                    and s.Saison = sch.Saison 
                    and s.Spieltag = sch.Spieltag;'''
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
                    
    if case == 3:
        query = ''' 
            select
            	e.Saison,
            	e.Spieltag, 
            	e.Heimmannschaft,
            	e.Heimmannschaft_ID, 
            	e.Auswärtsmannschaft_ID as Gegner_ID, 
                e.Auswärtsmannschaft AS Gegner,
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
                o.Statistic_Feature as Statistic,
                sch.Schiedsrichter_ID
            from 
            	bl1_staging_ergebnisse e
            inner join bl1_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID 
                and e.Saison = k.Saison 
                and e.Spieltag = k.Spieltag
            inner join bl1_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID 
                and e.Saison = kw.Saison 
                and e.Spieltag = kw.Spieltag
            inner join bl1_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID 
                and e.Saison = kw1.Saison 
                and e.Spieltag = kw1.Spieltag
            inner join bl1_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID 
                and e.Saison = ff.Saison 
                and e.Spieltag = ff.Spieltag
            inner join 
            	bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID 
            and 
                e.Saison = ff2.Saison 
            and 
                e.Spieltag = ff2.Spieltag
            inner join 
            	bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID 
            and 
                e.Saison = ts.Saison 
            and 
                e.Spieltag = ts.Spieltag
            inner join 
            	bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID 
            and 
                e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            inner join 
            	bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID 
            and 
                e.Saison = f.Saison 
            and 
                e.Spieltag = f.Spieltag
            inner join 
            	bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  
            and 
                e.Saison = fa.Saison 
            and 
                e.Spieltag = fa.Spieltag
            inner join 
            	bl1_feature_opponent_statistic o on e.Heimmannschaft_ID = o.Vereins_ID  
			and 
				e.Auswärtsmannschaft_ID = o.Gegner_ID  
            and 
                e.Saison = o.Saison 
            and 
                e.Spieltag = o.Spieltag
			join bl1_data_schiedsrichter_spiele sch on e.Heimmannschaft_ID = sch.Heimmannschaft_ID  
				and e.Auswärtsmannschaft_ID = sch.Auswärtsmannschaft_ID  
                and e.Saison = sch.Saison 
                and e.Spieltag = sch.Spieltag;'''


    if case == 4:
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
            	cl2.Shot_Feature as Away_Shot_Feature,
            	cl2.Shot_On_Goal_Feature as Away_Shot_On_Goal_Feature,
            	cl2.Fouls_Feature as Away_Fouls_Feature,
            	cl2.Corner_Feature as Away_Corner_Feature,
            	cl2.Yellowcard_Feature as Away_Yellowcard_Feature
            from 
            	bl1_staging_ergebnisse e
            inner join 
            	bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  
            and 
                e.Saison = o.Saison 
            and 
                e.Spieltag = o.Spieltag
            inner join 
            	bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  
            and 
                e.Saison = vss1.Saison 
            and 
                e.Spieltag = vss1.Spieltag
            inner join 
            	bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID 
            and 
                e.Saison = vss2.Saison 
            and 
                e.Spieltag = vss2.Spieltag
            left outer join 
            	master_system ms on ms.System = vss1.Spiel_System
            left outer join 
            	master_system ms1 on ms1.System = vss2.Spiel_System
            inner join 
            	bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  
            and 
                e.Saison = cl1.Saison 
            and 
                e.Spieltag = cl1.Spieltag
            inner join 
            	bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID 
            and 
                e.Saison = cl2.Saison 
            and 
                e.Spieltag = cl2.Spieltag;'''
                
    if case == 5:
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
            		AND s.Spieltag = fa.Spieltag;'''
    if case == 6:
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
            	pl_staging_vereine_kommende_spieltag s
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
;''' 
                    
    if case == 7:
        query = ''' 
            select
            	e.Saison,
            	e.Spieltag, 
            	e.Heimmannschaft,
            	e.Heimmannschaft_ID, 
            	e.Auswärtsmannschaft_ID as Gegner_ID, 
                e.Auswärtsmannschaft AS Gegner,
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
                o.Statistic_Feature as Statistic
            from 
            	pl_staging_ergebnisse e
            inner join 
            	pl_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID 
            and 
                e.Saison = k.Saison 
            and 
                e.Spieltag = k.Spieltag
            inner join 
            	pl_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID 
            and 
                e.Saison = kw.Saison 
            and 
                e.Spieltag = kw.Spieltag
            inner join 
            	pl_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID 
            and 
                e.Saison = kw1.Saison 
            and 
                e.Spieltag = kw1.Spieltag
            inner join 
            	pl_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID 
            and 
                e.Saison = ff.Saison 
            and 
                e.Spieltag = ff.Spieltag
            inner join 
            	pl_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID 
            and 
                e.Saison = ff2.Saison 
            and 
                e.Spieltag = ff2.Spieltag
            inner join 
            	pl_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID 
            and 
                e.Saison = ts.Saison 
            and 
                e.Spieltag = ts.Spieltag
            inner join 
            	pl_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID 
            and 
                e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            inner join 
            	pl_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID 
            and 
                e.Saison = f.Saison 
            and 
                e.Spieltag = f.Spieltag
            inner join 
            	pl_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  
            and 
                e.Saison = fa.Saison 
            and 
                e.Spieltag = fa.Spieltag
            inner join 
            	pl_feature_opponent_statistic o on e.Heimmannschaft_ID = o.Vereins_ID  
			and 
				e.Auswärtsmannschaft_ID = o.Gegner_ID  
            and 
                e.Saison = o.Saison 
            and 
                e.Spieltag = o.Spieltag;'''


    if case == 8:
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
            	cl2.Redcard_Feature as Away_Redcard_Feature
            from 
            	pl_staging_ergebnisse e
            inner join 
            	pl_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  
            and 
                e.Saison = o.Saison 
            and 
                e.Spieltag = o.Spieltag
            inner join 
            	pl_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  
            and 
                e.Saison = vss1.Saison 
            and 
                e.Spieltag = vss1.Spieltag
            inner join 
            	pl_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID 
            and 
                e.Saison = vss2.Saison 
            and 
                e.Spieltag = vss2.Spieltag
            left outer join 
            	master_system ms on ms.System = vss1.Spiel_System
            left outer join 
            	master_system ms1 on ms1.System = vss2.Spiel_System
            inner join 
            	pl_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  
            and 
                e.Saison = cl1.Saison 
            and 
                e.Spieltag = cl1.Spieltag
            inner join 
            	pl_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID 
            and 
                e.Saison = cl2.Saison 
            and 
                e.Spieltag = cl2.Spieltag
;'''
                
    df = pd.read_sql(query, con = connection)
        
    return df 

def create_layers_binary(nbr_of_layers, X):

    layers = [tf.keras.layers.Dense(units = X, activation='sigmoid', input_shape = (X,))]
      
    for i in range(1,nbr_of_layers):
        layers.append(tf.keras.layers.Dense(units = X, activation='sigmoid'))

    layers.append(tf.keras.layers.Dense(units=2, activation='softmax'))
    return layers

def create_layers_multiple(nbr_of_layers, X):

    layers = [tf.keras.layers.Dense(units = X, activation='sigmoid', input_shape = (X,))]
      
    for i in range(1,nbr_of_layers):
        layers.append(tf.keras.layers.Dense(units = X, activation='sigmoid'))

    layers.append(tf.keras.layers.Dense(units=3, activation='softmax'))
    return layers

def get_training_data():
    df1 = get_data(3)
    df2 = get_data(4)
    df = df1.merge(df2, on = ['Saison', 'Spieltag', 'Heimmannschaft', 'Heimmannschaft_ID', 'Gegner_ID']) 
    
    return df

def get_premierleague_training_data():
    df1 = get_data(7)
    df2 = get_data(8)
    df = df1.merge(df2, on = ['Saison', 'Spieltag', 'Heimmannschaft', 'Heimmannschaft_ID', 'Gegner_ID']) 
    
    return df

def random_forest_score(X_train, X_test, y_train, y_test, n_, criterion):
    
    classifier = RandomForestClassifier(n_estimators = n_, criterion = criterion,  random_state = random.seed(1234))
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)

    y_pred_test = classifier.predict(X_test)
    recall = recall_score(y_test, y_pred_test, average=None)
    precision = precision_score(y_test, y_pred_test, average=None)

    return score, recall, precision

def random_forest_scores_binary(X_train, X_test, y_train, y_test, n_, criterion):
    
    classifier = RandomForestClassifier(n_estimators = n_, criterion = criterion, random_state = 0)
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    
    y_pred_test = classifier.predict(X_test)
    recall = recall_score(y_test, y_pred_test, average=None)
    precision = precision_score(y_test, y_pred_test, average=None)
    
    return score, recall, precision

def split_data(df_variables, df_eplainatory, length):
    
    X_train = df_variables[:-length]
    X_test = df_variables[-length:]
    y_train = df_eplainatory[:-length]
    y_test = df_eplainatory[-length:] 
    
    return X_train, X_test, y_train, y_test


def prepare_data(df, saison, spieltag):
    
    df = df.sort_values(['Saison', 'Spieltag'])   
    df_seasons_before = df[df['Saison'] < saison]
    df_season_chosen = df[df['Saison'] == saison]
    df_season_chosen = df_season_chosen[df_season_chosen['Spieltag'] < spieltag]
    df_analyse = df_seasons_before.append(df_season_chosen, ignore_index = True)
    df_analyse = df_analyse.sort_values(by = ['Saison', 'Spieltag']) 
    
    return df_analyse


def get_startelf(variables):
     
    variables.extend(["Spieler_1", "Spieler_2", "Spieler_3", "Spieler_4", "Spieler_5", "Spieler_6", "Spieler_7", "Spieler_8", 
                      "Spieler_9", "Spieler_10", "Spieler_11", "Gegner_Spieler_1","Gegner_Spieler_2", "Gegner_Spieler_3", 
                      "Gegner_Spieler_4", "Gegner_Spieler_5", "Gegner_Spieler_6", "Gegner_Spieler_7", "Gegner_Spieler_8",
                      "Gegner_Spieler_9", "Gegner_Spieler_10", "Gegner_Spieler_11"])
    
    variables.remove("Startelf")
    
    return variables

def spielausgang_to_binary(df):
    
    df['Spiel_Ausgang'] = df['Spiel_Ausgang'].apply(lambda x: 1 if x > 0 else 0)
    
    return df

def spielausgang_to_binary_premier_league(df):
    
    df['Spiel_Ausgang'] = list(map(int, df['Spiel_Ausgang']))
    df['Spiel_Ausgang'] = df['Spiel_Ausgang'].apply(lambda x: 1 if x > 0 else 0)
    
    return df

def ann_score(X_train, X_test, y_categorical_train, y_test, uniques, epochs, batch_size, learning_rate, nbr_layers):
    seed(0)
    tf.random.set_seed(0)    
    layers = create_layers_binary(nbr_layers, X_train.shape[1])
    ann = tf.keras.Sequential( 
    
     layers
     
    )    
   
    opt = SGD(lr = learning_rate)
    ann.compile(optimizer = opt, loss = 'categorical_crossentropy')
    ann.fit(X_train, y_categorical_train, batch_size = batch_size, epochs = epochs)
    y_pred = ann.predict(X_test)
    y_pred_unique = uniques[y_pred.argmax(1)]
    score = accuracy_score(y_test, y_pred_unique)
    recall = recall_score(y_test, y_pred_unique, average=None)
    precision = precision_score(y_test, y_pred_unique, average=None)   
    
    return score, recall, precision

def random_forest_odds_against_bookmaker(X_train, X_test, y_train, y_test, home_odds, draw_odds, away_odds, n, criterion):
        
    classifier = RandomForestClassifier(n_estimators = n, criterion=criterion, random_state = 0)
    classifier.fit(X_train, y_train)
    y_proba = classifier.predict_proba(X_test)
    l_proba_1 = []
    l_proba_1.append(y_proba[0][2])
    l_proba_2 = []
    l_proba_2.append(y_proba[0][1])
    l_proba_3 = []
    
    l_proba_3.append(y_proba[0][0])
    l_proba_4 = []
    l_proba_4.append(home_odds)
    l_proba_5 = []
    l_proba_5.append(draw_odds)
    l_proba_6 = []
    l_proba_6.append(away_odds)


    home_difference = (1/y_proba[0][2]) - home_odds
    draw_difference = (1/y_proba[0][1]) - draw_odds
    away_difference = (1/y_proba[0][0]) - away_odds
    df_test = pd.DataFrame(data={"Proba_h": home_difference, "draw": draw_difference, "loss": away_difference,
                                     "odds_h": l_proba_4, "odds_d": l_proba_5, "odds_l": l_proba_6, 'result':y_test})
       
    
    if home_difference > draw_difference and home_difference > away_difference:
        
        if int(y_test) == 1:
            win = home_odds * 10
        else:
            win = -10

    if draw_difference > home_difference and draw_difference > away_difference:
        
        if int(y_test) == 0:
            win = draw_odds * 10
        else:
            win = -10
 
    if away_difference > draw_difference and away_difference > home_difference:
        
        if int(y_test) == -1:
            win = away_odds * 10
        else:
            win = -10
    
    return win, home_difference, draw_difference, away_difference, 1/y_proba[0][2], 1/y_proba[0][1], 1/y_proba[0][0], df_test


def ann_odds_against_bookmaker(X_train, X_test, y_train, y_test, home_odds, draw_odds, away_odds, learning_rate, number_layers):
        
    seed(0)
    tf.random.set_seed(0)    
    layers = create_layers_multiple(number_layers, X_train.shape[1])
    ann = tf.keras.Sequential(layers)    
    y_categorical_train = np_utils.to_categorical(y_train, num_classes=3)
    opt = SGD(lr = learning_rate)
    ann.compile(optimizer = opt, loss = 'categorical_crossentropy')
    ann.fit(X_train, y_categorical_train, batch_size = 16, epochs = 200)
    y_pred = ann.predict(X_test)
    
    home_difference = (1/y_pred[0][1]) - home_odds
    draw_difference = (1/y_pred[0][0]) - draw_odds
    away_difference = (1/y_pred[0][2]) - away_odds
    
    
    if home_difference > draw_difference and home_difference > away_difference:
        
        if int(y_test) == 1:
            win = home_odds * 10
        else:
            win = -10

    if draw_difference > home_difference and draw_difference > away_difference:
        
        if int(y_test) == 0:
            win = draw_odds * 10
        else:
            win = -10
 
    if away_difference > draw_difference and away_difference > home_difference:
        
        if int(y_test) == 1:
            win = away_odds * 10
        else:
            win = -10
    
    return win, home_difference, draw_difference, away_difference, 1/y_pred[0][1], 1/y_pred[0][2], 1/y_pred[0][0]


def group_by_odds(df):
    
    not_empty = []
    
    df['Home_Odds'] = pd.to_numeric(df['Home_Odds'])
    
    df_top_favorite = df[df['Home_Odds'] <= 1.5]
    if (len(df_top_favorite)>0):
        df_top_favorite = df_top_favorite.assign(Odds_Threshold = 'Under 1.5')
        not_empty.append(df_top_favorite)
    
    df_favorite = df[(df['Home_Odds'] > 1.5) & (df['Home_Odds'] <= 2)]
    if (len(df_favorite)>0):
        df_favorite = df_top_favorite.assign(Odds_Threshold = 'Between 1.5 and 2')
        not_empty.append(df_favorite)
        
    df_balanced = df[(df['Home_Odds'] > 2) & (df['Home_Odds'] <= 3)]
    if (len(df_balanced)>0):
        df_balanced = df_balanced.assign(Odds_Threshold = 'Between 2 and 3')
        not_empty.append(df_balanced)
        
    df_underdog = df[(df['Home_Odds'] > 3) & (df['Home_Odds'] <= 4)]
    if (len(df_underdog)>0):
        df_underdog = df_underdog.assign(Odds_Threshold = 'Between 3 and 4')
        not_empty.append(df_underdog)
        
    df_clear_underdog = df[df['Home_Odds'] > 4]
    if (len(df_clear_underdog)>0):
        df_clear_underdog = df_clear_underdog.assign(Odds_Threshold = 'Over 4')
        not_empty.append(df_clear_underdog)
        
    df_ordered = pd.concat(not_empty, axis = 0)
    

    return df_ordered


def split_train(X, y, split_size):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_size) 
    
    return X_train, X_test, y_train, y_test


def check_startelf(variables):
    if 'Startelf' in variables:
        variables = get_startelf(variables)
    return variables

def get_tree_importance(variables, test_size, df):

    
    X = df[variables]
    y = df[['Spiel_Ausgang']]
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    
    sel_ = SelectFromModel(RandomForestClassifier(n_estimators = 2000, criterion='gini', random_state = 0))
    sel_.fit(X_train.values, y_train.values.ravel())
    
    X_test_rf = pd.DataFrame(sel_.transform(X_test))
     
    X_test_rf.columns = X_train.columns[(sel_.get_support())]
    
    
    model = RandomForestClassifier(n_estimators = 2000, criterion='gini', random_state = 0)
    model.fit(X_train.values, y_train.values.ravel())
    features = model.feature_importances_
    features = pd.Series(features)
    features.index = X_train.columns
    features.sort_values(ascending = False, inplace = True) 
    df_features =  pd.DataFrame(list(zip(features.index, features)), columns = ['Features', 'Importance'])
    
    return X_test_rf.columns, df_features
    
def get_correlation_variables(variables_to_check, test_size, df):

    
    X = df[variables_to_check]
    y = df[['Spiel_Ausgang']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    
    corrmat = X_train.corr(method='pearson')
    corrmat = corrmat.abs().unstack() # absolute value of corr coef
    corrmat = corrmat.sort_values(ascending=False)
    corrmat = pd.DataFrame(corrmat).reset_index()
    corrmat.columns = ['Basefeature', 'Checkfeature', 'Correlation']   
    grouped_feature_ls = []
    correlated_groups = []
    
    for feature in corrmat.Basefeature.unique():
        
        if feature not in grouped_feature_ls:
    
            # find all features correlated to a single feature
            correlated_block = corrmat[corrmat.Basefeature == feature]
            grouped_feature_ls = grouped_feature_ls + list(
                correlated_block.Checkfeature.unique()) + [feature]
    
            # append the block of features to the list
            correlated_groups.append(correlated_block)
            
    df_corr = pd.DataFrame(correlated_block)
    return df_corr    


def forward_feature_selection(X, y, nbr_features, test_size, nbr_trees, scoring):
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size) 
    X_train_array, y_train_array = X_train.values,  y_train.values.ravel()
        
    sfs = SFS(
            estimator=RandomForestClassifier(n_estimators=nbr_trees, n_jobs=4, random_state=0),
            n_features_to_select = nbr_features,  # the number of features to retain
            direction='forward',  # the direction of the selection procedure
            scoring=scoring,  # the metric to evaluate
            cv=2,  # the cross-validation fold
            n_jobs=4,  # for parallelization
        )
    sfs = sfs.fit(X_train_array, y_train_array)
    selected_feat = sfs.get_feature_names_out()
    scores = []
    features = []
    features_selected = []
    
    for f in range(len(selected_feat)):
        f = int(selected_feat[f][1:])
        features.append(f)
    

    X_train_selected_feature_array = X_train.iloc[:,features].values
    X_test_selected_feature_array = X_test.iloc[:,features].values
    y_test_selected_feature_array = y_test.values.ravel()
    
    
    rf = RandomForestClassifier(n_estimators=nbr_trees, random_state=0, max_depth=4)
    rf.fit(X_train_selected_feature_array,y_train_array)    
    
        
    score = rf.score(X_test_selected_feature_array, y_test_selected_feature_array)        
    scores.append(score)
    features_selected.append(X_train.iloc[:,features].columns)  
    df_result = pd.DataFrame(list(zip(scores, features_selected)),
           columns = ['Scores', 'Selected'])
    return df_result

def backward_feature_selection(X, y, nbr_features, test_size, nbr_trees, scoring):
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size) 
    X_train_array, y_train_array = X_train.values,  y_train.values.ravel()
        
    sfs =  SFS(
        estimator=RandomForestClassifier(
            n_estimators = 2000, n_jobs = 4, random_state = 0),
        n_features_to_select = len(X_train.columns) - nbr_features,  
        direction = 'backward', 
        scoring = 'accuracy',  
        cv = 2,  
        n_jobs = 4,  
    )

    sfs = sfs.fit(X_train_array, y_train_array)
    selected_feat = sfs.get_feature_names_out()
    scores = []
    features = []
    features_selected = []
    
    for f in range(len(selected_feat)):
        f = int(selected_feat[f][1:])
        features.append(f)
    

    X_train_selected_feature_array = X_train.iloc[:,features].values
    X_test_selected_feature_array = X_test.iloc[:,features].values
    y_test_selected_feature_array = y_test.values.ravel()
    
    
    rf = RandomForestClassifier(n_estimators=nbr_trees, random_state=0, max_depth=4)
    rf.fit(X_train_selected_feature_array,y_train_array)    
    
        
    score = rf.score(X_test_selected_feature_array, y_test_selected_feature_array)        
    scores.append(score)
    features_selected.append(X_train.iloc[:,features].columns)  
    variable_kicked_out = list(set(X_train.columns) - set(X_train.iloc[:,features].columns))
    df_result = pd.DataFrame(list(zip(scores, variable_kicked_out)),
           columns = ['Scores', 'Selected'])
    return df_result


def exhaustive_feature_selection(X, y, nbr_features_min, nbr_features_max, test_size, nbr_trees, scoring):
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size) 
    X_train_array, y_train_array = X_train.values,  y_train.values.ravel()
        
    efs = EFS(RandomForestClassifier(n_estimators=2000,
                                 n_jobs=4,
                                 random_state=0,
                                 max_depth=2),
          min_features = nbr_features_min,
          max_features = nbr_features_max,
          scoring = 'accuracy',
          print_progress = True,
          cv = 2)

    efs = efs.fit(X_train_array, y_train_array)
    

    selected_feat = X_train.columns[list(efs.best_idx_)]

    df_result = pd.DataFrame(list(zip(selected_feat)),
           columns = ['Selected'])
    return df_result

def get_gradient_boost_importance(X, y, test_size, nbr_trees):
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size) 
     
    model = GradientBoostingClassifier(n_estimators = nbr_trees, random_state = random.seed(1234))
    model.fit(X_train.values, y_train.values.ravel())
  
    features = pd.Series(model.feature_importances_)
    features.index = X_train.columns
    features.sort_values(ascending = False, inplace = True) 
    df_features =  pd.DataFrame(list(zip(features.index, features)), columns = ['Features', 'Importance'])
    
    
    sel_gradient = SelectFromModel(GradientBoostingClassifier(n_estimators = 500, random_state = random.seed(1234)))
    sel_gradient.fit(X_train.values, y_train.values.ravel())

    chosen_features = X_train.columns[(sel_gradient.get_support())]
    
    return df_features, chosen_features

def encode_variable(df, variable):
    
    data = df[variable]
    df = df.drop([variable], axis = 1)
    values = array(data)
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    
    return df, onehot_encoded

def encode_variable_train_and_test(df_train, df_test, variable):
    
    data_train = df_train[variable]
    data_test = df_test[variable]
    
    df_train = df_train.drop([variable], axis = 1)
    df_test = df_test.drop([variable], axis = 1)
    
    values_train = array(data_train)
    values_test = array(data_test)
    
    label_encoder = LabelEncoder()
    
    integer_encoded_train = label_encoder.fit_transform(values_train)
    
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded_train = integer_encoded_train.reshape(len(integer_encoded_train), 1)
    integer_encoded_test = values_test.reshape(len(values_test), 1)
    
    
    onehot_encoded_train = onehot_encoder.fit_transform(integer_encoded_train)
    onehot_encoded_test = onehot_encoder.transform(integer_encoded_test)
    
    return df_train, df_test, onehot_encoded_train, onehot_encoded_test


def random_forest_odds_against_bookmaker_main(df, saison, spieltag_from, spieltag_to, variables, n, Criterion):
    
    
    df_seasons_before = df[df['Saison'] < saison]
    df_season_analysed = df[df['Saison'] == saison]
    df_season_analysed_before = df[df['Spieltag'] < spieltag_from]
    df_date_before_first_matchday = df_seasons_before.append(df_season_analysed_before, ignore_index = True)
    df_spieltag_seasons_analysed = df_season_analysed[(df_season_analysed['Spieltag'] >= spieltag_from) & (df_season_analysed['Spieltag']<spieltag_to)]  
 
    total = []
    home_teams = []
    away_teams = []
    games_results =  []
    home_odds_list =  []
    away_odds_list =  []
    draw_odds_list =  []
    
    home_difference_list =  []
    away_difference_list =  []
    draw_difference_list =  []
    
    spieltage = []
    df_test_all = pd.DataFrame()
    for spieltag_left in df_spieltag_seasons_analysed['Spieltag'].drop_duplicates():
        #get data of relevant season
        df_spieltag_left = df_spieltag_seasons_analysed[df_spieltag_seasons_analysed['Spieltag'] < spieltag_left]
         
        #get data history of passed seasons
        df_analyse = df_date_before_first_matchday.append(df_spieltag_left, ignore_index = True)
        test_data = df_spieltag_seasons_analysed[df_spieltag_seasons_analysed['Spieltag'] == spieltag_left]
        
        for v_id in test_data['Heimmannschaft_ID'].drop_duplicates():
            
            test_data_per_verein = test_data[test_data['Heimmannschaft_ID'] == v_id]
            df_all = df_analyse.append(test_data_per_verein)
            df_all = df_all.sort_values(['Saison', 'Spieltag'])
            
            home_team = test_data_per_verein['Heimmannschaft'].iloc[0]
            away_team = test_data_per_verein['Gegner'].iloc[0]
            
            df_variables = df_all[variables]
            #df_variables.to_csv('D:/Projects/Football/test.csv', index=False)
            
            if 'Heimmannschaft_ID' in variables:
                df_variables, home_teams_encoded = encode_variable(df_variables, 'Heimmannschaft_ID')  
                df_variables, away_teams_encoded = encode_variable(df_variables, 'Gegner_ID')
                teams_encoded = np.concatenate((home_teams_encoded, away_teams_encoded), axis=1)
            if 'Trainer_ID' in variables:
                df_variables, home_trainer_encoded = encode_variable(df_variables, 'Trainer_ID')  
                df_variables, away_trainer_encoded = encode_variable(df_variables, 'Gegner_Trainer_ID')
                trainer_encoded = np.concatenate((home_trainer_encoded, away_trainer_encoded), axis=1)
            if 'HeimSystem' in variables:
                df_variables, home_system_encoded = encode_variable(df_variables, 'HeimSystem')  
                df_variables, away_system_encoded = encode_variable(df_variables, 'AuswärtsSystem')  
                system_encoded = np.concatenate((home_system_encoded, away_system_encoded), axis=1)
                
            
            if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
                
                all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded, system_encoded), axis=1)
                
            if (('Heimmannschaft_ID' in variables) and ('HeimSystem' in variables) and ('Trainer_ID' not in variables)):
                
                all_encoded_variables = np.concatenate((teams_encoded, system_encoded), axis=1)
                
            if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
                
                all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded), axis=1)     
                
            if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
                
                all_encoded_variables = np.concatenate((trainer_encoded, system_encoded), axis=1)         
        
            if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' not in variables)):
                
                all_encoded_variables = teams_encoded 
                
            if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
                
                all_encoded_variables = trainer_encoded 
                
            if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' in variables)):
                
                all_encoded_variables = system_encoded       
        
            y_test = df_all['Spiel_Ausgang'][-1:] 
            y_train = df_all['Spiel_Ausgang'][:-1]
            x = df_variables.values
            x = np.concatenate((x, all_encoded_variables), axis=1)
            
            X_train = x[:-1]
            X_test = x[-1:] 
            
            #y_train = y[:-1]
            y_test = y_test.ravel()
            #test_data_per_verein.to_csv('D:/Projects/Football/test.csv', index=False)
            home_odds = test_data_per_verein['B365H'].iloc[0]
            draw_odds = test_data_per_verein['B365D'].iloc[0]
            away_odds = test_data_per_verein['B365A'].iloc[0]

            win, home_difference, draw_difference, away_difference, home_proba, away_proba, draw_proba, df_test = random_forest_odds_against_bookmaker(X_train, X_test, y_train, y_test, home_odds, draw_odds, away_odds, n, Criterion)
            
            df_test_all = df_test_all.append(df_test)
            
            total.append(round(win, 2))
            home_teams.append(home_team)
            away_teams.append(away_team)
            home_odds_list.append(round(home_odds, 2))
            away_odds_list.append(round(away_odds, 2))
            draw_odds_list.append(round(draw_odds, 2))
            home_difference_list.append(round(home_difference, 2))
            away_difference_list.append(round(away_difference, 2))
            draw_difference_list.append(round(draw_difference, 2))
            games_results.append(y_test[0])
            spieltage.append(spieltag_left)
    
    df_best_clubs_home =  pd.DataFrame(list(zip(home_teams, total)), columns = ['Home_Team', 'Balance'])
    df_odds_home =  pd.DataFrame(list(zip(home_odds_list, total)), columns = ['Home_Odds', 'Balance'])
    df_spieltage =  pd.DataFrame(list(zip(spieltage, total)), columns = ['Spieltag', 'Balance'])

    df_odds_home = group_by_odds(df_odds_home)   
    df_test_all.to_csv('D:/Projects/Football/df_test_all.csv', index=False) 
    return total, df_best_clubs_home, df_odds_home, df_spieltage


def ann_odds_against_bookmaker_main(df, saison, spieltag_from, spieltag_to, variables, learning_rate, number_layers):
    
    
    df_seasons_before = df[df['Saison'] < saison]
    df_season_analysed = df[df['Saison'] == saison]
    df_season_analysed_before = df[df['Spieltag'] < spieltag_from]
    df_date_before_first_matchday = df_seasons_before.append(df_season_analysed_before, ignore_index = True)
    df_spieltag_seasons_analysed = df_season_analysed[(df_season_analysed['Spieltag'] >= spieltag_from) & (df_season_analysed['Spieltag']<spieltag_to)]  

    total = []
    home_teams = []
    away_teams = []
    games_results =  []
    home_odds_list =  []
    away_odds_list =  []
    draw_odds_list =  []
    
    home_difference_list =  []
    away_difference_list =  []
    draw_difference_list =  []
    
    spieltage = []
    
    for spieltag_left in df_spieltag_seasons_analysed['Spieltag'].drop_duplicates():
        #get data of relevant season
        df_spieltag_left = df_spieltag_seasons_analysed[df_spieltag_seasons_analysed['Spieltag'] < spieltag_left]
         
        #get data history of passed seasons
        df_analyse = df_date_before_first_matchday.append(df_spieltag_left, ignore_index = True)
        test_data = df_spieltag_seasons_analysed[df_spieltag_seasons_analysed['Spieltag'] == spieltag_left]
        
        for v_id in test_data['Heimmannschaft_ID'].drop_duplicates():
            
            test_data_per_verein = test_data[test_data['Heimmannschaft_ID'] == v_id]
            df_all = df_analyse.append(test_data_per_verein)
            df_all = df_all.sort_values(['Saison', 'Spieltag'])
            
            home_team = test_data_per_verein['Heimmannschaft'].iloc[0]
            away_team = test_data_per_verein['Gegner'].iloc[0]
            
            df_variables = df_all[variables]
            
            if 'Heimmannschaft_ID' in variables:
                df_variables, home_teams_encoded = encode_variable(df_variables, 'Heimmannschaft_ID')  
                df_variables, away_teams_encoded = encode_variable(df_variables, 'Gegner_ID')
                teams_encoded = np.concatenate((home_teams_encoded, away_teams_encoded), axis=1)
            if 'Trainer_ID' in variables:
                df_variables, home_trainer_encoded = encode_variable(df_variables, 'Trainer_ID')  
                df_variables, away_trainer_encoded = encode_variable(df_variables, 'Gegner_Trainer_ID')
                trainer_encoded = np.concatenate((home_trainer_encoded, away_trainer_encoded), axis=1)
            if 'HeimSystem' in variables:
                df_variables, home_system_encoded = encode_variable(df_variables, 'HeimSystem')  
                df_variables, away_system_encoded = encode_variable(df_variables, 'AuswärtsSystem')  
                system_encoded = np.concatenate((home_system_encoded, away_system_encoded), axis=1)
                
            
            if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
                
                all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded, system_encoded), axis=1)
                
            if (('Heimmannschaft_ID' in variables) and ('HeimSystem' in variables) and ('Trainer_ID' not in variables)):
                
                all_encoded_variables = np.concatenate((teams_encoded, system_encoded), axis=1)
                
            if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
                
                all_encoded_variables = np.concatenate((teams_encoded, trainer_encoded), axis=1)     
                
            if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' in variables)):
                
                all_encoded_variables = np.concatenate((trainer_encoded, system_encoded), axis=1)         
        
            if (('Heimmannschaft_ID' in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' not in variables)):
                
                all_encoded_variables = teams_encoded 
                
            if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' in variables) and ('HeimSystem' not in variables)):
                
                all_encoded_variables = trainer_encoded 
                
            if (('Heimmannschaft_ID' not in variables) and ('Trainer_ID' not in variables) and ('HeimSystem' in variables)):
                
                all_encoded_variables = system_encoded             

            y_test = df_all['Spiel_Ausgang'][-1:] 
            y_train = df_all['Spiel_Ausgang'][:-1]
            x = df_variables.values
            x = np.concatenate((x, all_encoded_variables), axis=1)
            
            X_train = x[:-1]
            X_test = x[-1:] 
            y_test = y_test.ravel()
            
            home_odds = test_data_per_verein['B365H'].iloc[0]
            draw_odds = test_data_per_verein['B365D'].iloc[0]
            away_odds = test_data_per_verein['B365A'].iloc[0]
            #print(spieltag_left)
            win, home_difference, draw_difference, away_difference, home_proba, away_proba, draw_proba = ann_odds_against_bookmaker(X_train, X_test, y_train, y_test, home_odds, draw_odds, away_odds, learning_rate, number_layers)

            total.append(round(win, 2))
            home_teams.append(home_team)
            away_teams.append(away_team)
            home_odds_list.append(round(home_odds, 2))
            away_odds_list.append(round(away_odds, 2))
            draw_odds_list.append(round(draw_odds, 2))
            home_difference_list.append(round(home_difference, 2))
            away_difference_list.append(round(away_difference, 2))
            draw_difference_list.append(round(draw_difference, 2))
            games_results.append(y_test[0])
            spieltage.append(spieltag_left)
    
    df_best_clubs_home =  pd.DataFrame(list(zip(home_teams, total)), columns = ['Home_Team', 'Balance'])
    df_odds_home =  pd.DataFrame(list(zip(home_odds_list, total)), columns = ['Home_Odds', 'Balance'])
    df_spieltage =  pd.DataFrame(list(zip(spieltage, total)), columns = ['Spieltag', 'Balance'])

    df_odds_home = group_by_odds(df_odds_home)   
    
    return total, df_best_clubs_home, df_odds_home, df_spieltage 
from django.db import models
from django.db import connection 
import pandas as pd


def get_bundesliga_all_saison_spieltag_check():

    query = ''' 
            select
            	e.Saison,
            	count(distinct e.Spieltag)
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
            inner join bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID 
                and e.Saison = ff2.Saison 
            	and e.Spieltag = ff2.Spieltag
            inner join bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID 
            	and e.Saison = ts.Saison 
            	and e.Spieltag = ts.Spieltag
            inner join bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID 
            	and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            inner join bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID 
            	and e.Saison = f.Saison 
            	and e.Spieltag = f.Spieltag
            inner join bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  
            	and e.Saison = fa.Saison 
            	and e.Spieltag = fa.Spieltag
            inner join bl1_feature_opponent_statistic op on e.Heimmannschaft_ID = op.Vereins_ID  
            	and e.Auswärtsmannschaft_ID = op.Gegner_ID  
            	and e.Saison = op.Saison 
            	and e.Spieltag = op.Spieltag
            inner join bl1_data_schiedsrichter_spiele sch on e.Heimmannschaft_ID = sch.Heimmannschaft_ID  
            	and e.Auswärtsmannschaft_ID = sch.Auswärtsmannschaft_ID  
            	and e.Saison = sch.Saison 
            	and e.Spieltag = sch.Spieltag
            inner join bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  
            	and e.Saison = o.Saison 
            	and e.Spieltag = o.Spieltag
            inner join bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  
            	and e.Saison = vss1.Saison 
            	and e.Spieltag = vss1.Spieltag
            inner join bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID 
            	and e.Saison = vss2.Saison 
            	and e.Spieltag = vss2.Spieltag
            left outer join master_system ms on ms.System = vss1.Spiel_System
            left outer join master_system ms1 on ms1.System = vss2.Spiel_System
            inner join bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  
            	and e.Saison = cl1.Saison 
            	and e.Spieltag = cl1.Spieltag
            inner join bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID 
            	and e.Saison = cl2.Saison 
            	and e.Spieltag = cl2.Spieltag
            group by e.saison;'''    
    df = pd.read_sql(query, con = connection)      
    return df

def get_bundesliga_all_club_count():

    query = ''' 
            select
            	e.Saison,
                e.Spieltag,
            	count(distinct e.Heimmannschaft_ID)
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
            inner join bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID 
                and e.Saison = ff2.Saison 
            	and e.Spieltag = ff2.Spieltag
            inner join bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID 
            	and e.Saison = ts.Saison 
            	and e.Spieltag = ts.Spieltag
            inner join bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID 
            	and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            inner join bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID 
            	and e.Saison = f.Saison 
            	and e.Spieltag = f.Spieltag
            inner join bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  
            	and e.Saison = fa.Saison 
            	and e.Spieltag = fa.Spieltag
            inner join bl1_feature_opponent_statistic op on e.Heimmannschaft_ID = op.Vereins_ID  
            	and e.Auswärtsmannschaft_ID = op.Gegner_ID  
            	and e.Saison = op.Saison 
            	and e.Spieltag = op.Spieltag
            inner join bl1_data_schiedsrichter_spiele sch on e.Heimmannschaft_ID = sch.Heimmannschaft_ID  
            	and e.Auswärtsmannschaft_ID = sch.Auswärtsmannschaft_ID  
            	and e.Saison = sch.Saison 
            	and e.Spieltag = sch.Spieltag
            inner join bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  
            	and e.Saison = o.Saison 
            	and e.Spieltag = o.Spieltag
            inner join bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  
            	and e.Saison = vss1.Saison 
            	and e.Spieltag = vss1.Spieltag
            inner join bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID 
            	and e.Saison = vss2.Saison 
            	and e.Spieltag = vss2.Spieltag
            left outer join master_system ms on ms.System = vss1.Spiel_System
            left outer join master_system ms1 on ms1.System = vss2.Spiel_System
            inner join bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  
            	and e.Saison = cl1.Saison 
            	and e.Spieltag = cl1.Spieltag
            inner join bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID 
            	and e.Saison = cl2.Saison 
            	and e.Spieltag = cl2.Spieltag
            group by e.saison
            having count(distinct e.Heimmannschaft_ID) != 9;'''    
    df = pd.read_sql(query, con = connection)      
    return df


def get_premierleague_all_saison_spieltag_check():

    query = ''' 
            select
            	e.Saison,
            	count(distinct e.Spieltag)
            from 
            	pl_staging_ergebnisse e
            inner join pl_data_ergebnisse_kategorisiert k on e.Heimmannschaft_ID = k.Vereins_ID 
				and e.Saison = k.Saison 
				and e.Spieltag = k.Spieltag
            inner join pl_data_vereine_kader_wert kw on e.Heimmannschaft_ID = kw.Vereins_ID 
				and e.Saison = kw.Saison 
				and e.Spieltag = kw.Spieltag
            inner join pl_data_vereine_kader_wert kw1 on e.Auswärtsmannschaft_ID = kw1.Vereins_ID 
				and e.Saison = kw1.Saison 
				and e.Spieltag = kw1.Spieltag
            inner join pl_staging_vereine_fifa_features ff on e.Heimmannschaft_ID = ff.Vereins_ID 
				and e.Saison = ff.Saison 
				and e.Spieltag = ff.Spieltag
            inner join pl_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID 
				and e.Saison = ff2.Saison 
				and e.Spieltag = ff2.Spieltag
            inner join pl_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID 
				and e.Saison = ts.Saison 
				and e.Spieltag = ts.Spieltag
            inner join pl_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID 
				and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            inner join pl_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID 
				and e.Saison = f.Saison 
				and e.Spieltag = f.Spieltag
            inner join pl_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  
				and e.Saison = fa.Saison 
				and e.Spieltag = fa.Spieltag
            inner join pl_feature_opponent_statistic op on e.Heimmannschaft_ID = op.Vereins_ID  
				and e.Auswärtsmannschaft_ID = op.Gegner_ID  
				and e.Saison = op.Saison 
				and e.Spieltag = op.Spieltag
            inner join pl_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  
				and e.Saison = o.Saison 
				and e.Spieltag = o.Spieltag
            inner join pl_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  
				and e.Saison = vss1.Saison 
				and e.Spieltag = vss1.Spieltag
            inner join pl_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID 
				and e.Saison = vss2.Saison 
				and e.Spieltag = vss2.Spieltag
            left outer join master_system ms on ms.System = vss1.Spiel_System
            left outer join master_system ms1 on ms1.System = vss2.Spiel_System
            inner join pl_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  
				and e.Saison = cl1.Saison 
				and e.Spieltag = cl1.Spieltag
            inner join pl_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID 
				and e.Saison = cl2.Saison 
				and e.Spieltag = cl2.Spieltag
            group by e.saison;'''    
    df = pd.read_sql(query, con = connection)      
    return df

def get_premierleague_all_club_count():

    query = ''' 
            select
            	e.Saison,
                e.Spieltag,
            	count(distinct e.Heimmannschaft_ID)
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
            inner join bl1_staging_vereine_fifa_features ff2 on e.Auswärtsmannschaft_ID = ff2.Vereins_ID 
                and e.Saison = ff2.Saison 
            	and e.Spieltag = ff2.Spieltag
            inner join bl1_data_trainer_spiele ts on e.Heimmannschaft_ID = ts.Vereins_ID 
            	and e.Saison = ts.Saison 
            	and e.Spieltag = ts.Spieltag
            inner join bl1_data_trainer_spiele ts1 on e.Auswärtsmannschaft_ID = ts1.Vereins_ID 
            	and e.Saison = ts1.Saison and e.Spieltag = ts1.Spieltag
            inner join bl1_features_club_form f on e.Heimmannschaft_ID = f.Vereins_ID 
            	and e.Saison = f.Saison 
            	and e.Spieltag = f.Spieltag
            inner join bl1_features_club_form fa on e.Auswärtsmannschaft_ID = fa.Vereins_ID  
            	and e.Saison = fa.Saison 
            	and e.Spieltag = fa.Spieltag
            inner join bl1_feature_opponent_statistic op on e.Heimmannschaft_ID = op.Vereins_ID  
            	and e.Auswärtsmannschaft_ID = op.Gegner_ID  
            	and e.Saison = op.Saison 
            	and e.Spieltag = op.Spieltag
            inner join bl1_data_schiedsrichter_spiele sch on e.Heimmannschaft_ID = sch.Heimmannschaft_ID  
            	and e.Auswärtsmannschaft_ID = sch.Auswärtsmannschaft_ID  
            	and e.Saison = sch.Saison 
            	and e.Spieltag = sch.Spieltag
            inner join bl1_features_odds o on e.Heimmannschaft_ID = o.Heimmannschaft_ID  
            	and e.Saison = o.Saison 
            	and e.Spieltag = o.Spieltag
            inner join bl1_data_vereine_spielsystem vss1 on e.Heimmannschaft_ID = vss1.Vereins_ID  
            	and e.Saison = vss1.Saison 
            	and e.Spieltag = vss1.Spieltag
            inner join bl1_data_vereine_spielsystem vss2 on e.Auswärtsmannschaft_ID = vss2.Vereins_ID 
            	and e.Saison = vss2.Saison 
            	and e.Spieltag = vss2.Spieltag
            left outer join master_system ms on ms.System = vss1.Spiel_System
            left outer join master_system ms1 on ms1.System = vss2.Spiel_System
            inner join bl1_features_club_data cl1 on e.Heimmannschaft_ID = cl1.Vereins_ID  
            	and e.Saison = cl1.Saison 
            	and e.Spieltag = cl1.Spieltag
            inner join bl1_features_club_data cl2 on e.Auswärtsmannschaft_ID = cl2.Vereins_ID 
            	and e.Saison = cl2.Saison 
            	and e.Spieltag = cl2.Spieltag
            group by e.saison
            having count(distinct e.Heimmannschaft_ID) != 10;'''    
    df = pd.read_sql(query, con = connection)      
    return df
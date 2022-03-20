from django.db import models
from sqlalchemy import create_engine
import mysql
import mysql.connector



class bl1_data_ergebnisse_kategorisiert(models.Model):
    Saison = models.CharField(max_length=10)
    Spieltag = models.IntegerField()
    Vereins_ID = models.IntegerField(primary_key=True)
    Spiel_Ausgang = models.IntegerField()
    Gegner_ID = models.IntegerField()
    
    
class bl1_staging_ergebnisse(models.Model):
    Saison = models.CharField(max_length=10)
    Spieltag = models.IntegerField()
    Heimmannschaft_ID = models.IntegerField(primary_key=True)
    Auswärtsmannschaft_ID = models.IntegerField()


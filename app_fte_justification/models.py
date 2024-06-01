from django.db import models

class FteJustification(models.Model):
    solid_trial = models.IntegerField()
    solid_patient = models.IntegerField()
    heme_trial = models.IntegerField()
    heme_patient = models.IntegerField()
    research_solid_monthly = models.FloatField()
    research_solid_yearly = models.FloatField()
    research_heme_monthly = models.FloatField()
    research_heme_yearly = models.FloatField()
    care_solid_monthly = models.FloatField()
    care_solid_yearly = models.FloatField()
    care_heme_monthly = models.FloatField()
    care_heme_yearly = models.FloatField()
    staff_cost_primary = models.FloatField()
    staff_cost_admin = models.FloatField()
    potential_profit_yearly = models.FloatField()

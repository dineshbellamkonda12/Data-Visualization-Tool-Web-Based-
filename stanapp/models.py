from django.db import models

class RainfallData(models.Model):
    date = models.DateTimeField()
    rainfall = models.FloatField()
from django.db import models

# Create your models here.
class Tick(models.Model):
	year = models.IntegerField()
	month = models.IntegerField()
	day = models.IntegerField()
	volume = models.IntegerField()
	day_open = models.DecimalField(max_digits = 12, decimal_places = 3)
	percent_change = models.DecimalField(max_digits = 9, decimal_places = 8)
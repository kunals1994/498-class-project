from django.db import models

# Create your models here.
class Tick(models.Model):
	symbol = models.CharField(max_length = 5)
	year = models.IntegerField()
	month = models.IntegerField()
	day = models.IntegerField()
	volume = models.IntegerField()
	day_open = models.DecimalField(max_digits = 12, decimal_places = 3)
	percent_change = models.DecimalField(max_digits = 9, decimal_places = 8)

	def __str__(self):
		return symbol + " : " + str(day) + "/" + str(month) + "/" + str(year)
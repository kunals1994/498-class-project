from django.db import models

# Create your models here.
class Tick(models.Model):
	symbol = models.CharField(max_length = 5)
	date = models.IntegerField()
	volume = models.IntegerField()
	day_open = models.DecimalField(max_digits = 12, decimal_places = 3)
	percent_change = models.DecimalField(max_digits = 9, decimal_places = 8)

	def __str__(self):
		return self.symbol + " : " + str(self.date)


class Volitility(models.Model):
	symbol = models.CharField(max_length = 5)
	year = models.IntegerField(max_digits = 5)
	volitliity = models.DecimalField(max_digits = 9, decimal_places = 8)

	def __str__(self):
		return self.symbol + " : " + str(self.year)



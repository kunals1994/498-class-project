from django.shortcuts import render
from django.http import HttpResponse
from kensoDataStore.models import Tick
from kensoDataStore.models import Volitility
import simplejson as json
import math

from kensoDataStore import sentiment_analyzer

def temp_home(request):
	return HttpResponse("""
		<h1> Some sample requests </h1><br><br>

		<h3> /api/seeCorrelation </h3><br><br>
		<a href="http://104.236.25.141/api/seeCorrelation?symbol1=AAPL&symbol2=GOOG&startdate=2010/12/31&enddate=2013/12/31">http://104.236.25.141/api/seeCorrelation?symbol1=AAPL&symbol2=GOOG&startdate=2010/12/31&enddate=2013/12/31</a>
		<br>
		<a href="http://104.236.25.141/api/seeCorrelation?symbol1=A&symbol2=FM&startdate=2010/12/31&enddate=2013/12/31">http://104.236.25.141/api/seeCorrelation?symbol1=A&symbol2=FM&startdate=2010/12/31&enddate=2013/12/31</a>
		<br><br><br>
		<h3> /api/getData</h3> </br><br>
		<a href="http://104.236.25.141/api/getData?symbol=AAPL&startdate=2010/12/31&enddate=2013/12/31">http://104.236.25.141/api/getData?symbol=AAPL&startdate=2010/12/31&enddate=2013/12/31</a>
		<br>
		<a href="http://104.236.25.141/api/getData?symbol=ATX&startdate=2010/12/31&enddate=2013/12/31">http://104.236.25.141/api/getData?symbol=ATX&startdate=2010/12/31&enddate=2013/12/31</a>
		<br><br>
		""")

# Create your views here.
def display_volatility(request):

	symbol_one = request.GET.get("symbols").split(",")
	lower = {}
	neutral = {}
	upper = {}

	lower_sentiment = 0.0
	upper_sentiment = 0.0

	lower_count = 0
	upper_count = 0

	for symbol in symbol_one:
		data = 0
		sentiment = 0
		# Anything that is not in the database is considered inconclusive
		try:
			data = Volitility.objects.filter(symbol = symbol)[0]
			sentiment = (sentiment_analyzer.___get_news_sentiment___(data.symbol + " " + data.company_name)) * 2 - 1
		except:
			fiver = 5

		if(float(data.volitliity) > 0.3):
			upper[symbol] = {}
			upper[symbol]["volitility"] = float(data.volitliity)
			upper[symbol]["sentiment"] = sentiment
			upper_count += 1
			upper_sentiment += sentiment

		elif(float(data.volitliity) < -0.3):
			lower[symbol] = {}
			lower[symbol]["volitility"] = float(data.volitliity)
			lower[symbol]["sentiment"] = sentiment
			lower_count += 1
			lower_sentiment += sentiment

		else:
			neutral[symbol] = {}
			neutral[symbol]["volitility"] = float(data.volitliity)
			neutral[symbol]["sentiment"] = sentiment

	try:
		lower_sentiment /= lower_count
	except:
		lower_sentiment = 0
	try:
		upper_sentiment /= upper_count
	except:
		upper_sentiment = 0

	if (upper_sentiment < lower_count):
		temp = upper_sentiment
		upper_sentiment = lower_sentiment
		lower_sentiment = upper_sentiment

	return HttpResponse(json.dumps({
			"long" : upper,
			"neutral" : neutral,
			"short" : lower
		}))


def get_data(request):
	csymbol = request.GET.get("symbol")

	date_one = int(request.GET.get("startdate").replace("/", ""))
	date_two = int(request.GET.get("enddate").replace("/", ""))

	data = Tick.objects.filter(symbol = csymbol, date__gte = date_one, date__lte = date_two)

	data_out = {}

	data_out["data_" + csymbol] = {}

	for point in data:
		date = str(point.date)
		date = date[:4] + "-" + date[4:6] + "-" + date[6:]
		data_out["data_" + csymbol][date] = {
			"open" : point.day_open,
			"volume" : point.volume,
			"percent_change": point.percent_change
		}

	return HttpResponse(json.dumps(data_out))

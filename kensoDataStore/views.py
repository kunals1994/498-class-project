from django.shortcuts import render
from django.http import HttpResponse
from kensoDataStore.models import Tick
from kensoDataStore.models import Volitility
import simplejson as json
import math

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

	symbol_one = request.GET.get("symbol")

	volitility_data = Volitility.objects.filter(symbol = symbol_one)[0]

	ret = {}
	ret[symbol_one] = {}
	ret[symbol_one]["volitility"] = volitility_data.volitliity
	ret[symbol_one]["sentiment"] = None

	return HttpResponse(json.dumps(ret))


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

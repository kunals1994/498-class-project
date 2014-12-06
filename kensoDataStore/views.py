from django.shortcuts import render
from django.http import HttpResponse
from kensoDataStore.models import Tick
from kensoDataStore.models import Volitility
import simplejson as json
import math

import requests
from alchemyapi import AlchemyAPI
import json

# Helper Method for determining Sentiment
def ___get_news_sentiment___(query):
    query = str(query)
    
    r = requests.get('https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27'+ query+'%27maryland%27&$format=json', auth=('Ql9qEoqZut7Uy3i7mTtiX8Dv1SciVZf1Qwcz07BUx5k','Ql9qEoqZut7Uy3i7mTtiX8Dv1SciVZf1Qwcz07BUx5k'))
    rrr = r.json()
    rr = rrr['d']['results']
    length = len(rr)
    alchemyapi = AlchemyAPI()
    
    lurl = []
    linfo = []
    lscore = []
    ltitle = []
    ldesc = []
    
    for i in range(0, length-1):
        lurl.append(rr[i]['Url'])
        ltitle.append(rr[i]['Title'])
        ldesc.append(rr[i]['Description'])
    
    total = 0.0;
    counted = 0
    for i in range(0, length-1):
        try:
            linfo.append(alchemyapi.sentiment('text', rr[i]['Title'])['docSentiment'])
            if linfo[i]['type'] != 'neutral':
                total += float(linfo[i]['score'])
                counted += 1
        except:
            continue
    avg = total/counted
    
    return avg, html

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

	data = Volitility.objects.filter(symbol = symbol_one)[0]
	sentiment = ___get_news_sentiment___(data.symbol + " " + data.company_name)

	ret = {}
	ret[symbol_one] = {}
	ret[symbol_one]["volitility"] = data.volitliity
	ret[symbol_one]["sentiment"] = sentiment

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

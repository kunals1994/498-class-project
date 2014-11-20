from django.shortcuts import render
from django.http import HttpResponse
from kensoDataStore.models import Tick
import simplejson as json
import math


# Create your views here.
def display_volatility(request):

	symbol_one = request.GET.get("symbol1")
	symbol_two = request.GET.get("symbol2")

	date_one = int(request.GET.get("startdate").replace("/", ""))
	date_two = int(request.GET.get("enddate").replace("/", ""))

	listA = Tick.objects.filter(symbol = symbol_one, date__lte = date_two, date__gte = date_one).order_by("date")
	listB = Tick.objects.filter(symbol = symbol_two, date__lte = date_two, date__gte = date_one).order_by("date")

	lenA = len(listA)
	lenB = len(listB)

	if(lenA > lenB):
		diff = lenA-lenB
		lenA = lenA[diff:]
	elif(lenB > lenA):
		diff = lenB-lenA
		lenB = lenB[diff:]

	aSum, bSum = 0.0, 0.0
	aCount, bCount = 0, 0
	
	# TODO - Why do we have 3 loops here? Should be done in pass. 
	for a in listA:
		aSum += float(a.percent_change)
		aCount += 1
	for b in listB:
		bSum += float(b.percent_change)
		bCount += 1
	aAvg = aSum/aCount
	bAvg = bSum/bCount
	covNumerator = 0.0
	varxNumerator, varyNumerator = 0.0, 0.0
	for i in range(aCount): #acount and bcount should be equal
		covNumerator += (listA[i].percent_change - aAvg) * (listB[i].percent_change - bAvg)
		varxNumerator += math.pow((listA[i].percent_change - aAvg),2)
		varyNumerator += math.pow((listB[i].percent_change - bAvg),2)
	cov = covNumerator/aCount
	varx = float(varxNumerator) / aCount
	vary = float(varyNumerator) / bCount
	sigmax = math.pow(varx,0.5)
	sigmay = math.pow(vary,0.5)
	correlation = cov/(sigmax*sigmay)
	# END TODO; this algorithm needs to be cleaned up. Execution is too slow. 

	ret = {}
	ret ["result_%s_%s" % (symbol_one, symbol_two)] = {}
	ret["result_%s_%s" % (symbol_one, symbol_two)]["correlation"] = correlation
	ret["result_%s_%s" % (symbol_one, symbol_two)]["correlation"]["sentiment_%s" % symbol_one] = None
	ret["result_%s_%s" % (symbol_one, symbol_two)]["correlation"]["sentiment_%s" % symbol_two] = None

	return HttpResponse(json.dumps(ret))


def get_data(request):
	csymbol = request.GET.get("symbol")

	date_one = int(request.GET.get("startdate").replace("/", ""))
	date_two = int(request.GET.get("enddate").replace("/", ""))

	data = Tick.objects.filter(symbol = csymbol, date__gte = date_one, date__lte = date_two)

	data_out = {}

	data_out["data"] = {}

	for point in data:
		date = str(point.date)
		date = date[:4] + "-" + date[4:6] + "-" + date[6:]
		data_out["data"][date] = {
			"open" : point.day_open,
			"volume" : point.volume,
			"percent_change": point.percent_change
		}

	return HttpResponse(json.dumps(data_out))

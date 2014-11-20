from django.shortcuts import render

# Create your views here.
def calcVolatility(listA, listB):
	aSum, bSum = 0.0, 0.0
	aCount, bCount = 0.0, 0.0
	
	for a in listA:
		aSum += a.percent_change
		aCount++
	for b in listB:
		bSum += b.percent_change
		bCount++
	aAvg = aSum/aCount
	bAvg = bSum/bCount
	covNumerator = 0.0
	varxNumerator, varyNumerator = 0.0, 0.0
	for i in range(acount): #acount and bcount should be equal
		covNumerator += (listA.[i].percent_change - aAvg) * (listB.[i].percent_change - bAvg)
		varxNumerator += math.pow((listA.[i].percent_change - aAvg),2)
		varyNumerator += math.pow((listB.[i].percent_change - bAvg),2)
	cov = covNumerator/aCount
	varx = float(varxNumerator) / aCount
	vary = float(varyNumerator) / bCount
	sigmax = math.pow(varx,0.5)
	sigmay = math.pow(vary,0.5)
	correlation = cov/(sigmax*sigmay)
	

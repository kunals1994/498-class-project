import numpy
import os
import pickle
import sys

# A pickled version of the sp500 data
sp = pickle.load(open("sp500.p"))
for i in os.listdir("KenshoTickData"):
    if (".csv" not in i):
        continue
    symbol = i.replace(".csv", '')
    company_name = ""
    vol = 0
    try:
        x = json.load(urllib2.urlopen("http://dev.markitondemand.com/Api/Quote/json?symbol="+symbol).read())
        company_name += x["Data"]["Name"]
    except:
        company_name = "market performance"
    with open("KenshoTickData/" + i, 'r') as f:
        vals = []
        sp_vals = []
        for line in f:
            l = line.split(",")
            date = l[0].split("-")
            year = date[0][2:]
            # Remove leading zeros
            month = str(int(date[1]))
            day = str(int(date[2]))
            d = month + "/" + day + "/" + year
            try:
                sp_vals.append(float(sp[d]))
                vals.append(float(l[7]))
            except:
                continue
    vol = numpy.corrcoef([vals,sp_vals])
    try:
        print str(symbol) + "," + str(company_name) + "," + str(vol[0][1])
    except:
        continue


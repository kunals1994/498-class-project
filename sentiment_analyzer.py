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
    
    return avg



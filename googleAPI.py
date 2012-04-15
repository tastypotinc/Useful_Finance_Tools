#calculates annualized return by calendar days (not trading days)

import urllib2
import urllib
import json
import time
import datetime

snpData = 'SNPData.csv'

class GoogleFinanceAPI:
  def __init__(self):
    self.prefix = "http://finance.google.com/finance/info?client=ig&q="
    
  def get(self,symbol,exchange):
    if exchange == "":
      url = self.prefix+"%s"%(symbol)
    else:
      url = self.prefix+"%s:%s"%(exchange,symbol)
    u = urllib2.urlopen(url)
    content = u.read()    
    obj = json.loads(content[3:])
    return obj[0]
        
def findSNPPrice(boughtDate):
  f = open(snpData,'r')
  line = f.readline()
  line = f.readline()
  while line:
    ar = line[0:-1].split(",")
    date = ar[0].split("-")
    dateFormatted = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    if dateFormatted == boughtDate:
      return ar[4]
    line = f.readline()

def sign(num):
  if(num>=0):
    return 1
  return -1
    
if __name__ == "__main__":
  c = GoogleFinanceAPI()
  f = open('myStocks.csv','r')

  try:
    open('SNPData.csv', 'r')
  except IOError as e:
    webFile = urllib.urlopen("http://ichart.finance.yahoo.com/table.csv?s=^GSPC&c=2000")
    localFile = open(snpData, 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()

  snpPriceToday = c.get("^GSPC","")['l_cur'].replace(',','')
  print "Ticker, Annualized Return, Percent More than Market, Normalized to Market and Time"
  line = f.readline()
  while line:
    s = line[0:-1].split(',')    #take out the \n
    date = s[2].split('/')
    boughtDate = (datetime.date(int(date[2]),int(date[0]),int(date[1])))
    today = (datetime.date.today())
    numDays = (today - boughtDate).days
    currentInfo = c.get(s[0],"NASDAQ")
    buyPrice = s[3]
    currentPrice = currentInfo['l_cur']
    annualizedReturn = ((float(currentPrice)/float(buyPrice))**(1./(numDays/365.))-1)*100
    stockName = s[0]
    snpPriceOnBuyDate = findSNPPrice(boughtDate)
    differenceBetweenMyStockAndMarket = float(currentPrice)/float(buyPrice) - float(snpPriceToday)/float(snpPriceOnBuyDate)
    normalizedToMarketNormalizedToTime = sign(differenceBetweenMyStockAndMarket)*(abs(differenceBetweenMyStockAndMarket)**(1./(numDays/365.)))*100
    print stockName,annualizedReturn, differenceBetweenMyStockAndMarket*100, normalizedToMarketNormalizedToTime
    line = f.readline()
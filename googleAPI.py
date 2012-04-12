#calculates annualized return by calendar days (not trading days)

import urllib2
import json
import time
import datetime

class GoogleFinanceAPI:
  def __init__(self):
    self.prefix = "http://finance.google.com/finance/info?client=ig&q="
    
  def get(self,symbol,exchange):
    url = self.prefix+"%s:%s"%(exchange,symbol)
    u = urllib2.urlopen(url)
    content = u.read()    
    obj = json.loads(content[3:])
    return obj[0]
        
        
if __name__ == "__main__":
  c = GoogleFinanceAPI()
  f = open('myStocks.csv','r')
  line = f.readline()
  while line:
    s = line[0:-1].split(',')    #take out the \n
    date = s[2].split('/')
    bought = (datetime.date(int(date[2]),int(date[0]),int(date[1])))
    today = (datetime.date.today())
    numDays = (today - bought).days
    currentInfo = c.get(s[0],"NASDAQ")
    buyPrice = s[3]
    currentPrice = currentInfo['l_cur']
    print s[0],((float(currentPrice)/float(buyPrice))**(1./(numDays/365.))-1)*100
    line = f.readline()
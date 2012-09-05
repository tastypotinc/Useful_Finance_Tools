#calculates annualized return by calendar days (not trading days)

import urllib2
import urllib
import json
import time
import datetime

snpData = 'SNPData.csv'
nasdaqData = 'NASDAQData.csv'
debug = True

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
     
def findPrice(ff,boughtDate):
  f = open(ff,'r')
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
  
  if debug:
    try:
      open(snpData, 'r')
    except IOError as e:
      webFile = urllib.urlopen("http://ichart.finance.yahoo.com/table.csv?s=^GSPC&c=2000")
      localFile = open(snpData, 'w')
      localFile.write(webFile.read())
      webFile.close()
      localFile.close()


    try:
      open(nasdaqData, 'r')
    except IOError as e:
      webFile = urllib.urlopen("http://ichart.finance.yahoo.com/table.csv?s=QQQ&c=2000")
      localFile = open(nasdaqData, 'w')
      localFile.write(webFile.read())
      webFile.close()
      localFile.close()


  else:
    webFile = urllib.urlopen("http://ichart.finance.yahoo.com/table.csv?s=QQQ&c=2000")
    localFile = open(nasdaqData, 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()

    webFile = urllib.urlopen("http://ichart.finance.yahoo.com/table.csv?s=^GSPC&c=2000")
    localFile = open(snpData, 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()


  #snpPriceToday = c.get("^GSPC","")['l_cur'].replace(',','')
  snpPriceToday = c.get("QQQ","NASDAQ")['l_cur']
  #print "Ticker, Annualized Return, Percent More than Market, Normalized to Market and Time, Normalized to Market and Time2"
  line = f.readline()
  out = list()
  total = list()
  all = ""
  while line:
    s = line[0:-1].split(',')    #take out the \n
    date = s[2].split('/')
    volume = float(s[1])
    boughtDate = (datetime.date(int(date[2]),int(date[0]),int(date[1])))
    today = (datetime.date.today())
    numDays = (today - boughtDate).days
    currentInfo = c.get(s[0],"NASDAQ")
    buyPrice = s[3]
    currentPrice = currentInfo['l_cur']
    snpPriceOnBuyDate = findPrice(snpData,boughtDate)
    snpPriceOnBuyDate = findPrice(nasdaqData,boughtDate)
    stockName = s[0]
    dataFileName = stockName+"Data.csv"
    if not debug:
      webFile = urllib.urlopen("http://ichart.finance.yahoo.com/table.csv?s="+stockName+"&c=2000")
      localFile = open(dataFileName, 'w')
      localFile.write(webFile.read())
      webFile.close()
      localFile.close()
    
    dataFile = open(dataFileName,'r')
    data = dataFile.readlines()
    for i in range(len(data)):
        data[i] = data[i].split(',')
    all += stockName + ","
    l = list()
    i = len(data)-1
    while i>0:
      dated = data[i][0].split("-")
      dateFormatted = datetime.date(int(dated[0]),int(dated[1]),int(dated[2]))
      if dateFormatted == boughtDate:
        break
      i-=1
    while i>0:
      l.append([data[i][0],str(float(volume*float(data[i][4])))])
      i-=1
    total.append(l)
    #annualizedReturn = ((float(currentPrice)/float(buyPrice))**(1./(numDays/365.))-1)*100   
    #annualizedReturnSNP = ((float(snpPriceToday)/float(snpPriceOnBuyDate))**(1./(numDays/365.))-1)*100    
    #differenceBetweenMyStockAndMarket = (float(currentPrice)/float(buyPrice) - float(snpPriceToday)/float(snpPriceOnBuyDate))*100

    #normalizedToMarketNormalizedToTime = (annualizedReturn - annualizedReturnSNP)
    #print stockName, normalizedToMarketNormalizedToTime
    #print

    line = f.readline()
    
  indices = list()
  titles = list()
  length = len(total)
  line = list()
  titlesAll = all.split(',')
  for i in range(length):
    indices.append(-1)
    line.append(list())
    titles.append(titlesAll[i])
  curd = total[0][0][0]
  while(1):
    for i in range(length):
      if curd == total[i][0][0]:
        indices[i] = 0
    for i in range(length):    
      dated = total[0][indices[0]][0].split("-")
      dateFormatted = datetime.datetime(int(dated[0]),int(dated[1]),int(dated[2]))
      epoch = datetime.datetime.utcfromtimestamp(0)
      d = dateFormatted - epoch
      if(indices[i] == -1):
        line[i].append([str(dateFormatted.year)+","+str(dateFormatted.month)+","+str(dateFormatted.day),0])
      else:
        line[i].append([str(dateFormatted.year)+","+str(dateFormatted.month)+","+str(dateFormatted.day),float(total[i][indices[i]][1])])
        indices[i]+=1
      if(indices[0]>len(total[0])-1):
        break
    if(indices[0]>len(total[0])-1):
      break
    curd = total[0][indices[0]][0]
  data = ""
  dataTitles = ""
  for i in range(len(titles)):
    for j in range(len(line[i])):
      data += "seriesData["+str(i)+"]["+str(j)+"] = "+"{ x:Math.floor(new Date(" + str(line[i][j][0]) + ").getTime() / 1000), y:" + str(line[i][j][1]) + "};"
    dataTitles += "{color: palette.color(),data: seriesData["+str(i)+"],name: '"+titles[i]+"'},"
    #dataTitles += titles[i]+": '"+titles[i]+"',"
  dataTitles = dataTitles[0:-1]
  st = """
  <!doctype>
  <head>
  	<link type="text/css" rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css">
  	<link type="text/css" rel="stylesheet" href="http://code.shutterstock.com/rickshaw/src/css/graph.css">
  	<link type="text/css" rel="stylesheet" href="http://code.shutterstock.com/rickshaw/src/css/detail.css">
  	<link type="text/css" rel="stylesheet" href="http://code.shutterstock.com/rickshaw/src/css/legend.css">
  	<link type="text/css" rel="stylesheet" href="http://code.shutterstock.com/rickshaw/examples/css/extensions.css">

  	<script src="http://code.shutterstock.com/rickshaw/vendor/d3.min.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/vendor/d3.layout.min.js"></script>

  	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
  	<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>

  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Class.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Compat.ClassList.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Renderer.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Renderer.Area.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Renderer.Line.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Renderer.Bar.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Renderer.ScatterPlot.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.RangeSlider.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.HoverDetail.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Annotate.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Legend.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Axis.Time.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Behavior.Series.Toggle.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Behavior.Series.Order.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Behavior.Series.Highlight.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Smoother.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Unstacker.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Fixtures.Time.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Fixtures.Number.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Fixtures.RandomData.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Fixtures.Color.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Color.Palette.js"></script>
  	<script src="http://code.shutterstock.com/rickshaw/src/js/Rickshaw.Graph.Axis.Y.js"></script>

  	<script src="http://code.shutterstock.com/rickshaw/examples/js/extensions.js"></script>
  </head>
  <body>

  <div id="content">

  	<form id="side_panel">
  		<h1>Random Data in the Future</h1>
  		<section><div id="legend"></div></section>
  		<section>
  			<div id="renderer_form" class="toggler">
  				<input type="radio" name="renderer" id="area" value="area" checked>
  				<label for="area">area</label>
  				<input type="radio" name="renderer" id="bar" value="bar">
  				<label for="bar">bar</label>
  				<input type="radio" name="renderer" id="line" value="line">
  				<label for="line">line</label>
  				<input type="radio" name="renderer" id="scatter" value="scatterplot">
  				<label for="scatter">scatter</label>
  			</div>
  		</section>
  		<section>
  			<div id="offset_form">
  				<label for="stack">
  					<input type="radio" name="offset" id="stack" value="zero" checked>
  					<span>stack</span>
  				</label>
  				<label for="stream">
  					<input type="radio" name="offset" id="stream" value="wiggle">
  					<span>stream</span>
  				</label>
  				<label for="pct">
  					<input type="radio" name="offset" id="pct" value="expand">
  					<span>pct</span>
  				</label>
  				<label for="value">
  					<input type="radio" name="offset" id="value" value="value">
  					<span>value</span>
  				</label>
  			</div>
  			<div id="interpolation_form">
  				<label for="cardinal">
  					<input type="radio" name="interpolation" id="cardinal" value="cardinal" checked>
  					<span>cardinal</span>
  				</label>
  				<label for="linear">
  					<input type="radio" name="interpolation" id="linear" value="linear">
  					<span>linear</span>
  				</label>
  				<label for="step">
  					<input type="radio" name="interpolation" id="step" value="step-after">
  					<span>step</span>
  				</label>
  			</div>
  		</section>
  		<section>
  			<h6>Smoothing</h6>
  			<div id="smoother"></div>
  		</section>
  		<section></section>
  	</form>

  	<div id="chart_container">
  		<div id="chart"></div>
  		<div id="timeline"></div>
  		<div id="slider"></div>
  	</div>

  </div>

  <script>
  var seriesData = [ [], [], [], [], [], [], [], [], [] ];
  var random = new Rickshaw.Fixtures.RandomData(150);

  for (var i = 0; i < """+str(len(line[0]))+"""; i++) {
  	random.addData(seriesData);
  }
  // set up our data series with 50 random data points
  """+data+"""
  

  var palette = new Rickshaw.Color.Palette( { scheme: 'classic9' } );

  // instantiate our graph!

  var graph = new Rickshaw.Graph( {
  	element: document.getElementById("chart"),
  	width: 900,
  	height: 500,
  	renderer: 'area',
  	stroke: true,
  	series: ["""+ dataTitles +"""
  	]
  } );

  graph.render();

  var slider = new Rickshaw.Graph.RangeSlider( {
  	graph: graph,
  	element: $('#slider')
  } );

  var hoverDetail = new Rickshaw.Graph.HoverDetail( {
  	graph: graph
  } );

  var annotator = new Rickshaw.Graph.Annotate( {
  	graph: graph,
  	element: document.getElementById('timeline')
  } );

  var legend = new Rickshaw.Graph.Legend( {
  	graph: graph,
  	element: document.getElementById('legend')

  } );

  var shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
  	graph: graph,
  	legend: legend
  } );

  var order = new Rickshaw.Graph.Behavior.Series.Order( {
  	graph: graph,
  	legend: legend
  } );

  var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight( {
  	graph: graph,
  	legend: legend
  } );

  var smoother = new Rickshaw.Graph.Smoother( {
  	graph: graph,
  	element: $('#smoother')
  } );

  var ticksTreatment = 'glow';

  var xAxis = new Rickshaw.Graph.Axis.Time( {
  	graph: graph,
  	ticksTreatment: ticksTreatment
  } );

  xAxis.render();

  var yAxis = new Rickshaw.Graph.Axis.Y( {
  	graph: graph,
  	tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
  	ticksTreatment: ticksTreatment
  } );

  yAxis.render();


  var controls = new RenderControls( {
  	element: document.querySelector('form'),
  	graph: graph
  } );

  // add some data every so often

  var messages = [
  	"Changed home page welcome message",
  	"Minified JS and CSS",
  	"Changed button color from blue to green",
  	"Refactored SQL query to use indexed columns",
  	"Added additional logging for debugging",
  	"Fixed typo",
  	"Rewrite conditional logic for clarity",
  	"Added documentation for new methods"
  ];

  setInterval( function() {
  	random.addData(seriesData);
  	graph.update();

  }, 3000 );

  function addAnnotation(force) {
  	if (messages.length > 0 && (force || Math.random() >= 0.95)) {
  		annotator.add(seriesData[2][seriesData[2].length-1].x, messages.shift());
  	}
  }

  addAnnotation(true);
  setTimeout( function() { setInterval( addAnnotation, 6000 ) }, 6000 );

  </script>

  </body>

  """
  fff = open('stacked_area2/graph.html','w')
  fff.write(st)
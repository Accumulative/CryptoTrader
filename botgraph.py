# -*- coding: utf-8 -*-
from botlog import BotLog
class BotGraph(object):
    def __init__(self):
        self.output = BotLog()
        self.outputfile = open("output.html",'w')
        

    def outputGraph(self, dataPoints):
        self.output.log("Creating graph...")
        self.outputfile.truncate()
        self.outputfile.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotationText'});data.addColumn('number', 'trend');data.addRows([""")    
   
        for point in dataPoints:
            self.outputfile.write("['"+point['date']+"',"+point['price']+","+point['label']+","+point['desc']+","+point['trend'])
            self.outputfile.write("],\n")
            
        self.outputfile.write("""]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));chart.draw(data, options);}</script></head><body><div id="curve_chart" style="width: 100%; height: 100%"></div></body></html>""")
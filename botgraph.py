# -*- coding: utf-8 -*-
from botlog import BotLog
import matplotlib.pyplot as plt
import numpy as np

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
        
    def heatmap(self, datapoints):
        
        intensity = []
        minX = 100000
        minY = 100000
        maxX = 0
        maxY = 0
        x = []
        y = []
        for point in datapoints:
            if point[0][0][1] > maxX:
                maxX = point[0][0][1]
            elif point[0][0][1] < minX:
                minX = point[0][0][1]
                
            if point[0][1][1] > maxY:
                maxY = point[0][1][1]
            elif point[0][1][1] < minY:
                minY = point[0][1][1]
                
            intensity.append(point[1])
            
        x = np.arange(minX,maxX)
        y = np.arange(minY,maxY)
        
        #setup the 2D grid with Numpy
        x, y = np.meshgrid(x, y)
        
        #convert intensity (list of lists) to a numpy array for plotting
        intensity = np.array(intensity)
        
        #now just plug the data into pcolormesh, it's that easy!
        plt.pcolormesh(x, y, intensity)
        plt.colorbar() #need a colorbar to show the intensity scale
        plt.show() #boom
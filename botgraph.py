# -*- coding: utf-8 -*-
from botlog import BotLog
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from datehelper import DateHelper
import datetime

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
        
    def heatmap(datapoints):
        intensity = []
        minX = min(datapoints, key=lambda e: int(e[1][0][1]))[1][0][1]
        minY = min(datapoints, key=lambda e: int(e[1][1][1]))[1][1][1]
        maxX = max(datapoints, key=lambda e: int(e[1][0][1]))[1][0][1]
        maxY = max(datapoints, key=lambda e: int(e[1][1][1]))[1][1][1]
        xStep = datapoints[1][1][0][1]-datapoints[0][1][0][1]
        print(datapoints)
        yStep = datapoints[int(round((maxX-minX)/xStep,0))+1][1][1][1]-datapoints[0][1][1][1]
        x = []
        y = []
        print(minY,maxY+yStep,yStep)
        x = np.arange(minX,maxX+xStep,xStep)
        y = np.arange(minY,maxY+yStep,yStep)
        intensity = np.zeros([(maxY-minY)/yStep+1,(maxX-minX)/xStep+1])
        
        for point in datapoints:
            intensity[(point[1][1][1]-minY)/yStep,(point[1][0][1]-minX)/xStep] = point[2]
        
        #setup the 2D grid with Numpy
        x, y = np.meshgrid(x, y)
        
        
        fig = plt.figure()
        
        #now just plug the data into pcolormesh, it's that easy!
        plt.pcolormesh(x, y, intensity)
        plt.colorbar() #need a colorbar to show the intensity scale
        fig.savefig("Graphs/"+str(DateHelper.ut(datetime.datetime.now()))+'_heatmap.png')   # save the figure to file
        plt.close(fig) 
            
    def graph(datapoints):
        
        
        intensity = []
        #        minX = 100000
        #        minY = 100000
        #        maxX = 0
        #        maxY = 0
        x = []
        y = []
        for point in datapoints:
            x.append(point[1][0][1])
            y.append(point[1][1][1])
            intensity.append(point[2])
            
            
        x = np.array(x)
        y = np.array(y)
        intensity = np.array(intensity)
        
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, projection='3d')
        
        ax.plot(x, y, intensity)
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        
        fig.savefig("Graphs/"+str(DateHelper.ut(datetime.datetime.now()))+'_graph.png')   # save the figure to file
        plt.close(fig) 
            
# -*- coding: utf-8 -*-
from botlog import BotLog
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from datehelper import DateHelper
import datetime

class BotGraph(object):
    def __init__(self):
        self.output = BotLog()
        self.outputfile = open("output2.html",'w')
        

    def outputGraph(self, datapoints, trades):
        

#        currentHTrend = 0.018
#        currentLTrend = 0.018  
        for points in datapoints:
#            if points['label'] == 'null':
#                points['lowtrend'] = currentLTrend
#                points['hightrend'] = currentHTrend
#            elif 'MAX' in points['label']:
#                currentHTrend = points['hightrend']
#                points['lowtrend'] = currentLTrend
#            elif 'MIN' in points['label']:
#                currentLTrend = points['lowtrend']
#                points['hightrend'] = currentHTrend
                
            for trade in trades:
                if trade.dateOpened == points['date']:
                    points['buy'] = "'buy'"
                elif trade.dateClosed == points['date']:
                    points['sell'] = "'sell'"
        
        self.output.log("Creating graph...")
        self.outputfile.truncate()
#        self.outputfile.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotationText'});data.addColumn('number', 'lowtrend');data.addColumn('number', 'hightrend');data.addRows([""")    
#   
#        toWrite = ""
#        for point in datapoints:
#            toWrite += ("['"+point['date']+"',"+point['price']+","+point['buy']+","+point['sell']+",,,")#+point['label']+","+point['desc']+","+str(point['lowtrend'])+","+str(point['hightrend']))
#            toWrite += ("],\n")
#            
#        toWrite = toWrite[:-2]
#        self.outputfile.write(toWrite+"""]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));chart.draw(data, options);}</script></head><body><div id="curve_chart" style="width: 100%; height: 100%"></div></body></html>""")
#    
        self.outputfile.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotation'});data.addRows([""")    
   
        toWrite = ""
        for point in datapoints[:500]:
            toWrite += ("['"+point['date']+"',"+point['price']+","+point['buy']+","+point['sell'])#+point['label']+","+point['desc']+","+str(point['lowtrend'])+","+str(point['hightrend']))
            toWrite += ("],\n")
            
        toWrite = toWrite[:-2]
        self.outputfile.write(toWrite+"""]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));chart.draw(data, options);}</script></head><body><div id="curve_chart" style="width: 100%; height: 100%"></div></body></html>""")
    
       
    
    def heatmap(self, datapoints):
#        print(datapoints)
        
        dimensions = len(datapoints[0][1])        
        numberOfPoints = len(datapoints)
        closenessLimit = int(np.ceil(numberOfPoints * 0.01))
        
        intensity = []
        minArray = [min(datapoints, key=lambda e: float(e[1][i][1]))[1][i][1] for i in range(dimensions)]
        maxArray = [max(datapoints, key=lambda e: float(e[1][i][1]))[1][i][1] for i in range(dimensions)]
        
        steps = []
        nextStep = 1
        for j in range(dimensions):
            if nextStep < len(datapoints):
                steps.append(datapoints[nextStep][1][j][1]-datapoints[nextStep - 1][1][j][1])
#                print(j,maxArray[j],minArray[j],steps[j])
                
                nextStep *= int(round((maxArray[j]-minArray[j])/steps[j],0))+1
            else:
                steps.append(1)
        
        data = []
        for j in range(dimensions):
            data.append(np.arange(minArray[j],maxArray[j]+steps[j],steps[j]))
        
        #setup the 2D grid with Numpy
        mesh = np.meshgrid(*[np.linspace(minArray[i],maxArray[i],float((maxArray[i]-minArray[i])/steps[i])+1) for i in range(dimensions)])
        
        for i in range(dimensions):
            datapoints = sorted(datapoints, key=lambda x: x[1][dimensions-i-1][1])
        
        # WRONG
        m = []
        for s in range(len(steps)):
            m.append(int((maxArray[s]-minArray[s])/steps[s])+1)
        
        intensity = np.zeros(m[::-1])
        topFive = sorted([x if x[2]!=0 else [x[0],x[1],-10000] for x in datapoints], key=lambda x: x[2], reverse=True)[:5]
        topFiveIndex = np.zeros([len(topFive),dimensions])#sorted(range(len(datapoints)), key=lambda k: datapoints[k][2], reverse=True)[:5]
        
        count = 0
        for index,value in np.ndenumerate( intensity ):
            count += 1
            pos = index[dimensions-1]
            for i in range(dimensions-1):
#                print(index[i], index[i+1], int(round((maxArray[i+1]-minArray[i+1])/steps[i+1],0)) )
                pos += index[i] + index[i+1] * int(round((maxArray[i+1]-minArray[i+1])/steps[i+1],0))
            
#            print(index, pos)
            intensity[index] = datapoints[pos][2]
            
            for val in range(len(topFive)):
                if value == topFive[val][2]:
                    topFiveIndex[val] = index # (y, x)
        
        scoreArray = []
        for i in range(len(topFive)):
            if topFive[i][2] != 0:
#                simArray = np.subtract(intensity, topFive[i][2])
    #            print(simArray)
                score = 0
                counter = 0
                for index,value in np.ndenumerate( intensity ):
                    #print(topFiveIndex[i],index[::-1],np.sqrt(np.sum(np.square(np.subtract(topFiveIndex[i],index[::-1])))))
                    if np.sqrt(np.sum(np.square(np.subtract(topFiveIndex[i],index[::-1])))) <= closenessLimit:
    #                    
#                        if value != 0:
                        score += value
                        counter +=1 
                            
#                if counter != 0:    
                scoreArray.append((score/counter + topFive[i][2])/2)
        
        winner = max(range(len(scoreArray)), key=lambda k: scoreArray[k])    
        
        #self.output.log(', '.join([str(x) for x in topFive[winner]]))
        print(', '.join([str(x) for x in topFive[winner]]))
        
        if dimensions == 2:
            fig = plt.figure()
            
            #now just plug the data into pcolormesh, it's that easy!
            #print(mesh[0], mesh[1], intensity)
            plt.pcolormesh(mesh[0], mesh[1], intensity)
            plt.colorbar() #need a colorbar to show the intensity scale
            #plt.show()
            fig.savefig("Graphs/"+str(DateHelper.ut(datetime.datetime.now()))+'_heatmap.png')   # save the figure to file
            plt.close(fig) 
            
            x = [point[2] for point in datapoints]
            fig, axarr = plt.subplots(dimensions, sharex=True)
            for k in range(dimensions):
    #            fig = plt.figure()
                y = [x[1][k][1] for x in datapoints]
                
                axarr[k].scatter(x, y)
                axarr[k].set_title(datapoints[0][1][k][0])
                
            fig.savefig("Graphs/"+str(DateHelper.ut(datetime.datetime.now()))+'graph.png')   # save the figure to file
    #        plt.close(fig) 

            
    def graph(self, datapoints):
        
        
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
        fig.add_subplot(1,1,1, projection='3d')
        ax = Axes3D(fig)
        ax.plot(x, y, intensity)
        
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        
        fig.savefig("Graphs/"+str(DateHelper.ut(datetime.datetime.now()))+'_graph.png')   # save the figure to file
        plt.close(fig) 
            
    def stratGraph(self, datapoints, trades):
        
        for points in datapoints:
            if points['label'] == 'null':
                points['lowtrend'] = currentLTrend
                points['hightrend'] = currentHTrend
            elif 'MAX' in points['label']:
                currentHTrend = points['hightrend']
                points['lowtrend'] = currentLTrend
            elif 'MIN' in points['label']:
                currentLTrend = points['lowtrend']
                points['hightrend'] = currentHTrend
                
            for trade in trades:
                if trade.dateOpened == points['date']:
                    points['buy'] = "'buy'"
                elif trade.dateClosed == points['date']:
                    points['sell'] = "'sell'"
        
        self.output.log("Creating graph...")
        self.outputfile.truncate()
        self.outputfile.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotationText'});data.addColumn('number', 'lowtrend');data.addColumn('number', 'hightrend');data.addRows([""")    
   
        toWrite = ""
        for point in datapoints:
            toWrite += ("['"+point['date']+"',"+point['price']+","+point['buy']+","+point['sell']+","+point['label']+","+point['desc']+","+str(point['lowtrend'])+","+str(point['hightrend']))
            toWrite += ("],\n")
            
        toWrite = toWrite[:-2]
        self.outputfile.write(toWrite+"""]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));chart.draw(data, options);}</script></head><body><div id="curve_chart" style="width: 100%; height: 100%"></div></body></html>""")
    
        self.outputfile.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotationText'});data.addColumn('number', 'lowtrend');data.addColumn('number', 'hightrend');data.addRows([""")    
   
        toWrite = ""
        for point in datapoints:
            toWrite += ("['"+point['date']+"',"+point['price']+","+point['buy']+","+point['sell']+","+point['label']+","+point['desc']+","+str(point['lowtrend'])+","+str(point['hightrend']))
            toWrite += ("],\n")
            
        toWrite = toWrite[:-2]
        self.outputfile.write(toWrite+"""]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));chart.draw(data, options);}</script></head><body><div id="curve_chart" style="width: 100%; height: 100%"></div></body></html>""")
    
        
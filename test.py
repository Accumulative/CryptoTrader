#a = [[0.0, -1.1569814830602203, -1.5210630429081204, -2.2267587495516685, -2.2659075812960214, -2.313380663283428, -2.4588321391896035, -2.5521147238203925, -2.5874606512912823, -2.7301402483070203, -2.338680053957958, -2.5778177817963894, -2.8371829145176943, -2.8278559241735826]]
#b = [-7.228097370200745, 0.0, -1.300144766821885, -2.095316769917156, -2.115276129800277, -2.187663369993712, -2.213857010591769, -2.272336315561456, -2.4632703626166, -3.058285700948906, -2.7780231988596937, -2.5762858658501386, -2.5439621428866888, -2.113781589738441]
#import matplotlib
#import matplotlib.pyplot as plt
#import math
#import numpy as np
#
#
#
#fig, axarr = plt.subplots(2, sharex = True)
#axarr[0].scatter(range(0, len(a[0])), a[0])
#axarr[1].scatter(range(0, len(b)), b)
##fig.savefig("Graphs/123graph.png");
#
#def getLinearity(X, Y):
#    diff = np.subtract(X, Y)
#    c = [x for x in range(1, len(diff)+1)]
#    sumX2 = sum(np.square(c))
#    sumY2 = sum(np.square(diff))
#    sumXY = sum(np.multiply(c,diff))
#    sumX = sum(c)
#    sumY = sum(diff)
#    n = len(diff)
#    r = (n * sumXY - sumX * sumY) / (math.sqrt(n * sumX2 - sumX * sumX) * math.sqrt(n * sumY2 - sumY * sumY))
#    return r
#
#simArray = []
#for x in range(6, len(b) + 1):
##        print(x, y)
#    c = a[0][len(b)-x:]
#    d = b[len(b)-x:]
#    
##        print(c, d)
#    simArray.append([x, getLinearity(c,d), getLinearity(c,d) / math.sqrt(x)])
#
#res = sorted(simArray, key=lambda x: abs(x[2]))[-1]
#x = res[0]
#print(a[0][len(b)-x:], b[len(b)-x:])

import pstats
p = pstats.Stats('profile.txt')
p.strip_dirs().sort_stats('time').print_stats(50)
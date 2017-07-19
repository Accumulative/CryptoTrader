# -*- coding: utf-8 -*-

import os

class CreateIndex(object):
    def __init__(self, env):
        
        if env == 'PI':
            self.runningOnPi = True
        else:
            self.runningOnPi = False
        
        if self.runningOnPi == False:
            self.directory = os.path.abspath("") + "/"
        else:
            self.directory = ""
            
    def CreatePages(self):
        with open("index.html", "w") as text_file:
            print("""<h1>{0}</h1>""".format("INDEX"), file=text_file)
            print("""<h2>{0}</h2>""".format("BALANCE"), file=text_file)
            print("""<li><a href="{0}">{1}</a></li>""".format(self.directory + "/balance.html", "Link to balance"), file=text_file)
            print("""<h2>{0}</h2>""".format("GRAPH"), file=text_file)
            print("""<li><a href="{0}">{1}</a></li>""".format(self.directory + "/output.html", "Link to graph"), file=text_file)
            for folder in os.listdir("Logs"):
                if len(folder) == 8:
                    print("""<h3>{0}</h3>""".format(folder), file=text_file)
                    print("""<li><a href="{0}">{1}</a></li>""".format(self.directory + "/Logs/"+folder+"/trades.html", "Trades"), file=text_file)
                    print("""<li><a href="{0}">{1}</a></li>""".format(self.directory + "/Logs/"+folder+"/output.html", "Logs"), file=text_file)
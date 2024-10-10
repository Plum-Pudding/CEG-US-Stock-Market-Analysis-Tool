#system
from ipaddress import ip_interface
import os;
import sys;
import math
from tkinter import Button;
import webbrowser; 

#vendor libraries

'''
import vendor.requests.src.requests as requests; #Fucking stupid way of doing this but Python can't find the source and the above code isn't working
#Removed plotly-- see changelog
import vendor.PyQt6.sip as Qt6;
import vendor.pyqtgraph as QtGraph;
from vendor.PyQt6.sip.QtWidgets import qwidget;
from vendor.PyQt6.sip.QtGui import qicon;
'''

import PyQt6 as Qt6; #Backwards compat
import pyqtgraph as QtGraph; #Backwards compat
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget;
import requests;
import yfinance as yfin; #Backwards compat


#internal 
import utilAPI;
import utilStockAnalysis;
import stockPrediction;


#online sources for data
#import vendor.yfinance as yfin;


#TODO: Check if everyone has the vEnv sorted
#TODO: Check if the requirements.txt actually has everything, because I suspect it doesn't, despite the pip freeze

def main1():
    #Sort out yFinance stuff
    #print(utilAPI.textYFin("AAPL"));
    #print("Test:", utilAPI.testFunc())

    #todo: sample 

    # utilAPI.testFunction()

    #Start GUI
    
    #appMain is the main QApplication class
    appMain = QApplication(sys.argv)

    #Declaring some variables for the GUI
    windowTitle = "CEG Stock Anaylsis Tool";
    buttonAbleLabel = "Press test!";
    minWindowHeight = 300;
    minWindowWidth = 400;

    class mainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            #Test button widget
            buttonAble = QPushButton(buttonAbleLabel);
            buttonAble.setCheckable(True);
            buttonAble.clicked.connect(self.buttonAbleClicked);

            self.setWindowTitle(windowTitle); #Set window title
            self.setMinimumSize(minWindowWidth, minWindowHeight); #Set minimum window dimensions

            #Window widgets
            self.setCentralWidget(buttonAble); #Test set central widget to a button (doesn't do anything yet)

        def buttonAbleClicked(self):
            print("Button Able clicked.");

    window = mainWindow();
    window.show();

    #Start event loop
    appMain.exec();


    print("sus");
    pass;




if __name__ == "__main__":
    main1();
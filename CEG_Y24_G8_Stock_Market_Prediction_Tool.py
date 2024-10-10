#system-- check if we still need some of these, pretty sure we don't
from ast import main
from ipaddress import ip_interface
import os;
import sys;
import math
from tkinter import Button;
import webbrowser; 

#vendor libraries

import PyQt6 as Qt6; #Backwards compat
import pyqtgraph as QtGraph; #Backwards compat
from pyqtgraph import GraphicsLayout, PlotWidget, mkPen;
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QStackedLayout, QVBoxLayout, QWidget, QTabWidget;
from PyQt6.QtGui import QPalette, QColor;
import requests;
import yfinance as yfin; #Backwards compat
import pandas;
import numpy;


#internal 
import utilAPI;
import utilStockAnalysis;
import stockPrediction;


#online sources for data
#import vendor.yfinance as yfin;


#TODO: Check if everyone has the vEnv sorted
#TODO: Check if the requirements.txt actually has everything, because I suspect it doesn't, despite the pip freeze

#Blank coloured widget for GUI testing

class colourTest(QWidget):
    def __init__(self, colour):
        super(colourTest, self).__init__();
        #Fill self with colour
        self.setAutoFillBackground(True);
            
        #Set QPalette window colour to QColor
        paletteA = self.palette();
        paletteA.setColor(QPalette.ColorRole.Window, QColor(colour));
        self.setPalette(paletteA);

def main1():
    #Retrieve test stock data
    testDataHist = pandas.DataFrame();
    testDataHist = utilAPI.yFinGetHist("TSLA","1wk");

    testDataHistList_Closing = testDataHist["Close"].values.tolist();
    #testDataHistList_Date = testDataHist[testDataHist.columns[0]].values.tolist(); #dates column is empty on row 0, "Date" on row 1, data on row 2 onwards
    testDataHistList_Date = testDataHist.index.tolist(); #this might not work-- maybe use the current date and minus 1 per datapoint?

    #del testDataHistList_Date[0];
    #del testDataHistList_Date[0];

    print(testDataHistList_Closing);
    print(testDataHistList_Date);

    #Start GUI
    
    

    #appMain is the main QApplication class
    appMain = QApplication(sys.argv)

    #Declaring some variables for the GUI properties
    windowTitle = "CEG Stock Anaylsis Tool";
    buttonAbleLabel = "Press test!";
    minWindowHeight = 450;
    minWindowWidth = 800;
    backgroundPalette = "#0e140f"; #hex code colour for background
    tabPalette = "#1a241c" #hex code code colour for tabs

    class mainWindow(QMainWindow):
        def __init__(self):
            super(mainWindow, self).__init__()

            #Layouts
            layoutA = QHBoxLayout();
            layoutB = QVBoxLayout();
            layoutC = QHBoxLayout();
            layoutD = QHBoxLayout();

            #Colour box test widgets
            colourA = colourTest("red");
            colourB = colourTest("orange");
            colourC = colourTest("yellow");
            colourD = colourTest("green");
            colourE = colourTest("cyan");
            colourF = colourTest("blue");
            colourG = colourTest("magenta");
            colourH = colourTest("darkMagenta");

            #Tabs widget
            mainTabs = QTabWidget();
            mainTabs.setTabPosition(QTabWidget.TabPosition.West);
            mainTabs.setMovable(True);

            #Graph colours and pens
            #pen1 = mkPen("red", 2);

            #Graph plotting test
            dataTest1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16];
            dataTest2 = [1,4,2,15,3,3,5,12,7,14,0,5,5,1,2];
            dataTest3 = [21,3,2,5,6,62,47,9,3,6,32,14,21,2,5]; 
            graph1 = PlotWidget();
            graph2 = PlotWidget();
            graph3 = PlotWidget();
            graph1.plot(dataTest1, dataTest2);
            graph2.plot(dataTest1, dataTest3);
            graph3.plot(dataTest1, dataTest2);

            #Graph plotting with real data
            #fin1Ticker = utilAPI.textYFin("AAPL", "5d")
            #dataFin1Axis1 = fin1Ticker.to_numpy();


            graphA = PlotWidget();
            graphA.plot(y=testDataHistList_Closing, pen=(64, 102, 255)) #todo: change this to use real data
            #graphA.

            #Setting layouts
            layoutB.addWidget(colourC);
            layoutB.addWidget(graph2);
            layoutB.addWidget(colourE);
            layoutB.addWidget(graph1);
            layoutB.addWidget(colourTest("red"));

            layoutA.addLayout(layoutB);

            layoutA.addWidget(graph3);
            #layoutA.addWidget(colourB);

            layoutC.addWidget(colourTest("red"));
            layoutC.addWidget(colourTest("orange"));

            layoutD.addWidget(graphA);

            #Individual tab widgets
            tab1 = QWidget();
            tab2 = QWidget();
            tab3 = QWidget();
            tab1.setLayout(layoutA);
            tab2.setLayout(layoutC);
            tab3.setLayout(layoutD);

            #Assigning widgets to tabs, tab properties
            tab1.setAutoFillBackground(True);
            palettetab1 = tab1.palette(); 
            palettetab1.setColor(QPalette.ColorRole.Window, QColor(tabPalette)); #set widget palette to backgroundPalette hex code
            tab1.setPalette(palettetab1); 

            tab2.setAutoFillBackground(True);
            palettetab2 = tab2.palette(); 
            palettetab2.setColor(QPalette.ColorRole.Window, QColor(tabPalette)); #set widget palette to backgroundPalette hex code
            tab2.setPalette(palettetab2); 

            mainTabs.addTab(tab1, "tab1"); #set tab1 widget as first tab, tab2 as second tab for mainTabs widget
            mainTabs.addTab(tab2, "tab2");
            mainTabs.addTab(tab3, "tab3");

            #Test button widget
            buttonAble = QPushButton(buttonAbleLabel);
            buttonAble.setCheckable(True);
            buttonAble.clicked.connect(self.buttonAbleClicked);
            
            #Set main window properties
            self.setWindowTitle(windowTitle); #Set window title
            self.setMinimumSize(minWindowWidth, minWindowHeight); #Set minimum window dimensions
            self.setAutoFillBackground(True); #Auto fill widget background colour

            paletteMain = self.palette(); 
            paletteMain.setColor(QPalette.ColorRole.Window, QColor(backgroundPalette)); #set widget palette to backgroundPalette hex code
            self.setPalette(paletteMain); 


            #mainWidget = QWidget();
            #mainWidget.setLayout(   );
            self.setCentralWidget(mainTabs); #set this back to mainTabs after testing


        def buttonAbleClicked(self):
            print("Button Able clicked.");

    window = mainWindow();
    window.show();

    #Start event loop
    appMain.exec();


    print("End");
    pass;




if __name__ == "__main__":
    main1();
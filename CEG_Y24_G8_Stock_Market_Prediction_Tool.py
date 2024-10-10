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
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QStackedLayout, QVBoxLayout, QWidget, QTabWidget;
from PyQt6.QtGui import QPalette, QColor;
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
    #Sort out yFinance stuff
    

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

            #Setting layouts
            layoutB.addWidget(colourC);
            layoutB.addWidget(colourD);

            layoutA.addLayout(layoutB);

            layoutA.addWidget(colourA);
            #layoutA.addWidget(colourB);

            layoutC.addWidget(colourF);
            layoutC.addWidget(colourG);

            #layoutB.addLayout(layoutA);

            #Individual tab widgets
            tab1 = QWidget();
            tab2 = QWidget();
            tab1.setLayout(layoutA);
            tab2.setLayout(layoutC);

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
            self.setCentralWidget(mainTabs);


        def buttonAbleClicked(self):
            print("Button Able clicked.");

    window = mainWindow();
    window.show();

    #Start event loop
    appMain.exec();

    

    print("Hello there");
    pass;




if __name__ == "__main__":
    main1();
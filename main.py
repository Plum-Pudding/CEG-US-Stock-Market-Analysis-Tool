import sys
import PyQt6 as pyqt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QStackedWidget, QScrollArea, QTabWidget
from PyQt6.QtGui import QIcon
import pyqtgraph as pg

import yfinance as yf # Yahoo! Finance API to get data on stocks
import mplfinance as mpf 

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas # for matplotlib to work with PyQt6
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import numpy as np
import pandas as pd
import pandas_datareader as web
import datetime as dt


# from sklearn.preprocessing import MinMaxScaler
# import tensorflow as tf
# from tensorflow

from main_ticker import MainPage
from compare_ticker import ComparePage
from rank_ticker import RankPage
from ml_prediction import PredictionPage


class myApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # widgets settings
        self.setWindowTitle("Stocks Viewer")
        self.setWindowIcon(QIcon('icons/barcharticon.png'))
        self.resize(1500,850) # width, height
        
        #Tabs widget
        mainTabs = QTabWidget(); #Create base tab widget
        mainTabs.setTabPosition(QTabWidget.TabPosition.West); #Put the tabs on the left(west) side
        mainTabs.setMovable(True); #Allow user to drag and drop tabs

        # Main Layout
        layout = QVBoxLayout()

        #Individual tab layouts
        mainPage1 = MainPage(); #create instances of each page class
        comparePage1 = ComparePage();
        rankPage1 = RankPage();
        predictionPage1 = PredictionPage();

        layoutTab1 = QVBoxLayout();
        layoutTab2 = QVBoxLayout();
        layoutTab3 = QVBoxLayout();
        layoutTab4 = QVBoxLayout();
        layoutTab1.addWidget(mainPage1); #Put the page widgets in layouts
        layoutTab2.addWidget(comparePage1);
        layoutTab3.addWidget(rankPage1);
        layoutTab4.addWidget(predictionPage1);

        #Individual tab widgets
        tabMain = QWidget(); #Creating tab widgets
        tabCompare = QWidget();
        tabRank = QWidget();
        tabPredict = QWidget();
        tabMain.setLayout(layoutTab1); #Setting tabs to layout with page widgets
        tabCompare.setLayout(layoutTab2);
        tabRank.setLayout(layoutTab3);
        tabPredict.setLayout(layoutTab4);

        #Tab order
        mainTabs.addTab(tabMain, "Main"); #set tab1 widget as first tab, tab2 as second tab for mainTabs widget
        mainTabs.addTab(tabCompare, "Compare");
        mainTabs.addTab(tabRank, "Ranking");
        mainTabs.addTab(tabPredict, "Prediction");

        #Set mainTabs tab widget to the main one
        self.setCentralWidget(mainTabs);

def main():
    
    

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 15px;
            background-color:  /* set background color for all QWidgets elements (blank for now so default colors will be used) */
        }
        QPushButton {
            font-size: 25px;
            color: white
        }
        QLabel{
            color: white
        }
    ''')

    window = myApp()
    window.show()  # to display the window
    sys.exit(app.exec())  # to exit

    pass;

if __name__ == "__main__":
    main();

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


class myApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # widgets settings
        self.setWindowTitle("Stocks Viewer")
        self.setWindowIcon(QIcon('icons/barcharticon.png'))
        self.resize(1500,850) # width, height
        
        #Tabs widget
        mainTabs = QTabWidget();
        mainTabs.setTabPosition(QTabWidget.TabPosition.West);
        mainTabs.setMovable(True);

        # Main Layout
        layout = QVBoxLayout()

        mainPage1 = MainPage();
        comparePage1 = ComparePage();
        rankPage1 = RankPage();

        layoutTab1 = QVBoxLayout();
        layoutTab2 = QVBoxLayout();
        layoutTab3 = QVBoxLayout();
        layoutTab1.addWidget(mainPage1);
        layoutTab2.addWidget(comparePage1);
        layoutTab3.addWidget(rankPage1);

        #Individual tab widgets
        tabMain = QWidget();
        tabCompare = QWidget();
        tabRank = QWidget();
        tabMain.setLayout(layoutTab1);
        tabCompare.setLayout(layoutTab2);
        tabRank.setLayout(layoutTab3);

        #Tab layouts
        mainTabs.addTab(tabMain, "Main"); #set tab1 widget as first tab, tab2 as second tab for mainTabs widget
        mainTabs.addTab(tabCompare, "Compare");
        mainTabs.addTab(tabRank, "Ranking");

        self.setCentralWidget(mainTabs);

        """
        # Top Navigation Buttons
        button_layout = QHBoxLayout()
        self.main_button = QPushButton("View Single Stock")
        self.compare_button = QPushButton("Compare Stocks")
        self.rank_button = QPushButton("Stock Rankings")
        button_layout.addWidget(self.main_button)
        button_layout.addWidget(self.compare_button)
        button_layout.addWidget(self.rank_button)

        self.main_button.setStyleSheet('''
            QPushButton {
                background-color: #997300;             
                color: white;
            }
                                      
        ''')
        self.compare_button.setStyleSheet('''
            QPushButton {
                background-color: #191970;             
                color: white;
            }
                                      
        ''')
        self.rank_button.setStyleSheet('''
            QPushButton {
                background-color: #B87333;             
                color: white;
            }
                                      
        ''')

        # Stacks of Pages
        self.stacked_widget = QStackedWidget()

        # Add the other pages
        self.main_page = MainPage()
        self.compare_page = ComparePage()
        self.rank_page = RankPage()

        self.stacked_widget.addWidget(self.main_page) # index 0
        self.stacked_widget.addWidget(self.compare_page) # index 1
        self.stacked_widget.addWidget(self.rank_page) # index 2

        # add the menu and stacked widget to the main layout
        layout.addLayout(button_layout)
        layout.addWidget(self.stacked_widget)

        # set layout to main window
        self.setLayout(layout)

        # connect buttons to switch pages
        self.main_button.clicked.connect(self.show_main_page)
        self.compare_button.clicked.connect(self.show_compare_page)
        self.rank_button.clicked.connect(self.show_rank_page)
        

    def show_main_page(self):
        '''Switch to the main page'''
        self.stacked_widget.setCurrentIndex(0)

    def show_compare_page(self):
        '''Switch to the compare page'''
        self.stacked_widget.setCurrentIndex(1)
        
    def show_rank_page(self):
        '''Switch to the stocks ranking page'''
        self.stacked_widget.setCurrentIndex(2)
    """

def main():
    
    #pre-load ticker csv to a list
    with open("stockTickerSymbols.csv") as i1:
        tickerSymbolsList = [row.split()[0] for row in i1];
    #print(tickerSymbolsList);

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

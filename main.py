import sys
import PyQt6 as pyqt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QStackedWidget, QScrollArea
from PyQt6.QtGui import QIcon
import pyqtgraph as pg

import yfinance as yf # Yahoo! Finance API to get data on stocks

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


class myApp(QWidget):

    def __init__(self):
        super().__init__()

        # widgets settings
        self.setWindowTitle("Stocks Viewer")
        self.setWindowIcon(QIcon('icons/barcharticon.png'))
        self.resize(1500,850) # width, height

        # Main Layout
        layout = QVBoxLayout()

        # Top Navigation Buttons
        button_layout = QHBoxLayout()
        self.main_button = QPushButton("View Single Stock")
        self.compare_button = QPushButton("Compare Stocks")
        self.rank_button = QPushButton("Stock Rankings")
        button_layout.addWidget(self.main_button)
        button_layout.addWidget(self.compare_button)
        button_layout.addWidget(self.rank_button)

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

if __name__ == "__main__":
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
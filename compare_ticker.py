import sys
import PyQt6 as pyqt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QStackedWidget
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


from sklearn.preprocessing import MinMaxScaler
# import tensorflow as tf
# from tensorflow

class ComparePage(QWidget):
    def __init__(self):
        super().__init__()

        #layouts
        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        label_layout = QHBoxLayout()
        ticker_period_label_layout = QHBoxLayout()

        # dropdown list to select ticker
        self.ticker1_combo = QComboBox()
        ticker1 = self.get_stock_tickers()
        self.ticker1_combo.addItems(ticker1)

        self.ticker2_combo = QComboBox()
        ticker2 = self.get_stock_tickers()
        self.ticker2_combo.addItems(ticker2)

        # dropdown list to select period
        self.period1_combo = QComboBox()
        period1 = self.adjust_period('keys')
        period_values = self.adjust_period('values')
        self.period1_combo.addItems(period1)

        self.period2_combo = QComboBox()
        period2 = self.adjust_period('keys')
        self.period2_combo.addItems(period2)

        self.period_combo = QComboBox()
        period = self.adjust_period('keys')
        period_values = self.adjust_period('values')
        self.period_combo.addItems(period)

        # just a label
        self.label1 = QLabel('Select a stock to view data')
        self.period1_label = QLabel('Select period')

        self.label2 = QLabel('Select a stock to view data')
        self.period2_label = QLabel('Select period')

        # button to plot stock data
        self.plotButton = QPushButton('Plot Stock Data')
        self.plotButton.clicked.connect(self.plot_stock_data)

        # set layout to main window
        self.setLayout(layout)

        # side by side graphs layout
        figure_layout = QHBoxLayout()
        layout.addLayout(figure_layout)

        # layouts for dropdowns and button
        layout.addLayout(horizontal_layout)
        layout.addLayout(label_layout)

        horizontal_layout.addWidget(self.ticker1_combo)
        label_layout.addWidget(self.label1)

        horizontal_layout.addWidget(self.ticker2_combo)
        label_layout.addWidget(self.label2)


        layout.addWidget(self.period_combo)
        layout.addWidget(self.plotButton)

        # layout section to add widgets. (add widgets to QVBoxLayout)
        



    def get_stock_tickers(self):
        # fetch tickers from data source dynamically. currently a predefined list
        return['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
    

    def adjust_period(self, selection):
        period_dict = {'1d' :'1 day', '5d': '5 days', '1mo': '1 month', '3mo': '3 months', '6mo' : '6 months', '1y': '1 year', '2y' : '2 years', '5y' : '5 years', '10y' : '10 years', 'ytd' : 'year-to-date', 'max':'maximum data'}


        if selection == 'keys':
            return list(period_dict.keys())
        elif selection == 'values':
            return list(period_dict.values())
        elif selection == 'all':
            return period_dict

        # return['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']


    def plot_stock_data(self):
        selected_ticker1 = self.ticker1_combo.currentText()
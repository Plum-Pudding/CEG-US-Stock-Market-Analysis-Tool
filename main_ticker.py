import sys
import PyQt6 as pyqt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
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

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        # page layout
        layout = QVBoxLayout()
        dropdown_layout = QHBoxLayout()
        ticker_period_label_layout = QHBoxLayout()

        # dropdown list to select ticker
        self.ticker_combo = QComboBox()
        tickers = self.get_stock_tickers()
        self.ticker_combo.addItems(tickers)

        # dropdown list to select period
        self.period_combo = QComboBox()
        period = self.adjust_period('keys')
        period_values = self.adjust_period('values')
        self.period_combo.addItems(period)

        # just a label
        self.label = QLabel('Select a stock to view data')
        self.period_label = QLabel('Select period')

        # button to plot stock data
        self.plotButton = QPushButton('Plot Stock Data') 

        # matplotlib canvas to display graphs
        self.canvas = FigureCanvas(plt.figure()) 

        # set layout to main window
        self.setLayout(layout)

        # click button to connect to get stock data
        self.plotButton.clicked.connect(self.plot_stock_data)

        # layout section to add widgets. (add widgets to QVBoxLayout)
        layout.addWidget(self.canvas)

        dropdown_layout.addWidget(self.ticker_combo)
        dropdown_layout.addWidget(self.period_combo)
        layout.addLayout(dropdown_layout)

        ticker_period_label_layout.addWidget(self.label)
        ticker_period_label_layout.addWidget(self.period_label)
        layout.addLayout(ticker_period_label_layout)

        layout.addWidget(self.plotButton)


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
        selected_stock = self.ticker_combo.currentText() # pulls the stock selected in the dropdown list
        self.label.setText(f'Stock Selected: {selected_stock}')
        selected_period = self.period_combo.currentText() # pulls the period selected in the dropdown list
        self.period_label.setText(f'Period: {selected_period}')

        # historical data for selected stock. 1mo = 30/31 days, 1y = 1 year, max: from the beginning
        stock = yf.Ticker(selected_stock)
        history = stock.history(period = selected_period)
        
        # creating and plotting of graph
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(history.index, history['Close'], label = 'Close Price')
        ax.set_title(f"{selected_stock} Stock Price in {selected_period}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price")
        ax.legend()
        self.canvas.draw()

    def plot_bargraph_data(self):
        
        pass


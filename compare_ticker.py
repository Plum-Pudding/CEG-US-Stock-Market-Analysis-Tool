import sys
import PyQt6 as pyqt6
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QStackedWidget, QScrollArea, QTableView
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
        self.label2 = QLabel('Select a stock to view data')
        self.period_label = QLabel('Select period')

        # button to plot stock data
        self.plotButton = QPushButton('Plot Stock Data')
        self.plotButton.clicked.connect(self.plot_stock_data)
        self.plotButton.setStyleSheet('''
            QPushButton {
                background-color: #4B0000;             
                color: white;
            }
                                      
        ''')


        self.canvas = FigureCanvas(plt.figure())

        # set layout to main window
        self.setLayout(layout)


        # side by side graphs layout
        self.figure_layout = QHBoxLayout()
        self.figure_layout.addWidget(self.canvas)
        layout.addLayout(self.figure_layout)

        # layouts for dropdowns and button
        layout.addLayout(horizontal_layout)
        layout.addLayout(label_layout)

        horizontal_layout.addWidget(self.ticker1_combo)
        label_layout.addWidget(self.label1)

        horizontal_layout.addWidget(self.ticker2_combo)
        label_layout.addWidget(self.label2)


        layout.addWidget(self.period_combo)

        layout.addWidget(self.period_label)

        layout.addWidget(self.plotButton)
        



    def get_stock_tickers(self):
        # fetch tickers from data source dynamically. currently a predefined list
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA', 'AMD', 'INTC', 'META', 'JPM', 'V', 'JNJ', 'PG', 'KO', 'PFE', 'XOM', 'DIS', 'PEP', 'T', 'NFLX']
        sorted_tickers = sorted(tickers)
        return sorted(sorted_tickers)

    def adjust_period(self, selection):
        period_dict = {'5d': '5 days', '1mo': '1 month', '3mo': '3 months', '6mo' : '6 months', '1y': '1 year', '2y' : '2 years', '5y' : '5 years', '10y' : '10 years', 'ytd' : 'year-to-date', 'max':'maximum data'}


        if selection == 'keys':
            return list(period_dict.keys())
        elif selection == 'values':
            return list(period_dict.values())
        elif selection == 'all':
            return period_dict

        # return['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']


    def plot_stock_data(self):

        selected_period = self.period_combo.currentText()

        # historical data for selected stock. 1mo = 30/31 days, 1y = 1 year, max: from the beginning, 1st graph
        selected_ticker1 = self.ticker1_combo.currentText()
        stock_name1 = yf.Ticker(selected_ticker1)
        stock_info1 = stock_name1.info
        self.label1.setText(f'Stock 1: {selected_ticker1}')
        data1 = stock_name1.history(period = selected_period)

        # Calculate Simple Moving Averages (SMA) for 1st graph
        data1['SMA_10'] = data1['Close'].rolling(window=10).mean()  # 10-day SMA
        data1['SMA_50'] = data1['Close'].rolling(window=50).mean()  # 50-day SMA

        data1['EMA_10'] = data1['Close'].ewm(span=10, adjust=False).mean()  # 10-day EMA

        # historical data for 2nd graph
        selected_ticker2 = self.ticker2_combo.currentText()
        stock_name2 = yf.Ticker(selected_ticker2)
        stock_info2 = stock_name2.info
        self.label2.setText(f'Stock 2: {selected_ticker2}')
        data2 = stock_name2.history(period = selected_period)

        # Calculate Simple Moving Averages (SMA) for 1st graph
        data2['SMA_10'] = data2['Close'].rolling(window=10).mean()  # 10-day SMA
        data2['SMA_50'] = data2['Close'].rolling(window=50).mean()  # 50-day SMA

        # making the period label neater to show full period
        for key, value  in self.adjust_period('all').items(): # to get the graph label to show the period properly
            if selected_period == key:
                period_full = value
        self.period_label.setText(f'{period_full}')

        # Historical data for selected stock
        stock1 = yf.Ticker(selected_ticker1).history(period = selected_period)
        stock2 = yf.Ticker(selected_ticker2).history(period = selected_period)

        # creating 2 plots for stock data
        self.clear_existing_charts()
        # self.canvas.figure.clear()
        # fig1, ax1 = plt.subplots()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        ax1.plot(stock1.index, stock1['Close'], label =f'{selected_ticker1} Close Price')
        ax1.plot(data1.index, data1['SMA_10'], label='10-Day SMA', color='red')
        ax1.plot(data1.index, data1['SMA_50'], label='50-Day SMA', color='green')
        # ax.plot(data.index, data['EMA_10'], label='10-Day EMA', color= 'yellow')
        ax1.set_title(f'{stock_info1.get('longName')} Stock Price in {period_full}')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Close Price')
        ax1.legend()
        
        # fig2, ax2 = plt.subplots()
        ax2.plot(stock2.index, stock2['Close'], label = f'{selected_ticker2} Close Price')
        ax2.plot(data2.index, data2['SMA_10'], label='10-Day SMA', color='red')
        ax2.plot(data2.index, data2['SMA_50'], label='50-Day SMA', color='green')
        # ax.plot(data.index, data['EMA_10'], label='10-Day EMA', color= 'yellow')
        ax2.set_title(f'{stock_info2.get('longName')} Stock Price in {period_full}')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Close Price')
        ax2.legend()

        # Plotting 2 graphs
        # canvas1 = FigureCanvas(fig1)
        # canvas2 = FigureCanvas(fig2)
        canvas = FigureCanvas(fig)
        self.figure_layout.addWidget(canvas)
        # self.figure_layout.addWidget(canvas1)
        # self.figure_layout.addWidget(canvas2)

        self.layout().update()
        # self.canvas.draw()

    def clear_existing_charts(self):
        """Clear any existing charts before displaying new ones."""
        while self.figure_layout.count():
            child = self.figure_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
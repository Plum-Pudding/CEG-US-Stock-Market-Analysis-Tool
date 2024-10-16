import sys
import csv

import PyQt6 as pyqt6
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QScrollArea, QTableView
from PyQt6.QtGui import QIcon
import pyqtgraph as pg

import yfinance as yf # Yahoo! Finance API to get data on stocks
import mplfinance as mpf # for candlesticks graph purposes

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas # for matplotlib to work with PyQt6
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import numpy as np
import pandas as pd
import pandas_datareader as web
import datetime as dt

#from main import main

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        # page layout
        layout = QVBoxLayout()
        dropdown_layout = QHBoxLayout()
        ticker_period_label_layout = QHBoxLayout()
        evaluation_layout = QVBoxLayout()
        summary_layout = QVBoxLayout()

        # dropdown list to select ticker
        self.ticker_combo = QComboBox()
        tickers = self.get_stock_tickers()
        self.ticker_combo.addItems(tickers)

        # dropdown list to select period
        self.period_combo = QComboBox()
        period = self.adjust_period('keys')
        self.period_combo.addItems(period)

        # dropdown menu for graph type
        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems(['Line Graph', 'Candlestick'])

        # just a label
        self.label = QLabel('SELECT A STOCK TO VIEW DATA')
        self.period_label = QLabel('SELECT PERIOD')

        # evaluation label config
        self.eval_label = QLabel()
        self.eval_label.setWordWrap(True)
        self.eval_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eval_label.setMaximumWidth(1500)
        self.eval_label.setStyleSheet('''
            padding: 10px;
            font-family: verdana;
            font-weight: bold;                  
        ''')

        # Indicator Buttons
        button_layout = QHBoxLayout()
        self.sma_button = QPushButton('SMA')
        self.sma_button.setStyleSheet('''
            QPushButton {
                background-color: #086900;             
                color: white;
            }
                                      
        ''')
        self.sma_200_button = QPushButton('SMA (100 days and 200 days)')
        self.sma_200_button.setStyleSheet('''
            QPushButton {
                background-color: #330066;             
                color: white;
            }
                                      
        ''')
        self.rsi_button = QPushButton('RSI')
        self.rsi_button.setStyleSheet('''
            QPushButton {
                background-color: #b36b00;             
                color: white;
            }
                                      
        ''')
        self.bollinger_button = QPushButton('Bollinger Bands')

        # summary label config
        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.summary_label.setMaximumWidth(1500)
        self.summary_label.setStyleSheet("padding: 10px;")

        # button to plot stock data
        self.plotButton = QPushButton('Plot Stock Data')
        self.plotButton.setStyleSheet('''
            QPushButton {
                background-color: #4B0000;             
                color: white;
            }
                                      
        ''')

        # matplotlib canvas to display graphs
        self.canvas = FigureCanvas(plt.figure()) 

        # set layout to main window
        self.setLayout(layout)

        # Indicator buttons to connect to their functions
        self.sma_button.clicked.connect(self.toggle_sma)
        self.sma_200_button.clicked.connect(self.toggle_sma_200)
        self.rsi_button.clicked.connect(self.toggle_rsi)
        self.bollinger_button.clicked.connect(self.toggle_bollinger_bands)

        # click button to connect to get stock data
        self.plotButton.clicked.connect(self.plot_stock_data)

        # flags for showing indicators
        self.show_sma = False
        self.show_sma_200 = False
        self.show_rsi = False
        self.show_bollinger = False

        ''' layout section to add widgets. (add widgets to QVBoxLayout and make them appear) '''
        # graph layout
        layout.addWidget(self.canvas)

        layout.addWidget(self.graph_type_combo)

        # Indicator buttons
        button_layout.addWidget(self.sma_button)
        button_layout.addWidget(self.sma_200_button)
        button_layout.addWidget(self.rsi_button)
        button_layout.addWidget(self.bollinger_button)

        layout.addLayout(button_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # layout for dropdown ticker menu
        dropdown_layout.addWidget(self.ticker_combo)
        dropdown_layout.addWidget(self.period_combo)
        scroll_layout.addLayout(dropdown_layout)

        # layout for dropdown period menu
        ticker_period_label_layout.addWidget(self.label)
        ticker_period_label_layout.addWidget(self.period_label)
        scroll_layout.addLayout(ticker_period_label_layout)

        # plot button layout
        scroll_layout.addWidget(self.plotButton)
    
        # evaluation section
        self.setLayout(evaluation_layout)
        evaluation_layout.addWidget(self.eval_label)
        scroll_layout.addLayout(evaluation_layout)

        # summary section
        self.setLayout(summary_layout)
        summary_layout.addWidget(self.summary_label)
        scroll_layout.addLayout(summary_layout)
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        # scroll_area.setWidget(self.summary_label)

    def get_stock_tickers(self):
        # fetch tickers from data source dynamically. currently a predefined list
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA', 'AMD', 'INTC', 'META', 'JPM', 'V', 'JNJ', 'PG', 'KO', 'PFE', 'XOM', 'DIS', 'PEP', 'T', 'NFLX']
        sorted_tickers = sorted(tickers)
        return sorted(sorted_tickers)
    
    def isValidTickerSymbol(givenSymbol):
        #Check if stock ticker symbol is a real one
        #if givenSymbol in 
            
        pass;
    
    def adjust_period(self, selection): # to showcase the period properly in full form
        # get the time period of stock performance over the days/months/years
        period_dict = {'5d': '5 days', '1mo': '1 month', '3mo': '3 months', '6mo' : '6 months', '1y': '1 year', '2y' : '2 years', '5y' : '5 years', '10y' : '10 years', 'ytd' : 'year-to-date', 'max':'maximum data'}

        if selection == 'keys':
            return list(period_dict.keys())
        elif selection == 'values':
            return list(period_dict.values())
        elif selection == 'all':
            return period_dict
        
    ''' ============ INDICATORS FUNCTIONS ============'''

    def toggle_sma(self):
        self.show_sma = not self.show_sma
        self.plot_stock_data()

    def toggle_sma_200(self):
        self.show_sma_200 = not self.show_sma_200
        self.plot_stock_data()
    
    def toggle_rsi(self):
        self.show_rsi = not self.show_rsi
        self.plot_stock_data()

    def toggle_bollinger_bands(self):
        self.show_bollinger = not self.show_bollinger
        self.plot_stock_data()


    ''' ============ GRAPH PLOTTING CODES ============'''

    def plot_stock_data(self):

        # GET SELECTED STOCKS AND PERIOD
        selected_stock = self.ticker_combo.currentText() # pulls the stock selected in the dropdown list
        stock = yf.Ticker(selected_stock)
        stock_info = stock.info
        self.label.setText(f'Stock Selected: {selected_stock}') # callback to yf Ticker info to get longname to display proper name instead of Ticker symbol
        selected_period = self.period_combo.currentText() # pulls the period selected in the dropdown list
        for key, value  in self.adjust_period('all').items(): # to get the graph label to show the period properly
            if selected_period == key:
                period_full = value
        self.period_label.setText(f'Period: {period_full}')

        # historical data for selected stock. 1mo = 30/31 days, 1y = 1 year, max: from the beginning
        history = stock.history(period = selected_period)
        data = stock.history(period = selected_period) # for SMA

        # Calculate EMA
        data['EMA_10'] = data['Close'].ewm(span=10, adjust=False).mean()  # 10-day EMA
        
        # creating and plotting of graph
        self.canvas.figure.clear() # clear any existing graph in case
        # ax = self.canvas.figure.add_subplot(111)

        # check whether RSi is showing as RSI is indicated below the main graph, thus expanding the canvas is needed
        if self.show_rsi:
            ax, ax2 = self.canvas.figure.subplots(2, sharex=True, gridspec_kw={'height_ratios': [3,1]})
        else:
            ax = self.canvas.figure.add_subplot(111)


        # Determine type of graph selected
        selected_graph_type = self.graph_type_combo.currentText()

        if selected_graph_type == 'Line Graph':
            # Plot Line Graph
            ax.plot(history.index, history['Close'], label = 'Close Price', color='blue')
            # ax.plot(data.index, data['EMA_10'], label='10-Day EMA', color= 'yellow')
            ax.set_title(f'{stock_info.get("longName")} ({selected_stock}) Stock Price in {period_full}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Close Price')
            ax.legend(loc = 'upper left')

        elif selected_graph_type == 'Candlestick':
            # Plot candlestick
            mpf.plot(history, type='candle', ax=ax, style='yahoo')
            ax.set_title(f'{stock_info.get("longName")} ({selected_stock}) Stock Price in {period_full}')
            
        # ADD SMA (SIMPLE MOVING AVERAGE) IF SELECTED
        if self.show_sma:
            # Calculate Simple Moving Averages (SMA)
            data['SMA_10'] = data['Close'].rolling(window=10).mean()  # 10-day SMA
            data['SMA_50'] = data['Close'].rolling(window=50).mean()  # 50-day SMA
            ax.plot(data.index, data['SMA_10'], label='10-Day SMA', color='red')
            ax.plot(data.index, data['SMA_50'], label='50-Day SMA', color='green')
            ax.legend(loc='upper left')

        # ADD SMA FOR 100 - 200 DAYS IF SELECTED
        if self.show_sma_200:
            # Calculate Simple Moving Averages (SMA)
            data['SMA_100'] = data['Close'].rolling(window=100).mean()  # 100-day SMA
            data['SMA_200'] = data['Close'].rolling(window=200).mean()  # 200-day SMA
            ax.plot(data.index, data['SMA_100'], label='100-Day SMA', color='orange')
            ax.plot(data.index, data['SMA_200'], label='200-Day SMA', color='purple')
            ax.legend(loc='upper left')
        
        # ADD RSI (RELATIVE STRENGTH INDEX) IF SELECTED
        if self.show_rsi:
            # Calculate Relative Strength Index (RSI)
            delta = history['Close'].diff(1)
            delta.dropna(inplace=True) # drop the "not a number" values

            postive = delta.copy()
            negative = delta.copy()

            postive[postive < 0] = 0
            negative[negative > 0] = 0

            # RSI is calculated over a 14-day period
            days = 14

            # Relative Strength Calculation
            avg_gain = postive.rolling(window=days).mean()
            avg_loss = abs(negative.rolling(window=days).mean()) # absolute value as we need a positive value when knowing the absolute difference

            relative_strength = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + relative_strength))
            rsi = rsi.dropna()
            history_rsi = history.loc[rsi.index]

            # ax2 = ax.twinx()
            ax2.plot(history_rsi.index, rsi, label='RSI', color='orange')
            ax2.axhline(70, color='red', linestyle='--') # "financial experts" claimed that between 70 and 30 is important. 30 oversold, 70 overbought.
            ax2.axhline(30, color='green', linestyle='--')
            ax2.set_ylim(0,100)
            ax2.set_ylabel('RSI')
            ax2.legend()


        if self.show_bollinger:
            data['SMA'] = data['Close'].rolling(window=20).mean() # Simple Moving Average (20 days)
            # 20 period standard deviation
            data['SD'] = data['Close'].rolling(window=20).std() # standard deviation

            data['UB'] = data['SMA'] + (2 * data['SD']) # upper band = simple moving average + (2 * standard deviation)
            data['LB'] = data['SMA'] - (2 * data['SD']) # lower band = simple moving average - (2 * standard deviation)
            data = data.dropna()

            ax.plot(data.index, data['UB'], label='Upper Bollinger Band', color='red')
            ax.plot(data.index, data['LB'], label='Lower Bollinger Band', color='green')
            ax.fill_between(data.index, data['UB'], data['LB'], color='lightgray')
            ax.plot(data.index, data['SMA'], label='Middle Bollinger Band', color='orange')

            ax.legend(loc='upper left')


        self.canvas.draw()

        # display buy evaluation
        buy_evaluation = self.evaluate_stock_buy_quality(selected_stock)
        # self.label.setText(buy_evaluation)
        self.eval_label.setText(f'{buy_evaluation}')

        # display stock information
        stock_summary = stock_info.get('longBusinessSummary')
        self.summary_label.setText(f'Company summary:\n{stock_summary}')


    def plot_bargraph_data(self):
        
        pass

    def evaluate_stock_buy_quality(self, ticker):
        # Fetch stock information
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        # Criteria for stock to be "good buy"
        pe_ratio = stock_info.get('forwardPE', None)
        fifty_two_week_low = stock_info.get('fiftyTwoWeekLow', None)
        fifty_two_week_high = stock_info.get('fiftyTwoWeekHigh', None)
        current_price = stock_info.get('currentPrice', None)
        recommendations = stock.recommendations

        # Check if PE ratio is low
        if pe_ratio and pe_ratio < 15:
            buy_message = f"{ticker} has a low PE ratio ({pe_ratio}), potential good buy."
        else:
            buy_message = f"{ticker} has a high PE ratio ({pe_ratio}), be cautious."

        # Check if the stock is near its 52-week low
        if current_price and fifty_two_week_low and (current_price < fifty_two_week_low * 1.05):
            buy_message += f"\n{ticker} is trading close to its 52-week low. This might be a good buying opportunity."

        # Include analyst recommendations (if available)
        if recommendations is not None:
            recent_rec = recommendations.tail(1).iloc[0]
            buys = recent_rec['strongBuy'] + recent_rec['buy']
            sells = recent_rec['strongSell'] + recent_rec['sell']
            if buys == 0 or sells == 0:
                buys_ratioed = buys
                sells_ratioed = sells
            elif buys % sells == 0:
                buys_ratioed = buys / sells
                sells_ratioed = sells / sells
            else:
                buys_ratioed = buys
                sells_ratioed = sells
          
            buy_message += f"\nLatest analyst recommendation on buys to sells ratio: {int(buys_ratioed)}:{int(sells_ratioed)} with {recent_rec['hold']} analysts on hold."

        return buy_message


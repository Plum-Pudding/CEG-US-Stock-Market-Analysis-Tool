import sys
import PyQt6 as pyqt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QScrollArea
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

from main_ticker import MainPage

class RankPage(QWidget):
    def __init__(self):
        super().__init__()

        # page layout
        layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        #pre-load ticker csv to a list
        with open("stockTickerSymbols.csv") as i1:
            tickerSymbolsList = [row.split()[0] for row in i1];
        #print(tickerSymbolsList);


    def get_stock_tickers(self):
        # fetch tickers from data source dynamically. currently a predefined list
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA', 'AMD', 'INTC', 'META', 'JPM', 'V', 'JNJ', 'PG', 'KO', 'PFE', 'XOM', 'DIS', 'PEP', 'T', 'NFLX']
        sorted_tickers = sorted(tickers)
        return sorted(sorted_tickers)

    def isValidTickerSymbol(givenSymbol): #Check is given string is in stockTickerSymbols.csv i.e. is a real stock

        

        return (True);

    def plot_bar_graph(self):
        
        for ticker in self.get_stock_tickers():
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            hist = stock.history(period = '10y')
            pe_ratio = stock.info.get('forwardPE')

            
    


        
        

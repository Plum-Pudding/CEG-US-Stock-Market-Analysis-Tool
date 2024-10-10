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
        
        # tickers = MainPage.get_stock_tickers()
        
        

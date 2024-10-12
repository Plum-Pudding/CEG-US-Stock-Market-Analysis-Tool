import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QScrollArea, QTableView
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas # for matplotlib to work with PyQt6
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from train_page import train_model_with_filtered_data # import training logic

class PredictionPage(QWidget):
    def __init__(self):
        super().__init__()
            
        # page layout
        layout = QVBoxLayout()
        dropdown_layout = QHBoxLayout()

        # dropdown list to select ticker
        self.ticker_combo = QComboBox()
        tickers = self.get_stock_tickers()
        self.ticker_combo.addItems(tickers)
        
        # dropdown list to select period
        self.period_combo = QComboBox()
        period = self.adjust_period('keys')
        self.period_combo.addItems(period)

        # matplotlib canvas to display graphs
        self.canvas = FigureCanvas(plt.figure()) 

        # set layout to main window
        self.setLayout(layout)

        # button to plot stock data
        self.plotButton = QPushButton('Plot Stock Data')
        self.plotButton.setStyleSheet('''
            QPushButton {
                background-color: #4B0000;             
                color: white;
            }
                                      
        ''')
        # click button to connect to get stock data
        self.plotButton.clicked.connect(self.plot_stock_data)


        ''' layout section to add widgets. (add widgets to QVBoxLayout and make them appear) '''
        # graph layout
        layout.addWidget(self.canvas)

        # layout for dropdown ticker menu
        dropdown_layout.addWidget(self.ticker_combo)
        dropdown_layout.addWidget(self.period_combo)
        layout.addLayout(dropdown_layout)

        # layout for dropdown period menu
        # ticker_period_label_layout.addWidget(self.label)
        # ticker_period_label_layout.addWidget(self.period_label)
        # layout.addLayout(ticker_period_label_layout)

        # plot button layout
        layout.addWidget(self.plotButton)



    def get_stock_tickers(self):
        # fetch tickers from data source dynamically. currently a predefined list
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA', 'AMD', 'INTC', 'META', 'JPM', 'V', 'JNJ', 'PG', 'KO', 'PFE', 'XOM', 'DIS', 'PEP', 'T', 'NFLX']
        sorted_tickers = sorted(tickers)
        return sorted(sorted_tickers)
    
    def adjust_period(self, selection): # to showcase the period properly in full form
        # get the time period of stock performance over the days/months/years
        period_dict = {'5d': '5 days', '1mo': '1 month', '3mo': '3 months', '6mo' : '6 months', '1y': '1 year', '2y' : '2 years', '5y' : '5 years', '10y' : '10 years', 'ytd' : 'year-to-date', 'max':'maximum data'}

        if selection == 'keys':
            return list(period_dict.keys())
        elif selection == 'values':
            return list(period_dict.values())
        elif selection == 'all':
            return period_dict
    
    def plot_stock_data(self):
        selected_ticker = self.ticker_combo.currentText()
        selected_period = self.period_combo.currentText()

        # determine start and end year based on selected period
        current_year = pd.Timestamp.now().year
        if selected_period == '1y':
            start_year, end_year = current_year - 1, current_year
        elif selected_period == '2y':
            start_year, end_year = current_year - 2, current_year
        else:
            start_year, end_year = current_year - 10, current_year




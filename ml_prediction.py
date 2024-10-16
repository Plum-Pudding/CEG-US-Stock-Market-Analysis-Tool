import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QScrollArea, QTableView
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas # for matplotlib to work with PyQt6
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import tensorflow
from keras.api.models import Sequential
from keras.api.layers import Dense, Dropout, LSTM

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
        period_dict = {'1y': '1 year', '2y' : '2 years', '5y' : '5 years', '10y' : '10 years'}

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
        elif selected_period == '5y':
            start_year, end_year = current_year -5, current_year
        else:
            start_year, end_year = current_year - 10, current_year

        # Train model and get predictions (using train_page.py logic)
        model, X_test, y_test, predictions = train_model_with_filtered_data(selected_ticker, start_year, end_year)

        # plot the actual vs predicted graphs side by side
        self.plot_side_by_side(selected_ticker, X_test.index, y_test, predictions)
    
    def plot_side_by_side(self, ticker, dates, actual_prices, predicted_prices):

        dates = pd.to_datetime(dates)

        # Clear existing graphs (in case)
        self.canvas.figure.clear()

        fig = Figure(figsize=(13, 7))
        self.canvas.figure = fig
        # Create subplots for side-by-side comparison
        ax1, ax2 = fig.subplots(1, 2)

        # fig, (ax1, ax2) = plt.subplots(1,2, figsize=(13,7), sharey=True)

        # plot actual prices on the left
        ax1.plot(dates, actual_prices, label='Actual Price', color='blue')
        ax1.set_title(f'{ticker} - Actual Prices')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')
        ax1.legend()

        # plot predicted prices on the right
        ax2.plot(dates, predicted_prices, label='Predicted Price', color='red')
        ax2.set_title(f'{ticker} - Predicted Prices')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Price')
        ax2.legend()

        self.canvas.draw()

    




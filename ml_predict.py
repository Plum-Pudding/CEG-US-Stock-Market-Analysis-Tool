import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QScrollArea, QTableView
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas # for matplotlib to work with PyQt6
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import tensorflow
from keras.api.models import Sequential, load_model, Model
from keras.api.layers import Dense, Dropout, LSTM

from training_page import train_model, load_data # import training logic

class PredictPage(QWidget):
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
    

    def adjust_period(self, selection):
        period_dict = {'1y': '1 year', '2y' : '2 years', '5y' : '5 years', '10y' : '10 years'}


        if selection == 'keys':
            return list(period_dict.keys())
        elif selection == 'values':
            return list(period_dict.values())
        elif selection == 'all':
            return period_dict
        

    def plot_stock_data(self):
        # selects ticker name and period selected from the dropdown box
        selected_ticker = self.ticker_combo.currentText()
        selected_period = self.period_combo.currentText()

        #  load historical data and the trained model
        df = pd.read_csv(f'{selected_ticker}_10y_history.csv')

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


        # convert the index to datetimeindex and remove timezone info if present
        df['Date'] = pd.to_datetime(df['Date'], utc=True)

        
        filtered_data = df[(df['Date'] >= f'{start_year}-01-01') & (df['Date'] <= f'{end_year}-12-31')]


        # initiialize training of model and write a model (keras file) of the prediction written in the file ({ticker}_model.keras)
        train_model(selected_ticker)

        # Load model and make predictions
        model = load_model(f'{selected_ticker}_model.keras') 


        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(filtered_data['Close'].values.reshape(-1,1))


        # Testing the model
        X_test = []
        for i in range(60, len(scaled_data)):
            X_test.append(scaled_data[i-60:i, 0])

        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))  # reshape for LSTM

        predictions = model.predict(X_test)
        predictions = scaler.inverse_transform(predictions) # rescale predictions

        # Plot actual vs predicted prices
        self.canvas.figure.clear()

        ax = self.canvas.figure.add_subplot(111)

        ax.plot(filtered_data['Date'], filtered_data['Close'], label='Actual Price', color='black')
        ax.plot(filtered_data['Date'][60:], predictions, label = 'Predicted Price', color='green')
        ax.set_title(f'{selected_ticker} Share Price')
        ax.set_xlabel('Date')
        ax.set_ylabel(f'{selected_ticker} Price')
        ax.legend()

        self.canvas.draw()



import sys
import PyQt6 as pyqt6
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QStackedWidget,QMainWindow,QApplication
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

# Create a custom class for the Qt window
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set the title of the window
        self.setWindowTitle("Analyst Recommendations Pie Chart")
        
        # Create a widget to hold the plot and the dropdown
        widget = QWidget()
        self.setCentralWidget(widget)
        
        # Create a layout and add the canvas (plot)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Create a dropdown menu to select companies
        self.dropdown = QComboBox(self)
        layout.addWidget(self.dropdown)
        
        # Call the method that loads the companies in the dropdown
        self.load_companies()

        # Create a canvas for the pie chart
        self.canvas = FigureCanvas(plt.Figure(figsize=(7, 7)))
        layout.addWidget(self.canvas)
        
        # Connect the dropdown menu selection to the plot update
        self.dropdown.currentTextChanged.connect(self.update_chart)
        
        # Initialize the plot
        self.plot_chart(self.dropdown.currentText())

    def load_companies(self):
        # List of stock tickers
        self.tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        
        # Add companies to the dropdown
        self.dropdown.addItems(self.tickers)
    
    def update_chart(self, company):
        # When a company is selected from the dropdown, update the pie chart
        self.plot_chart(company)

    def plot_chart(self, ticker):
        # Clear the current plot
        self.canvas.figure.clear()

        # Download the analyst recommendations for the selected company
        data = yf.Ticker(ticker)

        # Count recommendations for Buy, Sell, Hold (simplified for illustration)
        recommendations_count = {
            'Buy': 0,
            'Sell': 0,
            'Hold': 0,
            'Strong Buy': 0,
            'Strong Sell': 0,
        }
        
        try:
            # Get the last 10 recommendations
            recommendations = data.recommendations.tail(10)
            for rec in recommendations['To Grade']:
                if rec in recommendations_count:
                    recommendations_count[rec] += 1
                else:
                    recommendations_count['Hold'] += 1  # Default to Hold if no exact match
        except:
            recommendations_count['Hold'] += 1  # If no recommendation data, default to Hold

        # Focus on Buy, Hold, and Sell recommendations only for simplicity
        buy_sell_data = {
            'Buy': recommendations_count['Buy'] + recommendations_count['Strong Buy'],
            'Sell': recommendations_count['Sell'] + recommendations_count['Strong Sell'],
            'Hold': recommendations_count['Hold'],
        }

        print(buy_sell_data)
        # Labels and sizes for the pie chart
        labels = list(buy_sell_data.keys())
        sizes = list(buy_sell_data.values())

        # Plotting the pie chart with labeldistance adjustment
        ax = self.canvas.figure.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, labeldistance=1.1)
        ax.set_title(f'Latest Analyst Recommendations for {ticker}')
        ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.

        # Adjust layout to prevent text cutoff
        self.canvas.figure.tight_layout()

        # Redraw the canvas to show the plot
        self.canvas.draw()


# Main part of the code to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create an instance of the MyWindow class
    window = MyWindow()
    window.show()
    
    # Execute the Qt application
    sys.exit(app.exec())

def plot_chart(self, ticker):
    # Clear the current plot
    self.canvas.figure.clear()

    # Download the analyst recommendations for the selected company
    data = yf.Ticker(ticker)

    # Count recommendations for Buy, Sell, Hold (expanded categories)
    recommendations_count = {
        'Buy': 0,
        'Sell': 0,
        'Hold': 0,
        'Strong Buy': 0,
        'Strong Sell': 0,
        'Outperform': 0,  # Additional categories
        'Underperform': 0
    }
    
    try:
        # Get the last 50 recommendations to ensure better data representation
        recommendations = data.recommendations.tail(50)
        print(recommendations)  # Add this line to debug and check what data is returned
        for rec in recommendations['To Grade']:
            if rec in recommendations_count:
                recommendations_count[rec] += 1
            else:
                recommendations_count['Hold'] += 1  # Default to Hold if no exact match
    except:
        recommendations_count['Hold'] += 1  # If no recommendation data, default to Hold

    # Combine relevant categories into Buy, Sell, Hold
    buy_sell_data = {
        'Buy': recommendations_count['Buy'] + recommendations_count['Strong Buy'] + recommendations_count['Outperform'],
        'Sell': recommendations_count['Sell'] + recommendations_count['Strong Sell'] + recommendations_count['Underperform'],
        'Hold': recommendations_count['Hold'],
    }

    # Check if data is available
    if sum(buy_sell_data.values()) == 0:
        buy_sell_data = {'No Data': 1}  # Display "No Data" if no recommendations are found

    # Labels and sizes for the pie chart
    labels = list(buy_sell_data.keys())
    sizes = list(buy_sell_data.values())

    # Plotting the pie chart with labeldistance adjustment
    ax = self.canvas.figure.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, labeldistance=1.1)
    ax.set_title(f'Latest Analyst Recommendations for {ticker}')
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.

    # Adjust layout to prevent text cutoff
    self.canvas.figure.tight_layout()

    # Redraw the canvas to show the plot
    self.canvas.draw()
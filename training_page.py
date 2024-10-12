import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import tensorflow
from keras.api.models import Sequential, Model, load_model
from keras.api.layers import Dense, Dropout, LSTM

import os


def load_data(ticker):

    df = pd.read_csv(f'{ticker}_10y_history.csv', index_col='Date', parse_dates=True) # reads the csv files according to the tickers

    df.index = pd.to_datetime(df.index, utc=True).tz_localize(None) # convert date to date format

    df['SMA'] = df['Close'].rolling(window=50).mean() # simple moving average in period of 50 days

    # scaling data for LSTM (Long short-term memory)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1,1))

    # Create training and testing data sets in 80/20 split
    train_size = int(len(scaled_data) * 0.8)
    train_data = scaled_data[:train_size]
    test_data = scaled_data[train_size:]

    return train_data, test_data, scaler

# Build LSTM model
def build_lstm_model():
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(60,1))) # past 60 days stock prices, and 1 feature (closing price of the stock)
    model.add(Dropout(0.2))

    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50))
    model.add(Dropout(0.2))

    model.add(Dense(1)) #  prediction of the next closing price

    model.compile(optimizer='adam', loss='mean_squared_error') 
    return model

# train model
def train_model(ticker):
    train_data, test_data, scaler = load_data(ticker)
    # Prepare data for LSTM (create sequence of 60 days)
    X_train = []
    y_train = []
    for i in range(60, len(train_data)):
        X_train.append(train_data[i-60 : i,0])
        y_train.append(train_data[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1],1)) # reshape for LSTM

    # Train LSTM model
    model = build_lstm_model()
    model.fit(X_train, y_train, epochs=5, batch_size=32)

    # Testing the model
    X_test = []
    y_test = test_data[60:, 0]
    for i in range(60, len(test_data)):
        X_test.append(test_data[i-60:i, 0])

    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))  # reshape for LSTM

    # Predict on test data
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)  # reverse scaling to get original values

    model.save(f"{ticker}_model.keras")
    print(f'Model for {ticker} saved as {ticker}_model.keras')
        

    return model, scaler

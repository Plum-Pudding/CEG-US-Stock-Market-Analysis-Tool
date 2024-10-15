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

    df['SMA'] = df['Close'].rolling(window=50).mean() # creates a new column for simple moving average in period of 50 days on closing prices

    # scaling data for LSTM (Long short-term memory)
    scaler = MinMaxScaler(feature_range=(0,1)) # transforms the closing prices into values between 0 and 1 which helps the LSTMs perform better
    scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1,1)) # reshapes closing prices into 2D array as required by the scaler and LSTM

    # Splitting the training and testing data sets in 80/20 split
    train_size = int(len(scaled_data) * 0.8)
    train_data = scaled_data[:train_size] # 80%
    test_data = scaled_data[train_size:] # 20%

    return train_data, test_data, scaler

# Build LSTM model
def build_lstm_model():
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(60,1))) # uses 50 units (neurons) and takes input sequences of shape (60 time steps, 1 feature) -> 60 days, closing price
    model.add(Dropout(0.2)) # randomly setting 20% of the neurons to zero during each update to the model

    model.add(LSTM(units=50, return_sequences=True)) # another layer
    model.add(Dropout(0.2))

    model.add(LSTM(units=50)) # and another
    model.add(Dropout(0.2))

    model.add(Dense(1)) # final layer that outputs the prediction of the next closing price

    model.compile(optimizer='adam', loss='mean_squared_error') # specifies how the model should be optimized and the loss function used (mean squared error)
    return model

# train model
def train_model(ticker):
    train_data, test_data, scaler = load_data(ticker)
    # Prepare data for LSTM (create sequence of 60 days)
    X_train = [] # stores the input features. for each day i, it appends the previous 60 days
    y_train = [] # stores the corresponding output (closing price of the ith day)
    for i in range(60, len(train_data)): 
        X_train.append(train_data[i-60 : i,0])
        y_train.append(train_data[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train) # converts the list to numPy arrays
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1],1)) # reshapes the data to fit the LSTM expected input format (nuimber of samples, time steps, features)

    # Train LSTM model
    model = build_lstm_model()
    model.fit(X_train, y_train, epochs=5, batch_size=32) # trains the LSTM model using the training data (X_train, y_train). epoch = one full cycle through the training dataset, batch size = number of training samples used in one iteration

    # once training is complete, the trained model is saved as a .keras file named according to the ticker
    model.save(f"{ticker}_model.keras")
    print(f'Model for {ticker} saved as {ticker}_model.keras')
        

    return model, scaler

import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import tensorflow
from keras.api.models import Sequential
from keras.api.layers import Dense, Dropout, LSTM


def load_and_filter_data(ticker, start_year, end_year):
    # Load the 10 year data from csv
    data = pd.read_csv(f'{ticker}_10y_history.csv', index_col='Date', parse_dates=True)

    # Convert the index to DateTimeIndex and remove timezone info if present
    data.index = pd.to_datetime(data.index, utc=True).tz_localize(None)

    # Filter the data to include only the specified years
    filtered_data = data[(data.index.year >= start_year) & (data.index.year <= end_year)]

    # Indicator features (Simple Moving Average, Volatility)
    filtered_data.loc[:, 'SMA_10'] = filtered_data['Close'].rolling(window=10).mean() # add 10 day sma
    filtered_data.loc[:, 'SMA_50'] = filtered_data['Close'].rolling(window=50).mean() # add 50 day sma
    filtered_data.loc[:, 'Volatility'] = filtered_data['Close'].rolling(window=10).std() # add rolling standard deviation
    filtered_data.loc[:, 'RSI'] = calculate_rsi(filtered_data) # add rsi
    filtered_data.loc[:, 'Upper_BB'], filtered_data.loc[:, 'Lower_BB'] = calculate_bollinger_bands(filtered_data) # add bollinger bands

    # Create the target variable (next day's price)
    filtered_data.loc[:, 'Target'] = filtered_data.loc[:, 'Close'].shift(-1)

    filtered_data.dropna(inplace=True)

    return filtered_data


# RSI calculation 
def calculate_rsi(data):

    # Calculate Relative Strength Index (RSI)
    delta = data['Close'].diff(1)
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
    # rsi = data.loc[rsi.index]
    return rsi

# Bollinger Bands Calculation
def calculate_bollinger_bands(data):

    # Simple Moving Average (20 days)
    data.loc[:, 'SMA_20'] = data['Close'].rolling(window=20).mean()
    # 20 period standard deviation
    data.loc[:, 'SD_20'] = data['Close'].rolling(window=20).std() # standard deviation

    upper_band = data.loc[:, 'UB'] = data.loc[:, 'SMA_20'] + (2 * data.loc[:, 'SD_20']) # upper band = simple moving average + (2 * standard deviation)
    lower_band = data.loc[:, 'LB'] = data.loc[:, 'SMA_20'] - (2 * data.loc[:, 'SD_20']) # lower band = simple moving average - (2 * standard deviation)
    # bollinger_bands = data.dropna()
    return upper_band, lower_band

# Train the model

def train_model_with_filtered_data(ticker, start_year, end_year):
    # Load the data
    data = load_and_filter_data(ticker, start_year, end_year)

    # select features for training (indicators above)
    X = data[['SMA_10', 'SMA_50', 'Volatility', 'RSI', 'Upper_BB', 'Lower_BB']]
    y = data['Target']

    # split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the Random Forest Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate the Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse: 4f}')

    return model, X_test, y_test, predictions
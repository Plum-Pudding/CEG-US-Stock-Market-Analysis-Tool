import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def load_and_filter_data(ticker, start_year, end_year):
    # Load the 10 year data from csv
    data = pd.read_csv(f'{ticker}_10y_history.csv', index_col='Date', parse_dates=True)

    # Filter the data to include only the specified years
    filtered_data = data[(data.index.year >= start_year) & (data.index.year <= end_year)]

    # Indicator features (Simple Moving Average, Volatility)
    filtered_data['SMA_10'] = filtered_data['Close'].rolling(window=10).mean() # add 10 day sma
    filtered_data['SMA_50'] = filtered_data['Close'].rolling(window=50).mean() # add 50 day sma
    filtered_data['Volatility'] = filtered_data['Close'].rolling(window=10).std() # add rolling standard deviation
    filtered_data = calculate_rsi(data) # add rsi
    filtered_data = calculate_bollinger_bands(data) # add bollinger bands

    # Create the target variable (next day's price)
    filtered_data['Target'] = filtered_data['Close'].shift(-1)

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
    data['RSI'] = data.loc[rsi.index]
    return data

# Bollinger Bands Calculation
def calculate_bollinger_bands(data):

    # Simple Moving Average (20 days)
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    # 20 period standard deviation
    data['SD_20'] = data['Close'].rolling(window=20).std() # standard deviation

    data['UB'] = data['SMA_20'] + (2 * data['SD_20']) # upper band = simple moving average + (2 * standard deviation)
    data['LB'] = data['SMA_20'] - (2 * data['SD_20']) # lower band = simple moving average - (2 * standard deviation)
    data = data.dropna()
    return data

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
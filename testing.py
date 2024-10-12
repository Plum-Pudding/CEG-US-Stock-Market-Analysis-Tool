from keras.api.models import Sequential
from keras.api.layers import Dense

# Create a simple Sequential model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(10,)))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Save the model
model.save("test_model.keras")

print("Model saved successfully.")
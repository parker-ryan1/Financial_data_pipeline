import pyodbc
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Step 1: Load Data from SQL Server
def load_data_from_sql():
    db_conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=DESKTOP-I3BERSO;"
        "DATABASE=financial_data;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    conn = pyodbc.connect(db_conn_str)
    query = "SELECT [Date], [Revenue], [Growth_Rate] FROM revenue_data"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Step 2: Preprocess Data
def preprocess_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Days'] = (df['Date'] - df['Date'].min()).dt.days
    features = df[['Days', 'Revenue']].values
    target = df['Growth_Rate'].values
    feature_scaler = MinMaxScaler()
    target_scaler = MinMaxScaler()
    features_scaled = feature_scaler.fit_transform(features)
    target_scaled = target_scaler.fit_transform(target.reshape(-1, 1))
    return features_scaled, target_scaled, feature_scaler, target_scaler

# Step 3: Create Sequences
def create_sequences(features, target, window_size):
    X, y = [], []
    for i in range(len(features) - window_size):
        X.append(features[i:i+window_size])
        y.append(target[i+window_size])
    return np.array(X), np.array(y)

# Step 4: Build and Train Model
def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Main Program
if __name__ == "__main__":
    # Load data
    financial_data = load_data_from_sql()

    # Preprocess data
    features, target, feature_scaler, target_scaler = preprocess_data(financial_data)

    # Create sequences
    window_size = 30
    X, y = create_sequences(features, target, window_size)

    # Build and train model
    input_shape = (X.shape[1], X.shape[2])
    model = build_lstm_model(input_shape)
    history = model.fit(X, y, batch_size=32, epochs=50, validation_split=0.2)

    # Evaluate model
    predictions = model.predict(X)
    predictions_actual = target_scaler.inverse_transform(predictions)
    y_actual = target_scaler.inverse_transform(y)

    # Plot results
    plt.plot(y_actual, label='Actual Growth Rate')
    plt.plot(predictions_actual, label='Predicted Growth Rate')
    plt.xlabel('Time')
    plt.ylabel('Growth Rate')
    plt.legend()
    plt.show()

    # Save model
    model.save('financial_growth_forecast_model.h5')

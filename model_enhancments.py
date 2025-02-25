#tuner
import keras_tuner as kt

def build_model(hp):
    model = Sequential()
    model.add(LSTM(units=hp.Int('units', min_value=32, max_value=128, step=32), return_sequences=True, input_shape=input_shape))
    model.add(Dropout(rate=hp.Float('dropout', min_value=0.1, max_value=0.5, step=0.1)))
    model.add(LSTM(units=hp.Int('units', min_value=32, max_value=128, step=32), return_sequences=False))
    model.add(Dropout(rate=hp.Float('dropout', min_value=0.1, max_value=0.5, step=0.1)))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

tuner = kt.RandomSearch(build_model, objective='val_loss', max_trials=5, executions_per_trial=3, directory='tuner_results')
tuner.search(X, y, epochs=50, validation_split=0.2)
best_model = tuner.get_best_models(num_models=1)[0]
#extra fetures
# Add moving average feature
financial_data['Revenue_MA'] = financial_data['Revenue'].rolling(window=7).mean()

# Add exponential smoothing feature
financial_data['Revenue_EMA'] = financial_data['Revenue'].ewm(span=7, adjust=False).mean()
# Deployment
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/predict")
def predict(data: dict):
    # Preprocess input data
    input_data = np.array(data['features']).reshape(1, -1)
    input_data_scaled = feature_scaler.transform(input_data)
    input_data_sequence = np.expand_dims(input_data_scaled, axis=0)

    # Make prediction
    prediction = model.predict(input_data_sequence)
    prediction_actual = target_scaler.inverse_transform(prediction)
    return {"prediction": prediction_actual[0][0]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
  #monitoring # Example: Retrain model with new data
new_data = load_data_from_sql()  # Load new data
new_features, new_target, _, _ = preprocess_data(new_data)
new_X, new_y = create_sequences(new_features, new_target, window_size)

# Retrain the model
model.fit(new_X, new_y, batch_size=32, epochs=50, validation_split=0.2)

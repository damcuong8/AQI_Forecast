import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from website._init_ import create_app

app = create_app()

def get_color(aqi_value):
    """Determine color based on AQI value"""
    aqi_value = float(aqi_value)
    if aqi_value <= 50:
        return 'green'
    elif aqi_value <= 100:
        return 'yellow'
    elif aqi_value <= 150:
        return 'orange'
    elif aqi_value <= 200:
        return 'red'
    else:
        return 'purple'

# Load model
model = load_model('model/best_model.keras')

# Load data
df = pd.read_csv('data/aqi_data.csv')

df['local_time'] = pd.to_datetime(df['local_time'])

numerical_features = ['CO', 'NO2', 'PM10', 'PM2.5', 'Temperature', 'Humidity', 'Wind Speed']
scaler = MinMaxScaler()
df[numerical_features] = scaler.fit_transform(df[numerical_features])

@app.route('/')
def index():
    try:
        # Get prediction results from predict_multiple_windows function
        response = predict_multiple_windows()
        predictions = response.get('predictions', [])
        error = response.get('error', '')

        # Ensure predictions are not empty
        if not predictions:
            raise ValueError("No predictions available")

        # Create a list of hours for the next 72 hours from local time
        hours = df['local_time'].tail(72).dt.strftime('%H:%M').tolist()

        # Ensure hours are not empty
        if not hours:
            raise ValueError("No hours available")

        # Create a list of colors based on AQI values
        colors = [get_color(aqi) for aqi in predictions]

        # Get historical data for the last 72 hours
        # Get historical data for the last 72 hours
        #historical_data = df[['AQI', 'PM2.5', 'PM10', 'CO', 'NO2']].tail(72).to_dict(orient='records')

        # Inverse transform the scaled data to get original values
        historical_data_scaled = df[numerical_features].tail(72)
        historical_data_original = scaler.inverse_transform(historical_data_scaled)
        historical_data_original_df = pd.DataFrame(historical_data_original, columns=numerical_features)

        # Add the AQI column back to the DataFrame
        historical_data_original_df['AQI'] = df['AQI'].tail(72).values

        # Convert to dictionary
        historical_data_original = historical_data_original_df.to_dict(orient='records')
        historical_data_color = df[['AQI', 'AQI_PM2.5', 'AQI_PM10', 'AQI_CO', 'AQI_NO2']].tail(72).to_dict(orient='records')

        # Generate colors for historical data
        historical_colors = {
            'AQI': [get_color(row['AQI']) for row in historical_data_color],
            'PM2.5': [get_color(row['AQI_PM2.5']) for row in historical_data_color],
            'PM10': [get_color(row['AQI_PM10']) for row in historical_data_color],
            'CO': [get_color(row['AQI_CO']) for row in historical_data_color],
            'NO2': [get_color(row['AQI_NO2']) for row in historical_data_color]
        }

        # Render HTML template and pass data
        return render_template('index.html', predictions=predictions, hours=hours, colors=colors, error=error, historical_data=historical_data_original, historical_colors=historical_colors)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/predict', methods=['POST'])
def predict_multiple_windows():
    predictions = []

    try:
        # Total number of features in your input (based on your previous code)
        total_features = 8  # PM2.5, CO, PM10, NO2, Temperature, Humidity, Wind Speed, AQI

        for i in range(len(df) - 480 - 72 + 1, len(df) - 480 + 1):
            # Select a window of 480 time steps
            input_window = df[['PM2.5', 'CO', 'PM10', 'NO2', 'Temperature', 'Humidity', 'Wind Speed', 'AQI']].iloc[
                           i:i + 480]

            # Convert to numpy array and add batch dimension
            input_data = np.array(input_window, dtype=np.float32)
            input_data = np.expand_dims(input_data, axis=0)  # Shape: (1, 480, 8)

            # Predict
            prediction = model.predict(input_data)

            # Convert numpy float32 to Python float and append
            predictions.append(float(prediction[0][0]))  # Assuming single output prediction

        # Return predictions as dictionary
        return {'predictions': predictions}
    except Exception as e:
        return {'predictions': [], 'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
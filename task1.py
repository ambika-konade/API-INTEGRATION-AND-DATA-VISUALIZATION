import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# OpenWeatherMap API Key (replace with your actual key)
API_KEY = "2675a30793dd5900b29fed7019c91a87"
CITY = "pune"  # Replace with desired city

# API Endpoint
url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json()

    if data and data['list']:
        # Extract relevant data
        timestamps = [item['dt_txt'] for item in data['list']]
        temperatures = [item['main']['temp'] for item in data['list']]
        humidity = [item['main']['humidity'] for item in data['list']]

        # Create Pandas DataFrame
        df = pd.DataFrame({
            'Timestamp': timestamps,
            'Temperature': temperatures,
            'Humidity': humidity
        })

        # Convert Timestamp to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        # Create subplots
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))

        # Temperature line plot
        sns.lineplot(x='Timestamp', y='Temperature', data=df, ax=axes[0])
        axes[0].set_title('Temperature Over Time')
        axes[0].set_xlabel('Time')
        axes[0].set_ylabel('Temperature (°C)')
        axes[0].tick_params(axis='x', rotation=45)

        # Humidity line plot
        sns.lineplot(x='Timestamp', y='Humidity', data=df, ax=axes[1])
        axes[1].set_title('Humidity Over Time')
        axes[1].set_xlabel('Time')
        axes[1].set_ylabel('Humidity (%)')
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()
    else:
        print("No weather data found")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except ValueError as e:
    print(f"Error decoding JSON: {e}")

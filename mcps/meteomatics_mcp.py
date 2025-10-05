import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import base64
from utils.config import METEOMATICS_USERNAME, METEOMATICS_PASSWORD

def get_meteomatics_data(city: str):
    """
    Fetches weather data for a given city from the Meteomatics API.
    Returns a dictionary containing the weather data.
    """
    geolocator = Nominatim(user_agent="meteomatics_weather_forecast")
    location = geolocator.geocode(city)
    if not location:
        return {"error": f"Could not find coordinates for {city}."}
    
    lat, lon = location.latitude, location.longitude

    start_time = datetime.utcnow()
    end_time = datetime.utcnow() + timedelta(days=3)
    interval = "PT1H"

    parameters = "t_2m:C,relative_humidity_2m:p,msl_pressure:hPa,prob_precip_1h:p"

    url = (
        f"https://api.meteomatics.com/"
        f"{start_time.isoformat()}Z--{end_time.isoformat()}Z:{interval}/"
        f"{parameters}/{lat},{lon}/json"
    )

    response = requests.get(url, auth=(METEOMATICS_USERNAME, METEOMATICS_PASSWORD))

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"error": f"Meteomatics API request failed with status code {response.status_code}."}

def generate_plot(data: dict, city: str):
    """
    Generates a plot from the weather data and returns a base64 encoded image.
    """
    df = pd.DataFrame()
    for param in data["data"]:
        param_name = param["parameter"]
        values = [v["value"] for v in param["coordinates"][0]["dates"]]
        df[param_name] = values
    
    df["datetime"] = [v["date"] for v in data["data"][0]["coordinates"][0]["dates"]]
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index("datetime", inplace=True)

    plt.figure(figsize=(12, 8))

    plt.subplot(4, 1, 1)
    plt.plot(df.index, df["t_2m:C"], color='orange')
    plt.title(f"Weather Forecast for {city} (Next 3 Days)")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)

    plt.subplot(4, 1, 2)
    plt.plot(df.index, df["relative_humidity_2m:p"], color='blue')
    plt.ylabel("Humidity (%)")
    plt.grid(True)

    plt.subplot(4, 1, 3)
    plt.plot(df.index, df["msl_pressure:hPa"], color='green')
    plt.ylabel("Pressure (hPa)")
    plt.grid(True)

    plt.subplot(4, 1, 4)
    plt.plot(df.index, df["prob_precip_1h:p"], color='purple')
    plt.ylabel("Rain Probability (%)")
    plt.xlabel("Time (UTC)")
    plt.grid(True)

    plt.tight_layout()
    
    # Save the plot to a temporary file
    plot_path = "/tmp/weather_plot.png"
    plt.savefig(plot_path)
    plt.close()

    # Encode the image in base64
    with open(plot_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    return encoded_image
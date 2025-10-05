import requests
from utils.config import METEOMATICS_USERNAME, METEOMATICS_PASSWORD
from datetime import datetime, timedelta
import json

def get_meteomatics_data(city: str):
    """
    Fetches weather data for a given city from the Meteomatics API.
    Returns a dictionary containing the weather data.
    """
    city = json.loads(city)["city"]
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    response = requests.get(geocoding_url)
    if response.status_code == 200 and response.json().get("results"):
        location = response.json()["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
    else:
        return {"error": "Could not find coordinates for the city."}

    start_time = datetime.utcnow()
    end_time = datetime.utcnow() + timedelta(days=3)
    interval = "PT1H"

    parameters = "t_2m:C,relative_humidity_2m:p,msl_pressure:hPa,prob_precip_1h:p"

    url = (
        f"https://api.meteomatics.com/"
        f"{start_time.isoformat()}Z--{end_time.isoformat()}Z:{interval}/"
        f"{parameters}/{latitude},{longitude}/json"
    )

    response = requests.get(url, auth=(METEOMATICS_USERNAME, METEOMATICS_PASSWORD))

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"error": f"Meteomatics API request failed with status code {response.status_code}."}
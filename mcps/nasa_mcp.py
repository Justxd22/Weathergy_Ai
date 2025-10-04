import requests, json
from utils.config import NASA_API_KEY

def get_nasa_data(city: str):
    """
    Fetches weather data for a given city from Nasa's POWER API.
    """
    # Get coordinates for the city using a free geocoding API
    city = json.loads(city)["city"]
    print(city)
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    response = requests.get(geocoding_url)
    if response.status_code == 200 and response.json().get("results"):
        location = response.json()["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
    else:
        return {"error": "Could not find coordinates for the city."}

    # Make a request to the Nasa POWER API
    power_api_url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,RH2M,PRECTOTCORR&community=RE&longitude={longitude}&latitude={latitude}&start=20230101&end=20230105&format=JSON&key={NASA_API_KEY}"
    response = requests.get(power_api_url)

    if response.status_code == 200:
        data = response.json()
        # Structure the data as needed
        # This is just an example, you might need to adjust it based on the actual API response
        structured_data = {
            "temperature": data.get("properties", {}).get("parameter", {}).get("T2M"),
            "humidity": data.get("properties", {}).get("parameter", {}).get("RH2M"),
            "precipitation": data.get("properties", {}).get("parameter", {}).get("PRECTOTCORR"),
        }
        return structured_data
    else:
        return {"error": "Could not fetch data from Nasa POWER API."}

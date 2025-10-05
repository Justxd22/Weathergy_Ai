import requests, json
from utils.config import FIREBASE_CONFIG

def get_firebase_data(city: str):
    """
    Fetches weather data for Egypt from a public Firebase Realtime Database.
    """
    city = json.loads(city)["city"]
    if city.lower() in ['cairo', 'alexandria', 'giza', 'luxor', 'aswan', 'egypt']:
        database_url = FIREBASE_CONFIG['databaseURL']
        # The data is at the root, so we can just append .json
        response = requests.get(f"{database_url}/.json")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Could not fetch data from Firebase."}
    else:
        return None
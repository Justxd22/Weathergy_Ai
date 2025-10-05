import os
from dotenv import load_dotenv

load_dotenv()

# Firebase configuration
FIREBASE_CONFIG = {
    "databaseURL": "https://skysnap-12d5a-default-rtdb.europe-west1.firebasedatabase.app/"
}

# Nasa API configuration
NASA_API_KEY = os.getenv("NASA_API_KEY")

# Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Meteomatics API configuration
METEOMATICS_USERNAME = os.getenv("METEOMATICS_USERNAME")
METEOMATICS_PASSWORD = os.getenv("METEOMATICS_PASSWORD")

# Weathery AI

A LangChain AI that predicts whether it will rain in a given city using MCP.

## Features

-   Predicts rain for any city worldwide.
-   Uses a combination of Firebase and Nasa APIs for weather data.
-   Provides fun facts and recommendations based on the weather.

## How it Works

The AI uses a ReAct agent that has access to two tools:

1.  **Firebase MCP:** Fetches weather data for cities in Egypt from a public Firebase Realtime Database.
2.  **Nasa MCP:** Fetches weather data for any city in the world from Nasa's POWER API.

The agent first checks if the city is in Egypt and tries to use the Firebase tool. If the city is not in Egypt or if the Firebase tool returns no data, it falls back to the Nasa tool.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Weathery-Ai.git
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file:**
    ```bash
    touch .env
    ```
4.  **Add your API keys to the `.env` file:**
    ```
    NASA_API_KEY="YOUR_NASA_API_KEY"
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    ```

## Usage

1.  **Run the main script:**
    ```bash
    python main.py
    ```
2.  **Enter a city name when prompted.**

The AI will then provide a weather prediction and a fun fact.

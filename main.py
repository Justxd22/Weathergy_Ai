from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GOOGLE_API_KEY
from langchain.agents import tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from mcps.firebase_mcp import get_firebase_data
from mcps.nasa_mcp import get_nasa_data
from mcps.meteomatics_mcp import get_meteomatics_data
import json

# Define the output structure
class WeatherPrediction(BaseModel):
    prediction: str = Field(description="The prediction of whether it will rain or not.")
    fun_fact: str = Field(description="A fun fact related to the weather prediction.")
    raw_data: dict = Field(description="The raw weather data from the Meteomatics API.")

# System prompt
system_prompt = """
You are a weather prediction AI. Your goal is to predict if it will rain in a given city.

You have access to three tools:
1. get_firebase_data_tool: This tool provides weather data for Egypt from a public Firebase database. This should be your first choice if the user asks for a city in Egypt.
2. get_meteomatics_data_tool: This tool provides detailed weather data for any city in the world from the Meteomatics API. This is the most powerful tool and should be used when the user asks for a city weather.
3. get_nasa_data_tool: This tool also provides weather data for any city in the world from Nasa's POWER API use as fallback if any errors in tool 2.

Here is your workflow:
1. Get the city name from the user.
2. If the city is in Egypt, use the get_firebase_data tool.
3. If the city is not in Egypt, or if the get_firebase_data tool returns no data, then use the get_meteomatics_data_tool.
4. Analyze the data from the tools to predict if it will rain.
5. Return a structured response with the prediction and a fun fact.

Example fun facts weather related:
- "Wear something heavy."
- "Wear a good sun block with SPF <level>."
- "Don't forget your umbrella!"
- Other... Get creative

You have access to the following tools:

{tools}

To use the tools, you must use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: The input to the action, which should be a JSON object with a single key "city". For example: {{"city": "cairo"}}
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

# Cache for Meteomatics data
meteomatics_cache = {}

# Define tools
@tool
def get_firebase_data_tool(city: str) -> str:
    """Fetches weather data from a public Firebase database for Egypt."""
    return get_firebase_data(city)

@tool
def get_nasa_data_tool(city: str) -> str:
    """Fetches weather data from Nasa's POWER API for any city."""
    return get_nasa_data(city)

@tool
def get_meteomatics_data_tool(city: str) -> str:
    """Fetches detailed weather data from the Meteomatics API."""
    data = get_meteomatics_data(city)
    index = json.loads(city)['city']
    meteomatics_cache[index] = data
    return data

tools = [get_firebase_data_tool, get_meteomatics_data_tool, get_nasa_data_tool]

# Create the agent
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=GOOGLE_API_KEY)
prompt = PromptTemplate.from_template(system_prompt)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=5  # Added to prevent infinite loops
)

def predict_weather(city: str):
    """
    Predicts the weather for a given city.
    """
    response = agent_executor.invoke({"input": f"Predict if it will rain in {city}"})
    print(city)
    # Check if the response contains meteomatics data
    if city in meteomatics_cache:
        print("yes")
        response["raw_data"] = meteomatics_cache[city]
        del meteomatics_cache[city] # Clear the cache for the city

    return response

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=['GET'])
def predict():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    response = predict_weather(city)
    return jsonify(response)

if __name__ == '__main__':
    #city = input("Enter a city name: ")
    #prediction = predict_weather(city)
    #print(prediction)
    app.run(host="0.0.0.0", port=8000)
import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("ASI_ONE_API_KEY")
BASE_URL = "https://api.asi1.ai/v1"

headers = {
  "Authorization": f"Bearer {API_KEY}",
  "Content-Type": "application/json"
}

# def get_weather(latitude, longitude):
#     response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
#     data = response.json()
#     return data['current']['temperature_2m']


# Define the get_weather tool
get_weather_tool = {
"type": "function",
"function": {
  "name": "get_weather",
  "description": "Get current temperature for a given location (latitude and longitude).",
  "parameters": {
    "type": "object",
    "properties": {
        "latitude": {"type": "number"},
        "longitude": {"type": "number"}
      },
      "required": ["latitude", "longitude"]
    }
  }
}

# Initial message setup
initial_message = [
  {
    "role": "system",
    "content": "You are a weather assistant. When a user asks for the weather in a location, use the get_weather tool with the appropriate latitude and longitude for that location."
  },
  {
    "role": "user",
    "content": "What's the current weather like in New York City right now?"
  }
]

# First call to model
payload = {
  "model": "asi1-mini",
  "messages": initial_message,
  "tools": [get_weather_tool],
  "temperature": 0.7,
  "max_tokens": 1024
}

first_response = requests.post(
  f"{BASE_URL}/chat/completions",
  headers=headers,
  json=payload
)

first_response.raise_for_status()
first_response_json = first_response.json()
tool_calls = first_response_json["choices"][0]["message"].get("tool_calls", [])
messages_history = list(initial_message)
messages_history.append(first_response_json["choices"][0]["message"])

# Simulate execution of get_weather tool
def get_weather(lat, lon):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
    )
    data = response.json()
    return data['current']['temperature_2m']

# Process tool call
for tool_call in tool_calls:
    function_name = tool_call["function"]["name"]
    arguments = json.loads(tool_call["function"]["arguments"])

    if function_name == "get_weather":
        latitude = arguments["latitude"]
        longitude = arguments["longitude"]
        temperature = get_weather(latitude, longitude)
        result = {
            "temperature_celsius": temperature,
            "location": f"lat: {latitude}, lon: {longitude}"
        }
    else:
        result = {"error": f"Unknown tool: {function_name}"}

    # Tool result message
    tool_result_message = {
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": json.dumps(result)
    }
    print("--------------------------------")
    print(tool_result_message)
    messages_history.append(tool_result_message)

print("--------------------------------")
print(messages_history)

# Final call to model with tool results
final_payload = {
    "model": "asi1-mini",
    "messages": messages_history,
    "temperature": 0.7,
    "max_tokens": 1024
}

final_response = requests.post(
    f"{BASE_URL}/chat/completions",
    headers=headers,
    json=final_payload
)

final_response.raise_for_status()
final_response_json = final_response.json()

# Final result
print(final_response_json["choices"][0]["message"]["content"])

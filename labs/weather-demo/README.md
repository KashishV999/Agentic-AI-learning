# Weather Demo

## Why This Lab Exists

This folder is a simple agent demo for tool use. The model receives a weather question, extracts the location and date, calls a forecast tool, and returns an answer. It is a smaller example of the same tool-calling ideas used in the later agent labs.

## What I Learned On The First Pass

- How to let the model call a tool instead of fabricating weather data.
- Why a schema is useful when the tool needs structured inputs like place and date.
- How an external API can be wrapped as a capability for an agent.
- How to keep a narrow agent focused on one task.
- Why tool-backed answers are more reliable than model-only answers for current information.

## Core AI And Tech Topics

- Agent tool use
- Structured tool input
- OpenAI Agents SDK
- Weather API integration
- Geocoding
- Schema validation

## Folder Structure

```text
weather-demo/
├── README.md
├── get_weather_forecast.py
├── index.py
├── requirements.txt
└── weather_schema.py
```

## Files

- `index.py` builds the agent and runs a sample weather query through OpenRouter.
- `get_weather_forecast.py` geocodes a place and fetches hourly temperatures from Open-Meteo.
- `weather_schema.py` defines the structured tool input.
- `requirements.txt` lists the dependencies.

## Setup

```bash
cd labs/weather-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
OPENAI_TRACING_KEY=your_openai_key_here
```

`OPENAI_TRACING_KEY` is optional and only affects tracing.

## Run

```bash
python3 index.py
```

## Notes

- The current query in `index.py` is hard-coded.
- The weather tool expects dates in `YYYY-MM-DD` format.

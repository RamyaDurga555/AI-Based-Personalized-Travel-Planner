# ✈️ AI-Based Personalized Travel Planner

A college AIML prototype combining destination exploration, recommendation, personalized itinerary generation, budget planning, route-aware activity sequencing, and an itinerary assistant.

## Features
- Country exploration dashboard
- Destination, food, transport, culture and budget information
- User preferences: duration, travelers, budget, interests, travel style
- Personalized day-wise itinerary
- Budget breakdown
- Interest-based recommendations
- AI-style incremental itinerary assistant
- Simple route-aware planning using travel-time metadata
- Runs locally with Streamlit; no API key required

## Run on Windows PowerShell

```powershell
cd AI-Based-Personalized-Travel-Planner
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Project structure
- `app.py` — Streamlit user interface
- `planner.py` — country data, recommendation logic, itinerary generation and assistant logic
- `requirements.txt` — dependencies

## Note
This is an educational prototype. Destination, cost, transport and weather values are illustrative rather than live booking information.

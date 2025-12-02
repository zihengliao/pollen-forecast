## Pollen Forecast & Heatmap
Tired of hayfever and allergies? Me too. Here is a full-stack pollen forecasting platform featuring a real-time heatmap, on-click forecasting, and a scalable caching layer.

## Link
Backend server will take a little bit to spin up, probably around 30 seconds
https://pollen-forecast.vercel.app/

## Features
- Interactive heatmap using Google Pollen API + Leaflet
- Click-anywhere forecasting (5-day pollen levels, index scoring)
- MongoDB caching for heatmap tiles & forecasts (geohash-based)
- FastAPI backend with async I/O + multi-worker scaling
- Production deployment on Vercel (frontend) + Render (backend)

## Architecture
Client -> Server -> MongoDB Cache -> Pollen API


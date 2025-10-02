#!/bin/bash
# Start Mosquitto in the background
mosquitto -c mosquitto/config/mosquitto.conf &

# Wait a few seconds to ensure Mosquitto starts
sleep 2

# Start FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
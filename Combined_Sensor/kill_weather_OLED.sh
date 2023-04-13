#!/bin/bash
#chmod +x kill_weather_OLED.sh
if [ -f "weather_OLED.pid" ]; then
  PID=$(cat weather_OLED.pid)
  kill -INT $PID
else
  echo "PID file not found. Weather_combined.py may not be running."
fi

#!/bin/sh
# Run the first script
./script1.sh &
# Wait for 60 seconds
sleep 60
# Run the second script
./script2.sh &
# Wait for another 60 seconds to ensure everything starts properly
sleep 60
# Run the Flask application
python3 app.py

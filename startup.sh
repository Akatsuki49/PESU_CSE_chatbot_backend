#!/bin/bash
set -e

# Run the add_data.py script
echo "Running add_data.py..."
python /app/add_data.py

# Start the main application (e.g., using uvicorn)
echo "Starting the backend service..."
exec fastapi run main.py --host 0.0.0.0 --port 8000
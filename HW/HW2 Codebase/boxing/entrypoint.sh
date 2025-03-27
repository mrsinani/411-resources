#!/bin/bash

# Load the environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

pip install -r requirements.txt

# Check if CREATE_DB is true, and run the database creation script if so
if [ "$CREATE_DB" = "true" ]; then
    echo "Creating the database..."
    sql/create_db.sh
else
    echo "Skipping database creation."
fi

# Start the Python application
exec python app.py

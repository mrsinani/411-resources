#!/bin/bash

# This script checks database setup inside the Docker container
echo "Checking database directory permissions..."
ls -la /app/db

echo -e "\nChecking if database file exists..."
if [ -f /app/db/app.db ]; then
  echo "Database file exists"
  ls -la /app/db/app.db
else
  echo "Database file does not exist yet"
fi

echo -e "\nChecking SQLite version..."
sqlite3 --version

echo -e "\nChecking if directories are writable..."
touch /app/db/test_file.txt
if [ -f /app/db/test_file.txt ]; then
  echo "Directory is writable"
  rm /app/db/test_file.txt
else
  echo "Directory is NOT writable"
fi

echo -e "\nChecking environment variables..."
echo "DOCKER_ENV=${DOCKER_ENV}"
echo "DATABASE_URL=${DATABASE_URL}"

echo -e "\nChecking SQLite connection..."
sqlite3 /app/db/app.db ".databases" 
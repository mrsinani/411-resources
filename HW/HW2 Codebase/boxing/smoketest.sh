#!/bin/bash

BASE_URL="http://localhost:5001/api"
ECHO_JSON=false

while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

print_json_if_requested() {
  if [ "$ECHO_JSON" = true ]; then
    echo "$1" | jq .
  fi
}

###############################################
# Health Checks
###############################################

echo "Checking health..."
curl -s "$BASE_URL/health" | grep -q '"status": "success"' || { echo "Health check failed."; exit 1; }
echo "Health check passed."

echo "Checking database..."
curl -s "$BASE_URL/db-check" | grep -q '"status": "success"' || { echo "Database check failed."; exit 1; }
echo "Database check passed."

###############################################
# Boxer Setup
###############################################

# Clear any state
echo "Emptying ring"
curl -s -X POST "$BASE_URL/clear-boxers" | grep -q '"status": "success"' || { echo "Failed to clear ring."; exit 1; }

# Add two boxers
echo "Creating boxer: Pardesh..."
curl -s -X POST "$BASE_URL/add-boxer" -H "Content-Type: application/json" \
  -d '{"name": "Pardesh", "weight": 180, "height": 180, "reach": 74.5, "age": 30}' | grep -q '"status": "success"' || { echo "Failed to add Pardesh."; exit 1; }

echo "Creating boxer: Danaid..."
curl -s -X POST "$BASE_URL/add-boxer" -H "Content-Type: application/json" \
  -d '{"name": "Danaid", "weight": 190, "height": 178, "reach": 72.0, "age": 28}' | grep -q '"status": "success"' || { echo "Failed to add Danaid."; exit 1; }

# Duplicate name should fail
echo "Trying to add Pardesh again (should fail)..."
response=$(curl -s -X POST "$BASE_URL/add-boxer" -H "Content-Type: application/json" \
  -d '{"name": "Pardesh", "weight": 180, "height": 180, "reach": 74.5, "age": 30}')
echo "$response" | grep -q '"status": "error"' || { echo "Duplicate boxer name check failed."; exit 1; }

###############################################
# Ring Tests
###############################################

# Enter both boxers
echo "Entering Pardesh into the ring."
curl -s -X POST "$BASE_URL/enter-ring" -H "Content-Type: application/json" -d '{"name": "Pardesh"}' | grep -q '"status": "success"' || { echo "Failed to enter Pardesh."; exit 1; }

echo "Entering Danaid into the ring."
curl -s -X POST "$BASE_URL/enter-ring" -H "Content-Type: application/json" -d '{"name": "Danaid"}' | grep -q '"status": "success"' || { echo "Failed to enter Danaid."; exit 1; }

# Third boxer should be rejected
echo "Creating third boxer: Peter."
curl -s -X POST "$BASE_URL/add-boxer" -H "Content-Type: application/json" \
  -d '{"name": "Peter", "weight": 200, "height": 185, "reach": 76.0, "age": 34}' | grep -q '"status": "success"' || { echo "Failed to add Peter."; exit 1; }

echo "Trying to enter third boxer into ring (failure expected)"
response=$(curl -s -X POST "$BASE_URL/enter-ring" -H "Content-Type: application/json" -d '{"name": "Peter"}')
echo "$response" | grep -q '"status": "error"' || { echo "Ring overfill check failed."; exit 1; }

###############################################
# Fight
###############################################

echo "Fight started!"
response=$(curl -s -X GET "$BASE_URL/fight")
echo "$response" | grep -q '"status": "success"' || { echo "Fight failed."; exit 1; }
echo "Fight succeeded."

print_json_if_requested "$response"

###############################################
# Leaderboard and Cleanup
###############################################

echo "Getting leaderboard."
response=$(curl -s "$BASE_URL/leaderboard")
echo "$response" | grep -q '"status": "success"' || { echo "Leaderboard failed."; exit 1; }
echo "Leaderboard retrieved."
print_json_if_requested "$response"

# Delete a boxer
echo "Getting Pardesh's ID."
response=$(curl -s "$BASE_URL/get-boxer-by-name/Pardesh")
id=$(echo "$response" | jq .boxer.id)

echo "Deleting Pardesh (ID: $id)."
curl -s -X DELETE "$BASE_URL/delete-boxer/$id" | grep -q '"status": "success"' || { echo "Failed to delete Pardesh."; exit 1; }

echo "Smoke tests passed successfully."

#!/bin/bash

# Get the current timestamp in the desired format
timestamp=$(date +"%Y-%m-%d %H:%M:%S") 

# Create the JSON content with the dynamic timestamp
json_content="{
  \"connectedUsers\": 1550,
  \"newOrders\": 42,
  \"totalTraffic\": 666,
  \"lastUpdate\": \"$timestamp\"
}"

# Write the JSON content to the stats.json file
echo "$json_content" > /home/flaffy/assets/stats.json
echo "oli" > /home/flaffy/demo
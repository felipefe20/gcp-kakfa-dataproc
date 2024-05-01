#!/bin/bash

# Variables
CLUSTER_URL="pkc-v12gj.northamerica-northeast2.gcp.confluent.cloud:9092"
AUTH_HEADER="Authorization: Basic your_token"
# Load the properties from the file
source client.properties

# Construct the AUTH_HEADER
AUTH_HEADER=$(echo -n "$sasl_username:$sasl_password" | base64)

# Print the AUTH_HEADER
echo $AUTH_HEADER
TOPICS=("equipment_failures" "passenger_flow" "ticket_validations" "train_departures" "incidents" "train_arrivals")

# Boucle pour créer chaque topic
for TOPIC in "${TOPICS[@]}"
do
  echo "Creating topic: $TOPIC"
  curl -X POST \
    -H "Content-Type: application/json" \
    -H "$AUTH_HEADER" \
    "$CLUSTER_URL" \
    -d '{
      "topic_name": "'$TOPIC'",
      "partitions_count": 6,
      "replication_factor": 3,
      "configs": [
        {"name": "cleanup.policy", "value": "delete"},
        {"name": "retention.ms", "value": "604800000"}
      ]
    }'
done
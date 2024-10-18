#!/bin/bash

docker build -t web-printer .
docker tag web-printer:latest dk2342235/web-printer:latest

docker push dk2342235/web-printer:latest

curl -X 'POST' \
  'http://10.25.0.112/api/v2.0/chart/release/redeploy' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46IUBTY2llbnRpc3Q5IUA=' \
  -H 'Content-Type: application/json' \
  -d '"web_printer"'

echo "Redeploy initiated"
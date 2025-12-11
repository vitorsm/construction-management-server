#!/bin/sh

# Check if a parameter was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <VERSION_NUMBER>"
  exit 1
fi

VERSION="$1"

docker build -t construction-management-server .

docker tag construction-management-server:latest vitorsmoreira/construction-management-server:$VERSION
docker push vitorsmoreira/construction-management-server:$VERSION
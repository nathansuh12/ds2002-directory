#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <local-file> <s3-bucket-name> <expiration-seconds>"
    exit 1
fi

# Assign arguments to variables
LOCAL_FILE=$1
BUCKET_NAME=$2
EXPIRATION=$3

# Extract the filename from the local file path
FILE_NAME=$(basename "$LOCAL_FILE")

aws s3 cp "$LOCAL_FILE" "s3://$BUCKET_NAME/$FILE_NAME"

SIGNED_URL=$(aws s3 presign "s3://$BUCKET_NAME/$FILE_NAME" --expires-in "$EXPIRATION")

echo "$SIGNED_URL"

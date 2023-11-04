#!/bin/bash
echo "Processing update please wait"
# Update Django and other dependencies
while read -r package; do
    package_name=$(echo "$package" | awk -F'==' '{print $1}')
    pip install -U "$package_name"
done < requirements.txt
echo "Dependencies updated successfully."

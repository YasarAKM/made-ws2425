#!/bin/bash

# Exit script on error
set -e

echo "Running pipeline and validating output..."

# Run the data pipeline
python pipeline.py

# Validate output files
if [[ -f "geo_data_cleaned.csv" && -f "merged_data.csv" ]]; then
  echo "Output files exist: geo_data_cleaned.csv, merged_data.csv"
else
  echo "Error: Output files are missing!"
  exit 1
fi

# Run unit tests
echo "Running unit tests..."
python -m unittest discover -s . -p "test.py"

echo "All tests passed!"

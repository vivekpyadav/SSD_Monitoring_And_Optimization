#!/bin/bash

# Run the SSD monitoring project

# Activate the Virtual Environment
source venv/bin/activate
export PYTHONPATH=$(pwd)

echo "Starting SSD Monitoring..."
python3 src/monitor.py

# To run maintenance tasks(Optimizing)
python3 src/maintenance.py

# Monitoring
python3 src/exporters/prometheus.py
python3 src/exporters/json_exporter.py

echo "Monitoring process completed."


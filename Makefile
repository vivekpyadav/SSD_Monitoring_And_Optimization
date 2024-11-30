# Makefile for SSD Monitoring Project

# Variables
PYTHON = python3
PIP = pip3

env:
	$(PYTHON) -m venv myenv
	source venv/bin/activate
	export PYTHONPATH=$(pwd)

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Run the monitoring script
run:
	$(PYTHON) src/monitor.py

# Run tests
test:
	$(PYTHON) -m unittest discover -s tests

# Deploy project (assumes deployment script is written)
deploy:
	bash scripts/deploy.sh

# Clean up
clean:
	rm -rf __pycache__ logs/

# Build Docker image
docker-build:
	docker build -t ssd-monitoring .

# Run Docker container
docker-run:
	docker run -p 8000:8000 ssd-monitoring


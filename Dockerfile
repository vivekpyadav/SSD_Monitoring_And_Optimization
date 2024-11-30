# Use official Python image as base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the project files into the container
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for Prometheus metrics
EXPOSE 8000

# Set the default command to run the project
CMD ["python", "src/monitor.py"]


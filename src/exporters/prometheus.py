import subprocess
from prometheus_client import Gauge, start_http_server
import time
from src.monitor import get_smart_data

# Define Prometheus metrics
temperature_gauge = Gauge("ssd_temperature", "SSD Temperature", ["disk"])
wear_gauge = Gauge("ssd_wear_level", "SSD Wear Level", ["disk"])
total_writes_gb_gauge = Gauge("ssd_total_writes_gb", "Total SSD Writes (GB)", ["disk"])
lifetime_remaining_pct_gauge = Gauge("ssd_lifetime_remaining_pct", "SSD Lifetime Remaining (%)", ["disk"])

def get_ssds():
    """Get a list of SSD devices (excluding partitions)."""
    # Run the lsblk command to get disks and filter for 'disk' type
    result = subprocess.run(['lsblk', '-d', '-o', 'NAME,TYPE'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    
    # Extract device names (excluding partitions) and filter for SSD
    disks = []
    for line in output.splitlines():
        if 'disk' in line:
            device = line.split()[0]  # Extract the device name (e.g., sda, nvme0n1)
            if "nvme" in device or "sd" in device:
                disks.append(f"/dev/{device}")
    
    return disks

def collect_metrics():
    """Collect SSD metrics and update Prometheus gauges."""
    disks = get_ssds()  # Get list of SSDs dynamically
    for disk in disks:
        smart_data = get_smart_data(disk)
        if smart_data:
            # Extract and parse the SMART data
            temperature = parse_temperature(smart_data.get("Temperature_Celsius", 0))
            wear_level = smart_data.get("Wear_Leveling_Count", "0")
            total_writes_gb = smart_data.get("Total_Writes_GiB", 0)
            lifetime_remaining_pct = smart_data.get("Lifetime_Remaining%", 0)

            try:
                # Try to convert all values to the correct types
                temperature = int(temperature)
                wear_level = int(wear_level)
                total_writes_gb = float(total_writes_gb)
                lifetime_remaining_pct = int(lifetime_remaining_pct)
            except ValueError:
                print(f"Error parsing SMART data for {disk}")
                continue

            # Update the Prometheus gauges
            temperature_gauge.labels(disk=disk).set(temperature)
            wear_gauge.labels(disk=disk).set(wear_level)
            total_writes_gb_gauge.labels(disk=disk).set(total_writes_gb)
            lifetime_remaining_pct_gauge.labels(disk=disk).set(lifetime_remaining_pct)

def parse_temperature(value):
    """Extract and parse the temperature value."""
    if isinstance(value, str):
        # Handle cases like '15/70)', where temperature is followed by a second value
        numeric_part = ''.join(filter(str.isdigit, value.split('/')[0]))  # Take part before '/' and extract digits
        return int(numeric_part) if numeric_part.isdigit() else 0
    return int(value) if isinstance(value, (int, float)) else 0

def main():
    try:
        start_http_server(8000)  # Prometheus HTTP server port
        print("Prometheus exporter running on port 8000...")
        while True:
            collect_metrics()
            time.sleep(60)  # Sleep for 60 seconds before collecting data again
    except KeyboardInterrupt:
        print("\nStopped")

if __name__ == "__main__":
    main()


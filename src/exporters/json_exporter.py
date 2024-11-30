import json
import os
from datetime import datetime
from src.monitor import get_smart_data

OUTPUT_DIR = "logs"
JSON_FILE = os.path.join(OUTPUT_DIR, "ssd_metrics.json")


def save_metrics_to_json(metrics, filename=JSON_FILE):
    """Save SSD metrics to a JSON file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        with open(filename, "w") as json_file:
            json.dump(metrics, json_file, indent=4)
        print(f"Metrics saved to {filename}")
    except Exception as e:
        print(f"Error saving metrics to JSON: {str(e)}")


def collect_metrics():
    """Collect SSD metrics and prepare them for export."""
    disks = ["/dev/sda", "/dev/nvme0n1"]  # Replace with your disk devices
    all_metrics = {}
    for disk in disks:
        smart_data = get_smart_data(disk)
        if smart_data:
            all_metrics[disk] = smart_data
    return all_metrics


def main():
    metrics = collect_metrics()
    if metrics:
        save_metrics_to_json(metrics)


if __name__ == "__main__":
    main()


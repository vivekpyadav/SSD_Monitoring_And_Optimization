import subprocess
import logging
from src.utils.logging import setup_logging



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



setup_logging("logs/ssd_monitor.log")

def run_command(command):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logging.error(f"Error running command {' '.join(command)}: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        logging.error(f"Exception while running command {' '.join(command)}: {str(e)}")
        return None


def get_smart_data(disk):
    """Fetch SMART data for the given disk."""
    command = ["sudo", "smartctl", "-A", disk]
    output = run_command(command)
    if output:
        return parse_smart_data(output)
    return None


def parse_smart_data(output):
    """Parse SMART data and return it as a dictionary."""
    data = {}
    for line in output.splitlines():
        if line.strip() and line[0].isdigit():  # Check for lines with attribute data
            parts = line.split()
            if len(parts) >= 5:  # Ensure it's a valid SMART attribute line
                attribute_name = parts[1]
                raw_value = parts[-1]
                data[attribute_name] = raw_value
    return data


def main():
    disks = get_ssds()
    for disk in disks:
        logging.info(f"Fetching SMART data for {disk}")
        smart_data = get_smart_data(disk)
        if smart_data:
            logging.info(f"SMART data for {disk}: {smart_data}")
        else:
            logging.warning(f"Could not fetch SMART data for {disk}")


if __name__ == "__main__":
    main()


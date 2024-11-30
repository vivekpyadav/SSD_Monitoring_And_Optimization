import subprocess
import logging
from utils.logging import setup_logging

setup_logging("logs/ssd_maintenance.log")


def run_trim(disk):
    """Run TRIM command on the SSD."""
    command = ["sudo","fstrim", disk]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logging.info(f"TRIM successful on {disk}: {result.stdout}")
        else:
            logging.error(f"TRIM failed on {disk}: {result.stderr}")
    except Exception as e:
        logging.error(f"Exception while running TRIM on {disk}: {str(e)}")


def optimize_drive(disk):
    """Perform optimization actions like TRIM."""
    
    try:
        logging.info(f"Starting optimization for {disk}")
        run_trim(disk)
        logging.info(f"Completed optimization for {disk}")

    except KeyboardInterrupt:
        logging.error("\nStopped")


def main():
    disks = ["/"]  # Replace with your disk devices
    for disk in disks:
        optimize_drive(disk)


if __name__ == "__main__":
    main()


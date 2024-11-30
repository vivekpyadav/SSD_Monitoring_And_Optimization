import os
import sys


def schedule_cron_job(command, interval="* * * * *"):
    """Schedule a cron job using the system's crontab."""
    cron_job = f"{interval} {command}\n"
    with open("/tmp/mycron", "w") as f:
        f.write(cron_job)
    os.system("crontab /tmp/mycron")
    os.remove("/tmp/mycron")
    print(f"Cron job scheduled: {command} every {interval}")


def main():
    # Example usage: schedule the monitor.py script to run every minute
    schedule_cron_job("python /path/to/ssd-monitoring-project/src/monitor.py", "* * * * *")

    # Schedule other tasks as needed
    # schedule_cron_job("python /path/to/ssd-monitoring-project/src/maintenance.py", "0 0 * * *")


if __name__ == "__main__":
    main()


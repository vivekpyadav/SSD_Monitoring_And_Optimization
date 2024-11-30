import platform
import psutil


def get_system_info():
    """Return basic system information."""
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture()[0],
        "Processor": platform.processor(),
        "Total Memory": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "Disk Info": [disk.device for disk in psutil.disk_partitions()],
    }


def main():
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()


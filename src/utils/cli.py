import argparse


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="SSD Monitoring and Maintenance Tool")
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Run the SSD monitoring tool",
    )
    parser.add_argument(
        "--maintain",
        action="store_true",
        help="Run SSD maintenance actions",
    )
    parser.add_argument(
        "--exporter",
        choices=["prometheus", "json"],
        help="Choose an exporter: prometheus or json",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.monitor:
        print("Running monitoring tool...")
        from src.monitor import main as monitor_main
        monitor_main()
    elif args.maintain:
        print("Running maintenance actions...")
        from src.maintenance import main as maintain_main
        maintain_main()
    elif args.exporter:
        print(f"Running {args.exporter} exporter...")
        if args.exporter == "prometheus":
            from src.exporters.prometheus import main as prometheus_main
            prometheus_main()
        elif args.exporter == "json":
            from src.exporters.json_exporter import main as json_exporter_main
            json_exporter_main()


if __name__ == "__main__":
    main()


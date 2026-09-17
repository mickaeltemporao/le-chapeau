"""Command Line Interface for Le Chapeau."""

import argparse
import os
import sys
from pathlib import Path

from chapeau.export import DEFAULT_EXPORT_PATH, DEFAULT_LOG_PATH, export_logs_to_csv, export_logs_to_dataframe


def run_app(port: int = 8501, address: str = "0.0.0.0", headless: bool = True) -> None:
    """Launch the Streamlit app."""
    import streamlit.web.cli as stcli

    app_path = str(Path(__file__).parent / "app.py")
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.port",
        str(port),
        "--server.address",
        address,
        "--server.headless",
        "true" if headless else "false",
        "--browser.gatherUsageStats",
        "false",
    ]
    sys.exit(stcli.main())


def export_command(args: argparse.Namespace) -> None:
    """Handle the 'export' command."""
    log_path = Path(args.log_file)
    out_path = Path(args.output)
    anonymize = not args.no_anonymize

    print(f"Reading logs from: {log_path}")
    if not log_path.exists():
        print(f"Error: Log file '{log_path}' does not exist.")
        sys.exit(1)

    df = export_logs_to_dataframe(log_file=log_path, anonymize=anonymize, salt=args.salt)
    if df.empty:
        print("No valid interaction logs found to export.")
        sys.exit(0)

    saved_path = export_logs_to_csv(log_file=log_path, output_csv=out_path, anonymize=anonymize, salt=args.salt)

    print("\n🎓 Export Summary:")
    print(f"  Total interactions : {len(df)}")
    print(f"  Unique participants: {df['participant_id'].nunique()}")
    print("  Interactions by group:")
    for group, count in df["group"].value_counts().items():
        print(f"    - Group {group}: {count}")
    print(f"  Anonymized (UUID)  : {'Yes' if anonymize else 'No'}")
    print(f"\n✅ Export successfully saved to: {saved_path}\n")


def main() -> None:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="chapeau",
        description="Le Chapeau: Educational A/B Testing Platform for Socratic AI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Launch the Streamlit web application")
    run_parser.add_argument("--port", type=int, default=8501, help="Port to run the server on (default: 8501)")
    run_parser.add_argument("--address", type=str, default="0.0.0.0", help="Address to bind to (default: 0.0.0.0)")
    run_parser.add_argument("--no-headless", action="store_true", help="Open a browser window automatically")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export study conversation logs to CSV")
    export_parser.add_argument(
        "--log-file",
        type=str,
        default=str(DEFAULT_LOG_PATH),
        help=f"Path to JSONL log file (default: {DEFAULT_LOG_PATH})",
    )
    export_parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=str(DEFAULT_EXPORT_PATH),
        help=f"Path to destination CSV (default: {DEFAULT_EXPORT_PATH})",
    )
    export_parser.add_argument(
        "--no-anonymize",
        action="store_true",
        help="Do NOT anonymize participant emails/identifiers in the CSV",
    )
    export_parser.add_argument(
        "--salt",
        type=str,
        default=None,
        help="Custom study salt for deterministic anonymization (defaults to config/salt.txt)",
    )

    args = parser.parse_args()

    # Default to 'run' if no subcommand given
    if args.command is None or args.command == "run":
        port = getattr(args, "port", 8501)
        address = getattr(args, "address", "0.0.0.0")
        headless = not getattr(args, "no_headless", False)
        run_app(port=port, address=address, headless=headless)
    elif args.command == "export":
        export_command(args)


if __name__ == "__main__":
    main()

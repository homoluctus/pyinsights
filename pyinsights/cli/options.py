import argparse
from typing import Type
from dataclasses import dataclass

from pyinsights.__version__ import __version__


@dataclass
class CliOption:
    config: str
    fmt: str
    profile: str
    region: str
    quiet: bool
    output: str


def parse_args() -> Type[CliOption]:
    """Parse arguments

    Returns:
        Type[CliOption]
    """

    parser = argparse.ArgumentParser(
        prog="pyinsights",
        description="AWS CloudWatch Logs Insights is wrapped by Python",
    )

    parser.add_argument(
        "-c",
        "--config",
        required=True,
        default="pyinsights.yml",
        help="PyInsights config file path",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "table"],
        default="json",
        dest="fmt",
        help='Output format "json" or "table"',
    )

    parser.add_argument("-p", "--profile", help="AWS profile name")

    parser.add_argument("-r", "--region", help="AWS region")

    parser.add_argument("-o", "--output", help="Output the result to file")

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress progress spinner and messages",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=__version__
    )

    return parser.parse_args(namespace=CliOption)

import argparse
import sys
from typing import Type
from dataclasses import dataclass

from pyinsights.__version__ import __version__
from pyinsights.config import load_config
from pyinsights.query import query
from pyinsights.formatter import format_result


@dataclass
class CliOption:
    config: str
    result_format: str
    profile: str
    region: str
    quiet: bool


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
        dest="result_format",
        help='Output format "json" or "table"',
    )

    parser.add_argument("-p", "--profile", help="AWS profile name")

    parser.add_argument("-r", "--region", help="AWS region")

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


def run() -> bool:
    cli_options = parse_args()
    config = load_config(cli_options.config)
    tmp_result = query(
        cli_options.region,
        cli_options.profile,
        config.get_query_params(),
        quiet=cli_options.quiet,
    )

    if isinstance(tmp_result, dict) and (results := tmp_result.get("results")):
        formatted_result = format_result(cli_options.result_format, results)  # type: ignore
        sys.stdout.write(formatted_result)
        return True

    return False


if __name__ == "__main__":
    sys.exit(run())

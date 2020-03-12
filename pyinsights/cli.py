import argparse
from typing import Any, Dict
import sys

from pyinsights.__version__ import __version__
from pyinsights.config import load_config
from pyinsights.query import query
from pyinsights.formatter import format_result


CliOptions = Dict[str, Any]


def parse_args() -> Dict[str, Any]:
    """Parse arguments

    Returns:
        Dict[str, Any]
    """

    parser = argparse.ArgumentParser(
        prog="pyinsights", description="AWS CloudWatch Logs Insights is wrapped by Python",
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
        help='Output format "json" or "table"',
    )

    parser.add_argument("-p", "--profile", help="AWS profile name")

    parser.add_argument("-r", "--region", help="AWS region")

    parser.add_argument("-v", "--version", action="version", version=__version__)

    return vars(parser.parse_args())


def run(cli_options: CliOptions) -> bool:
    config = load_config(cli_options["config"])
    tmp_result = query(cli_options["region"], cli_options["profile"], config.get_query_params())

    if isinstance(tmp_result, dict) and (results := tmp_result.get("results")):
        formatted_result = format_result(cli_options["format"], results)
        sys.stdout.write(formatted_result)
        return True

    return False


def main() -> bool:
    args = parse_args()
    sys.exit(run(args))

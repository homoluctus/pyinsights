import argparse
from typing import Any, Dict
import sys

from pyinsights import __version__
from pyinsights.pyinsights import run


def parse_args() -> Dict[str, Any]:
    """Parse arguments

    Returns:
        Dict[str, Any]
    """

    parser = argparse.ArgumentParser(
        prog='PyInsights',
        description='AWS CloudWatch Logs Insights is wrapped by Python',
    )

    parser.add_argument(
        '-c',
        '--config',
        required=True,
        default='pyinsights.yml',
        help='PyInsights config file path',
    )

    parser.add_argument('-p', '--profile', help='AWS profile name')

    parser.add_argument('-r', '--region', help='AWS region')

    parser.add_argument(
        '-v', '--version', action='version', version=__version__
    )

    return vars(parser.parse_args())


def cli() -> bool:
    args = parse_args()
    sys.exit(run(args))

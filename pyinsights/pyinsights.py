import sys

from pyinsights.cli.options import parse_args
from pyinsights.cli.formatter import format_result
from pyinsights.cli.writer import Writer
from pyinsights.config import load_config
from pyinsights.query import query


def run() -> bool:
    options = parse_args()
    config = load_config(options.config)
    tmp_result = query(
        options.region,
        options.profile,
        config.get_query_params(),
        quiet=options.quiet,
    )

    if isinstance(tmp_result, dict) and (results := tmp_result.get("results")):
        formatted_result = format_result(options.fmt, results)  # type: ignore
        writer = Writer.from_filename(options.output)
        writer.write(formatted_result)
        return True

    return False


if __name__ == "__main__":
    sys.exit(run())

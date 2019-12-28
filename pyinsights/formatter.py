import json
import shutil
from typing import Dict, List, Type


QueryResult = Type[List[List[Dict[str, str]]]]


class Formatter:
    def __init__(self, format_type: str = 'json') -> None:
        """
        Keyword Arguments:
            format_type {str} -- [description] (default: {'json'})
        """
        self.format_type = format_type

    def _to_pretty_dict(self, results: QueryResult) -> List[Dict[str, str]]:
        """Format results to python dict in list

        Arguments:
            results {QueryResult}

        Returns:
            List[Dict[str, str]]
        """

        formatted_result = [
            {
                field['field']: field['value']
                for field in result if field['field'] != '@ptr'
            }
            for result in results
        ]
        return formatted_result

    def to_json(self, results: QueryResult) -> str:
        """Format results to json

        Arguments:
            results {QueryResult}

        Returns:
            str
        """

        if not results:
            return ''

        tmp_resuls = self._to_pretty_dict(results)
        formatted_result = json.dumps(tmp_resuls, indent=2, ensure_ascii=False)
        return formatted_result

    def to_table(self, results: QueryResult) -> str:
        """Format results to string table

        Arguments:
            results {QueryResult}

        Returns:
            str
        """

        if not results:
            return ''

        tmp_results = self._to_pretty_dict(results)
        headers = list(tmp_results[0].keys())
        width, _ = shutil.get_terminal_size()
        length_per_column = width // len(headers)

        table_header = ''
        for header in headers:
            table_header += header.ljust(length_per_column)

        table_record = ''
        for result in tmp_results:
            for field in result.values():
                table_record += \
                    field[:length_per_column - 2].ljust(length_per_column)
            table_record += '\n'

        formatted_result = f'{table_header}\n{table_record}'
        return formatted_result


def format_result(
    format_type: str,
    results: QueryResult
) -> str:
    """Format the query result

    Arguments:
        format_type {str}: json or table
        results {QueryResult}

    Returns:
        str
    """

    formatter = Formatter(format_type)
    func = getattr(formatter, f'to_{format_type}')
    formatted_result = func(results)
    return formatted_result

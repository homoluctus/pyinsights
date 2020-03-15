class QueryNotYetStartError(Exception):
    """Raises error if the query has not yet started"""


class NotFetchQueryResultError(Exception):
    """Raises error if the query result could not be fetched"""


class QueryTimeoutError(Exception):
    """Raises timeout error if the query timeout"""


class QueryAlreadyCancelled(Exception):
    """Raises if the query has already been cancelled"""


class QueryUnknownError(Exception):
    """Raises if the query status is Unknown"""


class ConfigInvalidSyntaxError(Exception):
    """Raises error if the configuration is invalid syntax"""


class ConfigVersionUnknownError(Exception):
    """Raises error if not specify configuration version"""


class ConfigNotFoundError(Exception):
    """Raises error if the configuration could not be found"""


class InvalidVersionError(Exception):
    """Raises error if the configuration version is invalid"""


class InvalidDurationError(Exception):
    """Raises error if the duration parameter is not number"""

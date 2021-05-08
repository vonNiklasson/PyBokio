from uuid import UUID

from requests import Response


def is_valid_uuid4(uuid_string: str) -> bool:
    """
    Validate that a UUID string is in fact a valid uuid4.
    Happily, the uuid module does the actual checking for us.
    It is vital that the 'version' kwarg be passed to the UUID() call,
    otherwise any 32-character hex string is considered valid.

    Author: @ShawnMilo
    Source: https://gist.github.com/ShawnMilo/7777304

    :param uuid_string: The UUID string to verify is valid
    :return: True if the UUID string is a valid UUID4 instance, otherwise False.
    """
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return str(val) == uuid_string.lower()


def is_response_json(response: Response) -> bool:
    try:
        response.json()
    except ValueError:
        return False
    return "application/json" in response.headers["Content-Type"]

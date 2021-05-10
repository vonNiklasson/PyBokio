from typing import Dict

from requests import Response


class MockResponse(Response):
    def __init__(self, content: str = None, headers: Dict = None, status_code: int = 200):
        super(MockResponse, self).__init__()
        if content:
            self._content = content.encode()

        if headers:
            self.headers.update(headers)

        if status_code:
            self.status_code = status_code

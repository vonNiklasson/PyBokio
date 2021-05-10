from pybokio._utils.verification import is_response_json, is_valid_uuid4
from tests.mocks.requests import MockResponse


class TestIsValidUuid4:
    def test_valid_uuid(self):
        assert is_valid_uuid4("00000000-0000-4000-8000-000000000000") is True

    def test_invalid_uuid(self):
        assert is_valid_uuid4("00000000-0000-0000-0000-000000000000") is False

    def test_invalid_uuid_format(self):
        assert is_valid_uuid4("no") is False


class TestIsResponseJson:
    def test_valid_json_response(self):
        response = MockResponse(content="{}", headers={"Content-Type": "application/json"})
        assert is_response_json(response) is True

    def test_invalid_content_type_response(self):
        response = MockResponse(content="{}", headers={"Content-Type": "html"})
        assert is_response_json(response) is False

    def test_invalid_content_response(self):
        response = MockResponse(content="Just basic text", headers={"Content-Type": "application/json"})
        assert is_response_json(response) is False

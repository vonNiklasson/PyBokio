from pybokio.exceptions import UnexpectedResponseError

ExpectedJsonException = UnexpectedResponseError("Response expected to be JSON.")
InvalidJsonSchemaException = UnexpectedResponseError("Invalid JSON schema from response.")

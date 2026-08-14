class CRMFrameworkError(Exception):
    """Base exception for CRM API test framework."""


class HTTPClientError(CRMFrameworkError):
    def __init__(self, method: str, url: str, cause: Exception) -> None:
        super().__init__(f'{method.upper()} {url} → {cause}')
        self.cause = cause


class AuthenticationError(CRMFrameworkError):
    """Raised when session authentication fails."""


class ResponseValidationError(CRMFrameworkError):
    """Raised when response validation fails outside of an assertion context."""

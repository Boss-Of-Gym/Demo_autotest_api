from allure import step
import httpx


def validate_status_code(response: httpx.Response, expected: int) -> None:
    with step(title=f'HTTP status = {expected}'):
        actual = response.status_code
        assert actual == expected, f'Expected HTTP {expected}, got {actual}.\nBody: {response.text[:500]}'


def validate_content_type(response: httpx.Response, expected: str = 'application/json') -> None:
    with step(title=f'Content-Type contains "{expected}"'):
        actual = response.headers.get('content-type', '')
        assert expected in actual, f'Expected "{expected}" in Content-Type, got "{actual}"'


def validate_response_time(response: httpx.Response, max_seconds: float = 2.0) -> None:
    with step(title=f'Response time < {max_seconds}s'):
        elapsed = response.elapsed.total_seconds()
        assert elapsed < max_seconds, f'Response time {elapsed:.3f}s exceeds limit {max_seconds}s'


def validate_headers(response: httpx.Response) -> None:
    with step(title='Required response headers are present'):
        present = {k.lower() for k in response.headers}
        missing = {'content-type', 'server'} - present
        assert not missing, f'Missing required headers: {missing}'

import logging
from collections.abc import Generator

from allure import step
import pytest

from core.client import BaseHTTPClient
from services.application.authorization import AuthorizationService
from tests.data.application.authorization.request_body import ADMIN_AUTH_REQUEST

from validators.http import validate_status_code

_log = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def session_id(api_client: BaseHTTPClient) -> Generator[str, None, None]:
    """
    Authenticates once per session, yields session_id, signs out on teardown.
    Depends on api_client (session-scoped) — no multiple logins per session.
    """
    service = AuthorizationService(client=api_client)

    with step(title='Session setup: authenticate admin'):
        response = service.authorize(request=ADMIN_AUTH_REQUEST)
        validate_status_code(response=response, expected=200)
        sid: str = response.json()['data']['session_id']

    yield sid

    with step(title='Session teardown: sign out'):
        try:
            service.sign_out(session_id=sid)
        except Exception as exc:
            _log.warning('Sign-out failed: %s', exc)

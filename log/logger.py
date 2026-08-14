import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import allure
import httpx

_SENSITIVE_HEADERS: frozenset[str] = frozenset({
    'authorization', 'token-access', 'access-token',
    'token-authorization', 'signature', 'uuid',
    'cookie', 'set-cookie', 'x-api-key', 'session_id',
})

_SENSITIVE_FIELDS: frozenset[str] = frozenset({
    'login', 'password', 'pass', 'pwd', 'session_id', 'need_2fa',
    'captcha', 'token', 'access_token', 'recaptcha_token', 'secret',
    'qr'
})

_LOG_DIR = Path(__file__).parent.parent / 'logs'
_LOG_DIR.mkdir(exist_ok=True)

_FORMATTER = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s | %(message)s')


def _make_handler(handler: logging.Handler, level: int) -> logging.Handler:
    handler.setLevel(level)
    handler.setFormatter(_FORMATTER)
    return handler


class HTTPLogger:
    def __init__(self, name: str) -> None:
        self._log = logging.getLogger(name)
        if not self._log.handlers:
            self._log.setLevel(logging.DEBUG)
            self._log.addHandler(_make_handler(logging.StreamHandler(), logging.INFO))
            self._log.addHandler(
                _make_handler(
                    logging.FileHandler(
                        _LOG_DIR / 'crm_api_tests.log',
                        mode='a',
                        encoding='utf-8',
                    ),
                    logging.DEBUG,
                )
            )
            self._log.propagate = False

    def log_http(self, response: httpx.Response) -> None:
        trace = _build_trace(response)
        self._log.info(trace)
        _attach_to_allure(trace)


def get_logger(name: str) -> HTTPLogger:
    return HTTPLogger(name)


def _mask_header(name: str, value: str) -> str:
    return '***' if name.lower() in _SENSITIVE_HEADERS else value


def _mask_body(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {
            k: '***' if k.lower() in _SENSITIVE_FIELDS else _mask_body(v)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_mask_body(i) for i in obj]
    return obj


def _decode_body(raw: bytes) -> str:
    if not raw:
        return '<empty>'
    text = raw.decode('utf-8', errors='replace')
    try:
        return json.dumps(_mask_body(json.loads(text)), ensure_ascii=False, indent=2)
    except (ValueError, TypeError):
        return text


def _build_trace(response: httpx.Response) -> str:
    req = response.request
    lines: list[str] = [
        f'\n{"─" * 60}',
        f'[{datetime.now().isoformat(timespec="seconds")}]',
        f'► {req.method} {req.url}',
        'Request Headers:',
        *[f'  {k}: {_mask_header(k, v)}' for k, v in req.headers.items()],
        'Request Body:',
        _decode_body(req.content),
        f'◄ HTTP {response.status_code}  ({response.elapsed.total_seconds():.3f}s)',
        'Response Headers:',
        *[f'  {k}: {_mask_header(k, v)}' for k, v in response.headers.items()],
        'Response Body:',
        _decode_body(response.content),
        '─' * 60,
    ]
    return '\n'.join(lines)


def _attach_to_allure(trace: str) -> None:
    try:
        allure.attach(trace, name='HTTP Trace', attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass

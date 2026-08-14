import importlib.metadata
import json
import os
import platform
import shutil
import sys
import time
from pathlib import Path

from config.settings import get_settings

_PROJECT_ROOT = Path(__file__).parent.parent
_ALLURE_RESULTS = _PROJECT_ROOT / 'reports/allure-results'
_ALLURE_REPORT = _PROJECT_ROOT / 'reports/allure-report'
_EXECUTOR_FILE = _ALLURE_RESULTS / 'executor.json'
_HISTORY_SRC = _ALLURE_REPORT / 'history'
_HISTORY_DST = _ALLURE_RESULTS / 'history'

_METRICS: dict[str, int] = {
    'total': 0, 'passed': 0, 'failed': 0, 'broken': 0, 'skipped': 0,
}
_SESSION_START: float = 0.0


def pytest_configure() -> None:
    _ALLURE_RESULTS.mkdir(parents=True, exist_ok=True)
    _cleanup_results()
    _restore_history()
    _init_history_trend()
    _write_executor()
    _write_environment()


def pytest_sessionstart(session: object) -> None:
    global _SESSION_START
    _SESSION_START = time.time()


def pytest_runtest_logreport(report: object) -> None:
    if report.when != 'call':
        return
    _METRICS['total'] += 1
    if report.passed:
        _METRICS['passed'] += 1
    elif report.failed:
        key = 'failed' if 'AssertionError' in str(getattr(report, 'longrepr', '')) else 'broken'
        _METRICS[key] += 1
    elif report.skipped:
        _METRICS['skipped'] += 1


def pytest_sessionfinish(session: object, exitstatus: int) -> None:
    _update_history_trend()
    os.system(f'allure generate "{_ALLURE_RESULTS}" -o "{_ALLURE_REPORT}" --clean')
    _copy_history_back()
    if 'CI' not in os.environ:
        os.system(f'allure open "{_ALLURE_REPORT}"')


# ── Private helpers ────────────────────────────────────────────────

def _cleanup_results() -> None:
    protected = {'history', 'executor.json', 'environment.properties'}
    for item in _ALLURE_RESULTS.iterdir():
        if item.name not in protected:
            shutil.rmtree(item) if item.is_dir() else item.unlink()


def _restore_history() -> None:
    if _HISTORY_SRC.exists():
        shutil.copytree(_HISTORY_SRC, _HISTORY_DST, dirs_exist_ok=True)


def _init_history_trend() -> None:
    _HISTORY_DST.mkdir(parents=True, exist_ok=True)
    trend = _HISTORY_DST / 'history-trend.json'
    if not trend.exists():
        trend.write_text('[]', encoding='utf-8')


def _next_build_order() -> int:
    trend = _HISTORY_DST / 'history-trend.json'
    try:
        data = json.loads(trend.read_text(encoding='utf-8'))
        return max((e.get('buildOrder', 0) for e in data), default=0) + 1
    except Exception:
        return 1


def _write_executor() -> None:
    order = _next_build_order()
    _EXECUTOR_FILE.write_text(
        json.dumps(
            {
                'buildOrder': order,
                'buildName': f'Run #{order} — {time.strftime("%Y-%m-%d %H:%M")}',
                'reportUrl': f'file://{_ALLURE_REPORT.resolve()}',
                'name': 'Local Pytest',
                'type': 'local',
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding='utf-8',
    )


def _update_history_trend() -> None:
    trend = _HISTORY_DST / 'history-trend.json'
    try:
        data = json.loads(trend.read_text(encoding='utf-8'))
    except Exception:
        data = []
    executor = json.loads(_EXECUTOR_FILE.read_text(encoding='utf-8'))
    data.append(
        {
            **executor,
            **_METRICS,
            'duration': int((time.time() - _SESSION_START) * 1000),
        }
    )
    trend.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def _copy_history_back() -> None:
    if _HISTORY_DST.exists():
        shutil.copytree(_HISTORY_DST, _ALLURE_REPORT / 'history', dirs_exist_ok=True)


def _write_environment() -> None:
    s = get_settings()
    env_name = os.path.splitext(
        os.path.basename(str(s.model_config.get('env_file', 'dev')))
    )[-1].lstrip('.') or 'dev'
    lines = [
        f'Base.URL={s.base_url}',
        f'ENV={env_name}',
        f'Project={s.project}',
        f'Language={s.language}',
        f'Platform={s.platform}',
        f'Manufacturer={s.manufacturer}',
        f'Role={s.role}',
        f'Timeout.sec={s.timeout}',
        f'Python={sys.version.split()[0]}',
        f'Pytest={importlib.metadata.version("pytest")}',
        f'httpx={importlib.metadata.version("httpx")}',
        f'Pydantic={importlib.metadata.version("pydantic")}',
        f'Allure-Pytest={importlib.metadata.version("allure-pytest")}',
        f'OS={platform.system()} {platform.release()}',
        f'Arch={platform.machine()}',
    ]
    (_ALLURE_RESULTS / 'environment.properties').write_text(
        '\n'.join(lines),
        encoding='utf-8',
    )

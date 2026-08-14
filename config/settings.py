from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    """
    All values are loaded from .env.dev.
    Pydantic Settings auto-maps field names to env vars (field → FIELD).
    """
    model_config = SettingsConfigDict(
        env_file='.env.stage',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    # ── Connection ────────────────────────────────────────────────
    base_url: str       # BASE_URL
    timeout: int        # TIMEOUT

    # ── Credentials ───────────────────────────────────────────────
    admin_login: str    # ADMIN_LOGIN
    admin_password: str # ADMIN_PASSWORD

    # ── Default request headers ───────────────────────────────────
    platform: str       # PLATFORM
    manufacturer: str   # MANUFACTURER
    language: str       # LANGUAGE
    project: str        # PROJECT
    role: str           # ROLE

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            'platform': self.platform,
            'manufacturer': self.manufacturer,
            'language': self.language,
            'project': self.project,
            'role': self.role,
        }


@lru_cache(maxsize=1)
def get_settings() -> _Settings:
    return _Settings()

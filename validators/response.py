from typing import Any

import allure
import httpx
import jsonschema
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError


def validate_body_status(response: httpx.Response, expected: str = 'success') -> None:
    with allure.step(f'Response body status = "{expected}"'):
        body = response.json()
        actual = body.get('status')
        assert actual == expected, (
            f'Expected status "{expected}", got "{actual}".\nFull body: {body}'
        )


def validate_model(response: httpx.Response, model: type[BaseModel]) -> None:
    with allure.step(f'Validate Pydantic model: {model.__name__}'):
        try:
            model.model_validate(response.json())
        except PydanticValidationError as exc:
            raise AssertionError(
                f'{model.__name__} validation failed:\n{exc}'
            ) from exc


def validate_schema(response: httpx.Response, schema: dict[str, Any]) -> None:
    with allure.step('Validate JSON schema'):
        try:
            jsonschema.validate(response.json(), schema)
        except jsonschema.ValidationError as exc:
            path = ' → '.join(str(p) for p in exc.absolute_path)
            raise AssertionError(
                f'JSON schema validation failed{f" at {path}" if path else ""}:\n{exc.message}'
            ) from exc

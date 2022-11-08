from typing import Any

from pydantic import BaseModel


def _sanitize_value(
    value: str | int | bool | dict[Any, Any] | list[Any]
) -> str | dict[Any, Any] | list[Any]:
    if isinstance(value, (int, bool)):
        return str(value).lower()

    if isinstance(value, dict):
        return {key: _sanitize_value(item) for key, item in value.items()}

    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]

    return value


class SanitizedBaseModel(BaseModel):
    def dict(self, *, use_sanitization: bool = False, **kwargs) -> dict[str, Any]:  # type: ignore # noqa: E501
        base_object = super().dict(**kwargs)

        return (
            {key: _sanitize_value(item) for key, item in base_object.items()}
            if use_sanitization
            else base_object
        )

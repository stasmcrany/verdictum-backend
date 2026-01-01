"""Модели данных для системы поиска санкций Verdictum."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class SanctionSource(str, Enum):
    """Источник санкционных списков."""

    OFAC = "OFAC"
    EU = "EU"
    UN = "UN"


class SanctionEntity(BaseModel):
    """Модель сущности из санкционного списка.

    Представляет физическое или юридическое лицо, включенное в один из
    санкционных списков (OFAC, EU, UN).
    """

    name: str = Field(
        ...,
        min_length=2,
        description="Полное имя сущности из санкционного списка",
    )
    normalized_name: str = Field(
        ...,
        description="Нормализованное имя в верхнем регистре (UPPERCASE)",
    )
    source: SanctionSource = Field(
        ...,
        description="Источник санкционного списка (OFAC, EU, UN)",
    )
    entity_type: str = Field(
        default="INDIVIDUAL",
        description="Тип сущности (например, INDIVIDUAL, ENTITY)",
    )
    country: Optional[str] = Field(
        default=None,
        description="Страна происхождения или гражданства сущности",
    )
    meta_data: Optional[dict] = Field(
        default=None,
        description="Дополнительные метаданные в виде словаря",
    )

    @field_validator("normalized_name")
    @classmethod
    def validate_normalized_name(cls, v: str) -> str:
        """Проверяет, что normalized_name в верхнем регистре."""
        if v != v.upper():
            raise ValueError("normalized_name должен быть в верхнем регистре (UPPERCASE)")
        return v

    class Config:
        """Конфигурация Pydantic модели."""

        use_enum_values = True
        frozen = False


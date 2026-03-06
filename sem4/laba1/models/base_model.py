from abc import ABC
from typing import Optional
import uuid

class base_model(ABC):
    """Абстрактный базовый класс для всех сущностей с идентификатором."""

    def __init__(self, uid: Optional[str] = None):
        self._uid = uid or str(uuid.uuid4())

    @property
    def uid(self) -> str:
        """Уникальный идентификатор сущности."""
        return self._uid

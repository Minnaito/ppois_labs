from abc import ABC, abstractmethod
from datetime import datetime
from config import constants
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError


class BasePart(ABC):
    def __init__(self, part_id: str, name: str, material: str, weight: float):
        if len(name) < constants.MINIMUM_NAME_LENGTH:
            raise QualityStandardViolationError("Название детали", len(name), f">={constants.MINIMUM_NAME_LENGTH}")
        if weight < constants.MINIMUM_PART_WEIGHT:
            raise QualityStandardViolationError("Вес детали", weight, f">={constants.MINIMUM_PART_WEIGHT}")

        self._part_id = part_id
        self._name = name
        self._material = material
        self._weight = weight
        self._production_date = datetime.now()

    @abstractmethod
    def calculate_cost(self) -> float:
        pass

    @abstractmethod
    def check_quality(self) -> bool:
        pass
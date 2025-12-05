from abc import ABC, abstractmethod
from datetime import datetime
from config import constants
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError  # ← ИСПРАВЛЕНО


class BasePart(ABC):

    def __init__(self, partIdentifier: str, partName: str, materialType: str, partWeight: float):
        self._partIdentifier = partIdentifier
        self._partName = partName
        self._materialType = materialType
        self._partWeight = partWeight
        self._productionDate = datetime.now()
        self._isQualityApproved = False
        self._defectList = []
        self._productionCost = 0.0

        self._validateInitializationParameters()

    def _validateInitializationParameters(self) -> None:
        """Валидация параметров при создании детали"""
        if len(self._partName) < constants.MINIMUM_NAME_LENGTH:
            raise QualityStandardViolationError(
                "Название детали",
                len(self._partName),
                f"минимум {constants.MINIMUM_NAME_LENGTH} символов"
            )

        if self._partWeight < constants.MINIMUM_PART_WEIGHT:
            raise QualityStandardViolationError(
                "Вес детали",
                self._partWeight,
                f"минимум {constants.MINIMUM_PART_WEIGHT}"
            )

    @property
    def partIdentifier(self) -> str:
        """Уникальный идентификатор детали"""
        return self._partIdentifier

    @property
    def partName(self) -> str:
        """Название детали"""
        return self._partName

    @partName.setter
    def partName(self, newName: str) -> None:
        """Установка нового названия детали с валидацией"""
        if len(newName) < constants.MINIMUM_NAME_LENGTH:
            raise QualityStandardViolationError(
                "Название детали",
                len(newName),
                f"минимум {constants.MINIMUM_NAME_LENGTH} символов"
            )
        self._partName = newName

    @abstractmethod
    def calculateProductionCost(self) -> float:
        """Абстрактный метод для расчета стоимости производства"""
        pass

    @abstractmethod
    def performQualityCheck(self) -> bool:
        """Абстрактный метод для проверки качества"""
        pass

    def approveQuality(self) -> None:
        """Одобрить деталь после проверки качества"""
        self._isQualityApproved = True

    def addDefect(self, defectDescription: str) -> None:
        """Добавить дефект к детали"""
        self._defectList.append(defectDescription)
        self._isQualityApproved = False

    def getDefectList(self) -> list:
        """Получить список дефектов"""
        return self._defectList.copy()

    def __str__(self) -> str:
        return f"{self._partName} (ID: {self._partIdentifier}, Материал: {self._materialType})"

    def __repr__(self) -> str:
        return f"BasePart(partIdentifier='{self._partIdentifier}', partName='{self._partName}')"
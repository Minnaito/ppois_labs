from models.production.CarPart import CarPart
from config import constants


class QualityStandard:

    def __init__(self, standardIdentifier: str, standardName: str, expectedValueRange: str):
        self._standardIdentifier = standardIdentifier
        self._standardName = standardName
        self._expectedValueRange = expectedValueRange
        self._severityLevel = "MEDIUM"
        self._testMethod = ""
        self._applicableParts = []

    @property
    def standardIdentifier(self) -> str:
        """Идентификатор стандарта"""
        return self._standardIdentifier

    @property
    def standardName(self) -> str:
        """Название стандарта"""
        return self._standardName

    @property
    def expectedValueRange(self) -> str:
        """Ожидаемый диапазон значений"""
        return self._expectedValueRange

    def checkCompliance(self, carPart: CarPart) -> bool:
        """Проверка соответствия детали стандарту"""
        return True

    def setSeverityLevel(self, severity: str) -> None:
        """Установка уровня серьезности"""
        validSeverities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        if severity in validSeverities:
            self._severityLevel = severity

    def setTestMethod(self, testMethod: str) -> None:
        """Установка метода тестирования"""
        self._testMethod = testMethod

    def addApplicablePart(self, partType: str) -> None:
        """Добавление типа детали, к которой применим стандарт"""
        self._applicableParts.append(partType)

    def isApplicableToPart(self, partType: str) -> bool:
        """Проверка применимости стандарта к типу детали"""
        return partType in self._applicableParts or not self._applicableParts

    def getStandardInfo(self) -> dict:
        """Получение информации о стандарте"""
        return {
            "standardIdentifier": self._standardIdentifier,
            "standardName": self._standardName,
            "expectedValueRange": self._expectedValueRange,
            "severityLevel": self._severityLevel,
            "testMethod": self._testMethod,
            "applicablePartsCount": len(self._applicableParts)
        }
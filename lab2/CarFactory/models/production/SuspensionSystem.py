from models.production.CarPart import CarPart
from config import constants
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError


class SuspensionSystem(CarPart):

    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, suspensionType: str, springRate: float):
        super().__init__(partIdentifier, partName, materialType, partWeight, "Suspension")
        self._suspensionType = suspensionType
        self._springRate = springRate
        self._dampingForce = 0.0
        self._travelLengthMm = 0.0
        self._adjustableStiffness = False

    def calculateProductionCost(self) -> float:
        """Расчет стоимости производства подвески"""
        baseProductionCost = super().calculateProductionCost()

        springRateCostComponent = self._springRate * 8
        suspensionTypeCostComponent = len(self._suspensionType) * 30

        suspensionSpecificCost = springRateCostComponent + suspensionTypeCostComponent
        totalSuspensionCost = baseProductionCost + suspensionSpecificCost

        return totalSuspensionCost

    def performQualityCheck(self) -> bool:
        """Проверка качества подвески"""
        super().performQualityCheck()

        self._validateSpringRate()

        return True

    def _validateSpringRate(self) -> None:
        """Валидация жесткости пружины"""
        if self._springRate <= constants.ZERO_VALUE:
            raise QualityStandardViolationError(
                "Жесткость пружины",
                self._springRate,
                "положительное значение"
            )

    def calculateComfortIndex(self) -> float:
        """Расчет индекса комфорта"""
        comfortBaseValue = 100
        comfortIndex = comfortBaseValue / (self._springRate + 1)
        return comfortIndex

    def setDampingForce(self, newDampingForce: float) -> None:
        """Установка силы демпфирования"""
        self._dampingForce = newDampingForce

    def adjustStiffness(self, stiffnessLevel: int) -> bool:
        """Регулировка жесткости подвески"""
        if self._adjustableStiffness and 1 <= stiffnessLevel <= 10:
            adjustedSpringRate = self._springRate * (stiffnessLevel / 5)
            self._springRate = adjustedSpringRate
            return True
        return False

    def getSuspensionSpecifications(self) -> dict:
        """Получить спецификации подвески"""
        suspensionSpecifications = {
            "suspensionType": self._suspensionType,
            "springRate": self._springRate,
            "dampingForce": self._dampingForce,
            "travelLengthMm": self._travelLengthMm,
            "comfortIndex": self.calculateComfortIndex(),
            "adjustableStiffness": self._adjustableStiffness
        }
        return suspensionSpecifications
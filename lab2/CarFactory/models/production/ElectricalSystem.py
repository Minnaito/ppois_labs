from models.production.CarPart import CarPart
from config import constants
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError


class ElectricalSystem(CarPart):

    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, systemVoltage: float, currentRating: float):
        super().__init__(partIdentifier, partName, materialType, partWeight, "ElectricalSystem")
        self._systemVoltage = systemVoltage
        self._currentRating = currentRating
        self._wireGauge = 2.5
        self._insulationType = "PVC"
        self._batteryCapacity = 0.0

    def calculateProductionCost(self) -> float:
        """Расчет стоимости производства электрической системы"""
        baseProductionCost = super().calculateProductionCost()

        voltageCostComponent = self._systemVoltage * 2
        currentCostComponent = self._currentRating * 5

        electricalSpecificCost = voltageCostComponent + currentCostComponent
        totalElectricalCost = baseProductionCost + electricalSpecificCost

        return totalElectricalCost

    def performQualityCheck(self) -> bool:
        """Проверка качества электрической системы"""
        super().performQualityCheck()

        self._validateVoltageRange()

        return True

    def _validateVoltageRange(self) -> None:
        """Валидация диапазона напряжения"""
        if (self._systemVoltage < constants.MIN_VOLTAGE or
                self._systemVoltage > constants.MAX_VOLTAGE):
            raise QualityStandardViolationError(
                "Напряжение системы",
                self._systemVoltage,
                f"{constants.MIN_VOLTAGE}-{constants.MAX_VOLTAGE}V"
            )

    def calculatePowerCapacity(self) -> float:
        """Расчет мощности системы"""
        powerCapacity = self._systemVoltage * self._currentRating
        return powerCapacity

    def changeInsulationType(self, newInsulationType: str) -> None:
        """Изменение типа изоляции"""
        self._insulationType = newInsulationType

    def setBatteryCapacity(self, batteryCapacity: float) -> None:
        """Установка емкости батареи"""
        self._batteryCapacity = batteryCapacity

    def getElectricalSpecifications(self) -> dict:
        """Получить спецификации электрической системы"""
        electricalSpecifications = {
            "systemVoltage": self._systemVoltage,
            "currentRating": self._currentRating,
            "powerCapacity": self.calculatePowerCapacity(),
            "insulationType": self._insulationType,
            "batteryCapacity": self._batteryCapacity,
            "wireGauge": self._wireGauge
        }
        return electricalSpecifications
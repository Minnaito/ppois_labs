from models.production.CarPart import CarPart
from config import constants
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError  # ← ИСПРАВЛЕНО


class Transmission(CarPart):

    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, transmissionType: str, gearCount: int):
        super().__init__(partIdentifier, partName, materialType, partWeight, "Transmission")
        self._transmissionType = transmissionType
        self._gearCount = gearCount
        self._maximumTorqueCapacity = 0
        self._efficiencyRating = 0.0
        self._currentGear = 1

    def calculateProductionCost(self) -> float:
        """Расчет стоимости производства трансмиссии"""
        baseProductionCost = super().calculateProductionCost()

        gearCostComponent = self._gearCount * 80
        transmissionTypeCostComponent = len(self._transmissionType) * 25

        transmissionSpecificCost = gearCostComponent + transmissionTypeCostComponent
        totalTransmissionCost = baseProductionCost + transmissionSpecificCost

        return totalTransmissionCost

    def performQualityCheck(self) -> bool:
        """Проверка качества трансмиссии"""
        super().performQualityCheck()

        self._validateGearCount()

        return True

    def _validateGearCount(self) -> None:
        """Валидация количества передач"""
        if (self._gearCount < constants.MIN_TRANSMISSION_GEARS or
                self._gearCount > constants.MAX_TRANSMISSION_GEARS):
            raise QualityStandardViolationError(
                "Количество передач",
                self._gearCount,
                f"{constants.MIN_TRANSMISSION_GEARS}-{constants.MAX_TRANSMISSION_GEARS}"
            )

    def setMaximumTorqueCapacity(self, torqueCapacity: int) -> None:
        """Установка максимальной емкости крутящего момента"""
        self._maximumTorqueCapacity = torqueCapacity

    def calculateEfficiency(self, loadFactor: float) -> float:
        """Расчет эффективности трансмиссии"""
        baseEfficiency = 0.85
        efficiencyLossPerLoad = 0.1

        calculatedEfficiency = baseEfficiency - (loadFactor * efficiencyLossPerLoad)
        self._efficiencyRating = max(calculatedEfficiency, constants.ZERO_VALUE)

        return self._efficiencyRating

    def shiftGear(self, targetGear: int) -> bool:
        """Переключение передачи"""
        if 1 <= targetGear <= self._gearCount:
            self._currentGear = targetGear
            return True
        return False

    def getTransmissionSpecifications(self) -> dict:
        """Получить спецификации трансмиссии"""
        transmissionSpecifications = {
            "transmissionType": self._transmissionType,
            "gearCount": self._gearCount,
            "maximumTorqueCapacity": self._maximumTorqueCapacity,
            "efficiencyRating": self._efficiencyRating,
            "currentGear": self._currentGear
        }
        return transmissionSpecifications
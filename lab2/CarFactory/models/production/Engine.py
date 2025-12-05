from models.production.CarPart import CarPart
from config import constants
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError

class Engine(CarPart):
    """Класс двигателя автомобиля"""

    def __init__(self, partIdentifier, partName, materialType, partWeight, horsepower, cylinderCount, fuelType):
        super().__init__(partIdentifier, partName, materialType, partWeight, "Engine")
        self._horsepower = horsepower
        self._cylinderCount = cylinderCount
        self._fuelType = fuelType

    def calculateProductionCost(self):
        baseCost = super().calculateProductionCost()
        horsepowerCost = self._horsepower * 50
        cylinderCost = self._cylinderCount * 100
        return baseCost + horsepowerCost + cylinderCost

    def performQualityCheck(self):
        super().performQualityCheck()
        self._validateHorsepower()
        self._validateCylinderCount()
        return True

    def _validateHorsepower(self):
        if (self._horsepower < constants.MIN_ENGINE_HORSEPOWER or
            self._horsepower > constants.MAX_ENGINE_HORSEPOWER):
            raise QualityStandardViolationError(
                "Мощность двигателя",
                self._horsepower,
                f"{constants.MIN_ENGINE_HORSEPOWER}-{constants.MAX_ENGINE_HORSEPOWER}"
            )

    def _validateCylinderCount(self):
        if self._cylinderCount not in constants.VALID_ENGINE_CYLINDERS:
            raise QualityStandardViolationError(
                "Количество цилиндров",
                self._cylinderCount,
                str(constants.VALID_ENGINE_CYLINDERS)
            )

    def calculatePowerToWeightRatio(self):
        if self._partWeight > constants.ZERO_VALUE:
            return self._horsepower / self._partWeight
        return constants.ZERO_VALUE

    def getEngineSpecifications(self):
        baseSpecs = self.getPartSpecifications()
        engineSpecs = {
            "horsepower": self._horsepower,
            "cylinderCount": self._cylinderCount,
            "fuelType": self._fuelType,
            "powerToWeightRatio": self.calculatePowerToWeightRatio()
        }
        return {**baseSpecs, **engineSpecs}
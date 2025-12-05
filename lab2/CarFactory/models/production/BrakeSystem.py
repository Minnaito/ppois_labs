from models.production.CarPart import CarPart
from config import constants
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError


class BrakeSystem(CarPart):

    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, brakeType: str, discDiameter: float):
        super().__init__(partIdentifier, partName, materialType, partWeight, "BrakeSystem")
        self._brakeType = brakeType
        self._discDiameter = discDiameter
        self._padThicknessMm = 12.0
        self._brakeFluidType = "DOT4"
        self._isAbsEnabled = True

    def calculateProductionCost(self) -> float:
        """Расчет стоимости производства тормозной системы"""
        baseProductionCost = super().calculateProductionCost()

        discDiameterCostComponent = self._discDiameter * 15
        brakeTypeCostComponent = len(self._brakeType) * 20

        brakeSpecificCost = discDiameterCostComponent + brakeTypeCostComponent
        totalBrakeCost = baseProductionCost + brakeSpecificCost

        return totalBrakeCost

    def performQualityCheck(self) -> bool:
        """Проверка качества тормозной системы"""
        super().performQualityCheck()

        self._validateDiscDiameter()

        return True

    def _validateDiscDiameter(self) -> None:
        """Валидация диаметра тормозного диска"""
        if (self._discDiameter < constants.MIN_BRAKE_DISC_DIAMETER or
                self._discDiameter > constants.MAX_BRAKE_DISC_DIAMETER):
            raise QualityStandardViolationError(
                "Диаметр тормозного диска",
                self._discDiameter,
                f"{constants.MIN_BRAKE_DISC_DIAMETER}-{constants.MAX_BRAKE_DISC_DIAMETER} мм"
            )

    def calculateStoppingPower(self, vehicleSpeed: float) -> float:
        """Расчет тормозной мощности"""
        diameterComponent = self._discDiameter * self._padThicknessMm
        speedComponent = vehicleSpeed + 1

        stoppingPowerValue = diameterComponent / speedComponent
        return stoppingPowerValue

    def changeBrakeFluidType(self, newFluidType: str) -> None:
        """Изменение типа тормозной жидкости"""
        self._brakeFluidType = newFluidType

    def toggleAbsSystem(self, absEnabled: bool) -> None:
        """Включение/выключение ABS системы"""
        self._isAbsEnabled = absEnabled

    def getBrakeSystemSpecifications(self) -> dict:
        """Получить спецификации тормозной системы"""
        brakeSpecifications = {
            "brakeType": self._brakeType,
            "discDiameterMm": self._discDiameter,
            "padThicknessMm": self._padThicknessMm,
            "brakeFluidType": self._brakeFluidType,
            "absEnabled": self._isAbsEnabled
        }
        return brakeSpecifications

    def __str__(self) -> str:
        return f"{self._partName} ({self._brakeType}, Диаметр: {self._discDiameter}мм)"

    def __repr__(self) -> str:
        return f"BrakeSystem(partIdentifier='{self._partIdentifier}', brakeType='{self._brakeType}')"
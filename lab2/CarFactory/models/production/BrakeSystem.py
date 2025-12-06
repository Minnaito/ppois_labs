from models.production.CarPart import CarPart
from config import constants

class BrakeSystem(CarPart):
    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, brakeType: str, discDiameter: float):
        super().__init__(partIdentifier, partName, materialType, partWeight, "BrakeSystem")
        self._brakeType = brakeType
        self._discDiameter = discDiameter

    def calculateProductionCost(self) -> float:
        baseCost = super().calculateProductionCost()
        diameterCost = self._discDiameter * 15
        return baseCost + diameterCost

    def performQualityCheck(self) -> bool:
        super().performQualityCheck()
        return 200 <= self._discDiameter <= 400
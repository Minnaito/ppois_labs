from models.production.CarPart import CarPart
from config import constants

class SuspensionSystem(CarPart):
    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, suspensionType: str):
        super().__init__(partIdentifier, partName, materialType, partWeight, "SuspensionSystem")
        self._suspensionType = suspensionType

    def calculateProductionCost(self) -> float:
        baseCost = super().calculate_cost()
        typeCost = len(self._suspensionType) * constants.SUSPENSION_TYPE_COST_FACTOR
        return baseCost + typeCost

    def performQualityCheck(self) -> bool:
        super().check_quality()
        return self._suspensionType in constants.VALID_SUSPENSION_TYPES

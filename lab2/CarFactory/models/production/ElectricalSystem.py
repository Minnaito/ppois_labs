from models.production.CarPart import CarPart
from config import constants

class ElectricalSystem(CarPart):
    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, systemVoltage: float):
        super().__init__(partIdentifier, partName, materialType, partWeight)  # ← 4 параметра!
        self._systemVoltage = systemVoltage

    def calculateProductionCost(self) -> float:
        baseCost = super().calculate_cost()
        voltageCost = self._systemVoltage * 2
        return baseCost + voltageCost

    def performQualityCheck(self) -> bool:
        super().check_quality()
        return 12 <= self._systemVoltage <= 48

    def getElectricalSpecifications(self) -> dict:
        return {
            "systemVoltage": self._systemVoltage
        }
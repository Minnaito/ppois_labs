from models.production.CarPart import CarPart
from config import constants

class Transmission(CarPart):
    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, transmissionType: str, gearCount: int):
        super().__init__(partIdentifier, partName, materialType, partWeight, "Transmission")
        self._transmissionType = transmissionType
        self._gearCount = gearCount

    def calculateProductionCost(self) -> float:
        baseCost = super().calculateProductionCost()
        gearCost = self._gearCount * 80
        return baseCost + gearCost

    def performQualityCheck(self) -> bool:
        super().performQualityCheck()
        return 4 <= self._gearCount <= 10

    def getTransmissionSpecifications(self) -> dict:
        return {
            "transmissionType": self._transmissionType,
            "gearCount": self._gearCount
        }
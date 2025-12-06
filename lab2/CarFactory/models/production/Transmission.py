from models.production.CarPart import CarPart
from config import constants

class Transmission(CarPart):
    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, transmissionType: str, gearCount: int):
        super().__init__(partIdentifier, partName, materialType, partWeight, "Transmission")
        self._transmissionType = transmissionType
        self._gearCount = gearCount

    def calculateProductionCost(self) -> float:
        baseCost = super().calculate_cost() 
        gearCost = self._gearCount * constants.TRANSMISSION_GEAR_COST_FACTOR
        return baseCost + gearCost

    def performQualityCheck(self) -> bool:
        super().check_quality() 
        return (constants.MIN_TRANSMISSION_GEARS <= self._gearCount <= 
                constants.MAX_TRANSMISSION_GEARS)

    def getTransmissionSpecifications(self) -> dict:
        return {
            "transmissionType": self._transmissionType,
            "gearCount": self._gearCount,
            "min_allowed_gears": constants.MIN_TRANSMISSION_GEARS,
            "max_allowed_gears": constants.MAX_TRANSMISSION_GEARS,
            "gear_cost_factor": constants.TRANSMISSION_GEAR_COST_FACTOR
        }

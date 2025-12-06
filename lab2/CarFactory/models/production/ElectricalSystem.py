from models.production.CarPart import CarPart
from config import constants

class ElectricalSystem(CarPart):
    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, systemVoltage: float):
        # CarPart ожидает 5 параметров, добавляем тип системы
        super().__init__(partIdentifier, partName, materialType, partWeight, "ElectricalSystem")
        self._systemVoltage = systemVoltage

    def calculateProductionCost(self) -> float:
        baseCost = super().calculate_cost()
        voltageCost = self._systemVoltage * constants.ELECTRICAL_VOLTAGE_COST_FACTOR
        return baseCost + voltageCost

    def performQualityCheck(self) -> bool:
        super().check_quality()
        return (constants.MIN_ELECTRICAL_VOLTAGE <= self._systemVoltage <= 
                constants.MAX_ELECTRICAL_VOLTAGE)

    def getElectricalSpecifications(self) -> dict:
        return {
            "systemVoltage": self._systemVoltage,
            "min_allowed_voltage": constants.MIN_ELECTRICAL_VOLTAGE,
            "max_allowed_voltage": constants.MAX_ELECTRICAL_VOLTAGE,
            "voltage_cost_factor": constants.ELECTRICAL_VOLTAGE_COST_FACTOR
        }

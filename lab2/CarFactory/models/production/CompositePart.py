from models.production.CarPart import CarPart
from config import constants


class CompositePart(CarPart):
    """Составная деталь"""

    def __init__(self, partIdentifier: str, partName: str, materialType: str, partWeight: float):
        super().__init__(partIdentifier, partName, materialType, partWeight) 
        self._childParts = []

    def addChild(self, part):
        """Добавить дочернюю деталь"""
        self._childParts.append(part)
        return True

    def calculateProductionCost(self) -> float:
        base = super().calculate_cost()
        child_cost = len(self._childParts) * constants.COMPOSITE_CHILD_COST_FACTOR
        return base + child_cost

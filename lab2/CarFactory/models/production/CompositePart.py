from models.production.CarPart import CarPart


class CompositePart(CarPart):
    """Составная деталь"""

    def __init__(self, partIdentifier: str, partName: str, materialType: str, partWeight: float):
        super().__init__(partIdentifier, partName, materialType, partWeight)  # ← 4 параметра!
        self._childParts = []

    def addChild(self, part):
        """Добавить дочернюю деталь"""
        self._childParts.append(part)
        return True

    def calculateProductionCost(self) -> float:
        base = super().calculate_cost()
        return base + len(self._childParts) * 10
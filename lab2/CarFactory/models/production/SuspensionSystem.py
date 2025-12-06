from models.production.CarPart import CarPart

class SuspensionSystem(CarPart):
    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, suspensionType: str):
        super().__init__(partIdentifier, partName, materialType, partWeight)  # ← 4 параметра!
        self._suspensionType = suspensionType

    def calculateProductionCost(self) -> float:
        baseCost = super().calculate_cost()
        typeCost = len(self._suspensionType) * 30
        return baseCost + typeCost

    def performQualityCheck(self) -> bool:
        super().check_quality()
        return self._suspensionType in ["независимая", "зависимая", "independent", "dependent"]
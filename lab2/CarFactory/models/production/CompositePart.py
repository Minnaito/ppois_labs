from typing import List
from models.production.CarPart import CarPart


class CompositePart(CarPart):

    def __init__(self, partIdentifier: str, partName: str,
                 materialType: str, partWeight: float):
        super().__init__(partIdentifier, partName, materialType, partWeight, "Composite")
        self._childParts: List[CarPart] = []
        self._assemblyComplexity = 1.0

    def addChildPart(self, part: CarPart) -> None:
        """Добавление дочерней детали"""
        self._childParts.append(part)
        self._partWeight += part._partWeight

    def removeChildPart(self, partIdentifier: str) -> bool:
        """Удаление дочерней детали"""
        for part in self._childParts:
            if part.partIdentifier == partIdentifier:
                self._childParts.remove(part)
                self._partWeight -= part._partWeight
                return True
        return False

    def calculateProductionCost(self) -> float:
        """Расчет стоимости составной детали"""
        baseCost = super().calculateProductionCost()
        childrenCost = sum(part.calculateProductionCost() for part in self._childParts)
        assemblyCost = len(self._childParts) * 10 * self._assemblyComplexity

        return baseCost + childrenCost + assemblyCost

    def performQualityCheck(self) -> bool:
        """Проверка качества всех дочерних деталей"""
        if not super().performQualityCheck():
            return False

        for part in self._childParts:
            try:
                if not part.performQualityCheck():
                    return False
            except Exception:
                return False

        return True

    def getCompositeStructure(self) -> dict:
        """Получение структуры составной детали"""
        return {
            "compositeId": self._partIdentifier,
            "totalChildren": len(self._childParts),
            "totalWeight": self._partWeight,
            "children": [part.getPartSpecifications() for part in self._childParts]
        }
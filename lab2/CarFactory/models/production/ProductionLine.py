from config import constants
from exceptions.ProductionExceptions.ProductionCapacityExceededError import ProductionCapacityExceededError

class ProductionLine:

    def __init__(self, lineIdentifier, lineName, maximumCapacity):
        self._lineIdentifier = lineIdentifier
        self._lineName = lineName
        self._maximumCapacity = maximumCapacity
        self._currentProductionCount = 0
        self._assignedOperators = []
        self._isProductionActive = False

    def startProductionLine(self):
        """Запуск производственной линии"""
        self._isProductionActive = True
        return f"Линия {self._lineName} запущена"

    def stopProductionLine(self):
        """Остановка производственной линии"""
        self._isProductionActive = False
        return f"Линия {self._lineName} остановлена"

    def addOperator(self, machineOperator):
        """Добавление оператора на линию"""
        self._assignedOperators.append(machineOperator)

    def produceParts(self, partTemplate, quantity):
        """Производство деталей"""
        if not self._isProductionActive:
            raise Exception("Производственная линия не активна")

        totalAfterProduction = self._currentProductionCount + quantity
        if totalAfterProduction > self._maximumCapacity:
            raise ProductionCapacityExceededError(totalAfterProduction, self._maximumCapacity)

        producedParts = []
        for i in range(quantity):
            # Создаем копию детали
            newPart = type(partTemplate)(
                f"{partTemplate.partIdentifier}_{self._currentProductionCount + i + 1}",
                partTemplate.partName,
                partTemplate._materialType,
                partTemplate._partWeight,
                partTemplate._partCategory
            )
            producedParts.append(newPart)

        self._currentProductionCount += quantity
        return producedParts

    def getProductionStatistics(self):
        """Получение статистики производства"""
        return {
            "lineIdentifier": self._lineIdentifier,
            "lineName": self._lineName,
            "currentProduction": self._currentProductionCount,
            "maximumCapacity": self._maximumCapacity,
            "operatorCount": len(self._assignedOperators),
            "isActive": self._isProductionActive
        }
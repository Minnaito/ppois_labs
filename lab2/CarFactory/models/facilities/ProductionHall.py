from config import constants


class ProductionHall:

    def __init__(self, hallId: str, hallName: str, buildingId: str, area: float):
        self._hallId = hallId
        self._hallName = hallName
        self._buildingId = buildingId
        self._area = area
        self._productionLinesCount = 0
        self._maxCapacity = 0
        self._currentUtilization = 0.0
        self._temperatureControlled = False
        self._safetyRating = "HIGH"

    def addProductionLine(self) -> None:
        """Добавление производственной линии"""
        self._productionLinesCount += 1

    def removeProductionLine(self) -> bool:
        """Удаление производственной линии"""
        if self._productionLinesCount > 0:
            self._productionLinesCount -= 1
            return True
        return False

    def calculateUtilizationPercentage(self) -> float:
        """Расчет процента использования цеха"""
        if self._maxCapacity > 0:
            utilization = (self._currentUtilization / self._maxCapacity)
            return utilization * constants.PERCENTAGE_MULTIPLIER
        return 0.0

    def setMaxCapacity(self, capacity: int) -> None:
        """Установка максимальной мощности"""
        if capacity >= 0:
            self._maxCapacity = capacity

    def updateUtilization(self, utilization: float) -> None:
        """Обновление текущей загрузки"""
        if 0 <= utilization <= self._maxCapacity:
            self._currentUtilization = utilization

    def getHallStatistics(self) -> dict:
        """Получение статистики цеха"""
        return {
            "hallId": self._hallId,
            "hallName": self._hallName,
            "buildingId": self._buildingId,
            "areaSqM": self._area,
            "productionLinesCount": self._productionLinesCount,
            "maxCapacity": self._maxCapacity,
            "currentUtilization": self._currentUtilization,
            "utilizationPercentage": self.calculateUtilizationPercentage(),
            "temperatureControlled": self._temperatureControlled,
            "safetyRating": self._safetyRating
        }

    def __str__(self) -> str:
        return f"Цех {self._hallName} ({self._productionLinesCount} линий)"
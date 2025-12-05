from config import constants


class FactoryBuilding:

    def __init__(self, buildingId: str, buildingName: str, totalArea: float,
                 constructionYear: int, buildingType: str):
        self._buildingId = buildingId
        self._buildingName = buildingName
        self._totalArea = totalArea
        self._constructionYear = constructionYear
        self._buildingType = buildingType
        self._floorsCount = 1
        self._isOperational = True
        self._maintenanceSchedule = ""
        self._energyConsumptionKwh = 0.0

    def calculateBuildingAge(self, currentYear: int) -> int:
        """Расчет возраста здания"""
        return currentYear - self._constructionYear

    def setFloorsCount(self, floors: int) -> None:
        """Установка количества этажей"""
        if floors > 0:
            self._floorsCount = floors

    def calculateAreaPerFloor(self) -> float:
        """Расчет площади на этаж"""
        if self._floorsCount > 0:
            return self._totalArea / self._floorsCount
        return self._totalArea

    def updateEnergyConsumption(self, consumption: float) -> None:
        """Обновление потребления энергии"""
        if consumption >= 0:
            self._energyConsumptionKwh = consumption

    def getBuildingInfo(self) -> dict:
        """Получение информации о здании"""
        return {
            "buildingId": self._buildingId,
            "buildingName": self._buildingName,
            "totalAreaSqM": self._totalArea,
            "constructionYear": self._constructionYear,
            "buildingType": self._buildingType,
            "floorsCount": self._floorsCount,
            "areaPerFloor": self.calculateAreaPerFloor(),
            "isOperational": self._isOperational,
            "energyConsumptionKwh": self._energyConsumptionKwh
        }

    def __str__(self) -> str:
        return f"Здание {self._buildingName} ({self._buildingType}, {self._totalArea} м²)"
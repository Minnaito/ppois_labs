from config import constants


class StorageFacility:

    def __init__(self, facilityId: str, facilityName: str, facilityType: str,
                 totalCapacity: int, temperatureControlled: bool):
        self._facilityId = facilityId
        self._facilityName = facilityName
        self._facilityType = facilityType
        self._totalCapacity = totalCapacity
        self._temperatureControlled = temperatureControlled
        self._currentStock = 0
        self._securityLevel = "STANDARD"
        self._storageZones = []
        self._operatingTemperature = ""

    def updateStockLevel(self, newStock: int) -> bool:
        """Обновление уровня запасов"""
        if 0 <= newStock <= self._totalCapacity:
            self._currentStock = newStock
            return True
        return False

    def calculateAvailableCapacity(self) -> int:
        """Расчет доступной емкости"""
        return self._totalCapacity - self._currentStock

    def calculateUtilizationPercentage(self) -> float:
        """Расчет процента использования"""
        if self._totalCapacity > 0:
            utilization = (self._currentStock / self._totalCapacity)
            return utilization * constants.PERCENTAGE_MULTIPLIER
        return 0.0

    def addStorageZone(self, zoneName: str) -> None:
        """Добавление зоны хранения"""
        self._storageZones.append(zoneName)

    def setOperatingTemperature(self, temperature: str) -> None:
        """Установка рабочей температуры"""
        if self._temperatureControlled:
            self._operatingTemperature = temperature

    def getFacilityInfo(self) -> dict:
        """Получение информации о складе"""
        return {
            "facilityId": self._facilityId,
            "facilityName": self._facilityName,
            "facilityType": self._facilityType,
            "totalCapacity": self._totalCapacity,
            "currentStock": self._currentStock,
            "availableCapacity": self.calculateAvailableCapacity(),
            "utilizationPercentage": self.calculateUtilizationPercentage(),
            "temperatureControlled": self._temperatureControlled,
            "operatingTemperature": self._operatingTemperature,
            "securityLevel": self._securityLevel,
            "storageZonesCount": len(self._storageZones)
        }

    def __str__(self) -> str:
        return f"Склад {self._facilityName} ({self._facilityType}, {self.calculateUtilizationPercentage():.1f}% загружен)"
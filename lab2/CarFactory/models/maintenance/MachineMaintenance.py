from datetime import datetime
from config import constants
from exceptions.ProductionExceptions.MachineMaintenanceRequiredError import MachineMaintenanceRequiredError


class MachineMaintenance:

    def __init__(self, maintenanceId: str, machineId: str, maintenanceType: str):
        self._maintenanceId = maintenanceId
        self._machineId = machineId
        self._maintenanceType = maintenanceType
        self._maintenanceDate = datetime.now().strftime("%Y-%m-%d")
        self._technicianId = ""
        self._durationHours = 0.0
        self._cost = 0.0
        self._status = "SCHEDULED"
        self._partsUsed = []

    @property
    def machineIdentifier(self) -> str:
        """Идентификатор станка"""
        return self._machineId

    def assignTechnician(self, technicianId: str) -> None:
        """Назначение техника на обслуживание"""
        self._technicianId = technicianId
        self._status = "ASSIGNED"

    def startMaintenance(self) -> None:
        """Начало обслуживания"""
        self._status = "IN_PROGRESS"

    def completeMaintenanceTask(self) -> None:
        """Завершение обслуживания"""
        if self._status != "IN_PROGRESS":
            raise MachineMaintenanceRequiredError(self._machineId, "maintenance_not_started")

        self._status = "COMPLETED"

    def calculateMaintenanceCost(self, hourlyRate: float) -> float:
        """Расчет стоимости обслуживания"""
        laborCost = self._durationHours * hourlyRate
        partsCost = sum(part["cost"] for part in self._partsUsed)
        self._cost = laborCost + partsCost
        return self._cost

    def addUsedPart(self, partName: str, quantity: int, cost: float) -> None:
        """Добавление использованной детали"""
        part = {
            "partName": partName,
            "quantity": quantity,
            "cost": cost
        }
        self._partsUsed.append(part)

    def setDuration(self, hours: float) -> None:
        """Установка продолжительности обслуживания"""
        if hours > constants.ZERO_VALUE:
            self._durationHours = hours

    def getMaintenanceReport(self) -> dict:
        """Получение отчета по обслуживанию"""
        return {
            "maintenanceId": self._maintenanceId,
            "machineId": self._machineId,
            "maintenanceType": self._maintenanceType,
            "maintenanceDate": self._maintenanceDate,
            "technicianId": self._technicianId,
            "durationHours": self._durationHours,
            "cost": self._cost,
            "status": self._status,
            "partsUsedCount": len(self._partsUsed)
        }

    def isUrgentMaintenance(self) -> bool:
        """Проверка срочности обслуживания"""
        urgentTypes = ["EMERGENCY", "CRITICAL", "BREAKDOWN"]
        return self._maintenanceType in urgentTypes

    def __str__(self) -> str:
        return f"Обслуживание {self._maintenanceId} для станка {self._machineId} ({self._status})"
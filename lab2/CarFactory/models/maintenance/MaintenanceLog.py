from datetime import datetime
from typing import List
from config import constants


class MaintenanceLog:

    def __init__(self, logId: str):
        self._logId = logId
        self._maintenanceEntries = []
        self._totalMaintenanceHours = 0.0
        self._totalMaintenanceCost = 0.0
        self._machineDowntimeHours = 0.0
        self._preventiveMaintenanceCount = 0
        self._correctiveMaintenanceCount = 0

    def addMaintenanceEntry(self, machineId: str, maintenanceType: str,
                              durationHours: float, cost: float, technicianId: str) -> None:
        """Добавление записи о обслуживании"""
        entry = {
            "entryId": f"ENTRY_{len(self._maintenanceEntries) + 1:03d}",
            "machineId": machineId,
            "maintenanceType": maintenanceType,
            "durationHours": durationHours,
            "cost": cost,
            "technicianId": technicianId,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": f"{maintenanceType} обслуживание станка {machineId}"
        }

        self._maintenanceEntries.append(entry)
        self._totalMaintenanceHours += durationHours
        self._totalMaintenanceCost += cost

        if maintenanceType == "PREVENTIVE":
            self._preventiveMaintenanceCount += 1
        elif maintenanceType == "CORRECTIVE":
            self._correctiveMaintenanceCount += 1

    def getMachineMaintenanceHistory(self, machineId: str) -> List[dict]:
        """Получение истории обслуживания конкретного станка"""
        return [entry for entry in self._maintenanceEntries
                if entry["machineId"] == machineId]

    def calculateMaintenanceEfficiency(self) -> float:
        """Расчет эффективности обслуживания"""
        totalMaintenanceCount = len(self._maintenanceEntries)
        if totalMaintenanceCount > constants.ZERO_VALUE:
            preventiveRatio = self._preventiveMaintenanceCount / totalMaintenanceCount
            efficiency = preventiveRatio * constants.PERCENTAGE_MULTIPLIER
            return efficiency
        return constants.ZERO_VALUE

    def getTotalDowntime(self) -> float:
        """Получение общего времени простоя"""
        return self._machineDowntimeHours

    def addDowntime(self, downtimeHours: float) -> None:
        """Добавление времени простоя"""
        if downtimeHours > constants.ZERO_VALUE:
            self._machineDowntimeHours += downtimeHours

    def getCostAnalysis(self) -> dict:
        """Получение анализа затрат на обслуживание"""
        preventiveCost = sum(entry["cost"] for entry in self._maintenanceEntries
                              if entry["maintenanceType"] == "PREVENTIVE")
        correctiveCost = sum(entry["cost"] for entry in self._maintenanceEntries
                              if entry["maintenanceType"] == "CORRECTIVE")

        return {
            "totalCost": self._totalMaintenanceCost,
            "preventiveCost": preventiveCost,
            "correctiveCost": correctiveCost,
            "costSavingsPercentage": self._calculateCostSavings(preventiveCost, correctiveCost)
        }

    def _calculateCostSavings(self, preventiveCost: float, correctiveCost: float) -> float:
        """Расчет экономии от профилактического обслуживания"""
        totalCost = preventiveCost + correctiveCost
        if totalCost > constants.ZERO_VALUE:
            # Предполагаем, что профилактическое обслуживание дешевле на 30%
            potentialCorrectiveCost = correctiveCost * 1.3
            savings = (potentialCorrectiveCost - totalCost) / potentialCorrectiveCost
            return savings * constants.PERCENTAGE_MULTIPLIER
        return constants.ZERO_VALUE

    def generateMaintenanceReport(self) -> dict:
        """Генерация отчета по обслуживанию"""
        return {
            "logId": self._logId,
            "totalEntries": len(self._maintenanceEntries),
            "totalMaintenanceHours": self._totalMaintenanceHours,
            "totalMaintenanceCost": self._totalMaintenanceCost,
            "machineDowntimeHours": self._machineDowntimeHours,
            "preventiveMaintenanceCount": self._preventiveMaintenanceCount,
            "correctiveMaintenanceCount": self._correctiveMaintenanceCount,
            "maintenanceEfficiencyPercentage": self.calculateMaintenanceEfficiency(),
            "costAnalysis": self.getCostAnalysis()
        }

    def __str__(self) -> str:
        return f"Журнал обслуживания {self._logId} ({len(self._maintenanceEntries)} записей)"
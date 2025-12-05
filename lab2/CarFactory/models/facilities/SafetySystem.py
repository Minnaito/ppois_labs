from datetime import datetime
from config import constants


class SafetySystem:

    def __init__(self, systemId: str, systemName: str, systemType: str):
        self._systemId = systemId
        self._systemName = systemName
        self._systemType = systemType
        self._isActive = True
        self._lastInspectionDate = "2024-01-01"
        self._nextInspectionDate = "2024-07-01"
        self._safetyIncidentsCount = 0
        self._coverageArea = ""
        self._maintenanceRequired = False

    def reportSafetyIncident(self, incidentDescription: str, severity: str) -> None:
        """Сообщение о инциденте безопасности"""
        self._safetyIncidentsCount += 1

        incidentReport = {
            "incidentId": f"INC_{self._safetyIncidentsCount:04d}",
            "systemId": self._systemId,
            "description": incidentDescription,
            "severity": severity,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return incidentReport

    def scheduleMaintenance(self) -> None:
        """Планирование обслуживания"""
        self._maintenanceRequired = True

    def completeMaintenance(self) -> None:
        """Завершение обслуживания"""
        self._maintenanceRequired = False
        self._lastInspectionDate = datetime.now().strftime("%Y-%m-%d")

    def calculateSystemReliability(self, totalOperationalHours: float,
                                     downtimeHours: float) -> float:
        """Расчет надежности системы"""
        if totalOperationalHours > 0:
            reliability = ((totalOperationalHours - downtimeHours) / totalOperationalHours)
            return reliability * constants.PERCENTAGE_MULTIPLIER
        return 0.0

    def getSafetyStatus(self) -> dict:
        """Получение статуса безопасности"""
        return {
            "systemId": self._systemId,
            "systemName": self._systemName,
            "systemType": self._systemType,
            "isActive": self._isActive,
            "lastInspectionDate": self._lastInspectionDate,
            "nextInspectionDate": self._nextInspectionDate,
            "safetyIncidentsCount": self._safetyIncidentsCount,
            "maintenanceRequired": self._maintenanceRequired,
            "coverageArea": self._coverageArea
        }

    def __str__(self) -> str:
        status = "АКТИВНА" if self._isActive else "НЕАКТИВНА"
        return f"Система безопасности {self._systemName} ({status})"
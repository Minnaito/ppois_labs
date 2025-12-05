from datetime import datetime
from models.production.CarPart import CarPart
from models.employees.QualityInspector import QualityInspector


class DefectReport:

    def __init__(self, reportId: str, defectivePart: CarPart, inspector: QualityInspector):
        self._reportId = reportId
        self._defectivePart = defectivePart
        self._inspector = inspector
        self._reportDate = datetime.now().strftime("%Y-%m-%d")
        self._defectSeverity = "MEDIUM"
        self._correctiveAction = ""
        self._isResolved = False
        self._resolutionDate = None

    def addDefectDetails(self, defectDescription: str, severity: str) -> None:
        """Добавление деталей дефекта"""
        self._defectivePart.addDefect(defectDescription)
        self._defectSeverity = severity

    def assignCorrectiveAction(self, action: str) -> None:
        """Назначение корректирующего действия"""
        self._correctiveAction = action

    def markAsResolved(self) -> None:
        """Отметка как решенного"""
        self._isResolved = True
        self._resolutionDate = datetime.now().strftime("%Y-%m-%d")

    def calculateRepairCost(self) -> float:
        """Расчет стоимости ремонта"""
        baseRepairCost = 50.0
        severityMultipliers = {"LOW": 1.0, "MEDIUM": 1.5, "HIGH": 2.0, "CRITICAL": 3.0}

        multiplier = severityMultipliers.get(self._defectSeverity, 1.0)
        repairCost = baseRepairCost * multiplier

        return repairCost

    def getDefectStatistics(self) -> dict:
        """Получение статистики дефекта"""
        defectCount = len(self._defectivePart.getDefectList())

        return {
            "defectCount": defectCount,
            "defectSeverity": self._defectSeverity,
            "repairCostEstimate": self.calculateRepairCost(),
            "daysSinceReport": 1  # В реальной системе считались бы дни
        }

    def generateReportSummary(self) -> dict:
        """Генерация сводки отчета"""
        return {
            "reportId": self._reportId,
            "partIdentifier": self._defectivePart.partIdentifier,
            "partName": self._defectivePart.partName,
            "inspectorId": self._inspector.employeeIdentifier,
            "reportDate": self._reportDate,
            "defectSeverity": self._defectSeverity,
            "correctiveAction": self._correctiveAction,
            "isResolved": self._isResolved,
            "resolutionDate": self._resolutionDate
        }
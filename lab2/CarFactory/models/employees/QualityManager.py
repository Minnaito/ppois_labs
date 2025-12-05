from models.abstract.BaseEmployee import BaseEmployee
from config import constants
from exceptions.QualityExceptions import QualityStandardViolationError
from models.quality.QualityControl import QualityControl
from models.quality.QualityInspector import QualityInspector


class QualityManager(BaseEmployee):

    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, departmentName: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._departmentName = departmentName
        self._managedQualityControls = []
        self._managedInspectorsList = []
        self._completedAuditsCount = 0
        self._departmentQualityScore = 0.0
        self._qualityImprovementProjects = []
        self._certificationsHeld = []

    def performWorkDuties(self) -> str:
        """Выполнение рабочих обязанностей менеджера по качеству"""
        dutiesDescription = f"Управление системой качества в отделе {self._departmentName}"
        return dutiesDescription

    def addQualityControlSystem(self, qualityControlSystem: QualityControl) -> None:
        """Добавление системы контроля качества"""
        self._managedQualityControls.append(qualityControlSystem)

    def assignQualityInspector(self, qualityInspector: QualityInspector) -> None:
        """Назначение инспектора качества"""
        self._managedInspectorsList.append(qualityInspector)

    def conductQualityAudit(self, qualityControlSystem: QualityControl) -> dict:
        """Проведение аудита качества"""
        self._completedAuditsCount += 1

        try:
            auditReport = qualityControlSystem.generateQualityReport(100, 95)
            qualityScore = auditReport.get("passRatePercentage", 0)
            self._departmentQualityScore = qualityScore
            return auditReport
        except QualityStandardViolationError as qualityError:
            self._departmentQualityScore = 0
            raise qualityError

    def calculateDepartmentQualityScore(self, totalPartsProduced: int,
                                           defectivePartsCount: int) -> float:
        """Расчет показателя качества отдела"""
        if totalPartsProduced > constants.ZERO_VALUE:
            qualityRatio = (totalPartsProduced - defectivePartsCount)
            qualityRatio /= totalPartsProduced
            qualityScore = qualityRatio * constants.PERCENTAGE_MULTIPLIER
            self._departmentQualityScore = qualityScore
            return qualityScore
        return constants.ZERO_VALUE

    def addQualityImprovementProject(self, projectName: str) -> None:
        """Добавление проекта улучшения качества"""
        self._qualityImprovementProjects.append(projectName)

    def addCertification(self, certificationName: str) -> None:
        """Добавление сертификации"""
        self._certificationsHeld.append(certificationName)

    def generateQualityManagementReport(self) -> dict:
        """Генерация отчета управления качеством"""
        managementReport = {
            "managerIdentifier": self._employeeIdentifier,
            "departmentName": self._departmentName,
            "completedAuditsCount": self._completedAuditsCount,
            "departmentQualityScore": self._departmentQualityScore,
            "managedControlsCount": len(self._managedQualityControls),
            "managedInspectorsCount": len(self._managedInspectorsList),
            "improvementProjectsCount": len(self._qualityImprovementProjects),
            "certificationsCount": len(self._certificationsHeld)
        }
        return managementReport

    def calculateTeamProductivity(self) -> float:
        """Расчет продуктивности команды"""
        totalInspections = sum(
            inspector._completedInspectionsCount
            for inspector in self._managedInspectorsList
        )
        inspectorCount = len(self._managedInspectorsList)

        if inspectorCount > constants.ZERO_VALUE:
            averageProductivity = totalInspections / inspectorCount
            return averageProductivity
        return constants.ZERO_VALUE
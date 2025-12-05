from models.abstract.BaseEmployee import BaseEmployee
from config import constants

class QualityInspector(BaseEmployee):

    def __init__(self, employeeIdentifier, fullName, jobPosition, monthlySalary, departmentName):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._departmentName = departmentName
        self._completedInspectionsCount = 0
        self._inspectionSuccessRate = 0.0

    def performWorkDuties(self):
        return f"Проверка качества деталей в отделе {self._departmentName}"

    def inspectPart(self, partToInspect, qualityControlSystem):
        """Проведение инспекции детали"""
        try:
            qualityCheckPassed = partToInspect.performQualityCheck()
            if qualityCheckPassed:
                self._recordSuccessfulInspection()
                partToInspect.approveQuality()
                return True
            else:
                from exceptions.QualityExceptions.InspectionFailedError import InspectionFailedError
                raise InspectionFailedError(partToInspect.partIdentifier, self._employeeIdentifier)
        except Exception as e:
            from exceptions.QualityExceptions.InspectionFailedError import InspectionFailedError
            raise InspectionFailedError(partToInspect.partIdentifier, self._employeeIdentifier) from e

    def _recordSuccessfulInspection(self):
        self._completedInspectionsCount += 1

    def calculateSuccessRate(self, totalAssignments):
        if totalAssignments > constants.ZERO_VALUE:
            successRate = self._completedInspectionsCount / totalAssignments
            self._inspectionSuccessRate = successRate * constants.PERCENTAGE_MULTIPLIER
            return self._inspectionSuccessRate
        return constants.ZERO_VALUE

    def getInspectorStats(self):
        return {
            "inspectorId": self._employeeIdentifier,
            "department": self._departmentName,
            "completedInspections": self._completedInspectionsCount,
            "successRate": self._inspectionSuccessRate
        }
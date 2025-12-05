from models.abstract.BaseEmployee import BaseEmployee
from config import constants

class MachineOperator(BaseEmployee):

    def __init__(self, employeeIdentifier, fullName, jobPosition, monthlySalary, machineType):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._machineType = machineType
        self._producedPartsCount = 0
        self._operatorEfficiency = 0.0

    def performWorkDuties(self):
        return f"Оператор станка {self._machineType} производит детали"

    def operateMachine(self, productionLine, partTemplate, quantity=1):
        """Операция станка для производства детали"""
        try:
            producedParts = productionLine.produceParts(partTemplate, quantity)
            if producedParts:
                self._producedPartsCount += quantity
                return producedParts
        except Exception as e:
            from exceptions.ProductionExceptions.MachineMaintenanceRequiredError import MachineMaintenanceRequiredError
            raise MachineMaintenanceRequiredError(self._machineType, "routine") from e
        return None

    def getOperatorStats(self):
        return {
            "operatorId": self._employeeIdentifier,
            "machineType": self._machineType,
            "producedParts": self._producedPartsCount,
            "efficiency": self._operatorEfficiency
        }
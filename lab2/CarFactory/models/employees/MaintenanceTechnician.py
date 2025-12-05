from models.abstract.BaseEmployee import BaseEmployee
from config import constants
from exceptions.ProductionExceptions.MachineMaintenanceRequiredError import MachineMaintenanceRequiredError
from models.maintenance.MachineMaintenance import MachineMaintenance
from models.maintenance.RepairTicket import RepairTicket


class MaintenanceTechnician(BaseEmployee):

    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, technicalSpecialization: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._technicalSpecialization = technicalSpecialization
        self._completedRepairsCount = 0
        self._technicalCertificationsList = []
        self._availableToolsList = []
        self._averageResponseTimeMinutes = 0.0
        self._specializedEquipment = []

    def performWorkDuties(self) -> str:
        """Выполнение рабочих обязанностей техника"""
        dutiesDescription = f"Техническое обслуживание оборудования специализации {self._technicalSpecialization}"
        return dutiesDescription

    def performMachineMaintenance(self, maintenanceTask: MachineMaintenance) -> bool:
        """Выполнение обслуживания станка"""
        try:
            maintenanceTask.completeMaintenanceTask()
            self._completedRepairsCount += 1
            return True
        except MachineMaintenanceRequiredError as maintenanceError:
            raise MachineMaintenanceRequiredError(
                maintenanceTask.machineIdentifier,
                "emergency_maintenance"
            ) from maintenanceError

    def handleRepairTicket(self, repairTicket: RepairTicket) -> dict:
        """Обработка заявки на ремонт"""
        repairTicket.updateTicketStatus("IN_PROGRESS")

        repairSuccessful = self._simulateRepairProcess()
        if repairSuccessful:
            repairTicket.updateTicketStatus("COMPLETED")
            self._completedRepairsCount += 1

        repairReport = {
            "ticketIdentifier": repairTicket.ticketIdentifier,
            "technicianIdentifier": self._employeeIdentifier,
            "repairSuccessful": repairSuccessful,
            "completionTimeMinutes": 120
        }
        return repairReport

    def _simulateRepairProcess(self) -> bool:
        """Симуляция процесса ремонта"""
        baseSuccessProbability = 0.85
        certificationBonus = len(self._technicalCertificationsList) * 0.02
        totalSuccessProbability = baseSuccessProbability + certificationBonus

        return totalSuccessProbability > 0.5

    def addTechnicalCertification(self, certificationName: str) -> None:
        """Добавление технической сертификации"""
        self._technicalCertificationsList.append(certificationName)

    def addToolToInventory(self, toolName: str) -> None:
        """Добавление инструмента в инвентарь"""
        self._availableToolsList.append(toolName)

    def calculateSuccessRatePercentage(self, totalAssignmentsCount: int) -> float:
        """Расчет процента успешных ремонтов"""
        if totalAssignmentsCount > constants.ZERO_VALUE:
            successRate = self._completedRepairsCount / totalAssignmentsCount
            successRatePercentage = successRate * constants.PERCENTAGE_MULTIPLIER
            return successRatePercentage
        return constants.ZERO_VALUE

    def addSpecializedEquipment(self, equipmentName: str) -> None:
        """Добавление специализированного оборудования"""
        self._specializedEquipment.append(equipmentName)

    def getTechnicianPerformanceReport(self) -> dict:
        """Получение отчета о производительности техника"""
        performanceReport = {
            "employeeIdentifier": self._employeeIdentifier,
            "technicalSpecialization": self._technicalSpecialization,
            "completedRepairsCount": self._completedRepairsCount,
            "technicalCertificationsCount": len(self._technicalCertificationsList),
            "availableToolsCount": len(self._availableToolsList),
            "averageResponseTimeMinutes": self._averageResponseTimeMinutes,
            "specializedEquipmentCount": len(self._specializedEquipment)
        }
        return performanceReport
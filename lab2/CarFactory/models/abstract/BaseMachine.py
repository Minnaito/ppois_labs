from abc import ABC, abstractmethod
from config import constants
from exceptions.ProductionExceptions import MachineMaintenanceRequiredError


class BaseMachine(ABC):

    def __init__(self, machineIdentifier: str, machineName: str, machineType: str):
        self._machineIdentifier = machineIdentifier
        self._machineName = machineName
        self._machineType = machineType
        self._isOperational = True
        self._operationalHours = 0
        self._maintenanceRequired = False
        self._energyConsumptionKwh = 0.0
        self._manufacturer = ""
        self._installationDate = ""

    @property
    def machineIdentifier(self) -> str:
        """Уникальный идентификатор станка"""
        return self._machineIdentifier

    @abstractmethod
    def performOperation(self) -> bool:
        """Абстрактный метод для выполнения операции"""
        pass

    @abstractmethod
    def calculateEfficiency(self) -> float:
        """Абстрактный метод для расчета эффективности"""
        pass

    def scheduleMaintenance(self) -> None:
        """Запланировать обслуживание"""
        self._maintenanceRequired = True

    def completeMaintenance(self) -> None:
        """Завершить обслуживание"""
        self._maintenanceRequired = False
        self._isOperational = True

    def checkMaintenanceNeed(self) -> bool:
        """Проверить необходимость обслуживания"""
        if self._maintenanceRequired:
            raise MachineMaintenanceRequiredError(self._machineIdentifier, "routine_maintenance")
        return False

    def updateOperationalHours(self, hoursWorked: float) -> None:
        """Обновить отработанные часы"""
        if hoursWorked > constants.ZERO_VALUE:
            self._operationalHours += hoursWorked

    def calculateEnergyCost(self, energyRatePerKwh: float) -> float:
        """Рассчитать стоимость энергии"""
        return self._energyConsumptionKwh * energyRatePerKwh

    def getMachineStatus(self) -> dict:
        """Получить статус станка"""
        return {
            "machineIdentifier": self._machineIdentifier,
            "machineName": self._machineName,
            "isOperational": self._isOperational,
            "operationalHours": self._operationalHours,
            "maintenanceRequired": self._maintenanceRequired,
            "energyConsumption": self._energyConsumptionKwh
        }
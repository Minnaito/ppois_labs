from abc import ABC, abstractmethod
from config import constants

class BaseMachine(ABC):
    def __init__(self, machine_id: str, name: str, machine_type: str):
        self._machine_id = machine_id
        self._name = name
        self._machine_type = machine_type
        self._is_active = True

    @abstractmethod
    def operate(self) -> bool:
        pass

    @abstractmethod
    def calculate_efficiency(self) -> float:
        pass

    def schedule_maintenance(self):
        from exceptions.ProductionExceptions.MachineMaintenanceRequiredError import MachineMaintenanceRequiredError
        raise MachineMaintenanceRequiredError(self._machine_id, "плановое")
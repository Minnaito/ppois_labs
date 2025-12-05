from .ProductionException import ProductionException


class MachineMaintenanceRequiredError(ProductionException):
    """Исключение при необходимости обслуживания станка"""

    def __init__(self, machine_id: str, maintenance_type: str):
        self.machine_id = machine_id
        self.maintenance_type = maintenance_type
        message = f"Станок {machine_id} требует обслуживания типа: {maintenance_type}"
        super().__init__(message)
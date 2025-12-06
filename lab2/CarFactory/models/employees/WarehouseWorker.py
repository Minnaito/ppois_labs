from models.abstract.BaseEmployee import BaseEmployee

class WarehouseWorker(BaseEmployee):
    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, assignedZone: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._assignedZone = assignedZone

    def work(self) -> str:
        return f"Работа на складе: {self._assignedZone}"

    def move_items(self, item_name: str, quantity: int) -> dict:
        return {
            "worker": self._employeeIdentifier,
            "zone": self._assignedZone,
            "item": item_name,
            "quantity": quantity
        }
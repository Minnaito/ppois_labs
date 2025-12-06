from models.abstract.BaseEmployee import BaseEmployee

class MachineOperator(BaseEmployee):
    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, machineType: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._machineType = machineType

    def work(self) -> str:
        return f"Оператор станка {self._machineType}"

    def operate_machine(self, parts_count: int) -> dict:
        return {
            "operator": self._employeeIdentifier,
            "machine": self._machineType,
            "parts_produced": parts_count
        }
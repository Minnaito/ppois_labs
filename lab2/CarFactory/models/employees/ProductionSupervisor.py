from models.abstract.BaseEmployee import BaseEmployee

class ProductionSupervisor(BaseEmployee):
    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, supervisionArea: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._supervisionArea = supervisionArea

    def work(self) -> str:
        return f"Надзор за производством: {self._supervisionArea}"

    def monitor_production(self, production_count: int) -> dict:
        return {
            "supervisor": self._employeeIdentifier,
            "area": self._supervisionArea,
            "production": production_count
        }
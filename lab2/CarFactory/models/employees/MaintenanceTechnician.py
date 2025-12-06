from models.abstract.BaseEmployee import BaseEmployee

class MaintenanceTechnician(BaseEmployee):
    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, technicalSpecialization: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._technicalSpecialization = technicalSpecialization

    def work(self) -> str:
        return f"Техник по обслуживанию {self._technicalSpecialization}"

    def repair_machine(self, machine_id: str) -> dict:
        return {
            "technician": self._employeeIdentifier,
            "machine": machine_id,
            "status": "repaired"
        }
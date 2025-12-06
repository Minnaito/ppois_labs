from models.abstract.BaseEmployee import BaseEmployee
from config import constants

class QualityManager(BaseEmployee):
    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, department: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._department = department
        self._audits = constants.ZERO_VALUE

    def work(self) -> str:
        return f"Менеджер качества отдела {self._department}"

    def conduct_audit(self, passed: int, total: int) -> dict:
        self._audits += 1
        pass_rate = (passed / total) * constants.PERCENTAGE_MULTIPLIER if total > 0 else 0
        return {"audits": self._audits, "pass_rate": pass_rate}
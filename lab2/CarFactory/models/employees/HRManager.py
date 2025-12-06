from models.abstract.BaseEmployee import BaseEmployee
from datetime import datetime

class HRManager(BaseEmployee):
    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, hrDepartment: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._hrDepartment = hrDepartment

    def work(self) -> str:
        return f"Управление персоналом в отделе {self._hrDepartment}"

    def process_payroll(self, employees: list) -> dict:
        total_salary = sum(emp._monthlySalary for emp in employees)
        return {
            "processed_by": self._employeeIdentifier,
            "employees_count": len(employees),
            "total_salary": total_salary,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
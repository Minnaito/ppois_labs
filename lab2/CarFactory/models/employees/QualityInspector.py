from models.abstract.BaseEmployee import BaseEmployee

class QualityInspector(BaseEmployee):
    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, departmentName: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._departmentName = departmentName

    def work(self) -> str:
        return f"Проверка качества: {self._departmentName}"

    def inspect_part(self, part_id: str, passed: bool) -> dict:
        return {
            "inspector": self._employeeIdentifier,
            "part": part_id,
            "passed": passed
        }
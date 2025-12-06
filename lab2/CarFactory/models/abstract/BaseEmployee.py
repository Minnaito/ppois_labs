from abc import ABC, abstractmethod
from config import constants

class BaseEmployee(ABC):
    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str, monthlySalary: float):
        if len(fullName) < constants.MINIMUM_NAME_LENGTH:
            raise ValueError(f"Имя слишком короткое: {fullName}")
        if monthlySalary < constants.MINIMUM_EMPLOYEE_SALARY:
            raise ValueError(f"Зарплата ниже минимума: {monthlySalary}")

        self._employeeIdentifier = employeeIdentifier
        self._fullName = fullName
        self._jobPosition = jobPosition
        self._monthlySalary = monthlySalary

    @abstractmethod
    def work(self) -> str:
        pass

    def get_annual_salary(self) -> float:
        return self._monthlySalary * 12

    def calculate_tax(self) -> float:
        return self._monthlySalary * constants.EMPLOYEE_SALARY_TAX_RATE

    def get_info(self) -> dict:
        return {
            "id": self._employeeIdentifier,
            "name": self._fullName,
            "position": self._jobPosition,
            "salary": self._monthlySalary
        }
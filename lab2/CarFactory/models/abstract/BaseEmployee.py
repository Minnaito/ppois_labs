from abc import ABC, abstractmethod
from config import constants
from exceptions.EmployeeExceptions.InvalidEmployeeDataError import InvalidEmployeeDataError


class BaseEmployee(ABC):

    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str, monthlySalary: float):
        self._employeeIdentifier = employeeIdentifier
        self._fullName = fullName
        self._jobPosition = jobPosition
        self._monthlySalary = monthlySalary
        self._isActiveEmployee = True
        self._yearsOfExperience = 0

        self._validateEmployeeData()

    def _validateEmployeeData(self) -> None:
        """Валидация данных сотрудника"""
        if len(self._fullName) < constants.MINIMUM_NAME_LENGTH:
            raise InvalidEmployeeDataError("fullName", self._fullName)

        if self._monthlySalary < constants.MINIMUM_EMPLOYEE_SALARY:
            raise InvalidEmployeeDataError("monthlySalary", str(self._monthlySalary))

    @property
    def employeeIdentifier(self) -> str:
        """Идентификатор сотрудника"""
        return self._employeeIdentifier

    @property
    def fullName(self) -> str:
        """Полное имя сотрудника"""
        return self._fullName

    @property
    def jobPosition(self) -> str:
        """Должность сотрудника"""
        return self._jobPosition

    @property
    def monthlySalary(self) -> float:
        """Месячная зарплата"""
        return self._monthlySalary

    @abstractmethod
    def performWorkDuties(self) -> str:
        """Абстрактный метод для выполнения рабочих обязанностей"""
        pass

    def calculateAnnualSalary(self) -> float:
        """Расчет годовой зарплаты"""
        return self._monthlySalary * 12

    def updateYearsOfExperience(self, years: int) -> None:
        """Обновление лет опыта"""
        if years >= 0:
            self._yearsOfExperience = years

    def getEmployeeInfo(self) -> dict:
        """Получение информации о сотруднике"""
        return {
            "employeeIdentifier": self._employeeIdentifier,
            "fullName": self._fullName,
            "jobPosition": self._jobPosition,
            "monthlySalary": self._monthlySalary,
            "annualSalary": self.calculateAnnualSalary(),
            "yearsOfExperience": self._yearsOfExperience,
            "isActive": self._isActiveEmployee
        }

    def __str__(self) -> str:
        return f"{self._fullName} ({self._jobPosition})"

    def __repr__(self) -> str:
        return f"BaseEmployee(employeeIdentifier='{self._employeeIdentifier}', fullName='{self._fullName}')"
from models.abstract.BaseEmployee import BaseEmployee
from models.employees.MachineOperator import MachineOperator
from datetime import datetime


class HRManager(BaseEmployee):

    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, hrDepartment: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._hrDepartment = hrDepartment
        self._employeesManaged = []
        self._recruitmentCampaigns = 0
        self._trainingSessionsConducted = 0
        self._employeeSatisfactionScore = 0.0

    def performWorkDuties(self) -> str:
        return f"Управление персоналом в отделе {self._hrDepartment}"

    def hireEmployee(self, applicantData: dict) -> BaseEmployee:
        newEmployee = MachineOperator(
            applicantData.get("employeeId", "NEW_EMP"),
            applicantData.get("fullName", "Новый сотрудник"),
            applicantData.get("position", "Оператор станка"),
            applicantData.get("salary", 30000.0),
            "Не указан"
        )
        self._employeesManaged.append(newEmployee)
        return newEmployee

    def processPayroll(self, employees: list) -> dict:
        """Обработка payroll"""
        total_salary = sum(emp.monthlySalary for emp in employees)

        return {
            "processedBy": self._employeeIdentifier,
            "employeesCount": len(employees),
            "totalSalaryAmount": total_salary,
            "payrollDate": datetime.now().strftime("%Y-%m-%d")
        }

    def conductTrainingSession(self, trainingTopic: str, participants: list) -> dict:
        """Проведение тренинг-сессии"""
        self._trainingSessionsConducted += 1

        return {
            "trainerId": self._employeeIdentifier,
            "trainingTopic": trainingTopic,
            "participantsCount": len(participants),
            "sessionDurationHours": 2.0
        }

    def calculateEmployeeSatisfaction(self, surveyResponses: list) -> float:
        """Расчет удовлетворенности сотрудников"""
        if not surveyResponses:
            self._employeeSatisfactionScore = 0.0
            return 0.0

        score = sum(surveyResponses) / len(surveyResponses)
        self._employeeSatisfactionScore = score
        return score

    def getHRManagementReport(self) -> dict:
        """Получение отчета по управлению персоналом"""
        return {
            "hrManagerId": self._employeeIdentifier,
            "hrDepartment": self._hrDepartment,
            "employeesManagedCount": len(self._employeesManaged),
            "recruitmentCampaigns": self._recruitmentCampaigns,
            "trainingSessionsConducted": self._trainingSessionsConducted,
            "employeeSatisfactionScore": self._employeeSatisfactionScore
        }
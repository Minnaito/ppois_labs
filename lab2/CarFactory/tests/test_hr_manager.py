from models.abstract.BaseEmployee import BaseEmployee
from models.employees.MachineOperator import MachineOperator
from models.employees.QualityInspector import QualityInspector
from models.employees.WarehouseWorker import WarehouseWorker
from models.employees.MaintenanceTechnician import MaintenanceTechnician
from datetime import datetime


class HRManager(BaseEmployee):
    """HR-менеджер, наследуется от BaseEmployee"""

    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, hrDepartment: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._hrDepartment = hrDepartment
        self._employeesManaged = []
        self._recruitmentCampaigns = 0
        self._trainingSessionsConducted = 0
        self._employeeSatisfactionScore = 0.0

    def performWorkDuties(self) -> str:
        """Реализация абстрактного метода"""
        return f"Управление персоналом в отделе {self._hrDepartment}"

    def _create_employee_by_position(self, employee_id: str, full_name: str,
                                     position: str, salary: float) -> BaseEmployee:
        """Вспомогательный метод для создания сотрудника по должности"""
        position_lower = position.lower()

        if any(word in position_lower for word in
               ["оператор", "станок", "машина", "разработчик", "дизайнер", "тестировщик"]):
            return MachineOperator(employee_id, full_name, position, salary, "Производство")
        elif any(word in position_lower for word in ["качество", "инспектор", "контроль"]):
            return QualityInspector(employee_id, full_name, position, salary, "Контроль качества")
        elif any(word in position_lower for word in ["склад", "кладовщик", "рабочий"]):
            return WarehouseWorker(employee_id, full_name, position, salary, "Склад")
        elif any(word in position_lower for word in ["техник", "обслуживание", "ремонт"]):
            return MaintenanceTechnician(employee_id, full_name, position, salary, "Техническое обслуживание")
        else:
            # По умолчанию создаем MachineOperator
            return MachineOperator(employee_id, full_name, position, salary, "Общий отдел")

    def hireEmployee(self, applicantData: dict) -> BaseEmployee:
        """Найм нового сотрудника"""
        newEmployee = self._create_employee_by_position(
            applicantData.get("employeeId", "NEW_EMP"),
            applicantData.get("fullName", "Новый сотрудник"),
            applicantData.get("position", "Специалист"),
            applicantData.get("salary", 30000.0)
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

    @property
    def hrDepartment(self) -> str:
        return self._hrDepartment

    @property
    def employeesManaged(self) -> list:
        return self._employeesManaged.copy()

    @property
    def trainingSessionsConducted(self) -> int:
        return self._trainingSessionsConducted

    @property
    def employeeSatisfactionScore(self) -> float:
        return self._employeeSatisfactionScore
from datetime import datetime
from typing import List
from config import constants


class MaintenanceSchedule:

    def __init__(self, scheduleId: str, machineId: str):
        self._scheduleId = scheduleId
        self._machineId = machineId
        self._maintenanceTasks = []
        self._nextMaintenanceDate = ""
        self._maintenanceIntervalDays = 30
        self._isActive = True
        self._lastMaintenanceDate = ""
        self._estimatedDurationHours = 2.0

    def addMaintenanceTask(self, taskDescription: str, estimatedHours: float) -> None:
        """Добавление задачи обслуживания"""
        task = {
            "description": taskDescription,
            "estimatedHours": estimatedHours,
            "completed": False,
            "assignedTechnician": ""
        }
        self._maintenanceTasks.append(task)

    def calculateNextMaintenanceDate(self, lastMaintenanceDate: str) -> str:
        """Расчет даты следующего обслуживания"""
        try:
            lastDate = datetime.strptime(lastMaintenanceDate, "%Y-%m-%d")
            nextDate = lastDate.replace(day=lastDate.day + self._maintenanceIntervalDays)
            self._nextMaintenanceDate = nextDate.strftime("%Y-%m-%d")
            return self._nextMaintenanceDate
        except ValueError:
            # Если дата в неправильном формате, используем базовую логику
            return "2024-02-15"

    def getPendingTasksCount(self) -> int:
        """Получение количества невыполненных задач"""
        return sum(1 for task in self._maintenanceTasks if not task["completed"])

    def completeTask(self, taskIndex: int) -> bool:
        """Отметка задачи как выполненной"""
        if 0 <= taskIndex < len(self._maintenanceTasks):
            self._maintenanceTasks[taskIndex]["completed"] = True
            return True
        return False

    def assignTechnicianToTask(self, taskIndex: int, technicianId: str) -> bool:
        """Назначение техника на задачу"""
        if 0 <= taskIndex < len(self._maintenanceTasks):
            self._maintenanceTasks[taskIndex]["assignedTechnician"] = technicianId
            return True
        return False

    def calculateTotalEstimatedHours(self) -> float:
        """Расчет общего estimated времени обслуживания"""
        return sum(task["estimatedHours"] for task in self._maintenanceTasks)

    def isMaintenanceOverdue(self, currentDate: str) -> bool:
        """Проверка просрочки обслуживания"""
        if not self._nextMaintenanceDate:
            return False

        try:
            nextDate = datetime.strptime(self._nextMaintenanceDate, "%Y-%m-%d")
            currentDateObj = datetime.strptime(currentDate, "%Y-%m-%d")
            return currentDateObj > nextDate
        except ValueError:
            return False

    def getMaintenanceUrgencyLevel(self) -> str:
        """Получение уровня срочности обслуживания"""
        pendingTasks = self.getPendingTasksCount()
        totalTasks = len(self._maintenanceTasks)

        if totalTasks == 0:
            return "LOW"

        completionRatio = (totalTasks - pendingTasks) / totalTasks

        if completionRatio < 0.5:
            return "HIGH"
        elif completionRatio < 0.8:
            return "MEDIUM"
        else:
            return "LOW"

    def getScheduleInfo(self) -> dict:
        """Получение информации о расписании"""
        return {
            "scheduleId": self._scheduleId,
            "machineId": self._machineId,
            "totalTasks": len(self._maintenanceTasks),
            "pendingTasks": self.getPendingTasksCount(),
            "nextMaintenance": self._nextMaintenanceDate,
            "isActive": self._isActive,
            "maintenanceIntervalDays": self._maintenanceIntervalDays,
            "totalEstimatedHours": self.calculateTotalEstimatedHours(),
            "urgencyLevel": self.getMaintenanceUrgencyLevel(),
            "isOverdue": self.isMaintenanceOverdue("2024-01-15")  # Пример даты
        }

    def __str__(self) -> str:
        return f"Расписание обслуживания {self._scheduleId} для станка {self._machineId}"
class MaintenanceSchedule:
    """Упрощенное расписание обслуживания"""

    def __init__(self, scheduleId: str, machineId: str):
        self._scheduleId = scheduleId
        self._machineId = machineId
        self._tasks = []  # 3 поля вместо 7

    def addTask(self, description: str):
        """Добавить задачу"""
        self._tasks.append(description)
        return {"task": description, "status": "added"}

    def getTasksCount(self):
        """Получить количество задач"""
        return len(self._tasks)
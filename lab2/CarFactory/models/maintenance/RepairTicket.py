from datetime import datetime
from config import constants


class RepairTicket:

    def __init__(self, ticketId: str, machineId: str, issueDescription: str):
        self._ticketId = ticketId
        self._machineId = machineId
        self._issueDescription = issueDescription
        self._creationDate = datetime.now().strftime("%Y-%m-%d")
        self._reportedBy = ""
        self._assignedTechnician = ""
        self._priority = "MEDIUM"
        self._status = "OPEN"
        self._estimatedRepairTime = 0.0
        self._actualRepairTime = 0.0
        self._resolutionNotes = ""

    @property
    def ticketIdentifier(self) -> str:
        """Идентификатор заявки"""
        return self._ticketId

    def updateTicketStatus(self, newStatus: str) -> None:
        """Обновление статуса заявки"""
        validStatuses = ["OPEN", "IN_PROGRESS", "COMPLETED", "CANCELLED"]
        if newStatus in validStatuses:
            self._status = newStatus

    def assignToTechnician(self, technicianId: str) -> None:
        """Назначение заявки технику"""
        self._assignedTechnician = technicianId
        self._status = "IN_PROGRESS"

    def setPriority(self, priorityLevel: str) -> None:
        """Установка приоритета заявки"""
        validPriorities = ["LOW", "MEDIUM", "HIGH", "URGENT"]
        if priorityLevel in validPriorities:
            self._priority = priorityLevel

    def addResolutionNotes(self, notes: str) -> None:
        """Добавление заметок по решению проблемы"""
        self._resolutionNotes = notes
        if notes and self._status == "IN_PROGRESS":
            self._status = "COMPLETED"

    def calculateRepairEfficiency(self) -> float:
        """Расчет эффективности ремонта"""
        if self._estimatedRepairTime > constants.ZERO_VALUE:
            efficiency = (self._estimatedRepairTime / self._actualRepairTime)
            efficiency *= constants.PERCENTAGE_MULTIPLIER
            return min(efficiency, 100.0)
        return constants.ZERO_VALUE

    def isOverdue(self, currentDate: str) -> bool:
        """Проверка просрочки заявки"""
        # Простая логика проверки просрочки
        creationDateObj = datetime.strptime(self._creationDate, "%Y-%m-%d")
        currentDateObj = datetime.strptime(currentDate, "%Y-%m-%d")
        daysPending = (currentDateObj - creationDateObj).days

        priorityDays = {"LOW": 7, "MEDIUM": 3, "HIGH": 1, "URGENT": 0}
        maxDays = priorityDays.get(self._priority, 3)

        return daysPending > maxDays and self._status != "COMPLETED"

    def getTicketDetails(self) -> dict:
        """Получение деталей заявки"""
        return {
            "ticketId": self._ticketId,
            "machineId": self._machineId,
            "issueDescription": self._issueDescription,
            "creationDate": self._creationDate,
            "reportedBy": self._reportedBy,
            "assignedTechnician": self._assignedTechnician,
            "priority": self._priority,
            "status": self._status,
            "estimatedRepairTime": self._estimatedRepairTime,
            "actualRepairTime": self._actualRepairTime,
            "isUrgent": self._priority in ["HIGH", "URGENT"]
        }

    def __str__(self) -> str:
        return f"Заявка {self._ticketId} для {self._machineId} ({self._status})"
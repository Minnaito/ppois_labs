import unittest
from datetime import datetime
from models.maintenance.MachineMaintenance import MachineMaintenance
from models.maintenance.MaintenanceLog import MaintenanceLog
from models.maintenance.RepairTicket import RepairTicket
from models.maintenance.MaintenanceSchedule import MaintenanceSchedule


class TestAllMaintenance(unittest.TestCase):

    def testAllMaintenanceClasses(self):
        maintenance = MachineMaintenance("MAINT001", "CNC-001")
        log = MaintenanceLog("LOG001")
        ticket = RepairTicket("TICK001", "CNC-001", "Неисправность")
        schedule = MaintenanceSchedule("SCH001", "CNC-001")

        # Проверяем инициализацию
        self.assertEqual(maintenance._maint_id, "MAINT001")
        self.assertEqual(log._log_id, "LOG001")
        self.assertEqual(ticket._ticket_id, "TICK001")
        self.assertEqual(schedule._scheduleId, "SCH001")

        # Проверяем базовые операции
        maintenance.start()
        self.assertEqual(maintenance._status, "IN_PROGRESS")

        log_entry = log.add_entry("CNC-001", "плановое", 2.5, 5000.0, "TECH001")
        self.assertEqual(len(log._entries), 1)

        schedule.addTask("Замена масла")
        self.assertEqual(schedule.getTasksCount(), 1)


if __name__ == '__main__':
    unittest.main()
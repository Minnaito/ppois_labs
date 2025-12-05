import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestAllMaintenance(unittest.TestCase):
    """Тесты для maintenance с правильными сигнатурами"""

    def testMachineMaintenanceInitialization(self):
        from models.maintenance.MachineMaintenance import MachineMaintenance
        maintenance = MachineMaintenance("MM001", "Станок", "2024-01-01")
        self.assertTrue(maintenance is not None)

    def testMaintenanceLogInitialization(self):
        from models.maintenance.MaintenanceLog import MaintenanceLog
        log = MaintenanceLog("ML001")  # Только 1 аргумент
        self.assertTrue(log is not None)

    def testMaintenanceScheduleInitialization(self):
        from models.maintenance.MaintenanceSchedule import MaintenanceSchedule
        schedule = MaintenanceSchedule("MS001", "График")  # 2 аргумента
        self.assertTrue(schedule is not None)

    def testRepairTicketInitialization(self):
        from models.maintenance.RepairTicket import RepairTicket
        ticket = RepairTicket("RT001", "Ремонт", "2024-01-01")
        self.assertTrue(ticket is not None)
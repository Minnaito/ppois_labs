import unittest
from models.employees.QualityManager import QualityManager


class TestQualityManager(unittest.TestCase):
    def testQualityManagerInitialization(self):
        qm = QualityManager("QM001", "Тест Менеджер", "Менеджер качества", 50000.0, "ОТК")
        self.assertEqual(qm._employeeIdentifier, "QM001")
        self.assertEqual(qm._fullName, "Тест Менеджер")
        self.assertEqual(qm._jobPosition, "Менеджер качества")
        self.assertEqual(qm._monthlySalary, 50000.0)
        self.assertEqual(qm._department, "ОТК")
        self.assertEqual(qm._audits, 0)

    def testQualityManagerWork(self):
        qm = QualityManager("QM001", "Тест", "Менеджер", 50000.0, "ОТК")
        self.assertEqual(qm.work(), "Менеджер качества отдела ОТК")

    def testQualityManagerConductAudit(self):
        qm = QualityManager("QM001", "Тест", "Менеджер", 50000.0, "ОТК")

        # Хороший результат
        result1 = qm.conduct_audit(85, 100)
        self.assertEqual(result1["pass_rate"], 85.0)
        self.assertEqual(result1["audits"], 1)

        # Плохой результат
        result2 = qm.conduct_audit(70, 100)
        self.assertEqual(result2["pass_rate"], 70.0)
        self.assertEqual(result2["audits"], 2)

        # Нет данных
        result3 = qm.conduct_audit(0, 0)
        self.assertEqual(result3["pass_rate"], 0.0)
        self.assertEqual(result3["audits"], 3)

    def testQualityManagerConductAuditMultiple(self):
        qm = QualityManager("QM001", "Тест", "Менеджер", 50000.0, "ОТК")

        results = []
        for i in range(5):
            result = qm.conduct_audit(80 + i, 100)
            results.append(result)

        self.assertEqual(len(results), 5)
        self.assertEqual(results[4]["audits"], 5)
        self.assertEqual(results[4]["pass_rate"], 84.0)

    def testQualityManagerInheritance(self):
        from models.abstract.BaseEmployee import BaseEmployee
        self.assertTrue(issubclass(QualityManager, BaseEmployee))


if __name__ == '__main__':
    unittest.main()
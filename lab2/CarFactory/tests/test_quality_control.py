import unittest
from config import constants
from models.quality.QualityControl import QualityControl


class MockPart:
    def __init__(self, quality):
        self.quality = quality

    def check_quality(self):
        return self.quality


class TestQualityControl(unittest.TestCase):

    def setUp(self):
        self.qc = QualityControl("QC001", "Основной контроль")

    def testInitialization(self):
        self.assertEqual(self.qc._control_id, "QC001")
        self.assertEqual(self.qc._name, "Основной контроль")

    def testTestPartPass(self):
        part = MockPart(True)
        result = self.qc.test_part(part)
        self.assertTrue(result)

    def testTestPartFail(self):
        part = MockPart(False)
        result = self.qc.test_part(part)
        self.assertFalse(result)

    def testGenerateReport(self):
        report = self.qc.generate_report(75, 100)
        self.assertEqual(report["system"], "Основной контроль")
        self.assertEqual(report["pass_rate"], 75.0)

    def testGenerateReportZeroTotal(self):
        report = self.qc.generate_report(0, 0)
        self.assertEqual(report["pass_rate"], 0)


if __name__ == '__main__':
    unittest.main()
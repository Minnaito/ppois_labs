import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.quality.QualityControl import QualityControl
from models.quality.QualityStandard import QualityStandard
from models.production.CarPart import CarPart

class TestQualityControl(unittest.TestCase):
    """Тесты для контроля качества"""

    def setUp(self):
        self.qualityControl = QualityControl("QC001", "Основной контроль")
        self.qualityStandard = QualityStandard("STD001", "Стандарт веса", "10-20 кг")
        self.testPart = CarPart("PART001", "Тестовая деталь", "steel", 15.0, "Test")

    def testQualityControlInitialization(self):
        self.assertEqual(self.qualityControl._controlSystemIdentifier, "QC001")
        self.assertEqual(self.qualityControl._controlSystemName, "Основной контроль")

    def testPerformQualityTest(self):
        result = self.qualityControl.performQualityTest(self.testPart)
        self.assertTrue(result)
        self.assertEqual(self.qualityControl._performedTestsCount, 1)

    def testGenerateQualityReport(self):
        self.qualityControl.performQualityTest(self.testPart)
        report = self.qualityControl.generateQualityReport(10, 8)
        self.assertEqual(report["performedTests"], 1)
        self.assertEqual(report["passRate"], 80.0)

    def testGetControlSystemInfo(self):
        info = self.qualityControl.getControlSystemInfo()
        self.assertEqual(info["controlSystemIdentifier"], "QC001")

if __name__ == '__main__':
    unittest.main()
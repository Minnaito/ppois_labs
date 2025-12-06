import unittest
from models.quality.QualityStandard import QualityStandard
from models.production.CarPart import CarPart


class TestQualityStandard(unittest.TestCase):
    def testQualityStandardInitialization(self):
        standard = QualityStandard("STD001", "Стандарт веса", "10-100 кг")

        self.assertEqual(standard._standardIdentifier, "STD001")
        self.assertEqual(standard._standardName, "Стандарт веса")
        self.assertEqual(standard._expectedValueRange, "10-100 кг")
        self.assertEqual(standard._severityLevel, "MEDIUM")

    def testQualityStandardProperties(self):
        standard = QualityStandard("STD001", "Стандарт", "10-50")

        self.assertEqual(standard.standardIdentifier, "STD001")
        self.assertEqual(standard.standardName, "Стандарт")
        self.assertEqual(standard.expectedValueRange, "10-50")

    def testQualityStandardSetSeverityLevel(self):
        standard = QualityStandard("STD001", "Стандарт", "10-50")

        standard.setSeverityLevel("HIGH")
        self.assertEqual(standard._severityLevel, "HIGH")

        standard.setSeverityLevel("CRITICAL")
        self.assertEqual(standard._severityLevel, "CRITICAL")

    def testQualityStandardSetTestMethod(self):
        standard = QualityStandard("STD001", "Стандарт", "10-50")

        standard.setTestMethod("Визуальный осмотр")
        self.assertEqual(standard._testMethod, "Визуальный осмотр")

    def testQualityStandardAddApplicablePart(self):
        standard = QualityStandard("STD001", "Стандарт", "10-50")

        standard.addApplicablePart("Engine")
        standard.addApplicablePart("CarPart")

        self.assertEqual(len(standard._applicableParts), 2)
        self.assertIn("Engine", standard._applicableParts)

    def testQualityStandardIsApplicableToPart(self):
        standard = QualityStandard("STD001", "Стандарт", "10-50")

        self.assertTrue(standard.isApplicableToPart("Engine"))

        standard.addApplicablePart("Engine")
        self.assertTrue(standard.isApplicableToPart("Engine"))
        self.assertFalse(standard.isApplicableToPart("CarPart"))

    def testQualityStandardGetStandardInfo(self):
        standard = QualityStandard("STD001", "Стандарт веса", "10-100 кг")
        standard.setSeverityLevel("HIGH")
        standard.setTestMethod("Взвешивание")
        standard.addApplicablePart("Engine")

        info = standard.getStandardInfo()

        self.assertEqual(info["standardIdentifier"], "STD001")
        self.assertEqual(info["standardName"], "Стандарт веса")
        self.assertEqual(info["expectedValueRange"], "10-100 кг")
        self.assertEqual(info["severityLevel"], "HIGH")
        self.assertEqual(info["testMethod"], "Взвешивание")
        self.assertEqual(info["applicablePartsCount"], 1)

    def testQualityStandardCheckCompliance(self):
        standard = QualityStandard("STD001", "Стандарт", "10-50")

        # Создаем mock часть
        class MockCarPart:
            pass

        part = MockCarPart()
        result = standard.checkCompliance(part)

        # Метод всегда возвращает True в текущей реализации
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
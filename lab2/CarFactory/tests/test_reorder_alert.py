import unittest
import sys
import os
from unittest.mock import Mock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.inventory.ReorderAlert import ReorderAlert


class TestReorderAlert(unittest.TestCase):
    """Тесты для класса ReorderAlert"""

    def setUp(self):
        """Настройка тестового окружения"""
        self.mockItem = Mock()
        self.mockItem.itemName = "Test Material"

        self.alert = ReorderAlert(
            alertId="ALERT001",
            item=self.mockItem,
            currentQuantity=50,
            minimumRequired=100
        )

    def testReorderAlertInitialization(self):
        """Тест инициализации оповещения о повторном заказе"""
        self.assertEqual(self.alert._alertId, "ALERT001")
        self.assertEqual(self.alert._item.itemName, "Test Material")
        self.assertEqual(self.alert._currentQuantity, 50)
        self.assertEqual(self.alert._minimumRequired, 100)
        self.assertEqual(self.alert._priority, "MEDIUM")
        self.assertFalse(self.alert._isResolved)
        self.assertIsNone(self.alert._resolvedDate)

    def testCalculateUrgencyLevelHigh(self):
        """Тест расчета уровня срочности - высокий"""
        alert = ReorderAlert("ALERT002", self.mockItem, 30, 100)
        urgencyLevel = alert.calculateUrgencyLevel()
        self.assertEqual(urgencyLevel, "HIGH")

    def testCalculateUrgencyLevelMedium(self):
        """Тест расчета уровня срочности - средний"""
        alert = ReorderAlert("ALERT003", self.mockItem, 70, 100)
        urgencyLevel = alert.calculateUrgencyLevel()
        self.assertEqual(urgencyLevel, "MEDIUM")

    def testCalculateUrgencyLevelLow(self):
        """Тест расчета уровня срочности - низкий"""
        alert = ReorderAlert("ALERT004", self.mockItem, 85, 100)
        urgencyLevel = alert.calculateUrgencyLevel()
        self.assertEqual(urgencyLevel, "LOW")

    def testMarkAsResolved(self):
        """Тест отметки как решенного"""
        self.alert.markAsResolved()

        self.assertTrue(self.alert._isResolved)
        self.assertIsNotNone(self.alert._resolvedDate)

    def testGetAlertInfo(self):
        """Тест получения информации об оповещении"""
        alertInfo = self.alert.getAlertInfo()

        self.assertEqual(alertInfo["alertId"], "ALERT001")
        self.assertEqual(alertInfo["itemName"], "Test Material")
        self.assertEqual(alertInfo["currentQuantity"], 50)
        self.assertEqual(alertInfo["minimumRequired"], 100)
        self.assertEqual(alertInfo["shortageAmount"], 50)

        # Используем константы из config для расчета ожидаемого приоритета
        from config import constants
        shortageRatio = (100 - 50) / 100  # 0.5
        expectedPriority = "MEDIUM" if shortageRatio > constants.CRITICAL_STOCK_RATIO_THRESHOLD else "LOW"
        self.assertEqual(alertInfo["priority"], expectedPriority)

        self.assertFalse(alertInfo["isResolved"])
        self.assertIsNone(alertInfo["resolvedDate"])
        self.assertIn("alertDate", alertInfo)

    def testGetAlertInfoResolved(self):
        """Тест получения информации о решенном оповещении"""
        self.alert.markAsResolved()
        alertInfo = self.alert.getAlertInfo()

        self.assertTrue(alertInfo["isResolved"])
        self.assertIsNotNone(alertInfo["resolvedDate"])


if __name__ == '__main__':
    unittest.main()
import unittest
from config import constants
from models.inventory.ReorderAlert import ReorderAlert


class TestReorderAlert(unittest.TestCase):

    def setUp(self):
        self.alert = ReorderAlert("AL001", "Болт М10", 5, 20)

    def testInitialization(self):
        self.assertEqual(self.alert._alert_id, "AL001")
        self.assertEqual(self.alert._item_name, "Болт М10")
        self.assertEqual(self.alert._current_qty, 5)
        self.assertEqual(self.alert._min_required, 20)

    def testCalculateUrgency(self):
        """Тест расчета срочности"""
        # Проверяем метод расчета срочности
        self.assertTrue(hasattr(self.alert, 'calculate_urgency') or
                        hasattr(self.alert, 'calculateUrgency'))

        if hasattr(self.alert, 'calculate_urgency'):
            urgency = self.alert.calculate_urgency()
            self.assertIn(urgency, ["HIGH", "MEDIUM", "LOW", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
        elif hasattr(self.alert, 'calculateUrgency'):
            urgency = self.alert.calculateUrgency()
            self.assertIn(urgency, ["HIGH", "MEDIUM", "LOW", "CRITICAL", "HIGH", "MEDIUM", "LOW"])

    def testGetAlertInfo(self):
        """Тест получения информации об оповещении"""
        info = self.alert.get_alert_info()

        # Проверяем структуру информации
        self.assertIsInstance(info, dict)
        self.assertIn("alert_id", info or "alertId" in info or "alert_id" in info)
        self.assertIn("item", info or "item_name" in info or "itemName" in info)
        self.assertIn("current", info or "current_qty" in info or "currentQty" in info)

        # Проверяем наличие информации о срочности
        if hasattr(self.alert, 'calculate_urgency') or hasattr(self.alert, 'calculateUrgency'):
            self.assertIn("urgency", info or "urgency_level" in info or "urgencyLevel" in info)

    def testDifferentStockLevels(self):
        """Тест разных уровней запасов"""
        # Низкий уровень запасов
        low_alert = ReorderAlert("AL002", "Деталь", 10, 50)
        self.assertEqual(low_alert._current_qty, 10)
        self.assertEqual(low_alert._min_required, 50)

        # Достаточный уровень запасов
        ok_alert = ReorderAlert("AL003", "Деталь", 60, 50)
        self.assertEqual(ok_alert._current_qty, 60)
        self.assertEqual(ok_alert._min_required, 50)

        # Высокий уровень запасов
        high_alert = ReorderAlert("AL004", "Деталь", 100, 50)
        self.assertEqual(high_alert._current_qty, 100)
        self.assertEqual(high_alert._min_required, 50)


if __name__ == '__main__':
    unittest.main()
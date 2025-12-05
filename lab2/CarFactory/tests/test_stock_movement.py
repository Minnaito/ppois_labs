import unittest
import sys
import os
from unittest.mock import Mock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.inventory.StockMovement import StockMovement


class TestStockMovement(unittest.TestCase):
    """Тесты для класса StockMovement"""

    def setUp(self):
        """Настройка тестового окружения"""
        self.mock_item = Mock()
        self.mock_item.itemName = "Test Product"

        self.stock_movement = StockMovement(
            movementId="MOV001",
            item=self.mock_item,
            quantity=100,
            movementType="IN",
            fromLocation="Supplier A",
            toLocation="Main Warehouse"
        )

    def test_stock_movement_initialization(self):
        """Тест инициализации движения запасов"""
        self.assertEqual(self.stock_movement._movementId, "MOV001")
        self.assertEqual(self.stock_movement._item.itemName, "Test Product")
        self.assertEqual(self.stock_movement._quantity, 100)
        self.assertEqual(self.stock_movement._movementType, "IN")
        self.assertEqual(self.stock_movement._fromLocation, "Supplier A")
        self.assertEqual(self.stock_movement._toLocation, "Main Warehouse")
        self.assertEqual(self.stock_movement._processedBy, "")
        self.assertEqual(self.stock_movement._reason, "")
        self.assertIsNotNone(self.stock_movement._movementDate)

    def test_get_movement_details(self):
        """Тест получения деталей движения"""
        details = self.stock_movement.getMovementDetails()

        self.assertEqual(details["movementId"], "MOV001")
        self.assertEqual(details["itemName"], "Test Product")
        self.assertEqual(details["quantity"], 100)
        self.assertEqual(details["movementType"], "IN")
        self.assertEqual(details["fromLocation"], "Supplier A")
        self.assertEqual(details["toLocation"], "Main Warehouse")
        self.assertEqual(details["processedBy"], "")
        self.assertEqual(details["reason"], "")
        self.assertIsNotNone(details["movementDate"])

    def test_set_processor(self):
        """Тест установки сотрудника-обработчика"""
        self.stock_movement.setProcessor("EMP001")
        self.assertEqual(self.stock_movement._processedBy, "EMP001")

        details = self.stock_movement.getMovementDetails()
        self.assertEqual(details["processedBy"], "EMP001")

    def test_set_reason(self):
        """Тест установки причины движения"""
        self.stock_movement.setReason("Restocking")
        self.assertEqual(self.stock_movement._reason, "Restocking")

        details = self.stock_movement.getMovementDetails()
        self.assertEqual(details["reason"], "Restocking")

    def test_movement_types(self):
        """Тест различных типов движения"""
        movement_types = ["IN", "OUT", "TRANSFER"]

        for movement_type in movement_types:
            with self.subTest(movement_type=movement_type):
                movement = StockMovement(
                    movementId=f"MOV_{movement_type}",
                    item=self.mock_item,
                    quantity=50,
                    movementType=movement_type,
                    fromLocation="Location A",
                    toLocation="Location B"
                )

                details = movement.getMovementDetails()
                self.assertEqual(details["movementType"], movement_type)


if __name__ == '__main__':
    unittest.main()
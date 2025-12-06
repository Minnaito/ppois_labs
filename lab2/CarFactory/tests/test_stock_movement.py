import unittest
from config import constants
from models.inventory.StockMovement import StockMovement


class TestStockMovement(unittest.TestCase):

    def setUp(self):
        self.movement = StockMovement("MV001", "Болт М10", 100, "IN")

    def testInitialization(self):
        self.assertEqual(self.movement._movement_id, "MV001")
        self.assertEqual(self.movement._item_name, "Болт М10")
        self.assertEqual(self.movement._quantity, 100)
        self.assertEqual(self.movement._movement_type, "IN")

    def testValidateMovementValid(self):
        self.assertTrue(self.movement.validate_movement())

    def testValidateMovementInvalidType(self):
        movement = StockMovement("MV002", "Деталь", 50, "INVALID")
        self.assertFalse(movement.validate_movement())

    def testValidateMovementZeroQuantity(self):
        movement = StockMovement("MV003", "Деталь", 0, "OUT")
        self.assertFalse(movement.validate_movement())

    def testGetDetails(self):
        details = self.movement.get_details()
        self.assertEqual(details["item"], "Болт М10")
        self.assertEqual(details["quantity"], 100)


if __name__ == '__main__':
    unittest.main()
import unittest
from config import constants
from models.inventory.Warehouse import Warehouse


class TestWarehouse(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("WH001", 1000)

    def testInitialization(self):
        self.assertEqual(self.warehouse._wh_id, "WH001")
        self.assertEqual(self.warehouse._capacity, 1000)
        self.assertEqual(self.warehouse._stock, 0)

    def testAddItemSuccess(self):
        result = self.warehouse.add_item(500)
        self.assertTrue(result)
        self.assertEqual(self.warehouse._stock, 500)

    def testAddItemFailure(self):
        result = self.warehouse.add_item(1500)
        self.assertFalse(result)
        self.assertEqual(self.warehouse._stock, 0)

    def testCalculateAvailableSpace(self):
        self.warehouse.add_item(300)
        space = self.warehouse.calculate_available_space()
        self.assertEqual(space, 700)

    def testCalculateUtilization(self):
        self.warehouse.add_item(750)
        utilization = self.warehouse.calculate_utilization()
        self.assertEqual(utilization, 75.0)

    def testCheckStockLevelOK(self):
        self.warehouse.add_item(100)
        level = self.warehouse.check_stock_level()
        self.assertEqual(level, "OK")

    def testCheckStockLevelLow(self):
        level = self.warehouse.check_stock_level()
        self.assertEqual(level, "LOW")


if __name__ == '__main__':
    unittest.main()
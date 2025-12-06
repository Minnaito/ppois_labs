import unittest
from config import constants
from models.inventory.Supplier import Supplier


class TestSupplier(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("SUP001", "МеталлСервис", "8-800-555-3535", 4.5)

    def testInitialization(self):
        self.assertEqual(self.supplier._supplierIdentifier, "SUP001")
        self.assertEqual(self.supplier._supplierName, "МеталлСервис")
        self.assertEqual(self.supplier._rating, 4.5)

    def testProcessOrder(self):
        order = self.supplier.processOrder("Алюминий", 100, 500.0)
        self.assertEqual(order["supplierId"], "SUP001")
        self.assertEqual(order["totalAmount"], 50000.0)

    def testGetSupplierInfo(self):
        info = self.supplier.getSupplierInfo()
        self.assertEqual(info["supplierName"], "МеталлСервис")
        self.assertEqual(info["rating"], 4.5)


if __name__ == '__main__':
    unittest.main()
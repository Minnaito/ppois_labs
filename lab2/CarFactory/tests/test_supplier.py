import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.inventory.Supplier import Supplier

class TestSupplier(unittest.TestCase):
    """Тесты для поставщика"""

    def setUp(self):
        self.supplier = Supplier("SUP001", "Стальной поставщик", "contact@steel.com", 4.5)

    def testSupplierInitialization(self):
        self.assertEqual(self.supplier._supplierIdentifier, "SUP001")
        self.assertEqual(self.supplier._supplierName, "Стальной поставщик")

    def testAddMaterial(self):
        self.supplier.addMaterial("Стальной лист")
        self.assertIn("Стальной лист", self.supplier._suppliedMaterials)

    def testProcessOrder(self):
        self.supplier.addMaterial("Стальной лист")
        order = self.supplier.processOrder("Стальной лист", 100, 150.0)
        self.assertEqual(order["orderStatus"], "PROCESSED")
        self.assertEqual(order["totalAmount"], 15000.0)

    def testProcessOrderInvalidMaterial(self):
        with self.assertRaises(ValueError):
            self.supplier.processOrder("Неизвестный материал", 100, 150.0)

    def testGetSupplierInfo(self):
        info = self.supplier.getSupplierInfo()
        self.assertEqual(info["supplierIdentifier"], "SUP001")
        self.assertEqual(info["rating"], 4.5)

if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.finance.Invoice import Invoice
from models.inventory.Supplier import Supplier

class TestInvoice(unittest.TestCase):
    """Тесты для счетов"""

    def setUp(self):
        self.supplier = Supplier("SUP001", "Поставщик стальных деталей", "contact@supplier.com", 4.5)
        self.invoice = Invoice("INV001", self.supplier, 5000.0, "2024-02-01")

    def test_invoice_initialization(self):
        self.assertEqual(self.invoice.invoiceIdentifier, "INV001")
        self.assertEqual(self.invoice.invoiceAmount, 5000.0)

    def test_invoice_processing(self):
        result = self.invoice.processInvoice()
        self.assertEqual(result["status"], "PROCESSED")

if __name__ == '__main__':
    unittest.main()
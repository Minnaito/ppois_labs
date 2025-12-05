import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.finance.Transaction import Transaction
from exceptions.FinanceExceptions.InsufficientFundsError import InsufficientFundsError

class TestTransaction(unittest.TestCase):
    """Тесты для финансовых транзакций"""

    def setUp(self):
        self.transaction = Transaction("T001", 1000.0, "DEBIT", "Закупка материалов")

    def testTransactionInitialization(self):
        self.assertEqual(self.transaction._transactionIdentifier, "T001")
        self.assertEqual(self.transaction._transactionAmount, 1000.0)

    def testInsufficientFunds(self):
        with self.assertRaises(InsufficientFundsError):
            self.transaction.processTransaction(500.0)

    def testProcessTransaction(self):
        newBalance = self.transaction.processTransaction(1500.0)
        self.assertEqual(newBalance, 500.0)
        self.assertEqual(self.transaction._transactionStatus, "COMPLETED")

    def testCalculateTax(self):
        taxAmount = self.transaction.calculateTax()
        self.assertGreater(taxAmount, 0)

    def testGetTransactionDetails(self):
        details = self.transaction.getTransactionDetails()
        self.assertEqual(details["transactionIdentifier"], "T001")
        self.assertEqual(details["transactionType"], "DEBIT")

if __name__ == '__main__':
    unittest.main()
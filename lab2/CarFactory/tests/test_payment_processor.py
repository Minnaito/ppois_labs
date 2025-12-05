import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.utilities.PaymentProcessor import PaymentProcessor
from exceptions.FinanceExceptions.InsufficientFundsError import InsufficientFundsError

class TestPaymentProcessor(unittest.TestCase):
    """Тесты для процессора платежей"""

    def setUp(self):
        self.processor = PaymentProcessor("PP001")

    def testTransferFunds(self):
        fromBalance, toBalance = self.processor.transferFunds(10000, 5000, 2000)
        self.assertEqual(fromBalance, 8000)
        self.assertEqual(toBalance, 7000)

    def testTransferInsufficientFunds(self):
        with self.assertRaises(InsufficientFundsError):
            self.processor.transferFunds(1000, 5000, 2000)

    def testValidatePassword(self):
        # Сильный пароль
        result = self.processor.validatePassword("SecurePass123!")
        self.assertTrue(result["isValid"])
        self.assertGreaterEqual(result["score"], 70)

        # Слабый пароль
        weakResult = self.processor.validatePassword("123")
        self.assertFalse(weakResult["isValid"])

    def testGetProcessorStats(self):
        self.processor.transferFunds(10000, 5000, 2000)
        stats = self.processor.getProcessorStats()
        self.assertEqual(stats["processedTransactions"], 1)
        self.assertEqual(stats["successfulTransactions"], 1)

if __name__ == '__main__':
    unittest.main()
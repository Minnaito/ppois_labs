import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.finance.Payment import Payment
from config import constants


class TestPayment(unittest.TestCase):
    """Тесты для класса Payment"""

    def setUp(self):
        """Настройка тестового окружения"""
        self.paymentData = {
            "paymentId": "PAY001",
            "paymentAmount": 1000.0,
            "paymentMethod": "BANK_TRANSFER",
            "recipient": "Supplier ABC"
        }
        self.payment = Payment(**self.paymentData)

    def testPaymentInitialization(self):
        """Тест инициализации платежа"""
        self.assertEqual(self.payment._paymentId, "PAY001")
        self.assertEqual(self.payment._paymentAmount, 1000.0)
        self.assertEqual(self.payment._paymentMethod, "BANK_TRANSFER")
        self.assertEqual(self.payment._recipient, "Supplier ABC")
        self.assertEqual(self.payment._paymentStatus, "PENDING")
        self.assertEqual(self.payment._transactionFee, 0.0)

    def testProcessPaymentBankTransfer(self):
        """Тест обработки платежа банковским переводом"""
        result = self.payment.processPayment()

        self.assertTrue(result)
        self.assertEqual(self.payment._paymentStatus, "PROCESSED")
        self.assertEqual(self.payment._transactionFee, constants.BANK_TRANSFER_FEE_AMOUNT)

    def testProcessPaymentCreditCard(self):
        """Тест обработки платежа кредитной картой"""
        creditCardPayment = Payment(
            paymentId="PAY002",
            paymentAmount=500.0,
            paymentMethod="CREDIT_CARD",
            recipient="Vendor XYZ"
        )

        result = creditCardPayment.processPayment()

        self.assertTrue(result)
        self.assertEqual(creditCardPayment._paymentStatus, "PROCESSED")
        expectedFee = 500.0 * constants.CREDIT_CARD_FEE_PERCENTAGE
        self.assertEqual(creditCardPayment._transactionFee, expectedFee)

    def testGetTotalAmount(self):
        """Тест расчета общей суммы платежа"""
        self.payment.processPayment()
        totalAmount = self.payment.getTotalAmount()

        expectedTotal = 1000.0 + constants.BANK_TRANSFER_FEE_AMOUNT
        self.assertEqual(totalAmount, expectedTotal)

    def testGetPaymentDetails(self):
        """Тест получения деталей платежа"""
        self.payment.processPayment()
        details = self.payment.getPaymentDetails()

        self.assertEqual(details["paymentId"], "PAY001")
        self.assertEqual(details["paymentAmount"], 1000.0)
        self.assertEqual(details["paymentMethod"], "BANK_TRANSFER")
        self.assertEqual(details["recipient"], "Supplier ABC")
        self.assertEqual(details["paymentStatus"], "PROCESSED")
        self.assertEqual(details["transactionFee"], constants.BANK_TRANSFER_FEE_AMOUNT)
        self.assertIn("totalAmount", details)


if __name__ == '__main__':
    unittest.main()
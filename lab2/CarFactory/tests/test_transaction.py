import unittest
from config import constants
from models.finance.Transaction import Transaction


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.transaction = Transaction("T001", 50000, "DEBIT")

    def testInitialization(self):
        self.assertEqual(self.transaction._trans_id, "T001")
        self.assertEqual(self.transaction._amount, 50000)
        self.assertEqual(self.transaction._trans_type, "DEBIT")

    def testProcessDebit(self):
        new_balance = self.transaction.process(100000)
        self.assertEqual(new_balance, 50000)

    def testProcessCredit(self):
        transaction = Transaction("T002", 30000, "CREDIT")
        new_balance = transaction.process(50000)
        self.assertEqual(new_balance, 80000)

    def testCalculateFee(self):
        fee = self.transaction.calculate_fee()
        expected_fee = 50000 * constants.STANDARD_TAX_RATE
        self.assertEqual(fee, expected_fee)

    def testValidateTrue(self):
        self.assertTrue(self.transaction.validate())

    def testValidateFalse(self):
        transaction = Transaction("T003", -1000, "DEBIT")
        self.assertFalse(transaction.validate())


if __name__ == '__main__':
    unittest.main()
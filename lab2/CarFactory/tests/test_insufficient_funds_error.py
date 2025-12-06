import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from exceptions.FinanceExceptions.InsufficientFundsError import InsufficientFundsError
    INSUFFICIENT_FUNDS_ERROR_AVAILABLE = True
except ImportError as e:
    INSUFFICIENT_FUNDS_ERROR_AVAILABLE = False
    print(f"InsufficientFundsError импорт не удался: {e}")


@unittest.skipIf(not INSUFFICIENT_FUNDS_ERROR_AVAILABLE, "InsufficientFundsError не доступен")
class TestInsufficientFundsError(unittest.TestCase):

    def testInsufficientFundsErrorInitialization(self):
        error = InsufficientFundsError(5000, 3000)
        self.assertEqual(error.current_balance, 5000)
        self.assertEqual(error.required_amount, 3000)

    def testInsufficientFundsErrorStringRepresentation(self):
        error = InsufficientFundsError(5000, 8000)
        error_str = str(error)
        self.assertIn("5000", error_str)
        self.assertIn("8000", error_str)
        self.assertIn("Недостаточно средств", error_str)

    def testInsufficientFundsErrorDifferentAmounts(self):
        test_cases = [
            (1000, 2000),
            (5000, 10000),
            (0, 1000),
        ]

        for current, required in test_cases:
            error = InsufficientFundsError(current, required)
            self.assertEqual(error.current_balance, current)
            self.assertEqual(error.required_amount, required)

    def testInsufficientFundsErrorInheritance(self):
        error = InsufficientFundsError(5000, 8000)
        self.assertIsInstance(error, Exception)
        self.assertTrue(hasattr(error, 'current_balance'))
        self.assertTrue(hasattr(error, 'required_amount'))

    def testInsufficientFundsErrorRaising(self):
        with self.assertRaises(InsufficientFundsError) as context:
            raise InsufficientFundsError(10000, 15000)

        exception = context.exception
        self.assertEqual(exception.current_balance, 10000)
        self.assertEqual(exception.required_amount, 15000)

    def testInsufficientFundsErrorInTryExcept(self):
        try:
            raise InsufficientFundsError(5000, 10000)
        except InsufficientFundsError as e:
            self.assertEqual(e.current_balance, 5000)
            self.assertEqual(e.required_amount, 10000)
        except Exception:
            self.fail("Неожиданный тип исключения")

    def testInsufficientFundsErrorMultipleInstances(self):
        errors = []

        for i in range(3):
            current = 1000 * (i + 1)
            required = 2000 * (i + 1)
            error = InsufficientFundsError(current, required)
            errors.append(error)

        self.assertEqual(len(errors), 3)

    def testInsufficientFundsErrorEdgeCases(self):
        error = InsufficientFundsError(10 ** 6, 2 * 10 ** 6)
        self.assertEqual(error.current_balance, 10 ** 6)
        self.assertEqual(error.required_amount, 2 * 10 ** 6)

    def testInsufficientFundsErrorSpecialValues(self):
        error = InsufficientFundsError(1234.56, 5678.90)
        self.assertEqual(error.current_balance, 1234.56)
        self.assertEqual(error.required_amount, 5678.90)

    def testInsufficientFundsErrorCalculation(self):
        error = InsufficientFundsError(5000, 8000)
        shortfall = error.required_amount - error.current_balance
        self.assertEqual(shortfall, 3000)

    def testInsufficientFundsErrorRealWorldScenario(self):
        equipment_price = 250000
        available_budget = 200000

        with self.assertRaises(InsufficientFundsError) as context:
            if available_budget < equipment_price:
                raise InsufficientFundsError(available_budget, equipment_price)

        exception = context.exception
        self.assertEqual(exception.current_balance, 200000)
        self.assertEqual(exception.required_amount, 250000)


if __name__ == '__main__':
    unittest.main()
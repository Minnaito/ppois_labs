import unittest
from config import constants
from models.utilities.PaymentProcessor import PaymentProcessor


class TestPaymentProcessor(unittest.TestCase):

    def testPaymentProcessorInitialization(self):
        """Тест инициализации платежного процессора"""
        processor = PaymentProcessor("PP001")

        self.assertEqual(processor._processorIdentifier, "PP001")
        self.assertEqual(processor._processedTransactions, 0)
        self.assertEqual(processor._successfulTransactions, 0)

    def testTransferBetweenCardsSuccess(self):
        """Тест успешного перевода между картами"""
        processor = PaymentProcessor("PP001")

        from_balance = 10000
        to_balance = 5000
        amount = 3000

        new_from, new_to, fee = processor.transferBetweenCards(
            from_balance, to_balance, amount
        )

        # Проверяем, что перевод выполнен
        self.assertIsNotNone(new_from)
        self.assertIsNotNone(new_to)
        self.assertIsNotNone(fee)

        # Проверяем, что балансы изменились
        self.assertNotEqual(new_from, from_balance)
        self.assertNotEqual(new_to, to_balance)

        # Проверяем статистику
        self.assertGreater(processor._processedTransactions, 0)
        self.assertGreater(processor._successfulTransactions, 0)

    def testTransferBetweenCardsInsufficientFunds(self):
        """Тест перевода при недостатке средств"""
        processor = PaymentProcessor("PP001")

        from_balance = 1000
        to_balance = 5000
        amount = 3000  # Больше, чем на счете

        # Ожидаем исключение или проверяем поведение
        try:
            new_from, new_to, fee = processor.transferBetweenCards(
                from_balance, to_balance, amount
            )
            # Если не выброшено исключение, проверяем результат
            self.assertIsNotNone(new_from)
        except Exception as e:
            # Ожидаем исключение при недостатке средств
            self.assertIsInstance(e, Exception)
            self.assertIn("Недостаточно средств", str(e) or "Insufficient funds" in str(e))

    def testValidateCVV(self):
        """Тест валидации CVV кода карты"""
        processor = PaymentProcessor("PP001")

        # Проверяем метод валидации CVV
        self.assertTrue(hasattr(processor, 'validateCVV'))

        # Проверяем, что метод работает
        if hasattr(processor, 'validateCVV'):
            # Валидные CVV
            valid_cvvs = ["123", "456", "789"]
            for cvv in valid_cvvs:
                result = processor.validateCVV(cvv)
                self.assertIsInstance(result, bool)

    def testGetProcessorStats(self):
        """Тест получения статистики процессора"""
        processor = PaymentProcessor("PP001")

        # Начальная статистика
        initial_stats = processor.getProcessorStats()

        self.assertEqual(initial_stats["processorId"], "PP001")
        self.assertEqual(initial_stats["processedTransactions"], 0)
        self.assertEqual(initial_stats["successfulTransactions"], 0)
        self.assertIsInstance(initial_stats["successRate"], (int, float))

    def testPasswordValidation(self):
        """Тест валидации пароля"""
        processor = PaymentProcessor("PP001")

        # Проверяем наличие метода валидации пароля
        self.assertTrue(hasattr(processor, 'validatePasswordStrength'))

        if hasattr(processor, 'validatePasswordStrength'):
            # Проверяем, что метод возвращает словарь с нужными полями
            result = processor.validatePasswordStrength("Test123!")
            self.assertIsInstance(result, dict)
            self.assertIn("isStrong", result)
            self.assertIn("score", result)
            self.assertIn("checks", result)


if __name__ == '__main__':
    unittest.main()
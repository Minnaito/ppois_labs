import unittest
from config import constants
from models.finance.Payment import Payment


class TestPayment(unittest.TestCase):

    def testPaymentInitialization(self):
        """Тест инициализации платежа"""
        payment = Payment("PAY001", 100000, "BANK_TRANSFER")

        self.assertEqual(payment._payment_id, "PAY001")
        self.assertEqual(payment._amount, 100000)
        self.assertEqual(payment._method, "BANK_TRANSFER")

    def testPaymentProcessBankTransfer(self):
        """Тест обработки банковского перевода"""
        payment = Payment("PAY001", 100000, "BANK_TRANSFER")

        result = payment.process()

        # Проверяем структуру результата
        self.assertEqual(result["payment_id"], "PAY001")
        self.assertEqual(result["amount"], 100000)
        self.assertEqual(result["method"], "BANK_TRANSFER")

        # Проверяем комиссию для банковского перевода
        expected_fee = constants.BANK_TRANSFER_FEE_AMOUNT
        self.assertEqual(result["fee"], expected_fee)

        # Проверяем общую сумму
        expected_total = 100000 + expected_fee
        self.assertEqual(result["total"], expected_total)

    def testPaymentProcessCreditCard(self):
        """Тест обработки платежа кредитной картой"""
        payment = Payment("PAY001", 100000, "CREDIT_CARD")

        result = payment.process()

        # Проверяем структуру результата
        self.assertEqual(result["payment_id"], "PAY001")
        self.assertEqual(result["amount"], 100000)
        self.assertEqual(result["method"], "CREDIT_CARD")

        # Проверяем комиссию для кредитной карты
        expected_fee = 100000 * constants.STANDARD_TAX_RATE
        self.assertEqual(result["fee"], expected_fee)

        # Проверяем общую сумму
        expected_total = 100000 + expected_fee
        self.assertEqual(result["total"], expected_total)

    def testPaymentProcessOtherMethod(self):
        """Тест обработки платежа другим методом"""
        payment = Payment("PAY001", 100000, "CASH")

        result = payment.process()

        # Проверяем структуру результата
        self.assertEqual(result["payment_id"], "PAY001")
        self.assertEqual(result["amount"], 100000)
        self.assertEqual(result["method"], "CASH")

        # Для других методов комиссия должна быть 0
        self.assertEqual(result["fee"], 0)

        # Проверяем общую сумму
        self.assertEqual(result["total"], 100000)

    def testPaymentProcessDifferentAmounts(self):
        """Тест обработки платежей с разными суммами"""
        test_cases = [
            (50000, "BANK_TRANSFER", constants.BANK_TRANSFER_FEE_AMOUNT),
            (100000, "BANK_TRANSFER", constants.BANK_TRANSFER_FEE_AMOUNT),
            (200000, "BANK_TRANSFER", constants.BANK_TRANSFER_FEE_AMOUNT),
            (50000, "CREDIT_CARD", 50000 * constants.STANDARD_TAX_RATE),
            (100000, "CREDIT_CARD", 100000 * constants.STANDARD_TAX_RATE),
            (200000, "CREDIT_CARD", 200000 * constants.STANDARD_TAX_RATE),
            (50000, "CASH", 0),
            (100000, "CASH", 0),
            (200000, "CASH", 0),
        ]

        for amount, method, expected_fee in test_cases:
            payment = Payment(f"PAY_{amount}_{method}", amount, method)
            result = payment.process()

            self.assertEqual(result["amount"], amount)
            self.assertEqual(result["method"], method)
            self.assertEqual(result["fee"], expected_fee)
            self.assertEqual(result["total"], amount + expected_fee)

    def testPaymentProcessNegativeAmount(self):
        """Тест обработки платежа с отрицательной суммой"""
        payment = Payment("PAY_NEG", -50000, "BANK_TRANSFER")
        result = payment.process()

        # Комиссия должна быть положительной даже для отрицательной суммы
        expected_fee = constants.BANK_TRANSFER_FEE_AMOUNT
        self.assertEqual(result["fee"], expected_fee)

        # Общая сумма: -50000 + комиссия
        expected_total = -50000 + expected_fee
        self.assertEqual(result["total"], expected_total)

    def testPaymentProcessZeroAmount(self):
        """Тест обработки платежа с нулевой суммой"""
        payment = Payment("PAY_ZERO", 0, "BANK_TRANSFER")
        result = payment.process()

        # Комиссия все равно взимается
        expected_fee = constants.BANK_TRANSFER_FEE_AMOUNT
        self.assertEqual(result["fee"], expected_fee)

        # Общая сумма равна комиссии
        self.assertEqual(result["total"], expected_fee)

    def testPaymentProcessDecimalAmount(self):
        """Тест обработки платежа с дробной суммой"""
        payment = Payment("PAY_DEC", 123456.78, "CREDIT_CARD")
        result = payment.process()

        expected_fee = 123456.78 * constants.STANDARD_TAX_RATE
        expected_total = 123456.78 + expected_fee

        self.assertAlmostEqual(result["fee"], expected_fee, places=2)
        self.assertAlmostEqual(result["total"], expected_total, places=2)

    def testPaymentStructure(self):
        """Тест структуры результата обработки платежа"""
        payment = Payment("PAY001", 100000, "BANK_TRANSFER")
        result = payment.process()

        # Проверяем наличие всех полей
        required_fields = ["payment_id", "amount", "method", "fee", "total"]
        for field in required_fields:
            self.assertIn(field, result)

        # Проверяем типы данных
        self.assertIsInstance(result["payment_id"], str)
        self.assertIsInstance(result["amount"], (int, float))
        self.assertIsInstance(result["method"], str)
        self.assertIsInstance(result["fee"], (int, float))
        self.assertIsInstance(result["total"], (int, float))

    def testPaymentFeeCalculation(self):
        """Тест точности расчета комиссии"""
        # Банковский перевод - фиксированная комиссия
        payment1 = Payment("PAY1", 100000, "BANK_TRANSFER")
        result1 = payment1.process()
        self.assertEqual(result1["fee"], constants.BANK_TRANSFER_FEE_AMOUNT)

        # Кредитная карта - процентная комиссия
        payment2 = Payment("PAY2", 100000, "CREDIT_CARD")
        result2 = payment2.process()
        expected_fee2 = 100000 * constants.STANDARD_TAX_RATE
        self.assertEqual(result2["fee"], expected_fee2)

        # Другие методы - без комиссии
        payment3 = Payment("PAY3", 100000, "PAYPAL")
        result3 = payment3.process()
        self.assertEqual(result3["fee"], 0)

    def testPaymentWithDifferentConstants(self):
        """Тест платежа с разными значениями констант"""
        # Сохраняем оригинальные значения
        original_bank_fee = constants.BANK_TRANSFER_FEE_AMOUNT
        original_tax_rate = constants.STANDARD_TAX_RATE

        try:
            # Тест с разными комиссиями
            test_cases = [
                (500, 0.02),  # Банковская комиссия 500, налог 2%
                (1000, 0.03),  # Банковская комиссия 1000, налог 3%
                (0, 0.0),  # Без комиссий
            ]

            for bank_fee, tax_rate in test_cases:
                # Временно меняем константы
                constants.BANK_TRANSFER_FEE_AMOUNT = bank_fee
                constants.STANDARD_TAX_RATE = tax_rate

                # Тестируем банковский перевод
                payment_bank = Payment("PAY_BANK", 100000, "BANK_TRANSFER")
                result_bank = payment_bank.process()
                self.assertEqual(result_bank["fee"], bank_fee)
                self.assertEqual(result_bank["total"], 100000 + bank_fee)

                # Тестируем кредитную карту
                payment_card = Payment("PAY_CARD", 100000, "CREDIT_CARD")
                result_card = payment_card.process()
                expected_card_fee = 100000 * tax_rate
                self.assertEqual(result_card["fee"], expected_card_fee)
                self.assertEqual(result_card["total"], 100000 + expected_card_fee)

        finally:
            # Восстанавливаем оригинальные значения
            constants.BANK_TRANSFER_FEE_AMOUNT = original_bank_fee
            constants.STANDARD_TAX_RATE = original_tax_rate

    def testPaymentEdgeCases(self):
        """Тест крайних случаев"""
        # Очень большая сумма
        large_amount = 10 ** 9  # 1 миллиард
        payment = Payment("PAY_LARGE", large_amount, "CREDIT_CARD")
        result = payment.process()

        expected_fee = large_amount * constants.STANDARD_TAX_RATE
        self.assertEqual(result["fee"], expected_fee)

        # Очень маленькая сумма
        small_amount = 0.01
        payment = Payment("PAY_SMALL", small_amount, "BANK_TRANSFER")
        result = payment.process()

        self.assertEqual(result["fee"], constants.BANK_TRANSFER_FEE_AMOUNT)
        # Комиссия может быть больше самой суммы
        self.assertEqual(result["total"], small_amount + constants.BANK_TRANSFER_FEE_AMOUNT)

    def testMultiplePayments(self):
        """Тест работы с несколькими платежами"""
        payments = []

        methods = ["BANK_TRANSFER", "CREDIT_CARD", "CASH", "PAYPAL", "WIRE_TRANSFER"]

        for i, method in enumerate(methods):
            amount = 20000 * (i + 1)
            payment = Payment(f"PAY{i + 1:03d}", amount, method)
            payments.append(payment)

        # Обрабатываем и проверяем каждый платеж
        for i, payment in enumerate(payments):
            method = methods[i]
            amount = 20000 * (i + 1)
            result = payment.process()

            # Определяем ожидаемую комиссию
            if method == "BANK_TRANSFER":
                expected_fee = constants.BANK_TRANSFER_FEE_AMOUNT
            elif method == "CREDIT_CARD":
                expected_fee = amount * constants.STANDARD_TAX_RATE
            else:
                expected_fee = 0

            expected_total = amount + expected_fee

            self.assertEqual(result["payment_id"], f"PAY{i + 1:03d}")
            self.assertEqual(result["amount"], amount)
            self.assertEqual(result["method"], method)
            self.assertEqual(result["fee"], expected_fee)
            self.assertEqual(result["total"], expected_total)

    def testPaymentProperties(self):
        """Тест свойств платежа"""
        payment = Payment("PAY001", 100000, "BANK_TRANSFER")

        # Проверяем начальные свойства
        self.assertEqual(payment._payment_id, "PAY001")
        self.assertEqual(payment._amount, 100000)
        self.assertEqual(payment._method, "BANK_TRANSFER")

        # После обработки
        result = payment.process()

        # Проверяем, что свойства результата совпадают
        self.assertEqual(result["payment_id"], payment._payment_id)
        self.assertEqual(result["amount"], payment._amount)
        self.assertEqual(result["method"], payment._method)


if __name__ == '__main__':
    unittest.main()
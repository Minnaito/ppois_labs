import unittest
from config import constants
from models.finance.Invoice import Invoice


class TestInvoice(unittest.TestCase):

    def testInvoiceInitialization(self):
        """Тест инициализации счета"""
        invoice = Invoice("INV001", 250000)

        self.assertEqual(invoice._invoice_id, "INV001")
        self.assertEqual(invoice._amount, 250000)
        self.assertEqual(invoice._status, "PENDING")

    def testInvoiceProcess(self):
        """Тест обработки счета"""
        invoice = Invoice("INV001", 250000)

        result = invoice.process()

        # Проверяем структуру результата
        self.assertEqual(result["invoice_id"], "INV001")
        self.assertEqual(result["amount"], 250000)

        # Проверяем расчет налога
        expected_tax = 250000 * constants.STANDARD_TAX_RATE
        self.assertEqual(result["tax"], expected_tax)

        # Проверяем общую сумму
        expected_total = 250000 + expected_tax
        self.assertEqual(result["total"], expected_total)

        # Проверяем статус
        self.assertEqual(result["status"], "APPROVED")
        self.assertEqual(invoice._status, "APPROVED")

    def testInvoiceProcessDifferentAmounts(self):
        """Тест обработки счетов с разными суммами"""
        test_cases = [
            (100000, 100000 * constants.STANDARD_TAX_RATE),
            (500000, 500000 * constants.STANDARD_TAX_RATE),
            (1000000, 1000000 * constants.STANDARD_TAX_RATE),
            (0, 0),  # Нулевая сумма
            (1, 1 * constants.STANDARD_TAX_RATE),  # Минимальная сумма
        ]

        for amount, expected_tax in test_cases:
            invoice = Invoice(f"INV_{amount}", amount)
            result = invoice.process()

            self.assertEqual(result["amount"], amount)
            self.assertEqual(result["tax"], expected_tax)
            self.assertEqual(result["total"], amount + expected_tax)
            self.assertEqual(result["status"], "APPROVED")

    def testInvoiceProcessNegativeAmount(self):
        """Тест обработки счета с отрицательной суммой"""
        invoice = Invoice("INV_NEG", -100000)
        result = invoice.process()

        # Проверяем, что отрицательная сумма обрабатывается
        expected_tax = -100000 * constants.STANDARD_TAX_RATE
        self.assertEqual(result["tax"], expected_tax)
        self.assertEqual(result["total"], -100000 + expected_tax)

    def testInvoiceProcessDecimalAmount(self):
        """Тест обработки счета с дробной суммой"""
        invoice = Invoice("INV_DEC", 123456.78)
        result = invoice.process()

        expected_tax = 123456.78 * constants.STANDARD_TAX_RATE
        expected_total = 123456.78 + expected_tax

        self.assertAlmostEqual(result["tax"], expected_tax, places=2)
        self.assertAlmostEqual(result["total"], expected_total, places=2)

    def testInvoiceStatusTransition(self):
        """Тест перехода статуса счета"""
        invoice = Invoice("INV001", 250000)

        # Изначальный статус
        self.assertEqual(invoice._status, "PENDING")

        # После обработки
        invoice.process()
        self.assertEqual(invoice._status, "APPROVED")

    def testInvoiceMultipleProcessing(self):
        """Тест многократной обработки счета"""
        invoice = Invoice("INV001", 250000)

        # Первая обработка
        result1 = invoice.process()
        self.assertEqual(result1["status"], "APPROVED")
        self.assertEqual(invoice._status, "APPROVED")

        # Вторая обработка (статус должен остаться APPROVED)
        result2 = invoice.process()
        self.assertEqual(result2["status"], "APPROVED")
        self.assertEqual(invoice._status, "APPROVED")

    def testInvoiceStructure(self):
        """Тест структуры результата обработки счета"""
        invoice = Invoice("INV001", 100000)
        result = invoice.process()

        # Проверяем наличие всех полей
        required_fields = ["invoice_id", "amount", "tax", "total", "status"]
        for field in required_fields:
            self.assertIn(field, result)

        # Проверяем типы данных
        self.assertIsInstance(result["invoice_id"], str)
        self.assertIsInstance(result["amount"], (int, float))
        self.assertIsInstance(result["tax"], (int, float))
        self.assertIsInstance(result["total"], (int, float))
        self.assertIsInstance(result["status"], str)

    def testInvoiceTaxCalculation(self):
        """Тест точности расчета налога"""
        invoice = Invoice("INV001", 100000)
        result = invoice.process()

        # Проверяем, что налог рассчитывается правильно
        expected_tax = 100000 * constants.STANDARD_TAX_RATE
        self.assertEqual(result["tax"], expected_tax)

        # Проверяем, что общая сумма правильная
        expected_total = 100000 + expected_tax
        self.assertEqual(result["total"], expected_total)

    def testInvoiceWithDifferentConstants(self):
        """Тест счета с разными налоговыми ставками"""
        # Сохраняем оригинальную ставку
        original_tax_rate = constants.STANDARD_TAX_RATE

        try:
            # Тест с разными ставками
            test_rates = [0.1, 0.15, 0.2, 0.25, 0.0]

            for tax_rate in test_rates:
                # Временно меняем константу
                constants.STANDARD_TAX_RATE = tax_rate

                invoice = Invoice("INV_TEST", 100000)
                result = invoice.process()

                expected_tax = 100000 * tax_rate
                expected_total = 100000 + expected_tax

                self.assertEqual(result["tax"], expected_tax)
                self.assertEqual(result["total"], expected_total)

        finally:
            # Восстанавливаем оригинальную ставку
            constants.STANDARD_TAX_RATE = original_tax_rate

    def testInvoiceEdgeCases(self):
        """Тест крайних случаев"""
        # Очень большая сумма
        large_amount = 10 ** 12  # 1 триллион
        invoice = Invoice("INV_LARGE", large_amount)
        result = invoice.process()

        expected_tax = large_amount * constants.STANDARD_TAX_RATE
        self.assertEqual(result["tax"], expected_tax)

        # Очень маленькая сумма
        small_amount = 0.01
        invoice = Invoice("INV_SMALL", small_amount)
        result = invoice.process()

        expected_tax = small_amount * constants.STANDARD_TAX_RATE
        self.assertAlmostEqual(result["tax"], expected_tax, places=4)

    def testMultipleInvoices(self):
        """Тест работы с несколькими счетами"""
        invoices = []

        for i in range(5):
            amount = 50000 * (i + 1)
            invoice = Invoice(f"INV{i + 1:03d}", amount)
            invoices.append(invoice)

        # Обрабатываем и проверяем каждый счет
        for i, invoice in enumerate(invoices):
            amount = 50000 * (i + 1)
            result = invoice.process()

            expected_tax = amount * constants.STANDARD_TAX_RATE
            expected_total = amount + expected_tax

            self.assertEqual(result["invoice_id"], f"INV{i + 1:03d}")
            self.assertEqual(result["amount"], amount)
            self.assertEqual(result["tax"], expected_tax)
            self.assertEqual(result["total"], expected_total)
            self.assertEqual(result["status"], "APPROVED")

            # Проверяем статус объекта
            self.assertEqual(invoice._status, "APPROVED")

    def testInvoiceProperties(self):
        """Тест свойств счета"""
        invoice = Invoice("INV001", 250000)

        # Проверяем начальные свойства
        self.assertEqual(invoice._invoice_id, "INV001")
        self.assertEqual(invoice._amount, 250000)
        self.assertEqual(invoice._status, "PENDING")

        # После обработки
        result = invoice.process()
        self.assertEqual(invoice._status, "APPROVED")

        # Проверяем, что свойства результата совпадают
        self.assertEqual(result["invoice_id"], invoice._invoice_id)
        self.assertEqual(result["amount"], invoice._amount)
        self.assertEqual(result["status"], invoice._status)


if __name__ == '__main__':
    unittest.main()
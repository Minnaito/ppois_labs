import unittest
from config import constants
from models.inventory.InventoryItem import InventoryItem


class TestInventoryItem(unittest.TestCase):

    def testInventoryItemInitialization(self):
        """Тест инициализации элемента инвентаря"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)

        self.assertEqual(item._itemIdentifier, "ITEM001")
        self.assertEqual(item._itemName, "Болт М10")
        self.assertEqual(item._itemType, "крепление")
        self.assertEqual(item._unitPrice, 5.0)
        self.assertEqual(item._currentQuantity, 0)
        self.assertEqual(item._minimumStockLevel, constants.MINIMUM_STOCK_LEVEL)

    def testUpdateItemQuantity(self):
        """Тест обновления количества элемента"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)

        # Устанавливаем положительное количество
        item.updateItemQuantity(100)
        self.assertEqual(item._currentQuantity, 100)

        # Обновляем количество
        item.updateItemQuantity(150)
        self.assertEqual(item._currentQuantity, 150)

        # Устанавливаем 0
        item.updateItemQuantity(0)
        self.assertEqual(item._currentQuantity, 0)

    def testUpdateItemQuantityNegative(self):
        """Тест обновления количества с отрицательным значением"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)

        # Ожидаем исключение при отрицательном количестве
        with self.assertRaises(Exception) as context:
            item.updateItemQuantity(-50)

        # Проверяем, что количество не изменилось
        self.assertEqual(item._currentQuantity, 0)

    def testCalculateTotalValue(self):
        """Тест расчета общей стоимости"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)

        # С нулевым количеством
        value = item.calculateTotalValue()
        self.assertEqual(value, 0)

        # С положительным количеством
        item.updateItemQuantity(100)
        value = item.calculateTotalValue()
        expected_value = 100 * 5.0
        self.assertEqual(value, expected_value)

        # С другим количеством
        item.updateItemQuantity(250)
        value = item.calculateTotalValue()
        expected_value = 250 * 5.0
        self.assertEqual(value, expected_value)

    def testCalculateTotalValueDifferentPrices(self):
        """Тест расчета стоимости при разных ценах"""
        test_cases = [
            ("ITEM001", "Деталь 1", "деталь", 10.0, 50, 500.0),
            ("ITEM002", "Деталь 2", "деталь", 25.5, 100, 2550.0),
            ("ITEM003", "Деталь 3", "деталь", 0.5, 1000, 500.0),
            ("ITEM004", "Деталь 4", "деталь", 1000.0, 5, 5000.0),
        ]

        for item_id, name, item_type, price, quantity, expected_value in test_cases:
            item = InventoryItem(item_id, name, item_type, price)
            item.updateItemQuantity(quantity)
            value = item.calculateTotalValue()
            self.assertEqual(value, expected_value)

    def testNeedsReorder(self):
        """Тест проверки необходимости повторного заказа"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)

        # Ниже минимального уровня
        item.updateItemQuantity(constants.MINIMUM_STOCK_LEVEL - 1)
        self.assertTrue(item.needsReorder())

        # На минимальном уровне
        item.updateItemQuantity(constants.MINIMUM_STOCK_LEVEL)
        self.assertFalse(item.needsReorder())

        # Выше минимального уровня
        item.updateItemQuantity(constants.MINIMUM_STOCK_LEVEL + 1)
        self.assertFalse(item.needsReorder())

        # Нулевое количество (ниже минимального)
        item.updateItemQuantity(0)
        self.assertTrue(item.needsReorder())

    def testGetItemInformation(self):
        """Тест получения информации об элементе"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)
        item.updateItemQuantity(150)

        info = item.getItemInformation()

        # Проверяем структуру информации
        self.assertEqual(info["itemIdentifier"], "ITEM001")
        self.assertEqual(info["itemName"], "Болт М10")
        self.assertEqual(info["currentQuantity"], 150)
        self.assertEqual(info["unitPrice"], 5.0)

        # Проверяем расчетную стоимость
        expected_value = 150 * 5.0
        self.assertEqual(info["totalValue"], expected_value)

    def testGetItemInformationEmpty(self):
        """Тест получения информации при нулевом количестве"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)
        # Количество остается 0 по умолчанию

        info = item.getItemInformation()

        self.assertEqual(info["itemIdentifier"], "ITEM001")
        self.assertEqual(info["currentQuantity"], 0)
        self.assertEqual(info["totalValue"], 0)

    def testInventoryItemProperties(self):
        """Тест свойств элемента инвентаря"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)

        # Проверяем начальные свойства
        self.assertEqual(item._itemIdentifier, "ITEM001")
        self.assertEqual(item._itemName, "Болт М10")
        self.assertEqual(item._unitPrice, 5.0)
        self.assertEqual(item._currentQuantity, 0)

        # Изменяем количество и проверяем
        item.updateItemQuantity(200)
        self.assertEqual(item._currentQuantity, 200)

        # Проверяем расчет стоимости
        value = item.calculateTotalValue()
        self.assertEqual(value, 1000.0)  # 200 * 5.0

    def testMultipleInventoryItems(self):
        """Тест работы с несколькими элементами инвентаря"""
        items = []

        for i in range(5):
            item = InventoryItem(
                f"ITEM{i + 1:03d}",
                f"Деталь {i + 1}",
                f"тип_{i + 1}",
                10.0 * (i + 1)
            )
            item.updateItemQuantity(50 * (i + 1))
            items.append(item)

        # Проверяем каждый элемент
        for i, item in enumerate(items):
            expected_price = 10.0 * (i + 1)
            expected_quantity = 50 * (i + 1)
            expected_value = expected_price * expected_quantity

            self.assertEqual(item._unitPrice, expected_price)
            self.assertEqual(item._currentQuantity, expected_quantity)

            value = item.calculateTotalValue()
            self.assertEqual(value, expected_value)

            info = item.getItemInformation()
            self.assertEqual(info["totalValue"], expected_value)

            # Проверяем необходимость заказа
            needs_reorder = item.needsReorder()
            if expected_quantity < constants.MINIMUM_STOCK_LEVEL:
                self.assertTrue(needs_reorder)
            else:
                self.assertFalse(needs_reorder)

    def testInventoryItemEdgeCases(self):
        """Тест крайних случаев"""
        # Очень высокая цена
        item = InventoryItem("EXPENSIVE", "Дорогая деталь", "люкс", 1000000.0)
        item.updateItemQuantity(2)
        value = item.calculateTotalValue()
        self.assertEqual(value, 2000000.0)

        # Очень маленькая цена
        item = InventoryItem("CHEAP", "Дешевая деталь", "эконом", 0.01)
        item.updateItemQuantity(10000)
        value = item.calculateTotalValue()
        self.assertEqual(value, 100.0)

        # Очень большое количество
        item = InventoryItem("BULK", "Массовая деталь", "серийная", 1.0)
        item.updateItemQuantity(1000000)
        value = item.calculateTotalValue()
        self.assertEqual(value, 1000000.0)

    def testInventoryItemMinimumStockLevel(self):
        """Тест минимального уровня запасов"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)

        # Проверяем разные уровни относительно минимального
        test_quantities = [
            (0, True),  # Ниже минимума
            (constants.MINIMUM_STOCK_LEVEL - 1, True),  # Ниже минимума
            (constants.MINIMUM_STOCK_LEVEL, False),  # На минимуме
            (constants.MINIMUM_STOCK_LEVEL + 1, False),  # Выше минимума
            (constants.MINIMUM_STOCK_LEVEL * 2, False),  # Значительно выше
        ]

        for quantity, should_reorder in test_quantities:
            item.updateItemQuantity(quantity)
            reorder_needed = item.needsReorder()
            self.assertEqual(reorder_needed, should_reorder,
                             f"При количестве {quantity} reorder должен быть {should_reorder}")

    def testInventoryItemInformationConsistency(self):
        """Тест консистентности информации"""
        item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)
        item.updateItemQuantity(200)

        # Получаем информацию несколькими способами
        info = item.getItemInformation()
        direct_value = item.calculateTotalValue()

        # Проверяем, что значения совпадают
        self.assertEqual(info["totalValue"], direct_value)
        self.assertEqual(info["currentQuantity"], item._currentQuantity)
        self.assertEqual(info["unitPrice"], item._unitPrice)


if __name__ == '__main__':
    unittest.main()
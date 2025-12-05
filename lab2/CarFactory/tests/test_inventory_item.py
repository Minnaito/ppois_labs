import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.inventory.InventoryItem import InventoryItem
from exceptions.InventoryExceptions.StockLevelCriticalError import StockLevelCriticalError


class TestInventoryItem(unittest.TestCase):
    """Тесты для элемента инвентаря"""

    def setUp(self):
        self.item = InventoryItem("ITEM001", "Стальной лист", "RAW_MATERIAL", 150.0)

    def testInventoryItemInitialization(self):
        self.assertEqual(self.item._itemIdentifier, "ITEM001")
        self.assertEqual(self.item.itemName, "Стальной лист")
        self.assertEqual(self.item._itemType, "RAW_MATERIAL")
        self.assertEqual(self.item._unitPrice, 150.0)
        self.assertEqual(self.item._currentQuantity, 0)

    def testUpdateItemQuantity(self):
        self.item.updateItemQuantity(25)
        self.assertEqual(self.item._currentQuantity, 25)

    def testUpdateItemQuantityNegative(self):
        """Тест обновления количества на отрицательное значение"""
        with self.assertRaises(StockLevelCriticalError):
            self.item.updateItemQuantity(-5)

    def testNeedsReorder(self):
        """Тест необходимости пополнения запасов"""
        self.item.updateItemQuantity(5)  # Ниже минимального уровня (10)
        self.assertTrue(self.item.needsReorder())

    def testDoesNotNeedReorder(self):
        """Тест когда пополнение не требуется"""
        self.item.updateItemQuantity(50)  # Выше минимального уровня
        self.assertFalse(self.item.needsReorder())

    def testCalculateTotalValue(self):
        """Тест расчета общей стоимости"""
        self.item.updateItemQuantity(10)
        total_value = self.item.calculateTotalValue()
        expected_value = 10 * 150.0
        self.assertEqual(total_value, expected_value)

    def testCalculateTotalValueZeroQuantity(self):
        """Тест расчета стоимости при нулевом количестве"""
        total_value = self.item.calculateTotalValue()
        self.assertEqual(total_value, 0.0)

    def testCheckStockLevelStatus(self):
        """Тест проверки уровня запасов"""
        # CRITICAL статус
        self.item.updateItemQuantity(1)  # 1/10 = 0.1 < 0.2
        self.assertEqual(self.item.checkStockLevelStatus(), "CRITICAL")

        # LOW статус
        self.item.updateItemQuantity(5)  # 5 < 10
        self.assertEqual(self.item.checkStockLevelStatus(), "LOW")

        # NORMAL статус
        self.item.updateItemQuantity(15)  # 15 между 10 и 800
        self.assertEqual(self.item.checkStockLevelStatus(), "NORMAL")

        # HIGH статус
        self.item.updateItemQuantity(900)  # 900 > 1000*0.8 = 800
        self.assertEqual(self.item.checkStockLevelStatus(), "HIGH")

    def testGetItemInformation(self):
        """Тест получения информации о товаре"""
        self.item.updateItemQuantity(20)
        info = self.item.getItemInformation()

        self.assertEqual(info["itemIdentifier"], "ITEM001")
        self.assertEqual(info["itemName"], "Стальной лист")
        self.assertEqual(info["currentQuantity"], 20)
        self.assertEqual(info["unitPrice"], 150.0)
        self.assertEqual(info["totalValue"], 3000.0)
        self.assertEqual(info["stockLevelStatus"], "NORMAL")

    def testSetStockLevelLimits(self):
        """Тест установки пределов уровня запасов"""
        self.item.setStockLevelLimits(5, 50)
        self.assertEqual(self.item._minimumStockLevel, 5)
        self.assertEqual(self.item._maximumStockLevel, 50)

    def testSetSupplierInformation(self):
        """Тест установки информации о поставщике"""
        self.item.setSupplierInformation("ООО 'МеталлПоставка'")
        self.assertEqual(self.item._supplierInformation, "ООО 'МеталлПоставка'")

    def testSetStorageRequirements(self):
        """Тест установки требований к хранению"""
        self.item.setStorageRequirements("Сухое помещение, температура +15...+25°C")
        self.assertEqual(self.item._storageRequirements, "Сухое помещение, температура +15...+25°C")

    def testDifferentItemTypes(self):
        """Тест элементов разных типов"""
        finished_good = InventoryItem("ITEM002", "Готовый продукт", "FINISHED_GOOD", 500.0)
        component = InventoryItem("ITEM003", "Компонент", "COMPONENT", 75.0)

        self.assertEqual(finished_good._itemType, "FINISHED_GOOD")
        self.assertEqual(component._itemType, "COMPONENT")

    def testZeroPriceItem(self):
        """Тест элемента с нулевой ценой"""
        free_item = InventoryItem("ITEM004", "Бесплатный образец", "SAMPLE", 0.0)
        free_item.updateItemQuantity(100)
        total_value = free_item.calculateTotalValue()
        self.assertEqual(total_value, 0.0)


if __name__ == '__main__':
    unittest.main()
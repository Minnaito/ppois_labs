import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.inventory.Warehouse import Warehouse
from exceptions.InventoryExceptions.WarehouseCapacityExceededError import WarehouseCapacityExceededError
from exceptions.InventoryExceptions.StockLevelCriticalError import StockLevelCriticalError


class TestWarehouse(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse("WH001", "Тестовый склад", 1000, "Корпус А")

    def test_initialization(self):
        """Тестирование инициализации склада"""
        self.assertEqual(self.warehouse._warehouseIdentifier, "WH001")
        self.assertEqual(self.warehouse._warehouseName, "Тестовый склад")
        self.assertEqual(self.warehouse._maximumCapacity, 1000)
        self.assertEqual(self.warehouse._location, "Корпус А")
        self.assertEqual(self.warehouse._currentStock, 0)
        self.assertEqual(len(self.warehouse._inventoryItems), 0)

    def test_add_inventory_item(self):
        """Тестирование добавления товара на склад"""
        # Добавляем товар
        result = self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)
        self.assertTrue(result)
        self.assertEqual(self.warehouse._currentStock, 100)
        self.assertEqual(len(self.warehouse._inventoryItems), 1)
        self.assertEqual(self.warehouse._inventoryItems["Двигатель V6"]["quantity"], 100)
        self.assertEqual(self.warehouse._inventoryItems["Двигатель V6"]["unitPrice"], 45000)

    def test_add_multiple_inventory_items(self):
        """Тестирование добавления нескольких товаров"""
        self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)
        self.warehouse.addInventoryItem("Коробка передач", 50, 28000)

        self.assertEqual(self.warehouse._currentStock, 150)
        self.assertEqual(len(self.warehouse._inventoryItems), 2)
        self.assertEqual(self.warehouse._inventoryItems["Двигатель V6"]["quantity"], 100)
        self.assertEqual(self.warehouse._inventoryItems["Коробка передач"]["quantity"], 50)

    def test_add_existing_inventory_item(self):
        """Тестирование добавления существующего товара"""
        self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)
        self.warehouse.addInventoryItem("Двигатель V6", 50, 45000)

        self.assertEqual(self.warehouse._currentStock, 150)
        self.assertEqual(self.warehouse._inventoryItems["Двигатель V6"]["quantity"], 150)

    def test_add_inventory_item_exceeds_capacity(self):
        """Тестирование добавления товара сверх емкости склада"""
        # Добавляем товар до предела
        self.warehouse.addInventoryItem("Двигатель V6", 900, 45000)

        # Пытаемся добавить еще, что должно вызвать исключение
        with self.assertRaises(WarehouseCapacityExceededError):
            self.warehouse.addInventoryItem("Коробка передач", 200, 28000)

    def test_remove_inventory_item(self):
        """Тестирование удаления товара со склада"""
        self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)

        result = self.warehouse.removeInventoryItem("Двигатель V6", 50)
        self.assertTrue(result)
        self.assertEqual(self.warehouse._currentStock, 50)
        self.assertEqual(self.warehouse._inventoryItems["Двигатель V6"]["quantity"], 50)

    def test_remove_inventory_item_completely(self):
        """Тестирование полного удаления товара"""
        self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)

        result = self.warehouse.removeInventoryItem("Двигатель V6", 100)
        self.assertTrue(result)
        self.assertEqual(self.warehouse._currentStock, 0)
        self.assertNotIn("Двигатель V6", self.warehouse._inventoryItems)

    def test_remove_nonexistent_inventory_item(self):
        """Тестирование удаления несуществующего товара"""
        with self.assertRaises(StockLevelCriticalError):
            self.warehouse.removeInventoryItem("Несуществующий товар", 50)

    def test_remove_more_than_available(self):
        """Тестирование удаления большего количества, чем есть на складе"""
        self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)

        with self.assertRaises(StockLevelCriticalError):
            self.warehouse.removeInventoryItem("Двигатель V6", 150)

    def test_get_item_quantity(self):
        """Тестирование получения количества товара"""
        self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)

        quantity = self.warehouse.getItemQuantity("Двигатель V6")
        self.assertEqual(quantity, 100)

        # Проверяем несуществующий товар
        quantity = self.warehouse.getItemQuantity("Несуществующий товар")
        self.assertEqual(quantity, 0)

    def test_calculate_utilization(self):
        """Тестирование расчета использования склада"""
        # Пустой склад
        utilization = self.warehouse.calculateUtilization()
        self.assertEqual(utilization, 0)

        # Частично заполненный склад
        self.warehouse.addInventoryItem("Двигатель V6", 500, 45000)
        utilization = self.warehouse.calculateUtilization()
        self.assertEqual(utilization, 50.0)

        # Полностью заполненный склад
        self.warehouse.addInventoryItem("Коробка передач", 500, 28000)
        utilization = self.warehouse.calculateUtilization()
        self.assertEqual(utilization, 100.0)

    def test_calculate_utilization_edge_cases(self):
        """Тестирование крайних случаев расчета использования"""
        # Склад с нулевой емкостью (если бы такое было возможно)
        warehouse = Warehouse("WH002", "Маленький склад", 0, "Корпус Б")
        utilization = warehouse.calculateUtilization()
        self.assertEqual(utilization, 0)

    def test_get_warehouse_status(self):
        """Тестирование получения статуса склада"""
        self.warehouse.addInventoryItem("Двигатель V6", 300, 45000)
        self.warehouse.addInventoryItem("Коробка передач", 200, 28000)

        status = self.warehouse.getWarehouseStatus()

        self.assertEqual(status["warehouseIdentifier"], "WH001")
        self.assertEqual(status["warehouseName"], "Тестовый склад")
        self.assertEqual(status["currentStock"], 500)
        self.assertEqual(status["maximumCapacity"], 1000)
        self.assertEqual(status["utilizationPercentage"], 50.0)
        self.assertEqual(status["location"], "Корпус А")
        self.assertEqual(status["itemTypesCount"], 2)

    def test_get_warehouse_status_empty(self):
        """Тестирование статуса пустого склада"""
        status = self.warehouse.getWarehouseStatus()

        self.assertEqual(status["currentStock"], 0)
        self.assertEqual(status["utilizationPercentage"], 0.0)
        self.assertEqual(status["itemTypesCount"], 0)

    def test_edge_case_maximum_capacity(self):
        """Тестирование крайнего случая с максимальной емкостью"""
        # Заполняем склад до предела
        result = self.warehouse.addInventoryItem("Товар", 1000, 1000)
        self.assertTrue(result)
        self.assertEqual(self.warehouse._currentStock, 1000)

        # Проверяем использование
        utilization = self.warehouse.calculateUtilization()
        self.assertEqual(utilization, 100.0)

    def test_edge_case_small_quantities(self):
        """Тестирование добавления маленьких количеств"""
        # Добавляем очень маленькое количество
        result = self.warehouse.addInventoryItem("Маленький товар", 1, 100)
        self.assertTrue(result)
        self.assertEqual(self.warehouse._currentStock, 1)

        # Удаляем очень маленькое количество
        result = self.warehouse.removeInventoryItem("Маленький товар", 1)
        self.assertTrue(result)
        self.assertEqual(self.warehouse._currentStock, 0)

    def test_inventory_item_persistence(self):
        """Тестирование сохранения данных товара"""
        self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)

        # Проверяем, что данные сохранились правильно
        item_data = self.warehouse._inventoryItems["Двигатель V6"]
        self.assertEqual(item_data["quantity"], 100)
        self.assertEqual(item_data["unitPrice"], 45000)

        # Добавляем еще
        self.warehouse.addInventoryItem("Двигатель V6", 50, 45000)
        item_data = self.warehouse._inventoryItems["Двигатель V6"]
        self.assertEqual(item_data["quantity"], 150)
        self.assertEqual(item_data["unitPrice"], 45000)  # Цена не должна меняться

    def test_remove_with_multiple_items(self):
        """Тестирование удаления при наличии нескольких типов товаров"""
        self.warehouse.addInventoryItem("Двигатель V6", 100, 45000)
        self.warehouse.addInventoryItem("Коробка передач", 200, 28000)

        # Удаляем часть одного товара
        self.warehouse.removeInventoryItem("Коробка передач", 50)

        self.assertEqual(self.warehouse._currentStock, 250)  # 100 + 150
        self.assertEqual(self.warehouse._inventoryItems["Коробка передач"]["quantity"], 150)
        self.assertEqual(self.warehouse._inventoryItems["Двигатель V6"]["quantity"], 100)

    def test_warehouse_with_different_prices(self):
        """Тестирование склада с товарами разных цен"""
        self.warehouse.addInventoryItem("Дешевый товар", 100, 1000)
        self.warehouse.addInventoryItem("Дорогой товар", 10, 100000)

        status = self.warehouse.getWarehouseStatus()
        self.assertEqual(status["currentStock"], 110)
        self.assertEqual(status["itemTypesCount"], 2)


class TestWarehouseIntegration(unittest.TestCase):
    """Интеграционные тесты для Warehouse"""

    def test_complete_warehouse_cycle(self):
        """Тестирование полного цикла работы склада"""
        warehouse = Warehouse("WH003", "Интеграционный склад", 500, "Корпус В")

        # 1. Добавляем товары
        warehouse.addInventoryItem("Товар А", 100, 10000)
        warehouse.addInventoryItem("Товар Б", 200, 20000)

        # Проверяем состояние
        self.assertEqual(warehouse._currentStock, 300)
        self.assertEqual(len(warehouse._inventoryItems), 2)

        # 2. Получаем статус
        status = warehouse.getWarehouseStatus()
        self.assertEqual(status["utilizationPercentage"], 60.0)

        # 3. Удаляем часть товаров
        warehouse.removeInventoryItem("Товар А", 50)
        warehouse.removeInventoryItem("Товар Б", 100)

        # 4. Проверяем конечное состояние
        self.assertEqual(warehouse._currentStock, 150)
        self.assertEqual(warehouse._inventoryItems["Товар А"]["quantity"], 50)
        self.assertEqual(warehouse._inventoryItems["Товар Б"]["quantity"], 100)

        # 5. Проверяем использование
        utilization = warehouse.calculateUtilization()
        self.assertEqual(utilization, 30.0)

    def test_warehouse_capacity_management(self):
        """Тестирование управления емкостью склада"""
        warehouse = Warehouse("WH004", "Склад с управлением", 100, "Корпус Г")

        # Заполняем почти полностью
        for i in range(10):
            warehouse.addInventoryItem(f"Товар_{i}", 9, 1000)  # 9 * 10 = 90 единиц

        # Проверяем, что можно добавить еще 10
        warehouse.addInventoryItem("Последний товар", 10, 1000)
        self.assertEqual(warehouse._currentStock, 100)

        # Проверяем, что нельзя добавить больше
        with self.assertRaises(WarehouseCapacityExceededError):
            warehouse.addInventoryItem("Лишний товар", 1, 1000)

    def test_warehouse_error_messages(self):
        """Тестирование сообщений об ошибках"""
        warehouse = Warehouse("WH005", "Тестовый склад", 100, "Локация")

        # Проверяем сообщение при превышении емкости
        try:
            warehouse.addInventoryItem("Большой товар", 150, 1000)
            self.fail("Должно было возникнуть исключение")
        except WarehouseCapacityExceededError as e:
            self.assertIn("WH005", str(e))
            self.assertIn("150", str(e))
            self.assertIn("100", str(e))

        # Проверяем сообщение при недостатке товара
        warehouse.addInventoryItem("Маленький товар", 50, 1000)
        try:
            warehouse.removeInventoryItem("Маленький товар", 100)
            self.fail("Должно было возникнуть исключение")
        except StockLevelCriticalError as e:
            self.assertIn("Маленький товар", str(e))
            self.assertIn("100", str(e))
            self.assertIn("50", str(e))


if __name__ == '__main__':
    # Запуск всех тестов
    unittest.main(verbosity=2)
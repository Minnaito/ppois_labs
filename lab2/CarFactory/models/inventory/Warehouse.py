from config import constants
from exceptions.InventoryExceptions.WarehouseCapacityExceededError import WarehouseCapacityExceededError
from exceptions.InventoryExceptions.StockLevelCriticalError import StockLevelCriticalError

class Warehouse:

    def __init__(self, warehouseIdentifier, warehouseName, maximumCapacity, location):
        self._warehouseIdentifier = warehouseIdentifier
        self._warehouseName = warehouseName
        self._maximumCapacity = maximumCapacity
        self._location = location
        self._currentStock = 0
        self._inventoryItems = {}

    def addInventoryItem(self, itemName, quantity, unitPrice):
        """Добавление товара на склад"""
        totalAfterAddition = self._currentStock + quantity
        if totalAfterAddition > self._maximumCapacity:
            raise WarehouseCapacityExceededError(
                self._warehouseIdentifier,
                totalAfterAddition,
                self._maximumCapacity
            )

        if itemName in self._inventoryItems:
            self._inventoryItems[itemName]["quantity"] += quantity
        else:
            self._inventoryItems[itemName] = {
                "quantity": quantity,
                "unitPrice": unitPrice
            }

        self._currentStock += quantity
        return True

    def removeInventoryItem(self, itemName, quantity):
        """Удаление товара со склада"""
        if itemName not in self._inventoryItems:
            raise StockLevelCriticalError(itemName, quantity, 0)

        availableQuantity = self._inventoryItems[itemName]["quantity"]
        if availableQuantity < quantity:
            raise StockLevelCriticalError(itemName, quantity, availableQuantity)

        self._inventoryItems[itemName]["quantity"] -= quantity
        self._currentStock -= quantity

        if self._inventoryItems[itemName]["quantity"] == 0:
            del self._inventoryItems[itemName]

        return True

    def getItemQuantity(self, itemName):
        """Получение количества товара"""
        return self._inventoryItems.get(itemName, {}).get("quantity", 0)

    def calculateUtilization(self):
        """Расчет использования склада"""
        if self._maximumCapacity > constants.ZERO_VALUE:
            utilization = (self._currentStock / self._maximumCapacity) * constants.PERCENTAGE_MULTIPLIER
            return utilization
        return constants.ZERO_VALUE

    def getWarehouseStatus(self):
        """Получение статуса склада"""
        return {
            "warehouseIdentifier": self._warehouseIdentifier,
            "warehouseName": self._warehouseName,
            "currentStock": self._currentStock,
            "maximumCapacity": self._maximumCapacity,
            "utilizationPercentage": self.calculateUtilization(),
            "location": self._location,
            "itemTypesCount": len(self._inventoryItems)
        }
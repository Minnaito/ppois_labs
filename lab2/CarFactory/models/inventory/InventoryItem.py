from config import constants
from exceptions.InventoryExceptions import StockLevelCriticalError


class InventoryItem:

    def __init__(self, itemIdentifier: str, itemName: str,
                 itemType: str, unitPrice: float):
        self._itemIdentifier = itemIdentifier
        self._itemName = itemName
        self._itemType = itemType
        self._unitPrice = unitPrice
        self._currentQuantity = 0
        self._minimumStockLevel = constants.MINIMUM_STOCK_LEVEL
        self._maximumStockLevel = constants.MAXIMUM_STOCK_LEVEL
        self._supplierInformation = ""
        self._storageRequirements = ""

    @property
    def itemName(self) -> str:
        """Название товара"""
        return self._itemName

    def updateItemQuantity(self, newQuantity: int) -> None:
        """Обновление количества товара"""
        if newQuantity < constants.ZERO_VALUE:
            raise StockLevelCriticalError(self._itemName, 0, self._currentQuantity)

        self._currentQuantity = newQuantity

    def checkStockLevelStatus(self) -> str:
        """Проверка уровня запасов"""
        stockRatio = self._currentQuantity / self._minimumStockLevel if self._minimumStockLevel > 0 else 0

        if stockRatio < constants.CRITICAL_STOCK_RATIO_THRESHOLD:
            return "CRITICAL"
        elif self._currentQuantity < self._minimumStockLevel:
            return "LOW"
        elif self._currentQuantity > self._maximumStockLevel * constants.HIGH_STOCK_RATIO_THRESHOLD:
            return "HIGH"
        else:
            return "NORMAL"

    def calculateTotalValue(self) -> float:
        """Расчет общей стоимости"""
        totalValue = self._currentQuantity * self._unitPrice
        return totalValue

    def setStockLevelLimits(self, newMinimumLevel: int,
                               newMaximumLevel: int) -> None:
        """Установка пределов уровня запасов"""
        self._minimumStockLevel = newMinimumLevel
        self._maximumStockLevel = newMaximumLevel

    def setSupplierInformation(self, supplierInfo: str) -> None:
        """Установка информации о поставщике"""
        self._supplierInformation = supplierInfo

    def setStorageRequirements(self, storageRequirements: str) -> None:
        """Установка требований к хранению"""
        self._storageRequirements = storageRequirements

    def getItemInformation(self) -> dict:
        """Получение информации о товаре"""
        itemInformation = {
            "itemIdentifier": self._itemIdentifier,
            "itemName": self._itemName,
            "itemType": self._itemType,
            "currentQuantity": self._currentQuantity,
            "unitPrice": self._unitPrice,
            "totalValue": self.calculateTotalValue(),
            "stockLevelStatus": self.checkStockLevelStatus(),
            "minimumStockLevel": self._minimumStockLevel,
            "maximumStockLevel": self._maximumStockLevel
        }
        return itemInformation

    def needsReorder(self) -> bool:
        """Проверка необходимости повторного заказа"""
        return self._currentQuantity < self._minimumStockLevel
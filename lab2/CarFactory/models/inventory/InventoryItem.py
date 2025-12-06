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

    def updateItemQuantity(self, newQuantity: int) -> None:
        if newQuantity < 0:
            raise StockLevelCriticalError(self._itemName, 0, self._currentQuantity)
        self._currentQuantity = newQuantity

    def calculateTotalValue(self) -> float:
        return self._currentQuantity * self._unitPrice

    def needsReorder(self) -> bool:
        return self._currentQuantity < self._minimumStockLevel

    def getItemInformation(self) -> dict:
        return {
            "itemIdentifier": self._itemIdentifier,
            "itemName": self._itemName,
            "currentQuantity": self._currentQuantity,
            "unitPrice": self._unitPrice,
            "totalValue": self.calculateTotalValue()
        }
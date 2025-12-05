from datetime import datetime
from models.inventory.InventoryItem import InventoryItem


class StockMovement:

    def __init__(self, movementId: str, item: InventoryItem, quantity: int,
                 movementType: str, fromLocation: str, toLocation: str):
        self._movementId = movementId
        self._item = item
        self._quantity = quantity
        self._movementType = movementType  # IN, OUT, TRANSFER
        self._fromLocation = fromLocation
        self._toLocation = toLocation
        self._movementDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._processedBy = ""
        self._reason = ""

    def getMovementDetails(self) -> dict:
        """Получение деталей движения"""
        return {
            "movementId": self._movementId,
            "itemName": self._item.itemName,
            "quantity": self._quantity,
            "movementType": self._movementType,
            "fromLocation": self._fromLocation,
            "toLocation": self._toLocation,
            "movementDate": self._movementDate,
            "processedBy": self._processedBy,
            "reason": self._reason
        }

    def setProcessor(self, employeeId: str) -> None:
        """Установка сотрудника, обработавшего движение"""
        self._processedBy = employeeId

    def setReason(self, reason: str) -> None:
        """Установка причины движения"""
        self._reason = reason
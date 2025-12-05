from models.inventory.InventoryItem import InventoryItem
from datetime import datetime


class ReorderAlert:

    def __init__(self, alertId: str, item: InventoryItem, currentQuantity: int,
                 minimumRequired: int):
        self._alertId = alertId
        self._item = item
        self._currentQuantity = currentQuantity
        self._minimumRequired = minimumRequired
        self._alertDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._priority = "MEDIUM"
        self._isResolved = False
        self._resolvedDate = None

    def calculateUrgencyLevel(self) -> str:
        """Расчет уровня срочности"""
        shortageRatio = (self._minimumRequired - self._currentQuantity) / self._minimumRequired

        if shortageRatio > 0.5:
            return "HIGH"
        elif shortageRatio > 0.2:
            return "MEDIUM"
        else:
            return "LOW"

    def markAsResolved(self) -> None:
        """Отметка как решенного"""
        self._isResolved = True
        self._resolvedDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def getAlertInfo(self) -> dict:
        """Получение информации об оповещении"""
        return {
            "alertId": self._alertId,
            "itemName": self._item.itemName,
            "currentQuantity": self._currentQuantity,
            "minimumRequired": self._minimumRequired,
            "shortageAmount": self._minimumRequired - self._currentQuantity,
            "alertDate": self._alertDate,
            "priority": self.calculateUrgencyLevel(),
            "isResolved": self._isResolved,
            "resolvedDate": self._resolvedDate
        }
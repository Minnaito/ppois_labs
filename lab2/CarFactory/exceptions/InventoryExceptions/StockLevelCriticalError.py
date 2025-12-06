from .InventoryException import InventoryException


class StockLevelCriticalError(InventoryException):
    """Исключение при критическом уровне запасов"""

    def __init__(self, item_name: str, current_stock: int, minimum_required: int):
        self.item_name = item_name
        self.current_stock = current_stock
        self.minimum_required = minimum_required
        message = f"Критический уровень запасов {item_name}: {current_stock} (минимум {minimum_required})"
        super().__init__(message)
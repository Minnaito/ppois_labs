from .InventoryException import InventoryException


class WarehouseCapacityExceededError(InventoryException):
    """Исключение при переполнении склада"""

    def __init__(self, warehouse_id: str, current_capacity: int, max_capacity: int):
        self.warehouse_id = warehouse_id
        self.current_capacity = current_capacity
        self.max_capacity = max_capacity
        message = f"Склад {warehouse_id} переполнен: {current_capacity}/{max_capacity}"
        super().__init__(message)
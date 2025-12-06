from config import constants

class Warehouse:
    def __init__(self, wh_id: str, capacity: int):
        self._wh_id = wh_id
        self._capacity = capacity
        self._stock = constants.ZERO_VALUE

    def add_item(self, quantity: int) -> bool:
        if self._stock + quantity <= self._capacity:
            self._stock += quantity
            return True
        return False

    def calculate_available_space(self) -> int:
        return self._capacity - self._stock

    def calculate_utilization(self) -> float:
        if self._capacity > constants.ZERO_VALUE:
            return (self._stock / self._capacity) * constants.PERCENTAGE_MULTIPLIER
        return constants.ZERO_VALUE

    def check_stock_level(self) -> str:
        if self._stock < constants.MINIMUM_STOCK_LEVEL:
            return "LOW"
        return "OK"
from config import constants

class StorageFacility:
    def __init__(self, facility_id: str, capacity: int):
        self._facility_id = facility_id
        self._capacity = capacity
        self._stock = constants.ZERO_VALUE

    def update_stock(self, quantity: int) -> bool:
        if constants.ZERO_VALUE <= quantity <= self._capacity:
            self._stock = quantity
            return True
        return False

    def get_available(self) -> int:
        return self._capacity - self._stock
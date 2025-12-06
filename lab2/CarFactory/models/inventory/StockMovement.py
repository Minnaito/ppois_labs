from config import constants

class StockMovement:
    def __init__(self, movement_id: str, item_name: str, quantity: int, movement_type: str):
        self._movement_id = movement_id
        self._item_name = item_name
        self._quantity = quantity
        self._movement_type = movement_type

    def validate_movement(self) -> bool:
        return self._quantity > constants.ZERO_VALUE and self._movement_type in ["IN", "OUT", "TRANSFER"]

    def get_details(self) -> dict:
        return {
            "movement_id": self._movement_id,
            "item": self._item_name,
            "quantity": self._quantity,
            "type": self._movement_type
        }
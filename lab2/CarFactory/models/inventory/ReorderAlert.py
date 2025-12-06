from config import constants

class ReorderAlert:
    def __init__(self, alert_id: str, item_name: str, current_qty: int, min_required: int):
        self._alert_id = alert_id
        self._item_name = item_name
        self._current_qty = current_qty
        self._min_required = min_required

    def calculate_urgency(self) -> str:
        shortage = self._min_required - self._current_qty
        if shortage > self._min_required * constants.MIN_QUALITY_STANDARD:
            return "HIGH"
        return "MEDIUM" if shortage > constants.ZERO_VALUE else "LOW"

    def get_alert_info(self) -> dict:
        return {
            "alert_id": self._alert_id,
            "item": self._item_name,
            "current": self._current_qty,
            "required": self._min_required,
            "urgency": self.calculate_urgency()
        }
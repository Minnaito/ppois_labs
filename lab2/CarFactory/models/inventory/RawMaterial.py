from models.inventory.InventoryItem import InventoryItem
from config import constants

class RawMaterial(InventoryItem):
    def __init__(self, item_id: str, name: str, quality: str):
        # InventoryItem ожидает: itemIdentifier, itemName, itemType, unitPrice
        item_type = "RAW_MATERIAL"
        unit_price = constants.MATERIAL_COST_MULTIPLIER * constants.DEMO_ENGINE_CYLINDERS
        super().__init__(item_id, name, item_type, unit_price)  # ← 4 параметра
        self._quality = quality

    def check_quality_compliance(self, required_quality: str) -> bool:
        quality_levels = ["LOW", "MEDIUM", "HIGH", "PREMIUM"]
        current_index = quality_levels.index(self._quality) if self._quality in quality_levels else constants.ZERO_VALUE
        required_index = quality_levels.index(required_quality) if required_quality in quality_levels else constants.ZERO_VALUE
        return current_index >= required_index

    def get_specs(self) -> dict:
        base = super().getItemInformation()
        base.update({"quality": self._quality})
        return base
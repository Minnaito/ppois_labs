from models.abstract.BasePart import BasePart
from config import constants

from models.abstract.BasePart import BasePart
from config import constants


class CarPart(BasePart):
    def __init__(self, part_id: str, name: str, material: str, weight: float):  # ← 4 параметра
        super().__init__(part_id, name, material, weight)

    def calculate_cost(self) -> float:
        return self._weight * constants.MATERIAL_COST_MULTIPLIER

    def check_quality(self) -> bool:
        return self._weight >= constants.MINIMUM_PART_WEIGHT

    def calculate_shipping_cost(self, distance: float) -> float:
        # SHIPPING_COST_PER_KG_PER_KM = 0.1
        return self._weight * distance * constants.SHIPPING_COST_PER_KG_PER_KM
from config import constants

class FactoryBuilding:
    def __init__(self, building_id: str, area: float):
        self._building_id = building_id
        self._area = area
        self._is_operational = True

    def calculate_age(self, current_year: int) -> int:
        return current_year - constants.ZERO_VALUE  # упрощенный расчет

    def get_info(self) -> dict:
        return {"id": self._building_id, "area": self._area, "operational": self._is_operational}
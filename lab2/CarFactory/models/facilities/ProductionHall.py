from config import constants

class ProductionHall:
    def __init__(self, hall_id: str, building_id: str, area: float):
        self._hall_id = hall_id
        self._building_id = building_id
        self._area = area

    def add_line(self) -> bool:
        return True

    def get_stats(self) -> dict:
        return {"hall_id": self._hall_id, "area": self._area}
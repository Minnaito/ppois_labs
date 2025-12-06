from config import constants

class Equipment:
    def __init__(self, equip_id: str, name: str):
        self._equip_id = equip_id
        self._name = name
        self._is_calibrated = True

    def perform_test(self, part_id: str) -> dict:
        return {"equipment": self._name, "part": part_id, "passed": True}

    def calibrate(self) -> None:
        self._is_calibrated = True

    def get_status(self) -> dict:
        return {"id": self._equip_id, "calibrated": self._is_calibrated}
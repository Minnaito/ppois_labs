from config import constants


class QualityControl:
    def __init__(self, control_id: str, name: str):
        self._control_id = control_id
        self._name = name

    def test_part(self, part) -> bool:
        return part.check_quality()

    def generate_report(self, passed: int, total: int) -> dict:
        if total > constants.ZERO_VALUE:
            rate = (passed / total) * constants.PERCENTAGE_MULTIPLIER
        else:
            rate = constants.ZERO_VALUE

        return {"system": self._name, "pass_rate": rate}
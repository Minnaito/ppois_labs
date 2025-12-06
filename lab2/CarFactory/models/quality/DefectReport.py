from config import constants

class DefectReport:
    def __init__(self, report_id: str, part_id: str, inspector_id: str):
        self._report_id = report_id
        self._part_id = part_id
        self._inspector_id = inspector_id
        self._defects = []

    def add_defect(self, defect: str) -> None:
        self._defects.append(defect)

    def calculate_repair_cost(self) -> float:
        base = constants.BASE_REPAIR_COST
        defect_cost = len(self._defects) * constants.MATERIAL_COST_MULTIPLIER
        return base + defect_cost

    def get_summary(self) -> dict:
        return {
            "report_id": self._report_id,
            "part_id": self._part_id,
            "defects_count": len(self._defects),
            "repair_cost": self.calculate_repair_cost()
        }
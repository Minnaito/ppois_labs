from datetime import datetime
from config import constants


class MaintenanceLog:
    def __init__(self, log_id: str):
        self._log_id = log_id
        self._entries = []
        self._total_hours = constants.ZERO_VALUE
        self._total_cost = constants.ZERO_VALUE

    def add_entry(self, machine_id: str, maint_type: str, hours: float, cost: float, tech_id: str):
        if hours <= constants.ZERO_VALUE or cost < constants.ZERO_VALUE:
            raise ValueError("Часы и стоимость должны быть положительными")

        entry = {
            "entry_id": f"ENT{len(self._entries) + 1:03d}",
            "machine_id": machine_id,
            "type": maint_type,
            "hours": hours,
            "cost": cost,
            "technician": tech_id,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        self._entries.append(entry)
        self._total_hours += hours
        self._total_cost += cost

        return entry

    def get_machine_history(self, machine_id: str) -> list:
        return [entry for entry in self._entries if entry["machine_id"] == machine_id]

    def calculate_efficiency(self) -> float:
        preventive_count = sum(1 for e in self._entries if e["type"] == "PREVENTIVE")
        total_count = len(self._entries)

        if total_count > constants.ZERO_VALUE:
            return (preventive_count / total_count) * constants.PERCENTAGE_MULTIPLIER
        return constants.ZERO_VALUE

    def get_cost_analysis(self) -> dict:
        preventive_cost = sum(e["cost"] for e in self._entries if e["type"] == "PREVENTIVE")
        corrective_cost = sum(e["cost"] for e in self._entries if e["type"] == "CORRECTIVE")

        return {
            "total_cost": self._total_cost,
            "preventive_cost": preventive_cost,
            "corrective_cost": corrective_cost,
            "preventive_percentage": (preventive_cost / self._total_cost * constants.PERCENTAGE_MULTIPLIER) if self._total_cost > constants.ZERO_VALUE else constants.ZERO_VALUE

        }

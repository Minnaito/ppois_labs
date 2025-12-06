from config import constants

class SafetySystem:
    def __init__(self, system_id: str):
        self._system_id = system_id
        self._is_active = True

    def report_incident(self, description: str) -> dict:
        return {"system": self._system_id, "incident": description}
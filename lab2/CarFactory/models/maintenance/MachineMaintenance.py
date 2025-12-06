from config import constants

class MachineMaintenance:
    def __init__(self, maint_id: str, machine_id: str):
        self._maint_id = maint_id
        self._machine_id = machine_id
        self._status = constants.PRODUCTION_ORDER_STATUSES[constants.ZERO_VALUE]  

    def start(self) -> None:
        self._status = constants.PRODUCTION_ORDER_STATUSES[constants.ZERO_VALUE + 1]  

    def complete(self) -> None:
        self._status = constants.PRODUCTION_ORDER_STATUSES[constants.ZERO_VALUE + 2]  

    def get_report(self) -> dict:

        return {"id": self._maint_id, "machine": self._machine_id, "status": self._status}

from config import constants

class RepairTicket:
    def __init__(self, ticket_id: str, machine_id: str, issue: str):
        self._ticket_id = ticket_id
        self._machine_id = machine_id
        self._issue = issue

    def update_status(self, new_status: str) -> None:
        if new_status in constants.TRANSACTION_STATUSES:
            pass  

    def get_details(self) -> dict:

        return {"ticket": self._ticket_id, "machine": self._machine_id, "issue": self._issue}

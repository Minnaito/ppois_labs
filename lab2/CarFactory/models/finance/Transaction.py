from config import constants

class Transaction:
    def __init__(self, trans_id: str, amount: float, trans_type: str):
        self._trans_id = trans_id
        self._amount = amount
        self._trans_type = trans_type

    def process(self, balance: float) -> float:
        if self._trans_type == "DEBIT":
            return balance - self._amount
        return balance + self._amount

    def calculate_fee(self) -> float:
        return self._amount * constants.STANDARD_TAX_RATE

    def validate(self) -> bool:
        return self._amount > constants.ZERO_VALUE
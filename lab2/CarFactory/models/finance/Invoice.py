from config import constants

class Invoice:
    def __init__(self, invoice_id: str, amount: float):
        self._invoice_id = invoice_id
        self._amount = amount
        self._status = constants.TRANSACTION_STATUSES[constants.ZERO_VALUE]  

    def process(self) -> dict:
        self._status = constants.TRANSACTION_STATUSES[constants.ZERO_VALUE + 1]  
        tax = self._amount * constants.STANDARD_TAX_RATE
        return {
            "invoice_id": self._invoice_id,
            "amount": self._amount,
            "tax": tax,
            "total": self._amount + tax,
            "status": self._status

        }

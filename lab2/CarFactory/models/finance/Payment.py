from config import constants


class Payment:
    def __init__(self, payment_id: str, amount: float, method: str):
        self._payment_id = payment_id
        self._amount = amount
        self._method = method

    def process(self) -> dict:
        if self._method == "BANK_TRANSFER":
            fee = constants.BANK_TRANSFER_FEE_AMOUNT
        elif self._method == "CREDIT_CARD":
            fee = self._amount * constants.STANDARD_TAX_RATE 
        else:
            fee = constants.ZERO_VALUE

        return {
            "payment_id": self._payment_id,
            "amount": self._amount,
            "method": self._method,
            "fee": fee,
            "total": self._amount + fee

        }

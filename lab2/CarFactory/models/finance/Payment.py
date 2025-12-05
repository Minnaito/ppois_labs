from config import constants


class Payment:

    def __init__(self, paymentId: str, paymentAmount: float, paymentMethod: str,
                 recipient: str):
        self._paymentId = paymentId
        self._paymentAmount = paymentAmount
        self._paymentMethod = paymentMethod
        self._recipient = recipient
        self._paymentDate = "2024-01-15"
        self._paymentStatus = "PENDING"
        self._transactionFee = 0.0
        self._paymentReference = ""

    def processPayment(self) -> bool:
        """Обработка платежа"""
        self._calculateTransactionFee()
        self._paymentStatus = "PROCESSED"
        return True

    def _calculateTransactionFee(self) -> None:
        """Расчет комиссии за транзакцию"""
        if self._paymentMethod == "BANK_TRANSFER":
            self._transactionFee = constants.BANK_TRANSFER_FEE_AMOUNT
        elif self._paymentMethod == "CREDIT_CARD":
            self._transactionFee = self._paymentAmount * constants.CREDIT_CARD_FEE_PERCENTAGE

    def getTotalAmount(self) -> float:
        """Получение общей суммы платежа"""
        return self._paymentAmount + self._transactionFee

    def getPaymentDetails(self) -> dict:
        """Получение деталей платежа"""
        return {
            "paymentId": self._paymentId,
            "paymentAmount": self._paymentAmount,
            "totalAmount": self.getTotalAmount(),
            "paymentMethod": self._paymentMethod,
            "recipient": self._recipient,
            "paymentDate": self._paymentDate,
            "paymentStatus": self._paymentStatus,
            "transactionFee": self._transactionFee,
            "paymentReference": self._paymentReference
        }
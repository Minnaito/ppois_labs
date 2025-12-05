from config import constants
from exceptions.FinanceExceptions.InsufficientFundsError import InsufficientFundsError

class Transaction:

    def __init__(self, transactionIdentifier, transactionAmount, transactionType, description):
        self._transactionIdentifier = transactionIdentifier
        self._transactionAmount = transactionAmount
        self._transactionType = transactionType  # "DEBIT" or "CREDIT"
        self._description = description
        self._transactionStatus = "PENDING"
        self._resultingBalance = 0.0

    def processTransaction(self, currentBalance):
        """Обработка транзакции"""
        if self._transactionType == "DEBIT" and self._transactionAmount > currentBalance:
            raise InsufficientFundsError(currentBalance, self._transactionAmount)

        if self._transactionType == "DEBIT":
            newBalance = currentBalance - self._transactionAmount
        else:  # CREDIT
            newBalance = currentBalance + self._transactionAmount

        self._transactionStatus = "COMPLETED"
        self._resultingBalance = newBalance
        return newBalance

    def getTransactionDetails(self):
        """Получение деталей транзакции"""
        return {
            "transactionIdentifier": self._transactionIdentifier,
            "transactionAmount": self._transactionAmount,
            "transactionType": self._transactionType,
            "description": self._description,
            "status": self._transactionStatus,
            "resultingBalance": self._resultingBalance
        }

    def calculateTax(self, taxRate=None):
        """Расчет налога"""
        if taxRate is None:
            taxRate = constants.STANDARD_TAX_RATE
        return self._transactionAmount * taxRate
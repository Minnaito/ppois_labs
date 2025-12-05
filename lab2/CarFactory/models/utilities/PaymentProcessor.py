import re
from config import constants
from exceptions.FinanceExceptions.InsufficientFundsError import InsufficientFundsError

class PaymentProcessor:

    def __init__(self, processorIdentifier):
        self._processorIdentifier = processorIdentifier
        self._processedTransactions = 0
        self._successfulTransactions = 0

    def transferFunds(self, fromAccountBalance, toAccountBalance, transferAmount):
        """Перевод средств между счетами"""
        if transferAmount > fromAccountBalance:
            raise InsufficientFundsError(fromAccountBalance, transferAmount)

        newFromBalance = fromAccountBalance - transferAmount
        newToBalance = toAccountBalance + transferAmount

        self._processedTransactions += 1
        self._successfulTransactions += 1

        return newFromBalance, newToBalance

    def validatePassword(self, password):
        """Проверка сложности пароля"""
        validationResult = {
            "isValid": False,
            "score": 0,
            "checks": {
                "length": len(password) >= 8,
                "uppercase": bool(re.search(r'[A-Z]', password)),
                "lowercase": bool(re.search(r'[a-z]', password)),
                "digits": bool(re.search(r'\d', password)),
                "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
            }
        }

        if validationResult["checks"]["length"]:
            validationResult["score"] += 25
        if validationResult["checks"]["uppercase"]:
            validationResult["score"] += 25
        if validationResult["checks"]["lowercase"]:
            validationResult["score"] += 25
        if validationResult["checks"]["digits"]:
            validationResult["score"] += 15
        if validationResult["checks"]["special"]:
            validationResult["score"] += 10

        validationResult["isValid"] = validationResult["score"] >= 70
        return validationResult

    def getProcessorStats(self):
        """Получение статистики процессора"""
        successRate = 0
        if self._processedTransactions > 0:
            successRate = (self._successfulTransactions / self._processedTransactions) * 100

        return {
            "processorId": self._processorIdentifier,
            "processedTransactions": self._processedTransactions,
            "successfulTransactions": self._successfulTransactions,
            "successRate": successRate
        }
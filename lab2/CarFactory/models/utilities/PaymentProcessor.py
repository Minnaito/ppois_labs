import re
from config import constants


class PaymentProcessor:
    def __init__(self, processorIdentifier):
        self._processorIdentifier = processorIdentifier
        self._processedTransactions = constants.ZERO_VALUE
        self._successfulTransactions = constants.ZERO_VALUE

    def transferBetweenCards(self, fromCardBalance: float, toCardBalance: float,
                             amount: float) -> tuple:
        """Перевод с одной карты на другую с фиксированной комиссией"""
        if amount > fromCardBalance:
            raise Exception(f"Недостаточно средств: {fromCardBalance}, требуется: {amount}")

        fee = constants.BANK_TRANSFER_FEE_AMOUNT
        totalDebit = amount + fee

        newFromBalance = fromCardBalance - totalDebit
        newToBalance = toCardBalance + amount

        self._processedTransactions += 1
        self._successfulTransactions += 1

        return newFromBalance, newToBalance, fee

    def validatePasswordStrength(self, password: str) -> dict:
        """Проверка надежности пароля с использованием констант"""
        checks = {
            "length": len(password) >= constants.PASSWORD_MIN_LENGTH,
            "uppercase": bool(re.search(r'[A-Z]', password)),
            "lowercase": bool(re.search(r'[a-z]', password)),
            "digits": bool(re.search(r'\d', password)),
            "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }

        # Рассчитываем баллы на основе процента
        checks_count = len(checks)
        points_per_check = constants.PERCENTAGE_MULTIPLIER / checks_count

        score = constants.ZERO_VALUE
        for check in checks.values():
            if check:
                score += points_per_check  # 20% за каждый критерий

        isStrong = score >= constants.PASSWORD_STRONG_SCORE

        return {
            "isStrong": isStrong,
            "score": score,
            "checks": checks
        }

    def validateCVV(self, cvv: str) -> bool:
        """Валидация CVV кода карты"""
        STANDARD_CVV_LENGTH = 3
        return len(cvv) == STANDARD_CVV_LENGTH and cvv.isdigit()

    def getProcessorStats(self):
        """Статистика процессора"""
        successRate = constants.ZERO_VALUE
        if self._processedTransactions > constants.ZERO_VALUE:
            successRate = (self._successfulTransactions / self._processedTransactions) * constants.PERCENTAGE_MULTIPLIER

        return {
            "processorId": self._processorIdentifier,
            "processedTransactions": self._processedTransactions,
            "successfulTransactions": self._successfulTransactions,
            "successRate": successRate
        }
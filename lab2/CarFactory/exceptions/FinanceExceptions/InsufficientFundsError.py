from .FinanceException import FinanceException


class InsufficientFundsError(FinanceException):
    """Исключение при недостатке средств"""

    def __init__(self, current_balance: float, required_amount: float):
        self.current_balance = current_balance
        self.required_amount = required_amount
        message = f"Недостаточно средств: баланс {current_balance}, требуется {required_amount}"
        super().__init__(message)
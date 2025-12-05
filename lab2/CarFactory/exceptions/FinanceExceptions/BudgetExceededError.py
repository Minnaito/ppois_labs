from .FinanceException import FinanceException


class BudgetExceededError(FinanceException):
    """Исключение при превышении бюджета"""

    def __init__(self, budget_category: str, allocated_amount: float, spent_amount: float):
        self.budget_category = budget_category
        self.allocated_amount = allocated_amount
        self.spent_amount = spent_amount
        message = f"Превышен бюджет {budget_category}: выделено {allocated_amount}, потрачено {spent_amount}"
        super().__init__(message)
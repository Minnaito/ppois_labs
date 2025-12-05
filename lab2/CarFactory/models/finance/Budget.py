from config import constants
from exceptions.FinanceExceptions.BudgetExceededError import BudgetExceededError


class Budget:

    def __init__(self, budgetId: str, budgetName: str, totalAmount: float,
                 budgetPeriod: str):
        self._budgetId = budgetId
        self._budgetName = budgetName
        self._totalAmount = totalAmount
        self._budgetPeriod = budgetPeriod
        self._allocatedAmount = 0.0
        self._spentAmount = 0.0
        self._remainingAmount = totalAmount
        self._budgetCategories = {}
        self._categorySpent = {}
        self._isActive = True

    def allocateFunds(self, category: str, amount: float) -> bool:
        """Выделение средств по категориям"""
        if amount <= self._remainingAmount:
            self._allocatedAmount += amount
            self._remainingAmount -= amount
            self._budgetCategories[category] = amount
            self._categorySpent[category] = 0.0
            return True
        return False

    def recordExpense(self, category: str, amount: float) -> None:
        """Запись расхода"""
        if category not in self._budgetCategories:
            raise ValueError(f"Категория '{category}' не найдена в бюджете")

        categoryBudget = self._budgetCategories[category]
        currentCategorySpent = self._categorySpent.get(category, 0)

        if currentCategorySpent + amount > categoryBudget:
            raise BudgetExceededError(category, categoryBudget, currentCategorySpent + amount)

        if self._spentAmount + amount > self._totalAmount:
            raise BudgetExceededError("Общий бюджет", self._totalAmount, self._spentAmount + amount)

        self._categorySpent[category] = currentCategorySpent + amount
        self._spentAmount += amount
        self._remainingAmount -= amount

    def calculateUtilizationPercentage(self) -> float:
        """Расчет процента использования бюджета"""
        if self._totalAmount > constants.ZERO_VALUE:
            utilization = (self._spentAmount / self._totalAmount)
            return utilization * constants.PERCENTAGE_MULTIPLIER
        return constants.ZERO_VALUE

    def getBudgetStatus(self) -> dict:
        """Получение статуса бюджета"""
        return {
            "budgetId": self._budgetId,
            "budgetName": self._budgetName,
            "totalAmount": self._totalAmount,
            "allocatedAmount": self._allocatedAmount,
            "spentAmount": self._spentAmount,
            "remainingAmount": self._remainingAmount,
            "utilizationPercentage": self.calculateUtilizationPercentage(),
            "categoriesCount": len(self._budgetCategories),
            "isActive": self._isActive
        }
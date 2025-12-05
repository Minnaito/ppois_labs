from datetime import datetime
from config import constants


class FinancialReport:

    def __init__(self, reportId: str, reportPeriod: str):
        self._reportId = reportId
        self._reportPeriod = reportPeriod
        self._revenue = 0.0
        self._expenses = 0.0
        self._profit = 0.0
        self._assets = 0.0
        self._liabilities = 0.0
        self._equity = 0.0
        self._reportDate = datetime.now().strftime("%Y-%m-%d")

    def addRevenue(self, amount: float) -> None:
        self._revenue += amount
        self._calculateProfit()

    def addExpense(self, amount: float) -> None:
        self._expenses += amount
        self._calculateProfit()

    def _calculateProfit(self) -> None:
        self._profit = self._revenue - self._expenses

    def calculateProfitMargin(self) -> float:
        if self._revenue > constants.ZERO_VALUE:
            margin = (self._profit / self._revenue) * constants.PERCENTAGE_MULTIPLIER
            return margin
        return constants.ZERO_VALUE

    def calculateDebtToEquityRatio(self) -> float:
        if self._equity > constants.ZERO_VALUE:
            return self._liabilities / self._equity
        return 0.0

    def generateReport(self) -> dict:
        return {
            "reportId": self._reportId,
            "reportPeriod": self._reportPeriod,
            "reportDate": self._reportDate,
            "revenue": self._revenue,
            "expenses": self._expenses,
            "profit": self._profit,
            "profitMarginPercentage": self.calculateProfitMargin(),
            "assets": self._assets,
            "liabilities": self._liabilities,
            "equity": self._equity,
            "debtToEquityRatio": self.calculateDebtToEquityRatio()
        }
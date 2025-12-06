from config import constants


class FinancialReport:
    def __init__(self, report_id: str, period: str):
        self._report_id = report_id
        self._period = period
        # revenue и expenses не храним как поля, считаем при вызове

    def generate(self, revenue: float, expenses: float) -> dict:
        profit = revenue - expenses
        margin = constants.ZERO_VALUE
        if revenue > constants.ZERO_VALUE:
            margin = (profit / revenue) * constants.PERCENTAGE_MULTIPLIER

        return {
            "report_id": self._report_id,
            "period": self._period,
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
            "margin": margin
        }
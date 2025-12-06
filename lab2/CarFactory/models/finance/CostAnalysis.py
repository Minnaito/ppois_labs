from config import constants

class CostAnalysis:
    def __init__(self, analysisId: str, analysisPeriod: str):
        self._analysisId = analysisId
        self._analysisPeriod = analysisPeriod
        self._totalCosts = 0.0
        self._costBreakdown = {}

    def addCostCategory(self, category: str, amount: float) -> None:
        self._costBreakdown[category] = amount
        self._totalCosts += amount

    def calculateCostDistribution(self) -> dict:
        if self._totalCosts > 0:
            distribution = {}
            for category, amount in self._costBreakdown.items():
                distribution[category] = (amount / self._totalCosts) * 100
            return distribution
        return {}

    def getAnalysisReport(self) -> dict:
        return {
            "analysisId": self._analysisId,
            "analysisPeriod": self._analysisPeriod,
            "totalCosts": self._totalCosts,
            "costDistribution": self.calculateCostDistribution()
        }
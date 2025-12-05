from config import constants


class CostAnalysis:

    def __init__(self, analysisId: str, analysisPeriod: str):
        self._analysisId = analysisId
        self._analysisPeriod = analysisPeriod
        self._materialCosts = 0.0
        self._laborCosts = 0.0
        self._overheadCosts = 0.0
        self._maintenanceCosts = 0.0
        self._totalCosts = 0.0
        self._costBreakdown = {}

    def addCostCategory(self, category: str, amount: float) -> None:
        self._costBreakdown[category] = amount
        self._totalCosts += amount

        category_lower = category.lower()

        if any(keyword in category_lower for keyword in ["material", "raw", "supply", "inventory"]):
            self._materialCosts += amount

        elif any(
                keyword in category_lower for keyword in ["labor", "wage", "salary", "employee", "personnel", "staff"]):
            self._laborCosts += amount

        elif any(keyword in category_lower for keyword in ["maintenance", "repair", "service", "equipment"]):
            self._maintenanceCosts += amount

        else:
            self._overheadCosts += amount

    def calculateCostDistribution(self) -> dict:
        if self._totalCosts > constants.ZERO_VALUE:
            return {
                "materialPercentage": (self._materialCosts / self._totalCosts) * 100,
                "laborPercentage": (self._laborCosts / self._totalCosts) * 100,
                "overheadPercentage": (self._overheadCosts / self._totalCosts) * 100,
                "maintenancePercentage": (self._maintenanceCosts / self._totalCosts) * 100
            }
        return {}

    def getAnalysisReport(self) -> dict:
        costDistribution = self.calculateCostDistribution()

        return {
            "analysisId": self._analysisId,
            "analysisPeriod": self._analysisPeriod,
            "totalCosts": self._totalCosts,
            "materialCosts": self._materialCosts,
            "laborCosts": self._laborCosts,
            "overheadCosts": self._overheadCosts,
            "maintenanceCosts": self._maintenanceCosts,
            "costDistribution": costDistribution,
            "categoriesCount": len(self._costBreakdown)
        }
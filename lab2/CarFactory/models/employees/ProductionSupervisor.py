from models.abstract.BaseEmployee import BaseEmployee
from config import constants
from exceptions.ProductionExceptions.ProductionCapacityExceededError import ProductionCapacityExceededError
from models.production.ProductionLine import ProductionLine
from models.employees.MachineOperator import MachineOperator


class ProductionSupervisor(BaseEmployee):

    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, supervisionArea: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._supervisionArea = supervisionArea
        self._managedProductionLines = []
        self._supervisedOperatorsList = []
        self._managedShiftsCount = 0
        self._productionTargetQuantity = 0
        self._safetyViolationsCount = 0
        self._efficiencyImprovements = []

    def performWorkDuties(self) -> str:
        """Выполнение рабочих обязанностей руководителя"""
        dutiesDescription = f"Надзор за производством в зоне {self._supervisionArea}"
        return dutiesDescription

    def assignProductionLine(self, productionLine: ProductionLine) -> None:
        """Назначение производственной линии"""
        self._managedProductionLines.append(productionLine)

    def superviseMachineOperator(self, machineOperator: MachineOperator) -> None:
        """Надзор за оператором станка"""
        self._supervisedOperatorsList.append(machineOperator)

    def monitorProductionPerformance(self) -> dict:
        """Мониторинг производственной производительности"""
        totalProductionOutput = 0
        totalEfficiencyScore = 0.0

        for productionLine in self._managedProductionLines:
            lineStatistics = productionLine.getProductionStatistics()
            totalProductionOutput += lineStatistics["currentProductionCount"]
            totalEfficiencyScore += lineStatistics["productionEfficiency"]

        lineCount = len(self._managedProductionLines)
        averageEfficiency = totalEfficiencyScore / lineCount if lineCount > 0 else 0

        performanceReport = {
            "supervisorIdentifier": self._employeeIdentifier,
            "totalProductionOutput": totalProductionOutput,
            "averageEfficiencyScore": averageEfficiency,
            "managedLinesCount": len(self._managedProductionLines),
            "supervisedOperatorsCount": len(self._supervisedOperatorsList)
        }
        return performanceReport

    def setProductionTarget(self, targetQuantity: int) -> None:
        """Установка производственного плана"""
        self._productionTargetQuantity = targetQuantity

    def calculateTargetAchievementPercentage(self) -> float:
        """Расчет процента выполнения плана"""
        totalProduction = sum(
            line._currentProductionCount
            for line in self._managedProductionLines
        )

        if self._productionTargetQuantity > constants.ZERO_VALUE:
            achievementPercentage = (totalProduction / self._productionTargetQuantity)
            achievementPercentage *= constants.PERCENTAGE_MULTIPLIER
            return achievementPercentage
        return constants.ZERO_VALUE

    def reportSafetyViolation(self) -> None:
        """Сообщение о нарушении безопасности"""
        self._safetyViolationsCount += 1

    def addEfficiencyImprovement(self, improvementDescription: str) -> None:
        """Добавление улучшения эффективности"""
        self._efficiencyImprovements.append(improvementDescription)

    def getSupervisorPerformanceReport(self) -> dict:
        """Получение отчета о производительности руководителя"""
        return {
            "employeeIdentifier": self._employeeIdentifier,
            "supervisionArea": self._supervisionArea,
            "managedProductionLinesCount": len(self._managedProductionLines),
            "supervisedOperatorsCount": len(self._supervisedOperatorsList),
            "productionTargetQuantity": self._productionTargetQuantity,
            "targetAchievementPercentage": self.calculateTargetAchievementPercentage(),
            "safetyViolationsCount": self._safetyViolationsCount,
            "efficiencyImprovementsCount": len(self._efficiencyImprovements)
        }
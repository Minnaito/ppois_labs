from config import constants


class CalculationUtils:
    """Утилиты для расчетов с использованием констант"""

    @staticmethod
    def calculatePercentage(part, whole):
        """Расчет процента"""
        if whole == constants.ZERO_VALUE:
            return constants.ZERO_VALUE
        return (part / whole) * constants.PERCENTAGE_MULTIPLIER

    @staticmethod
    def calculateTax(amount):
        """Расчет налога"""
        return amount * constants.STANDARD_TAX_RATE

    @staticmethod
    def calculateAverage(numbers):
        """Расчет среднего"""
        if not numbers:
            return constants.ZERO_VALUE
        return sum(numbers) / len(numbers)

    @staticmethod
    def calculateEfficiency(actual, target):
        """Расчет эффективности"""
        if target == constants.ZERO_VALUE:
            return constants.ZERO_VALUE
        efficiency = (actual / target) * constants.PERCENTAGE_MULTIPLIER
        return min(efficiency, constants.PERCENTAGE_MULTIPLIER)

    @staticmethod
    def calculateMaterialCost(quantity):
        """Расчет стоимости материала"""
        return quantity * constants.MATERIAL_COST_MULTIPLIER
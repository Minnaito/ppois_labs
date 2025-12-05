from config import constants


class CalculationUtils:

    @staticmethod
    def calculatePercentage(part, whole):
        """Расчет процента"""
        if whole == constants.ZERO_VALUE:
            return constants.ZERO_VALUE
        return (part / whole) * constants.PERCENTAGE_MULTIPLIER

    @staticmethod
    def calculateTax(amount, taxRate=None):
        """Расчет налога"""
        if taxRate is None:
            taxRate = constants.STANDARD_TAX_RATE
        return amount * taxRate

    @staticmethod
    def calculateEmployeeSalaryTax(salary):
        """Расчет налога на зарплату сотрудника"""
        return salary * constants.EMPLOYEE_SALARY_TAX_RATE

    @staticmethod
    def calculateDiscount(amount, discountRate=None):
        """Расчет скидки"""
        if discountRate is None:
            discountRate = constants.STANDARD_DISCOUNT_RATE
        return amount * discountRate

    @staticmethod
    def calculateShippingCost(weight_kg, distance_km):
        """Расчет стоимости доставки"""
        return weight_kg * distance_km * constants.SHIPPING_COST_PER_KG_PER_KM

    @staticmethod
    def calculateCreditCardFee(amount):
        """Расчет комиссии за кредитную карту"""
        return amount * constants.CREDIT_CARD_FEE_PERCENTAGE

    @staticmethod
    def calculateBankTransferTotal(amount):
        """Расчет итоговой суммы с комиссией банковского перевода"""
        return amount + constants.BANK_TRANSFER_FEE_AMOUNT

    @staticmethod
    def calculateAverage(numbers):
        """Расчет среднего значения"""
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
    def calculateRepairCost(baseRepairCost, complexityLevel, partWeight):
        """Расчет стоимости ремонта с учетом сложности и веса"""
        complexity_cost = baseRepairCost * complexityLevel * constants.COMPLEXITY_COST_MULTIPLIER
        weight_cost = partWeight * constants.WEIGHT_COST_MULTIPLIER
        return max(constants.BASE_REPAIR_COST, baseRepairCost + complexity_cost + weight_cost)

    @staticmethod
    def calculateMaterialCost(materialType, quantity):
        """Расчет стоимости материала"""
        if materialType not in constants.VALID_MATERIAL_TYPES:
            raise ValueError(f"Invalid material type. Must be one of: {constants.VALID_MATERIAL_TYPES}")
        return quantity * constants.MATERIAL_COST_MULTIPLIER

    @staticmethod
    def calculateProductionEfficiency(actualOutput, maxCapacity=None):
        """Расчет эффективности производства"""
        if maxCapacity is None:
            maxCapacity = constants.MAX_PRODUCTION_CAPACITY
        if maxCapacity == constants.ZERO_VALUE:
            return constants.ZERO_VALUE
        return (actualOutput / maxCapacity) * constants.PERCENTAGE_MULTIPLIER

    @staticmethod
    def calculateQualityScore(qualityValue):
        """Расчет показателя качества"""
        return max(constants.MIN_QUALITY_STANDARD, min(1.0, qualityValue))

    @staticmethod
    def calculateStockRatio(currentStock, minStock=None, maxStock=None):
        """Расчет коэффициента запасов"""
        if minStock is None:
            minStock = constants.MINIMUM_STOCK_LEVEL
        if maxStock is None:
            maxStock = constants.MAXIMUM_STOCK_LEVEL

        if maxStock == minStock:
            return constants.ZERO_VALUE

        return (currentStock - minStock) / (maxStock - minStock)

    @staticmethod
    def getStockStatus(currentStock, minStock=None, maxStock=None):
        """Определение статуса запасов на основе коэффициента"""
        ratio = CalculationUtils.calculateStockRatio(currentStock, minStock, maxStock)

        if ratio < constants.CRITICAL_STOCK_RATIO_THRESHOLD:
            return "CRITICAL"
        elif ratio < constants.LOW_STOCK_RATIO_THRESHOLD:
            return "LOW"
        elif ratio > constants.HIGH_STOCK_RATIO_THRESHOLD:
            return "HIGH"
        else:
            return "NORMAL"

    @staticmethod
    def calculateWarehouseUtilization(currentStock, capacity=None):
        """Расчет использования склада"""
        if capacity is None:
            capacity = constants.DEFAULT_WAREHOUSE_CAPACITY
        if capacity == constants.ZERO_VALUE:
            return constants.ZERO_VALUE
        return (currentStock / capacity) * constants.PERCENTAGE_MULTIPLIER

    @staticmethod
    def calculateOperatorBonus(baseSalary, hasCertification, skillLevel):
        """Расчет бонуса оператора"""
        bonus = constants.ZERO_VALUE

        if hasCertification:
            bonus += baseSalary * constants.CERTIFICATION_BONUS_RATE

        if skillLevel > 0:
            bonus += baseSalary * constants.OPERATOR_SKILL_BONUS * skillLevel

        return bonus

    @staticmethod
    def calculateEfficiencyWithLoad(baseEfficiency, loadPercentage):
        """Расчет эффективности с учетом загрузки"""
        if loadPercentage > constants.PERCENTAGE_MULTIPLIER:
            loadPercentage = constants.PERCENTAGE_MULTIPLIER

        efficiency_loss = (loadPercentage / constants.PERCENTAGE_MULTIPLIER) * constants.EFFICIENCY_LOSS_PER_LOAD
        return max(constants.BASE_EFFICIENCY - efficiency_loss, constants.ZERO_VALUE)

    @staticmethod
    def calculateWeeklyWorkingHours(dailyHours):
        """Расчет недельных рабочих часов"""
        return dailyHours * 5  # 5 рабочих дней в неделю

    @staticmethod
    def isWorkingHoursValid(dailyHours):
        """Проверка валидности рабочих часов"""
        return dailyHours <= constants.STANDARD_WORKING_HOURS_PER_DAY

    @staticmethod
    def isWeeklyHoursValid(weeklyHours):
        """Проверка валидности недельных рабочих часов"""
        return weeklyHours <= constants.MAX_WORKING_HOURS_PER_WEEK

    @staticmethod
    def calculateWarrantyEndDate(startDate, warrantyMonths=None):
        """Расчет даты окончания гарантии"""
        if warrantyMonths is None:
            warrantyMonths = constants.STANDARD_WARRANTY_MONTHS
        # Возвращаем количество месяцев для дальнейшей обработки
        return warrantyMonths

    @staticmethod
    def calculateProductionSuccessProbability(baseProbability=None, qualityScore=None):
        """Расчет вероятности успеха производства"""
        if baseProbability is None:
            baseProbability = constants.BASE_SUCCESS_PROBABILITY

        if qualityScore is None:
            qualityScore = constants.MIN_QUALITY_STANDARD

        return min(1.0, baseProbability * qualityScore)

    @staticmethod
    def validateEngineSpecs(horsepower, cylinders):
        """Валидация спецификаций двигателя"""
        if not (constants.MIN_ENGINE_HORSEPOWER <= horsepower <= constants.MAX_ENGINE_HORSEPOWER):
            raise ValueError(
                f"Horsepower must be between {constants.MIN_ENGINE_HORSEPOWER} and {constants.MAX_ENGINE_HORSEPOWER}")

        if cylinders not in constants.VALID_ENGINE_CYLINDERS:
            raise ValueError(f"Cylinders must be one of: {constants.VALID_ENGINE_CYLINDERS}")

        return True

    @staticmethod
    def validateName(name):
        """Валидация имени"""
        if not (constants.MINIMUM_NAME_LENGTH <= len(name) <= constants.MAXIMUM_NAME_LENGTH):
            raise ValueError(
                f"Name length must be between {constants.MINIMUM_NAME_LENGTH} and {constants.MAXIMUM_NAME_LENGTH}")
        return True
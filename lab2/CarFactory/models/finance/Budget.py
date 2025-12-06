from config import constants

class Budget:
    def __init__(self, budget_id: str, total: float):
        self._budget_id = budget_id
        self._total = total
        self._spent = constants.ZERO_VALUE

    def spend(self, amount: float) -> bool:
        if self._spent + amount <= self._total:
            self._spent += amount
            return True
        return False

    def calculate_remaining(self) -> float:
        return self._total - self._spent

    def calculate_utilization(self) -> float:
        if self._total > constants.ZERO_VALUE:
            return (self._spent / self._total) * constants.PERCENTAGE_MULTIPLIER
        return constants.ZERO_VALUE

    def allocate_to_department(self, department: str, amount: float) -> bool:
        """Выделить средства отделу"""
        if self._spent + amount <= self._total:
            self._spent += amount
            return True
        return False

    def calculate_savings(self, planned: float) -> float:
        """Рассчитать экономию"""
        return planned - self._spent

    def forecast_next_quarter(self, growth_rate: float) -> float:
        """Прогноз на следующий квартал"""
        return self._total * (1 + growth_rate)

    def compare_with_previous(self, previous_amount: float) -> dict:
        """Сравнение с предыдущим периодом"""
        change = self._total - previous_amount
        change_percent = (change / previous_amount * 100) if previous_amount > 0 else 0
        return {"change": change, "percent": change_percent}

    def generate_budget_report(self) -> dict:
        """Отчет по бюджету"""
        return {
            "budget_id": self._budget_id,
            "total": self._total,
            "spent": self._spent,
            "remaining": self.calculate_remaining(),
            "utilization_percent": self.calculate_utilization()
        }

    def calculate_tax_on_budget(self) -> float:
        """Рассчитать налог на бюджет с использованием STANDARD_TAX_RATE"""
        return self._total * constants.STANDARD_TAX_RATE

    def allocate_based_on_standard_rates(self) -> dict:
        """Распределить бюджет на основе стандартных ставок"""
        salary_allocation = self._total * constants.EMPLOYEE_SALARY_TAX_RATE
        tax_allocation = self._total * constants.STANDARD_TAX_RATE
        materials_allocation = self._total * constants.MATERIAL_COST_MULTIPLIER / 100  

        return {
            "salaries": salary_allocation,
            "taxes": tax_allocation,
            "materials": materials_allocation,
            "remaining": self._total - (salary_allocation + tax_allocation + materials_allocation)
        }

    def check_budget_health(self) -> str:
        """Проверить здоровье бюджета с использованием новых констант"""
        utilization = self.calculate_utilization()

        # Используем новые константы для пороговых значений
        if utilization >= constants.BUDGET_WARNING_LIMIT:
            return "CRITICAL"
        elif utilization >= constants.BUDGET_HEALTHY_LIMIT:
            return "WARNING"
        else:
            return "HEALTHY"



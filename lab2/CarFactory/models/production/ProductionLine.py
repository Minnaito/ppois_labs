from config import constants

class ProductionLine:
    def __init__(self, line_id: str, name: str, capacity: int):
        self._line_id = line_id
        self._name = name
        self._capacity = capacity
        self._produced = constants.ZERO_VALUE
        self._is_active = True

    def produce(self, quantity: int) -> bool:
        if not self._is_active:
            return False
        if self._produced + quantity <= self._capacity:
            self._produced += quantity
            return True
        return False

    def start_line(self):
        self._is_active = True
        return f"Линия {self._name} запущена"

    def stop_line(self):
        self._is_active = False
        return f"Линия {self._name} остановлена"

    def calculate_utilization(self) -> float:
        if self._capacity > constants.ZERO_VALUE:
            return (self._produced / self._capacity) * constants.PERCENTAGE_MULTIPLIER
        return constants.ZERO_VALUE

    def get_info(self) -> dict:
        return {
            "id": self._line_id,
            "name": self._name,
            "capacity": self._capacity,
            "produced": self._produced,
            "utilization": self.calculate_utilization(),
            "is_active": self._is_active
        }

    def calculate_efficiency(self, target: int) -> float:
        """Эффективность линии"""
        if target > constants.ZERO_VALUE:
            return min((self._produced / target) * constants.PERCENTAGE_MULTIPLIER, constants.PERCENTAGE_MULTIPLIER)
        return constants.ZERO_VALUE

    def predict_completion_date(self, daily_target: int) -> str:
        """Предсказать дату завершения"""
        remaining = self._capacity - self._produced
        days_needed = remaining / daily_target if daily_target > constants.ZERO_VALUE else constants.ZERO_VALUE
        from datetime import datetime, timedelta
        return (datetime.now() + timedelta(days=days_needed)).strftime("%Y-%m-%d")

    def calculate_downtime_cost(self, downtime_hours: float, cost_per_hour: float) -> float:
        """Стоимость простоя"""
        return downtime_hours * cost_per_hour

    def optimize_schedule(self, orders: list) -> dict:
        """Оптимизация расписания"""
        total_orders = sum(orders)
        days_needed = total_orders / self._capacity if self._capacity > 0 else 0
        return {"total_orders": total_orders, "estimated_days": days_needed}

    def generate_report(self) -> dict:
        """Генерация отчета"""
        return {
            "line_id": self._line_id,
            "name": self._name,
            "produced": self._produced,
            "capacity": self._capacity,
            "utilization": self.calculate_utilization(),
            "available": self._capacity - self._produced

        }

from .ProductionException import ProductionException


class ProductionCapacityExceededError(ProductionException):
    """Исключение при превышении производственной мощности"""

    def __init__(self, current_production: int, max_capacity: int):
        self.current_production = current_production
        self.max_capacity = max_capacity
        message = f"Превышена производственная мощность: {current_production}/{max_capacity}"
        super().__init__(message)
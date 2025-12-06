from .ProductionException import ProductionException


class InsufficientMaterialsError(ProductionException):
    """Исключение при недостатке материалов для производства"""

    def __init__(self, material_name: str, required_quantity: int, available_quantity: int):
        self.material_name = material_name
        self.required_quantity = required_quantity
        self.available_quantity = available_quantity
        message = f"Недостаточно материала {material_name}: требуется {required_quantity}, доступно {available_quantity}"
        super().__init__(message)
from .QualityException import QualityException


class QualityStandardViolationError(QualityException):
    """Исключение при нарушении стандартов качества"""

    def __init__(self, standard_name: str, actual_value: float, expected_range: str):
        self.standard_name = standard_name
        self.actual_value = actual_value
        self.expected_range = expected_range
        message = f"Нарушен стандарт {standard_name}: {actual_value} не входит в диапазон {expected_range}"
        super().__init__(message)
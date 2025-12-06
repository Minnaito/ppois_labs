from .EmployeeException import EmployeeException


class InvalidEmployeeDataError(EmployeeException):
    """Исключение при невалидных данных сотрудника"""

    def __init__(self, field_name: str, invalid_value: str):
        self.field_name = field_name
        self.invalid_value = invalid_value
        message = f"Невалидные данные сотрудника в поле {field_name}: {invalid_value}"
        super().__init__(message)
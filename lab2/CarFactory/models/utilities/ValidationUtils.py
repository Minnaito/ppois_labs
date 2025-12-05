import re
from config import constants


class ValidationUtils:
    """
    Утилиты для валидации данных
    """

    @staticmethod
    def validateEmail(email: str) -> bool:
        """Валидация email адреса"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validatePhone(phone: str) -> bool:
        """Валидация номера телефона"""
        pattern = r'^(\+7|8)\d{10}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def validateName(name: str) -> bool:
        """Валидация имени"""
        if not name:
            return False

        if len(name) < constants.MINIMUM_NAME_LENGTH:
            return False

        pattern = r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$'
        return bool(re.match(pattern, name))

    @staticmethod
    def validateSalary(salary: float) -> bool:
        """Валидация зарплаты"""
        return salary >= constants.MINIMUM_EMPLOYEE_SALARY

    @staticmethod
    def validateWeight(weight: float) -> bool:
        """Валидация веса"""
        return weight >= constants.MINIMUM_PART_WEIGHT
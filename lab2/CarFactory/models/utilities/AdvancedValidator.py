import re
from datetime import datetime
from typing import Union
from config import constants


class AdvancedValidator:

    @staticmethod
    def validateEmail(email: str) -> bool:
        """Валидация email адреса"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validatePhone(phone: str) -> bool:
        """Валидация номера телефона"""
        pattern = r'^\+?[1-9]\d{1,14}$'
        return bool(re.match(pattern, phone))

    @staticmethod
    def validateDateFormat(dateString: str, format: str = "%Y-%m-%d") -> bool:
        """Валидация формата даты"""
        try:
            datetime.strptime(dateString, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validateNumericRange(value: Union[int, float],
                             minVal: Union[int, float],
                             maxVal: Union[int, float]) -> bool:
        """Валидация числового диапазона"""
        return minVal <= value <= maxVal

    @staticmethod
    def validateMaterialType(material: str) -> bool:
        """Валидация типа материала"""
        return material in constants.VALID_MATERIAL_TYPES
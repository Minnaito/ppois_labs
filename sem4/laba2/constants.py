"""Constants used throughout the application."""

from enum import Enum


class ProductFields(Enum):
    """Product field names."""
    PRODUCT_NAME = "product_name"
    MANUFACTURER_NAME = "manufacturer_name"
    MANUFACTURER_UNP = "manufacturer_unp"
    STOCK_QUANTITY = "stock_quantity"
    WAREHOUSE_ADDRESS = "warehouse_address"


class Messages(Enum):
    """User messages."""
    ADD_SUCCESS = "Товар успешно добавлен!"
    ADD_ERROR = "Ошибка при добавлении товара: {}"
    DELETE_SUCCESS = "Удалено записей: {}"
    DELETE_NONE = "Записей для удаления не найдено"
    DELETE_ERROR = "Ошибка при удалении: {}"
    SEARCH_ERROR = "Ошибка при поиске: {}"
    SAVE_SUCCESS = "Файл успешно сохранен!"
    SAVE_ERROR = "Ошибка при сохранении файла: {}"
    LOAD_SUCCESS = "Файл успешно загружен! Загружено записей: {}"
    LOAD_ERROR = "Ошибка при загрузке файла: {}"
    INVALID_DATA = "Неверный формат данных в файле"
    CONFIRM_EXIT = "Вы уверены, что хотите выйти?"


class ValidationMessages(Enum):
    """Validation error messages."""
    PRODUCT_NAME_REQUIRED = "Название товара обязательно"
    MANUFACTURER_NAME_REQUIRED = "Название производителя обязательно"
    MANUFACTURER_UNP_REQUIRED = "УНП производителя обязателен"
    MANUFACTURER_UNP_INVALID = "УНП должен содержать 9 цифр"
    STOCK_QUANTITY_INVALID = "Количество должно быть неотрицательным числом"
    WAREHOUSE_ADDRESS_REQUIRED = "Адрес склада обязателен"

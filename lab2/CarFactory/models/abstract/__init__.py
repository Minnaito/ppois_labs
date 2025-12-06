from abc import ABC, abstractmethod

class IProducible(ABC):
    """Интерфейс для производимых объектов"""
    @abstractmethod
    def get_production_specs(self) -> dict:
        pass

class IQualityCheckable(ABC):
    """Интерфейс для объектов с проверкой качества"""
    @abstractmethod
    def perform_quality_check(self) -> bool:
        pass

class IFinancialEntity(ABC):
    """Интерфейс для финансовых сущностей"""
    @abstractmethod
    def get_financial_data(self) -> dict:
        pass

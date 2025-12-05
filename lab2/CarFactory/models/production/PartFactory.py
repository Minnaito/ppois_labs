from typing import Dict, Type
from models.abstract.BasePart import BasePart
from models.production.CarPart import CarPart
from models.production.Engine import Engine
from models.production.Transmission import Transmission
from models.production.BrakeSystem import BrakeSystem
from config import constants


class PartFactory:
    """Фабрика для создания автомобильных деталей"""

    _partRegistry: Dict[str, Type[BasePart]] = {
        "carPart": CarPart,
        "engine": Engine,
        "transmission": Transmission,
        "brakeSystem": BrakeSystem
    }

    @classmethod
    def createPart(cls, partType: str, **kwargs) -> BasePart:
        """Создание детали по типу"""
        if partType not in cls._partRegistry:
            raise ValueError(f"Неизвестный тип детали: {partType}")

        # Создаем деталь в зависимости от типа
        if partType == "carPart":
            return cls._createCarPart(**kwargs)
        elif partType == "engine":
            return cls._createEngine(**kwargs)
        elif partType == "transmission":
            return cls._createTransmission(**kwargs)
        elif partType == "brakeSystem":
            return cls._createBrakeSystem(**kwargs)
    @classmethod
    def _createCarPart(cls, **kwargs) -> CarPart:
        """Создание базовой детали"""
        return CarPart(
            partIdentifier=kwargs.get("partIdentifier"),
            partName=kwargs.get("partName"),
            materialType=kwargs.get("materialType"),
            partWeight=kwargs.get("partWeight"),
            partCategory=kwargs.get("partCategory", "Standard")
        )

    @classmethod
    def _createEngine(cls, **kwargs) -> Engine:
        """Создание двигателя"""
        return Engine(
            partIdentifier=kwargs.get("partIdentifier"),
            partName=kwargs.get("partName"),
            materialType=kwargs.get("materialType"),
            partWeight=kwargs.get("partWeight"),
            horsepower=kwargs.get("horsepower"),
            cylinderCount=kwargs.get("cylinderCount"),
            fuelType=kwargs.get("fuelType", "gasoline")
        )

    @classmethod
    def _createTransmission(cls, **kwargs) -> Transmission:
        """Создание трансмиссии"""
        return Transmission(
            partIdentifier=kwargs.get("partIdentifier"),
            partName=kwargs.get("partName"),
            materialType=kwargs.get("materialType"),
            partWeight=kwargs.get("partWeight"),
            transmissionType=kwargs.get("transmissionType", "manual"),
            gearCount=kwargs.get("gearCount", 6)
        )

    @classmethod
    def _createBrakeSystem(cls, **kwargs) -> BrakeSystem:
        """Создание тормозной системы"""
        return BrakeSystem(
            partIdentifier=kwargs.get("partIdentifier"),
            partName=kwargs.get("partName"),
            materialType=kwargs.get("materialType"),
            partWeight=kwargs.get("partWeight"),
            brakeType=kwargs.get("brakeType", "disc"),
            discDiameter=kwargs.get("discDiameter", 300.0)
        )

    @classmethod
    def createDemoEngine(cls) -> Engine:
        """Создание демо-двигателя"""
        return cls._createEngine(
            partIdentifier="DEMO_ENG_001",
            partName="Демонстрационный двигатель V6",
            materialType="aluminum",
            partWeight=constants.DEMO_ENGINE_WEIGHT,
            horsepower=constants.DEMO_ENGINE_HORSEPOWER,
            cylinderCount=constants.DEMO_ENGINE_CYLINDERS,
            fuelType="gasoline"
        )

    @classmethod
    def createDemoCarPart(cls) -> CarPart:
        """Создание демо-детали"""
        return cls._createCarPart(
            partIdentifier="DEMO_PART_001",
            partName="Демонстрационная деталь",
            materialType="steel",
            partWeight=10.5,
            partCategory="Standard"
        )
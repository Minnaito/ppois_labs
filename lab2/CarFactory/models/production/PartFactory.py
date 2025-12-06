from models.production.CarPart import CarPart
from models.production.Engine import Engine
from config import constants


class PartFactory:
    @staticmethod
    def createEngine(part_id: str, name: str) -> Engine:
        """Создать двигатель с демо-параметрами"""
        engine = Engine(part_id, constants.DEMO_ENGINE_HORSEPOWER)  
        engine._name = name  
        return engine

    @staticmethod
    def createCarPart(part_id: str, name: str) -> CarPart:
        """Создать деталь"""
        return CarPart(
            part_id=part_id,
            name=name,
            material="steel",
            weight=constants.DEMO_ENGINE_WEIGHT / 10
        )

    @staticmethod
    def createDemoEngine() -> Engine:
        """Создать демо-двигатель"""
        return PartFactory.createEngine("DEMO_ENG", "Демо двигатель")

    @staticmethod
    def createDemoCarPart() -> CarPart:
        """Создать демо-деталь"""

        return PartFactory.createCarPart("DEMO_PART", "Демо деталь")

from models.production.CarPart import CarPart
from config import constants

class Engine(CarPart):
    def __init__(self, part_id: str, horsepower: int):
        super().__init__(part_id, "Engine", "steel", constants.DEMO_ENGINE_WEIGHT)  
        self._horsepower = horsepower

    def calculate_cost(self) -> float:
        base = super().calculate_cost()
        hp_cost = self._horsepower * constants.MATERIAL_COST_MULTIPLIER
        cylinder_cost = constants.DEMO_ENGINE_CYLINDERS * constants.MATERIAL_COST_MULTIPLIER
        return base + hp_cost + cylinder_cost

    def check_quality(self) -> bool:
        min_ok = self._horsepower >= constants.MIN_ENGINE_HORSEPOWER
        max_ok = self._horsepower <= constants.MAX_ENGINE_HORSEPOWER
        demo_ok = self._horsepower >= constants.DEMO_ENGINE_HORSEPOWER * constants.MIN_QUALITY_STANDARD
        return min_ok and max_ok and demo_ok

    def calculate_power_to_weight(self) -> float:
        if self._weight > constants.ZERO_VALUE:
            return self._horsepower / self._weight
        return constants.ZERO_VALUE

    def calculate_fuel_consumption(self, distance: float) -> float:
        """Расход топлива с использованием константы DEMO_ENGINE_HORSEPOWER как базового значения"""
        base_consumption = constants.DEMO_ENGINE_HORSEPOWER * 0.01
        relative_power = self._horsepower / constants.DEMO_ENGINE_HORSEPOWER
        return (base_consumption * relative_power) * distance

    def calculate_emissions(self) -> float:
        """Выбросы CO2 с использованием констант"""
        # BASE_REPAIR_COST как базовая стоимость выбросов
        hp_emissions = self._horsepower * (constants.BASE_REPAIR_COST / 1000)
        cylinder_emissions = self._cylinders * (constants.MATERIAL_COST_MULTIPLIER / 2)
        return hp_emissions + cylinder_emissions

    def estimate_maintenance_cost(self, age_years: int) -> float:
        """Стоимость обслуживания с использованием констант"""
        base_cost = constants.BASE_REPAIR_COST
        hp_factor = self._horsepower / constants.DEMO_ENGINE_HORSEPOWER
        cylinder_factor = self._cylinders / constants.DEMO_ENGINE_CYLINDERS

        wear_rate = constants.STANDARD_TAX_RATE

        return base_cost * hp_factor * cylinder_factor * age_years * (1 + wear_rate)

    def get_technical_specs(self) -> dict:
        """Технические характеристики с использованием констант"""
        power_to_weight = self.calculate_power_to_weight()

        if self._horsepower >= constants.MAX_ENGINE_HORSEPOWER * constants.MIN_QUALITY_STANDARD:
            engine_class = "HIGH_PERFORMANCE"
        elif self._horsepower >= constants.DEMO_ENGINE_HORSEPOWER:
            engine_class = "STANDARD"
        else:
            engine_class = "ECONOMY"

        return {
            "horsepower": self._horsepower,
            "cylinders": self._cylinders,
            "valid_cylinders": self._cylinders in constants.VALID_ENGINE_CYLINDERS,
            "power_to_weight": power_to_weight,
            "engine_class": engine_class,
            "min_horsepower": constants.MIN_ENGINE_HORSEPOWER,
            "max_horsepower": constants.MAX_ENGINE_HORSEPOWER,
            "demo_horsepower": constants.DEMO_ENGINE_HORSEPOWER,
            "weight": self._weight,
            "demo_weight": constants.DEMO_ENGINE_WEIGHT
        }

    def calculate_annual_fuel_cost(self, annual_km: float, fuel_price: float) -> float:
        """Годовая стоимость топлива с использованием констант"""
        consumption = self.calculate_fuel_consumption(constants.PERCENTAGE_MULTIPLIER)  # на 100 км
        return (consumption * annual_km / constants.PERCENTAGE_MULTIPLIER) * fuel_price

    def validate_engine_configuration(self) -> dict:
        """Валидация конфигурации двигателя с использованием констант"""
        hp_valid = constants.MIN_ENGINE_HORSEPOWER <= self._horsepower <= constants.MAX_ENGINE_HORSEPOWER
        cylinders_valid = self._cylinders in constants.VALID_ENGINE_CYLINDERS
        weight_valid = self._weight >= constants.MINIMUM_PART_WEIGHT

        overall_valid = hp_valid and cylinders_valid and weight_valid

        return {
            "hp_valid": hp_valid,
            "cylinders_valid": cylinders_valid,
            "weight_valid": weight_valid,
            "overall_valid": overall_valid,
            "hp_range": f"{constants.MIN_ENGINE_HORSEPOWER}-{constants.MAX_ENGINE_HORSEPOWER}",
            "valid_cylinders": constants.VALID_ENGINE_CYLINDERS,
            "min_weight": constants.MINIMUM_PART_WEIGHT

        }


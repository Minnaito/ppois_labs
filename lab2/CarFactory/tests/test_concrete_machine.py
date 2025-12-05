from models.abstract.BaseMachine import BaseMachine


class ConcreteMachine(BaseMachine):
    """Конкретная реализация BaseMachine для тестирования"""

    def perform_operation(self) -> bool:
        return True

    def calculate_efficiency(self) -> float:
        return 0.85
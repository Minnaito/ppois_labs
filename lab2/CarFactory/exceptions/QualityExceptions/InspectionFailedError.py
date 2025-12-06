from .QualityException import QualityException


class InspectionFailedError(QualityException):
    """Исключение при проваленной инспекции качества"""

    def __init__(self, part_id: str, inspector_id: str):
        self.part_id = part_id
        self.inspector_id = inspector_id
        message = f"Инспекция детали {part_id} провалена инспектором {inspector_id}"
        super().__init__(message)
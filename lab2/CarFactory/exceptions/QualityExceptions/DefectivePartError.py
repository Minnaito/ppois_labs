from .QualityException import QualityException


class DefectivePartError(QualityException):
    """Исключение при обнаружении бракованной детали"""

    def __init__(self, part_id: str, defect_list: list):
        self.part_id = part_id
        self.defect_list = defect_list
        defects_string = ", ".join(defect_list)
        message = f"Деталь {part_id} имеет дефекты: {defects_string}"
        super().__init__(message)
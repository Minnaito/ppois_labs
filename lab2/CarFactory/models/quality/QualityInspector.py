from models.abstract.BaseEmployee import BaseEmployee
from config import constants
from exceptions.QualityExceptions.InspectionFailedError import InspectionFailedError
from exceptions.QualityExceptions.DefectivePartError import DefectivePartError
from models.production.CarPart import CarPart


class QualityInspector(BaseEmployee):

    def __init__(self, employee_identifier: str, full_name: str, job_position: str,
                 monthly_salary: float, department_name: str):
        super().__init__(employee_identifier, full_name, job_position, monthly_salary)
        self._department_name = department_name
        self._completed_inspections_count = 0
        self._certification_level = "BASIC"
        self._specialization_areas = []
        self._inspection_success_rate = 0.0
        self._tools_certified = []


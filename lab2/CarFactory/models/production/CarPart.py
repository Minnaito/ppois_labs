from models.abstract.BasePart import BasePart
from config import constants
from exceptions.QualityExceptions.DefectivePartError import DefectivePartError


class CarPart(BasePart):

    def __init__(self, partIdentifier: str, partName: str, materialType: str,
                 partWeight: float, partCategory: str):
        # Вызываем конструктор BasePart
        super().__init__(partIdentifier, partName, materialType, partWeight)
        self._partCategory = partCategory

    def calculateProductionCost(self) -> float:
        """Расчет стоимости производства детали"""
        materialCost = len(self._materialType) * constants.MATERIAL_COST_MULTIPLIER
        complexityCost = len(self._partCategory) * constants.COMPLEXITY_COST_MULTIPLIER
        weightCost = self._partWeight * constants.WEIGHT_COST_MULTIPLIER

        totalCost = materialCost + complexityCost + weightCost
        self._productionCost = totalCost
        return totalCost

    def performQualityCheck(self) -> bool:
        """Проверка качества детали"""
        if len(self._defectList) > constants.ZERO_VALUE:
            raise DefectivePartError(self._partIdentifier, self._defectList)

        weightCheck = self._partWeight >= constants.MINIMUM_PART_WEIGHT
        materialCheck = len(self._materialType) > constants.ZERO_VALUE
        nameCheck = len(self._partName) >= constants.MINIMUM_NAME_LENGTH

        return weightCheck and materialCheck and nameCheck

    def getPartSpecifications(self) -> dict:
        """Получить спецификации детали"""
        return {
            "partIdentifier": self._partIdentifier,
            "partName": self._partName,
            "materialType": self._materialType,
            "partWeight": self._partWeight,
            "partCategory": self._partCategory,
            "isQualityApproved": self._isQualityApproved,
            "defectCount": len(self._defectList)
        }

    @property
    def partCategory(self) -> str:
        """Категория детали"""
        return self._partCategory

    @partCategory.setter
    def partCategory(self, newCategory: str) -> None:
        """Установка новой категории детали"""
        self._partCategory = newCategory

    def __str__(self) -> str:
        return f"{self._partName} (ID: {self._partIdentifier}, Категория: {self._partCategory})"

    def __repr__(self) -> str:
        return f"CarPart(partIdentifier='{self._partIdentifier}', partName='{self._partName}', category='{self._partCategory}')"
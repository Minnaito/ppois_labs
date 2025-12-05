from models.inventory.InventoryItem import InventoryItem
from config import constants


class RawMaterial(InventoryItem):

    def __init__(self, itemIdentifier: str, itemName: str,
                 materialType: str, unitPrice: float, qualityGrade: str):
        super().__init__(itemIdentifier, itemName, "RAW_MATERIAL", unitPrice)
        self._materialType = materialType
        self._qualityGrade = qualityGrade
        self._expirationDate = None
        self._batchNumber = ""
        self._storageTemperature = ""
        self._materialSpecifications = {}

    def checkQualityCompliance(self, requiredQualityGrade: str) -> bool:
        """Проверка соответствия качества"""
        gradeHierarchy = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "PREMIUM": 4}
        currentGradeValue = gradeHierarchy.get(self._qualityGrade, 0)
        requiredGradeValue = gradeHierarchy.get(requiredQualityGrade, 0)

        return currentGradeValue >= requiredGradeValue

    def calculateMaterialYield(self, inputMaterialAmount: float,
                                 outputProductAmount: float) -> float:
        """Расчет выхода материала"""
        if inputMaterialAmount > constants.ZERO_VALUE:
            yieldPercentage = (outputProductAmount / inputMaterialAmount)
            yieldPercentage *= constants.PERCENTAGE_MULTIPLIER
            return yieldPercentage
        return constants.ZERO_VALUE

    def setStorageTemperature(self, temperatureRange: str) -> None:
        """Установка температуры хранения"""
        self._storageTemperature = temperatureRange

    def setBatchNumber(self, batchNumber: str) -> None:
        """Установка номера партии"""
        self._batchNumber = batchNumber

    def addMaterialSpecification(self, specificationName: str,
                                   specificationValue: str) -> None:
        """Добавление спецификации материала"""
        self._materialSpecifications[specificationName] = specificationValue

    def getMaterialSpecifications(self) -> dict:
        """Получение спецификаций материала"""
        baseInformation = self.getItemInformation()
        materialSpecificInfo = {
            "materialType": self._materialType,
            "qualityGrade": self._qualityGrade,
            "storageTemperature": self._storageTemperature,
            "batchNumber": self._batchNumber,
            "expirationDate": self._expirationDate,
            "specificationsCount": len(self._materialSpecifications)
        }

        completeSpecifications = {**baseInformation, **materialSpecificInfo}
        return completeSpecifications

    def isMaterialExpired(self, currentDate: str) -> bool:
        """Проверка истечения срока годности"""
        if not self._expirationDate:
            return False
        return currentDate > self._expirationDate
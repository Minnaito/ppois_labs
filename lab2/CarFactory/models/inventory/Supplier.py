from config import constants

class Supplier:

    def __init__(self, supplierIdentifier, supplierName, contactInfo, rating):
        self._supplierIdentifier = supplierIdentifier
        self._supplierName = supplierName
        self._contactInfo = contactInfo
        self._rating = rating
        self._suppliedMaterials = []

    def addMaterial(self, materialName):
        """Добавление материала в список поставляемых"""
        self._suppliedMaterials.append(materialName)

    def processOrder(self, materialName, quantity, unitPrice):
        """Обработка заказа"""
        if materialName not in self._suppliedMaterials:
            raise ValueError(f"Поставщик не поставляет материал: {materialName}")

        totalAmount = quantity * unitPrice
        return {
            "supplierId": self._supplierIdentifier,
            "materialName": materialName,
            "quantity": quantity,
            "unitPrice": unitPrice,
            "totalAmount": totalAmount,
            "orderStatus": "PROCESSED"
        }

    def getSupplierInfo(self):
        """Получение информации о поставщике"""
        return {
            "supplierIdentifier": self._supplierIdentifier,
            "supplierName": self._supplierName,
            "contactInfo": self._contactInfo,
            "rating": self._rating,
            "suppliedMaterialsCount": len(self._suppliedMaterials)
        }
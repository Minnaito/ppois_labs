from config import constants

class Supplier:
    def __init__(self, supplierIdentifier, supplierName, contactInfo, rating):
        self._supplierIdentifier = supplierIdentifier
        self._supplierName = supplierName
        self._contactInfo = contactInfo
        self._rating = rating

    def processOrder(self, materialName, quantity, unitPrice):
        totalAmount = quantity * unitPrice
        return {
            "supplierId": self._supplierIdentifier,
            "materialName": materialName,
            "quantity": quantity,
            "unitPrice": unitPrice,
            "totalAmount": totalAmount
        }

    def getSupplierInfo(self):
        return {
            "supplierIdentifier": self._supplierIdentifier,
            "supplierName": self._supplierName,
            "rating": self._rating
        }
from config import constants


class Invoice:

    def __init__(self, invoiceIdentifier, supplier, invoiceAmount, dueDate):
        self._invoiceIdentifier = invoiceIdentifier
        self._supplier = supplier
        self._invoiceAmount = invoiceAmount
        self._dueDate = dueDate
        self._invoiceStatus = "PENDING"
        self._taxAmount = 0.0

    @property
    def invoiceIdentifier(self):
        return self._invoiceIdentifier

    @property
    def invoiceAmount(self):
        return self._invoiceAmount

    def processInvoice(self):
        """Обработка счета"""
        self._taxAmount = self._invoiceAmount * constants.STANDARD_TAX_RATE
        self._invoiceStatus = "PROCESSED"

        return {
            "invoiceId": self._invoiceIdentifier,
            "amount": self._invoiceAmount,
            "taxAmount": self._taxAmount,
            "totalAmount": self._invoiceAmount + self._taxAmount,
            "status": self._invoiceStatus,
            "dueDate": self._dueDate
        }

    def getInvoiceDetails(self):
        """Получение деталей счета"""
        return {
            "invoiceIdentifier": self._invoiceIdentifier,
            "supplierName": self._supplier._supplierName,
            "invoiceAmount": self._invoiceAmount,
            "dueDate": self._dueDate,
            "status": self._invoiceStatus,
            "taxAmount": self._taxAmount
        }
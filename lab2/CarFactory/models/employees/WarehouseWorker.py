from models.abstract.BaseEmployee import BaseEmployee
from config import constants
from models.inventory.Warehouse import Warehouse
from models.inventory.InventoryItem import InventoryItem


class WarehouseWorker(BaseEmployee):

    def __init__(self, employeeIdentifier: str, fullName: str, jobPosition: str,
                 monthlySalary: float, assignedZone: str):
        super().__init__(employeeIdentifier, fullName, jobPosition, monthlySalary)
        self._assignedZone = assignedZone
        self._itemsProcessedCount = 0
        self._shippingOrdersProcessed = 0
        self._inventoryAccuracyPercentage = 0.0
        self._equipmentCertifications = []

    def performWorkDuties(self) -> str:
        """Выполнение рабочих обязанностей складского работника"""
        dutiesDescription = f"Управление складскими операциями в зоне {self._assignedZone}"
        return dutiesDescription

    def moveInventoryItem(self, warehouse: Warehouse, itemName: str,
                            fromLocation: str, toLocation: str, quantity: int) -> bool:
        """Перемещение товара на складе"""
        try:
            warehouse.removeInventoryItem(itemName, quantity)
            # Логика перемещения между зонами
            self._itemsProcessedCount += quantity
            return True
        except Exception:
            return False

    def prepareShipment(self, orderItems: dict) -> dict:
        """Подготовка отгрузки"""
        self._shippingOrdersProcessed += 1

        shipmentReport = {
            "workerId": self._employeeIdentifier,
            "orderItems": orderItems,
            "preparationTimeMinutes": 30,
            "itemsCount": sum(orderItems.values())
        }
        return shipmentReport

    def conductInventoryCount(self, expectedItems: dict, actualItems: dict) -> float:
        """Проведение инвентаризации"""
        correctCount = 0
        totalCount = len(expectedItems)

        for itemName, expectedQuantity in expectedItems.items():
            if actualItems.get(itemName) == expectedQuantity:
                correctCount += 1

        if totalCount > 0:
            accuracy = (correctCount / totalCount) * 100
            self._inventoryAccuracyPercentage = accuracy
            return accuracy
        return 0.0

    def addEquipmentCertification(self, equipmentType: str) -> None:
        """Добавление сертификации оборудования"""
        self._equipmentCertifications.append(equipmentType)

    def getWarehousePerformanceReport(self) -> dict:
        """Получение отчета о производительности"""
        performanceReport = {
            "employeeIdentifier": self._employeeIdentifier,
            "assignedZone": self._assignedZone,
            "itemsProcessedCount": self._itemsProcessedCount,
            "shippingOrdersProcessed": self._shippingOrdersProcessed,
            "inventoryAccuracyPercentage": self._inventoryAccuracyPercentage,
            "equipmentCertificationsCount": len(self._equipmentCertifications)
        }
        return performanceReport
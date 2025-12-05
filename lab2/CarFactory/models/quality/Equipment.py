from config import constants


class Equipment:

    def __init__(self, equipmentId: str, equipmentName: str, equipmentType: str):
        self._equipmentId = equipmentId
        self._equipmentName = equipmentName
        self._equipmentType = equipmentType
        self._isCalibrated = True
        self._lastCalibrationDate = "2024-01-01"
        self._accuracyPercentage = 99.5
        self._testsPerformed = 0
        self._maintenanceRequired = False

    def performTest(self, partIdentifier: str, testParameters: dict) -> dict:
        """Выполнение теста детали"""
        self._testsPerformed += 1

        # Симуляция процесса тестирования
        testResult = {
            "equipmentId": self._equipmentId,
            "partIdentifier": partIdentifier,
            "testPassed": True,
            "measurements": {"value": 10.5, "unit": "mm"},
            "testTimestamp": "2024-01-15 10:30:00"
        }

        return testResult

    def calibrateEquipment(self) -> None:
        """Калибровка оборудования"""
        self._isCalibrated = True
        self._lastCalibrationDate = "2024-01-15"
        self._accuracyPercentage = 99.8
        self._maintenanceRequired = False

    def scheduleMaintenance(self) -> None:
        """Планирование обслуживания"""
        self._maintenanceRequired = True

    def calculateUtilizationRate(self, totalAvailableTests: int) -> float:
        """Расчет коэффициента использования"""
        if totalAvailableTests > constants.ZERO_VALUE:
            utilizationRate = (self._testsPerformed / totalAvailableTests)
            utilizationRate *= constants.PERCENTAGE_MULTIPLIER
            return utilizationRate
        return constants.ZERO_VALUE

    def getEquipmentStatus(self) -> dict:
        """Получение статуса оборудования"""
        return {
            "equipmentId": self._equipmentId,
            "equipmentName": self._equipmentName,
            "equipmentType": self._equipmentType,
            "isCalibrated": self._isCalibrated,
            "lastCalibration": self._lastCalibrationDate,
            "accuracyPercentage": self._accuracyPercentage,
            "testsPerformed": self._testsPerformed,
            "maintenanceRequired": self._maintenanceRequired
        }
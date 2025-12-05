from config import constants
from exceptions.ProductionExceptions.InsufficientMaterialsError import InsufficientMaterialsError
from models.employees.MachineOperator import MachineOperator
from models.production.CarPart import CarPart


class AssemblyStation:

    def __init__(self, stationIdentifier: str, stationType: str, stationCapacity: int):
        self._stationIdentifier = stationIdentifier
        self._stationType = stationType
        self._stationCapacity = stationCapacity
        self._currentPartsInventory = []
        self._assignedOperator = None
        self._averageAssemblyTimeMinutes = 0.0
        self._qualitySuccessRate = 0.95
        self._isStationOperational = True
        self._toolsAvailable = []

    def assignOperatorToStation(self, machineOperator: MachineOperator) -> None:
        """Назначение оператора на станцию"""
        self._assignedOperator = machineOperator

    def addPartToStation(self, carPart: CarPart) -> None:
        """Добавление детали на станцию"""
        if len(self._currentPartsInventory) >= self._stationCapacity:
            raise InsufficientMaterialsError("Место на станции", 1, 0)
        self._currentPartsInventory.append(carPart)

    def removePartFromStation(self, partIdentifier: str) -> bool:
        """Удаление детали со станции"""
        for part in self._currentPartsInventory:
            if part.partIdentifier == partIdentifier:
                self._currentPartsInventory.remove(part)
                return True
        return False

    def assemblePartsIntoComponent(self, targetComponentName: str) -> bool:
        """Сборка деталей в компонент"""
        minimumPartsForAssembly = 2
        if len(self._currentPartsInventory) < minimumPartsForAssembly:
            requiredParts = minimumPartsForAssembly
            availableParts = len(self._currentPartsInventory)
            raise InsufficientMaterialsError("Детали для сборки", requiredParts, availableParts)

        assemblySuccess = self._simulateAssemblyProcess()
        if assemblySuccess:
            self._currentPartsInventory.clear()

        return assemblySuccess

    def _simulateAssemblyProcess(self) -> bool:
        """Симуляция процесса сборки"""
        baseSuccessProbability = 0.95
        operatorSkillBonus = 0.0

        if self._assignedOperator:
            operatorSkillBonus = 0.03

        totalSuccessProbability = baseSuccessProbability + operatorSkillBonus
        return totalSuccessProbability > 0.5

    def calculateAssemblyTime(self, complexityLevel: int) -> float:
        """Расчет времени сборки"""
        baseAssemblyTimeMinutes = 2.5
        assemblyTime = baseAssemblyTimeMinutes * complexityLevel
        self._averageAssemblyTimeMinutes = assemblyTime
        return assemblyTime

    def addToolToStation(self, toolName: str) -> None:
        """Добавление инструмента на станцию"""
        self._toolsAvailable.append(toolName)

    def getStationStatusReport(self) -> dict:
        """Получение отчета о статусе станции"""
        stationStatus = {
            "stationIdentifier": self._stationIdentifier,
            "stationType": self._stationType,
            "currentPartsCount": len(self._currentPartsInventory),
            "stationCapacity": self._stationCapacity,
            "assignedOperator": self._assignedOperator.employeeIdentifier if self._assignedOperator else None,
            "isOperational": self._isStationOperational,
            "toolsCount": len(self._toolsAvailable),
            "assemblyTimeMinutes": self._averageAssemblyTimeMinutes
        }
        return stationStatus
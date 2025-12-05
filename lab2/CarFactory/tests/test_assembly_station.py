import unittest
import sys
import os
from unittest.mock import Mock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.production.AssemblyStation import AssemblyStation
from models.employees.MachineOperator import MachineOperator
from models.production.CarPart import CarPart
from exceptions.ProductionExceptions.InsufficientMaterialsError import InsufficientMaterialsError


class TestAssemblyStation(unittest.TestCase):
    """Тесты для класса AssemblyStation"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.assembly_station = AssemblyStation("ST001", "Engine Assembly", 10)
        self.machine_operator = self._create_mock_operator()
        self.car_part = self._create_mock_car_part()

    def _create_mock_operator(self):
        """Создание тестового оператора"""
        operator = Mock(spec=MachineOperator)
        operator.employeeIdentifier = "OP001"
        return operator

    def _create_mock_car_part(self):
        """Создание тестовой детали"""
        part = Mock(spec=CarPart)
        part.partIdentifier = "PART001"
        return part

    def test_initialization(self):
        """Тест инициализации станции"""
        self.assertEqual(self.assembly_station._stationIdentifier, "ST001")
        self.assertEqual(self.assembly_station._stationType, "Engine Assembly")
        self.assertEqual(self.assembly_station._stationCapacity, 10)
        self.assertEqual(self.assembly_station._currentPartsInventory, [])
        self.assertIsNone(self.assembly_station._assignedOperator)
        self.assertTrue(self.assembly_station._isStationOperational)
        self.assertEqual(self.assembly_station._toolsAvailable, [])
        self.assertEqual(self.assembly_station._qualitySuccessRate, 0.95)

    def test_assign_operator_to_station(self):
        """Тест назначения оператора на станцию"""
        self.assembly_station.assignOperatorToStation(self.machine_operator)
        self.assertEqual(self.assembly_station._assignedOperator, self.machine_operator)

    def test_add_part_to_station_success(self):
        """Тест успешного добавления детали на станцию"""
        self.assembly_station.addPartToStation(self.car_part)
        self.assertEqual(len(self.assembly_station._currentPartsInventory), 1)
        self.assertEqual(self.assembly_station._currentPartsInventory[0], self.car_part)

    def test_add_part_to_station_overflow(self):
        """Тест добавления детали при переполнении станции"""
        # Заполняем станцию до предела
        for i in range(self.assembly_station._stationCapacity):
            part = Mock(spec=CarPart)
            part.partIdentifier = f"PART{i}"
            self.assembly_station.addPartToStation(part)

        # Попытка добавить еще одну деталь должна вызвать исключение
        with self.assertRaises(InsufficientMaterialsError) as context:
            self.assembly_station.addPartToStation(self.car_part)

        self.assertIn("Место на станции", str(context.exception))

    def test_remove_part_from_station_success(self):
        """Тест успешного удаления детали со станции"""
        self.assembly_station.addPartToStation(self.car_part)
        result = self.assembly_station.removePartFromStation("PART001")

        self.assertTrue(result)
        self.assertEqual(len(self.assembly_station._currentPartsInventory), 0)

    def test_remove_part_from_station_not_found(self):
        """Тест удаления несуществующей детали"""
        result = self.assembly_station.removePartFromStation("NON_EXISTENT")
        self.assertFalse(result)

    def test_assemble_parts_into_component_success(self):
        """Тест успешной сборки компонента"""
        # Добавляем достаточно деталей для сборки
        for i in range(2):
            part = Mock(spec=CarPart)
            part.partIdentifier = f"PART{i}"
            self.assembly_station.addPartToStation(part)

        result = self.assembly_station.assemblePartsIntoComponent("TestComponent")

        # Результат может быть True или False в зависимости от вероятности успеха
        self.assertIsInstance(result, bool)
        # Инвентарь должен быть очищен после успешной сборки
        if result:
            self.assertEqual(len(self.assembly_station._currentPartsInventory), 0)

    def test_assemble_parts_into_component_insufficient_materials(self):
        """Тест сборки при недостаточном количестве деталей"""
        # Добавляем только одну деталь (недостаточно для сборки)
        part = Mock(spec=CarPart)
        part.partIdentifier = "PART001"
        self.assembly_station.addPartToStation(part)

        with self.assertRaises(InsufficientMaterialsError) as context:
            self.assembly_station.assemblePartsIntoComponent("TestComponent")

        self.assertIn("Детали для сборки", str(context.exception))

    def test_simulate_assembly_process_with_operator(self):
        """Тест симуляции сборки с оператором"""
        self.assembly_station.assignOperatorToStation(self.machine_operator)
        result = self.assembly_station._simulateAssemblyProcess()
        self.assertIsInstance(result, bool)

    def test_simulate_assembly_process_without_operator(self):
        """Тест симуляции сборки без оператора"""
        result = self.assembly_station._simulateAssemblyProcess()
        self.assertIsInstance(result, bool)

    def test_calculate_assembly_time(self):
        """Тест расчета времени сборки"""
        complexity_level = 3
        expected_time = 2.5 * complexity_level

        result = self.assembly_station.calculateAssemblyTime(complexity_level)

        self.assertEqual(result, expected_time)
        self.assertEqual(self.assembly_station._averageAssemblyTimeMinutes, expected_time)

    def test_add_tool_to_station(self):
        """Тест добавления инструмента на станцию"""
        tool_name = "Wrench"
        self.assembly_station.addToolToStation(tool_name)

        self.assertIn(tool_name, self.assembly_station._toolsAvailable)
        self.assertEqual(len(self.assembly_station._toolsAvailable), 1)

    def test_get_station_status_report_with_operator(self):
        """Тест получения отчета о статусе станции с оператором"""
        self.assembly_station.assignOperatorToStation(self.machine_operator)
        self.assembly_station.addPartToStation(self.car_part)
        self.assembly_station.addToolToStation("Wrench")
        self.assembly_station.calculateAssemblyTime(2)

        report = self.assembly_station.getStationStatusReport()

        expected_report = {
            "stationIdentifier": "ST001",
            "stationType": "Engine Assembly",
            "currentPartsCount": 1,
            "stationCapacity": 10,
            "assignedOperator": "OP001",
            "isOperational": True,
            "toolsCount": 1,
            "assemblyTimeMinutes": 5.0
        }
        self.assertEqual(report, expected_report)

    def test_get_station_status_report_without_operator(self):
        """Тест получения отчета о статусе станции без оператора"""
        report = self.assembly_station.getStationStatusReport()

        expected_report = {
            "stationIdentifier": "ST001",
            "stationType": "Engine Assembly",
            "currentPartsCount": 0,
            "stationCapacity": 10,
            "assignedOperator": None,
            "isOperational": True,
            "toolsCount": 0,
            "assemblyTimeMinutes": 0.0
        }
        self.assertEqual(report, expected_report)

    def test_multiple_tools_addition(self):
        """Тест добавления нескольких инструментов"""
        tools = ["Wrench", "Screwdriver", "Pliers"]

        for tool in tools:
            self.assembly_station.addToolToStation(tool)

        self.assertEqual(len(self.assembly_station._toolsAvailable), 3)
        for tool in tools:
            self.assertIn(tool, self.assembly_station._toolsAvailable)

    def test_station_operational_status(self):
        """Тест проверки операционного статуса станции"""
        self.assertTrue(self.assembly_station._isStationOperational)

    def test_calculate_assembly_time_parameterized(self):
        """Параметризованный тест расчета времени сборки"""
        test_cases = [
            (1, 2.5),
            (2, 5.0),
            (5, 12.5),
            (0, 0.0),
        ]

        for complexity, expected_time in test_cases:
            with self.subTest(complexity=complexity):
                result = self.assembly_station.calculateAssemblyTime(complexity)
                self.assertEqual(result, expected_time)


if __name__ == '__main__':
    unittest.main()
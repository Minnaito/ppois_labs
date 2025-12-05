import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.abstract.BaseMachine import BaseMachine
from exceptions.ProductionExceptions import MachineMaintenanceRequiredError


class TestBaseMachine(unittest.TestCase):
    """Тесты для базового класса станка"""

    def setUp(self):
        # Создаем конкретную реализацию для тестирования
        class ConcreteMachine(BaseMachine):
            def __init__(self, machineIdentifier: str, machineName: str, machineType: str):
                super().__init__(machineIdentifier, machineName, machineType)
                self.test_operations = 0

            def performOperation(self) -> bool:
                """Реализация абстрактного метода"""
                self.test_operations += 1
                return True

            def calculateEfficiency(self) -> float:
                """Реализация абстрактного метода"""
                return 0.85

        self.machine_class = ConcreteMachine
        self.machine = ConcreteMachine("MACH001", "Токарный станок", "Токарный")

    def test_machine_initialization(self):
        """Тест инициализации станка"""
        self.assertEqual(self.machine._machineIdentifier, "MACH001")
        self.assertEqual(self.machine._machineName, "Токарный станок")
        self.assertEqual(self.machine._machineType, "Токарный")
        self.assertTrue(self.machine._isOperational)
        self.assertEqual(self.machine._operationalHours, 0)
        self.assertFalse(self.machine._maintenanceRequired)
        self.assertEqual(self.machine._energyConsumptionKwh, 0.0)
        self.assertEqual(self.machine._manufacturer, "")
        self.assertEqual(self.machine._installationDate, "")

    def test_machine_identifier_property(self):
        """Тест свойства machineIdentifier"""
        self.assertEqual(self.machine.machineIdentifier, "MACH001")

        # Проверяем, что свойство только для чтения
        with self.assertRaises(AttributeError):
            self.machine.machineIdentifier = "NEW_ID"

    def test_schedule_maintenance(self):
        """Тест планирования обслуживания"""
        self.machine.scheduleMaintenance()
        self.assertTrue(self.machine._maintenanceRequired)

    def test_complete_maintenance(self):
        """Тест завершения обслуживания"""
        self.machine._maintenanceRequired = True
        self.machine._isOperational = False

        self.machine.completeMaintenance()

        self.assertFalse(self.machine._maintenanceRequired)
        self.assertTrue(self.machine._isOperational)

    def test_check_maintenance_need_no_maintenance(self):
        """Тест проверки необходимости обслуживания - обслуживание не требуется"""
        result = self.machine.checkMaintenanceNeed()
        self.assertFalse(result)

    def test_check_maintenance_need_maintenance_required(self):
        """Тест проверки необходимости обслуживания - обслуживание требуется"""
        self.machine._maintenanceRequired = True

        with self.assertRaises(MachineMaintenanceRequiredError):
            self.machine.checkMaintenanceNeed()

    def test_update_operational_hours_positive(self):
        """Тест обновления отработанных часов с положительным значением"""
        self.machine.updateOperationalHours(8.5)
        self.assertEqual(self.machine._operationalHours, 8.5)

        self.machine.updateOperationalHours(4.0)
        self.assertEqual(self.machine._operationalHours, 12.5)

    def test_update_operational_hours_zero(self):
        """Тест обновления отработанных часов с нулевым значением"""
        initial_hours = self.machine._operationalHours
        self.machine.updateOperationalHours(0.0)
        self.assertEqual(self.machine._operationalHours, initial_hours)

    def test_update_operational_hours_negative(self):
        """Тест обновления отработанных часов с отрицательным значением"""
        initial_hours = self.machine._operationalHours
        self.machine.updateOperationalHours(-5.0)
        self.assertEqual(self.machine._operationalHours, initial_hours)

    def test_calculate_energy_cost(self):
        """Тест расчета стоимости энергии"""
        self.machine._energyConsumptionKwh = 15.5
        energy_rate = 2.5

        cost = self.machine.calculateEnergyCost(energy_rate)
        expected_cost = 15.5 * 2.5

        self.assertEqual(cost, expected_cost)

    def test_calculate_energy_cost_zero_consumption(self):
        """Тест расчета стоимости энергии при нулевом потреблении"""
        self.machine._energyConsumptionKwh = 0.0
        energy_rate = 2.5

        cost = self.machine.calculateEnergyCost(energy_rate)
        self.assertEqual(cost, 0.0)

    def test_calculate_energy_cost_zero_rate(self):
        """Тест расчета стоимости энергии при нулевой ставке"""
        self.machine._energyConsumptionKwh = 10.0
        energy_rate = 0.0

        cost = self.machine.calculateEnergyCost(energy_rate)
        self.assertEqual(cost, 0.0)

    def test_get_machine_status(self):
        """Тест получения статуса станка"""
        self.machine._operationalHours = 100.5
        self.machine._energyConsumptionKwh = 25.3

        status = self.machine.getMachineStatus()

        self.assertEqual(status["machineIdentifier"], "MACH001")
        self.assertEqual(status["machineName"], "Токарный станок")
        self.assertTrue(status["isOperational"])
        self.assertEqual(status["operationalHours"], 100.5)
        self.assertFalse(status["maintenanceRequired"])
        self.assertEqual(status["energyConsumption"], 25.3)

    def test_abstract_methods_implementation(self):
        """Тест реализации абстрактных методов"""
        # Проверяем, что методы реализованы и работают
        self.assertTrue(self.machine.performOperation())
        self.assertEqual(self.machine.calculateEfficiency(), 0.85)

    def test_abstract_methods_called(self):
        """Тест вызова абстрактных методов"""
        # Проверяем, что методы действительно вызываются и выполняют логику
        initial_operations = self.machine.test_operations
        result = self.machine.performOperation()

        self.assertTrue(result)
        self.assertEqual(self.machine.test_operations, initial_operations + 1)


if __name__ == '__main__':
    unittest.main()
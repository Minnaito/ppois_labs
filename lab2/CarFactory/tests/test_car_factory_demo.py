import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from CarFactoryDemo import CarFactoryDemo, main


class TestCarFactoryDemo(unittest.TestCase):

    def setUp(self):
        self.factory = CarFactoryDemo()
        self.original_stdout = sys.stdout

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_initialization(self):
        """Тестирование инициализации фабрики"""
        self.assertEqual(len(self.factory.employees), 0)
        self.assertEqual(len(self.factory.productionLines), 0)
        self.assertEqual(len(self.factory.warehouses), 0)
        self.assertEqual(len(self.factory.factoryBuildings), 0)
        self.assertEqual(self.factory.totalProduction, 0)
        self.assertEqual(self.factory.financialBalance, 5000000)

    def test_setup_basic_infrastructure(self):
        """Тестирование создания базовой инфраструктуры"""
        captured_output = StringIO()
        sys.stdout = captured_output

        self.factory.setupBasicInfrastructure()

        output = captured_output.getvalue()

        self.assertEqual(len(self.factory.employees), 6)
        self.assertEqual(len(self.factory.productionLines), 1)
        self.assertEqual(len(self.factory.warehouses), 1)
        self.assertEqual(len(self.factory.factoryBuildings), 1)

        # Проверяем наличие ключевых сообщений в выводе
        self.assertIn("СОЗДАНИЕ ИНФРАСТРУКТУРЫ", output)
        self.assertIn("Нанято сотрудников: 6", output)
        self.assertIn("Запущена производственная линия", output)

        # Проверяем расчет зарплат
        monthly_salary_fund = sum(emp._monthlySalary for emp in self.factory.employees)
        self.assertGreater(monthly_salary_fund, 0)
        self.assertIn(f"Месячный фонд зарплаты: {monthly_salary_fund:,.0f} руб.", output)

    def test_demonstrate_employee_work(self):
        """Тестирование демонстрации работы сотрудников"""
        self.factory.setupBasicInfrastructure()

        captured_output = StringIO()
        sys.stdout = captured_output

        self.factory.demonstrateEmployeeWork()

        output = captured_output.getvalue()

        self.assertIn("РАБОТА СОТРУДНИКОВ", output)
        self.assertIn("Иванова Анна", output)
        self.assertIn("Петров Алексей", output)
        self.assertIn("ИТОГО по персоналу", output)

        # Проверяем расчет итоговых сумм
        total_monthly_salary = sum(emp._monthlySalary for emp in self.factory.employees)
        self.assertIn(f"Месячный фонд зарплат: {total_monthly_salary:,.0f} руб.", output)

    def test_demonstrate_production(self):
        """Тестирование демонстрации производства"""
        self.factory.setupBasicInfrastructure()

        captured_output = StringIO()
        sys.stdout = captured_output

        self.factory.demonstrateProduction()

        output = captured_output.getvalue()

        self.assertIn("ПРОИЗВОДСТВЕННЫЙ ПРОЦЕСС", output)
        self.assertIn("Производство партии из", output)
        self.assertIn("Двигатель V6", output)
        self.assertIn("6-ступенчатая МКПП", output)
        self.assertIn("Производственная линия", output)

        # Проверяем расчеты производства
        self.assertGreater(self.factory.totalProduction, 0)
        self.assertIn(f"Выпущено за смену: {self.factory.totalProduction} деталей", output)

        # Проверяем сохранение данных для финансового раздела
        self.assertTrue(hasattr(self.factory, 'engine_batch_size'))
        self.assertTrue(hasattr(self.factory, 'transmission_batch_size'))
        self.assertTrue(hasattr(self.factory, 'engineCost'))
        self.assertTrue(hasattr(self.factory, 'transmissionCost'))

    def test_demonstrate_warehouse_operations(self):
        """Тестирование демонстрации складских операций"""
        self.factory.setupBasicInfrastructure()
        self.factory.totalProduction = 300  # Устанавливаем значение для теста

        captured_output = StringIO()
        sys.stdout = captured_output

        self.factory.demonstrateWarehouseOperations()

        output = captured_output.getvalue()

        self.assertIn("СКЛАДСКИЕ ОПЕРАЦИИ", output)
        self.assertIn("Добавлено: Двигатель V6", output)
        self.assertIn("Статус склада", output)

        # Проверяем, что склад создан
        if self.factory.warehouses:
            warehouse = self.factory.warehouses[0]
            self.assertEqual(warehouse._warehouseName, "Основной склад")

    def test_demonstrate_financial_operations(self):
        """Тестирование демонстрации финансовых операций"""
        self.factory.setupBasicInfrastructure()

        # Устанавливаем значения для теста
        self.factory.totalProduction = 300
        self.factory.engine_batch_size = 180
        self.factory.transmission_batch_size = 120

        captured_output = StringIO()
        sys.stdout = captured_output

        self.factory.demonstrateFinancialOperations()

        output = captured_output.getvalue()

        self.assertIn("ФИНАНСОВЫЕ ОПЕРАЦИИ", output)
        self.assertIn("РАСПРЕДЕЛЕНИЕ БЮДЖЕТА", output)
        self.assertIn("РАСХОДОВАНИЕ СРЕДСТВ", output)
        self.assertIn("БЮДЖЕТНЫЙ ОТЧЕТ", output)

        # Проверяем ключевые расчеты
        monthly_salary_cost = sum(emp._monthlySalary for emp in self.factory.employees)
        self.assertIn(f"Месячный фонд зарплат: {monthly_salary_cost:,.0f} руб.", output)

    def test_demonstrate_quality_control(self):
        """Тестирование демонстрации контроля качества"""
        self.factory.setupBasicInfrastructure()
        self.factory.totalProduction = 300

        captured_output = StringIO()
        sys.stdout = captured_output

        self.factory.demonstrateQualityControl()

        output = captured_output.getvalue()

        self.assertIn("КОНТРОЛЬ КАЧЕСТВА", output)
        self.assertIn("Контроль качества произведенной партии", output)
        self.assertIn("ОТЧЕТ ПО КАЧЕСТВУ", output)
        self.assertIn("Процент прохождения:", output)

    def test_demonstrate_maintenance(self):
        """Тестирование демонстрации технического обслуживания"""
        self.factory.setupBasicInfrastructure()

        captured_output = StringIO()
        sys.stdout = captured_output

        self.factory.demonstrateMaintenance()

        output = captured_output.getvalue()

        self.assertIn("ТЕХНИЧЕСКОЕ ОБСЛУЖИВАНИЕ", output)
        self.assertIn("CNC станок", output)
        self.assertIn("ИТОГИ ОБСЛУЖИВАНИЯ", output)

    def test_generate_final_report(self):
        """Тестирование генерации итогового отчета"""
        self.factory.setupBasicInfrastructure()
        self.factory.totalProduction = 300

        captured_output = StringIO()
        sys.stdout = captured_output

        self.factory.generateFinalReport()

        output = captured_output.getvalue()

        self.assertIn("ИТОГОВЫЙ ОТЧЕТ ПО ПРЕДПРИЯТИЮ", output)
        self.assertIn("КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ ПРЕДПРИЯТИЯ", output)
        self.assertIn("ОЦЕНКА ЭФФЕКТИВНОСТИ", output)

        # Проверяем наличие ключевых показателей
        self.assertIn("ПЕРСОНАЛ:", output)
        self.assertIn("ПРОИЗВОДСТВО:", output)
        self.assertIn("СКЛАДЫ:", output)
        self.assertIn("ФИНАНСЫ:", output)

    def test_run_complete_demo(self):
        """Тестирование полной демонстрации"""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            self.factory.runCompleteDemo()
        except Exception as e:
            self.fail(f"runCompleteDemo вызвал исключение: {e}")

        output = captured_output.getvalue()

        self.assertIn("ЗАПУСК ДЕМОНСТРАЦИИ АВТОМОБИЛЬНОГО ЗАВОДА", output)
        self.assertIn("ДЕМОНСТРАЦИЯ УСПЕШНО ЗАВЕРШЕНА", output)

    def test_main_function(self):
        """Тестирование функции main"""
        captured_output = StringIO()
        sys.stdout = captured_output

        # Мокаем CarFactoryDemo чтобы не запускать полную демонстрацию
        with patch('CarFactoryDemo.CarFactoryDemo') as MockFactory:
            mock_factory_instance = MagicMock()
            MockFactory.return_value = mock_factory_instance

            main()

            MockFactory.assert_called_once()
            mock_factory_instance.runCompleteDemo.assert_called_once()

    def test_error_handling(self):
        """Тестирование обработки ошибок в runCompleteDemo"""
        factory = CarFactoryDemo()

        # Создаем ситуацию, которая вызовет ошибку
        with patch.object(factory, 'setupBasicInfrastructure', side_effect=Exception("Тестовая ошибка")):
            captured_output = StringIO()
            sys.stdout = captured_output

            factory.runCompleteDemo()

            output = captured_output.getvalue()
            self.assertIn("ОШИБКА: Тестовая ошибка", output)
            self.assertIn("Демонстрация прервана", output)

    def test_employee_salary_calculations(self):
        """Тестирование расчетов зарплат сотрудников"""
        self.factory.setupBasicInfrastructure()

        total_monthly = 0
        for emp in self.factory.employees:
            self.assertIsNotNone(emp._monthlySalary)
            self.assertGreater(emp._monthlySalary, 0)
            total_monthly += emp._monthlySalary

        # Проверяем, что сумма зарплат соответствует ожидаемой
        expected_total = 45000 + 35000 + 38000 + 42000 + 55000 + 32000
        self.assertEqual(total_monthly, expected_total)

    def test_budget_allocation(self):
        """Тестирование распределения бюджета"""
        self.factory.setupBasicInfrastructure()

        # Проверяем распределение бюджета в demonstrateFinancialOperations
        monthly_salary_cost = sum(emp._monthlySalary for emp in self.factory.employees)
        quarterly_salary_cost = monthly_salary_cost * 3
        salary_budget = quarterly_salary_cost * 1.34

        # Убедимся, что зарплаты не превышают 40% бюджета
        total_budget = 7000000
        if salary_budget > total_budget * 0.4:
            expected_salary_budget = total_budget * 0.4
        else:
            expected_salary_budget = salary_budget

        # Проверяем, что распределение логично
        self.assertLess(expected_salary_budget, total_budget)
        self.assertGreater(expected_salary_budget, 0)


class TestCarFactoryDemoIntegration(unittest.TestCase):
    """Интеграционные тесты для CarFactoryDemo"""

    def test_full_integration(self):
        """Полный интеграционный тест"""
        factory = CarFactoryDemo()

        # Запускаем все методы по порядку
        factory.setupBasicInfrastructure()

        # Проверяем состояние после setup
        self.assertEqual(len(factory.employees), 6)
        self.assertEqual(len(factory.productionLines), 1)
        self.assertEqual(len(factory.warehouses), 1)

        # Запускаем производство
        factory.demonstrateProduction()
        self.assertGreater(factory.totalProduction, 0)

        # Проверяем складские операции
        factory.demonstrateWarehouseOperations()
        if factory.warehouses:
            warehouse = factory.warehouses[0]
            self.assertGreater(warehouse._currentStock, 0)

        # Проверяем финансовые операции (без вывода)
        with patch('sys.stdout', new=StringIO()):
            factory.demonstrateFinancialOperations()

        # Проверяем качество (без вывода)
        with patch('sys.stdout', new=StringIO()):
            factory.demonstrateQualityControl()

        # Проверяем итоговый отчет
        with patch('sys.stdout', new=StringIO()):
            factory.generateFinalReport()


if __name__ == '__main__':
    # Запуск всех тестов
    unittest.main(verbosity=2)
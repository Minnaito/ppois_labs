import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.finance.CostAnalysis import CostAnalysis
from config import constants


class TestCostAnalysis(unittest.TestCase):
    """Тесты для класса CostAnalysis"""

    def test_cost_analysis_initialization(self):
        """Тест инициализации анализа затрат"""
        analysis = CostAnalysis("CA001", "2024-Q1")

        self.assertEqual(analysis._analysisId, "CA001")
        self.assertEqual(analysis._analysisPeriod, "2024-Q1")
        self.assertEqual(analysis._totalCosts, 0.0)
        self.assertEqual(analysis._costBreakdown, {})

    def test_add_cost_category_material(self):
        """Тест добавления категории материальных затрат"""
        analysis = CostAnalysis("CA001", "2024-Q1")
        analysis.addCostCategory("material_purchase", 5000.0)

        self.assertEqual(analysis._materialCosts, 5000.0)
        self.assertEqual(analysis._totalCosts, 5000.0)
        self.assertIn("material_purchase", analysis._costBreakdown)

    def test_add_cost_category_labor(self):
        """Тест добавления категории трудовых затрат"""
        analysis = CostAnalysis("CA001", "2024-Q1")
        analysis.addCostCategory("labor_wages", 3000.0)

        self.assertEqual(analysis._laborCosts, 3000.0)
        self.assertEqual(analysis._totalCosts, 3000.0)

    def test_add_cost_category_maintenance(self):
        """Тест добавления категории затрат на обслуживание"""
        analysis = CostAnalysis("CA001", "2024-Q1")
        analysis.addCostCategory("maintenance_repairs", 1000.0)

        self.assertEqual(analysis._maintenanceCosts, 1000.0)
        self.assertEqual(analysis._totalCosts, 1000.0)

    def test_add_cost_category_overhead(self):
        """Тест добавления накладных расходов"""
        analysis = CostAnalysis("CA001", "2024-Q1")
        analysis.addCostCategory("office_supplies", 500.0)

        self.assertEqual(analysis._overheadCosts, 500.0)
        self.assertEqual(analysis._totalCosts, 500.0)

    def test_add_multiple_cost_categories(self):
        """Тест добавления нескольких категорий затрат"""
        analysis = CostAnalysis("CA001", "2024-Q1")

        analysis.addCostCategory("raw_materials", 5000.0)
        analysis.addCostCategory("employee_salaries", 3000.0)
        analysis.addCostCategory("equipment_maintenance", 1000.0)
        analysis.addCostCategory("utilities", 500.0)

        self.assertEqual(analysis._totalCosts, 9500.0)
        self.assertEqual(analysis._materialCosts, 5000.0)
        self.assertEqual(analysis._laborCosts, 3000.0)
        self.assertEqual(analysis._maintenanceCosts, 1000.0)
        self.assertEqual(analysis._overheadCosts, 500.0)
        self.assertEqual(len(analysis._costBreakdown), 4)

    def test_calculate_cost_distribution(self):
        """Тест расчета распределения затрат"""
        analysis = CostAnalysis("CA001", "2024-Q1")

        analysis.addCostCategory("materials", 4000.0)  # 40%
        analysis.addCostCategory("labor", 3000.0)  # 30%
        analysis.addCostCategory("maintenance", 2000.0)  # 20%
        analysis.addCostCategory("overhead", 1000.0)  # 10%

        distribution = analysis.calculateCostDistribution()

        self.assertEqual(distribution["materialPercentage"], 40.0)
        self.assertEqual(distribution["laborPercentage"], 30.0)
        self.assertEqual(distribution["maintenancePercentage"], 20.0)
        self.assertEqual(distribution["overheadPercentage"], 10.0)

    def test_calculate_cost_distribution_zero_total(self):
        """Тест расчета распределения при нулевых затратах"""
        analysis = CostAnalysis("CA001", "2024-Q1")
        distribution = analysis.calculateCostDistribution()

        self.assertEqual(distribution, {})

    def test_get_analysis_report(self):
        """Тест получения полного отчета анализа"""
        analysis = CostAnalysis("CA001", "2024-Q1")

        analysis.addCostCategory("materials", 4000.0)
        analysis.addCostCategory("labor", 3000.0)

        report = analysis.getAnalysisReport()

        self.assertEqual(report["analysisId"], "CA001")
        self.assertEqual(report["analysisPeriod"], "2024-Q1")
        self.assertEqual(report["totalCosts"], 7000.0)
        self.assertEqual(report["materialCosts"], 4000.0)
        self.assertEqual(report["laborCosts"], 3000.0)
        self.assertEqual(report["categoriesCount"], 2)
        self.assertIn("costDistribution", report)

    def test_cost_categorization_logic(self):
        """Тест логики автоматической категоризации"""
        analysis = CostAnalysis("CA001", "2024-Q1")

        # Тестируем различные варианты названий категорий
        test_cases = [
            ("material_supplies", 1000.0, "material"),
            ("raw_materials", 2000.0, "material"),
            ("labor_costs", 1500.0, "labor"),
            ("employee_wages", 1200.0, "labor"),
            ("maintenance_fee", 800.0, "maintenance"),
            ("equipment_repair", 600.0, "maintenance"),
            ("office_rent", 500.0, "overhead"),
            ("utilities_bill", 300.0, "overhead")
        ]

        for category, amount, expected_type in test_cases:
            with self.subTest(category=category):
                analysis.addCostCategory(category, amount)

        self.assertEqual(analysis._materialCosts, 3000.0)  # 1000 + 2000
        self.assertEqual(analysis._laborCosts, 2700.0)  # 1500 + 1200
        self.assertEqual(analysis._maintenanceCosts, 1400.0)  # 800 + 600
        self.assertEqual(analysis._overheadCosts, 800.0)  # 500 + 300
        self.assertEqual(analysis._totalCosts, 7900.0)

    def test_cost_distribution_rounding(self):
        """Тест округления при распределении затрат"""
        analysis = CostAnalysis("CA001", "2024-Q1")

        analysis.addCostCategory("materials", 3333.33)
        analysis.addCostCategory("labor", 3333.33)
        analysis.addCostCategory("overhead", 3333.34)

        distribution = analysis.calculateCostDistribution()

        # Проверяем что сумма процентов равна 100%
        total_percentage = (distribution["materialPercentage"] +
                            distribution["laborPercentage"] +
                            distribution["overheadPercentage"])
        self.assertAlmostEqual(total_percentage, 100.0, places=2)


if __name__ == '__main__':
    unittest.main()
import unittest
from models.finance.CostAnalysis import CostAnalysis


class TestCostAnalysis(unittest.TestCase):

    def testCostAnalysisInitialization(self):
        """Тест инициализации анализа затрат"""
        analysis = CostAnalysis("CA001", "Q1 2024")
        self.assertEqual(analysis._analysisId, "CA001")
        self.assertEqual(analysis._analysisPeriod, "Q1 2024")
        self.assertEqual(analysis._totalCosts, 0.0)
        self.assertEqual(len(analysis._costBreakdown), 0)

    def testAddCostCategory(self):
        """Тест добавления категории затрат"""
        analysis = CostAnalysis("CA001", "Q1 2024")

        # Добавляем категории
        analysis.addCostCategory("Материалы", 600000)
        analysis.addCostCategory("Зарплаты", 400000)
        analysis.addCostCategory("Аренда", 200000)

        # Проверяем количество категорий
        self.assertEqual(len(analysis._costBreakdown), 3)

        # Проверяем значения
        self.assertEqual(analysis._costBreakdown["Материалы"], 600000)
        self.assertEqual(analysis._costBreakdown["Зарплаты"], 400000)
        self.assertEqual(analysis._costBreakdown["Аренда"], 200000)

        # Проверяем общую сумму
        self.assertEqual(analysis._totalCosts, 1200000)

    def testAddCostCategoryUpdatesTotal(self):
        """Тест обновления общей суммы при добавлении категорий"""
        analysis = CostAnalysis("CA001", "Q1 2024")

        # Добавляем категории и проверяем общую сумму после каждой
        analysis.addCostCategory("Категория1", 100000)
        self.assertEqual(analysis._totalCosts, 100000)

        analysis.addCostCategory("Категория2", 250000)
        self.assertEqual(analysis._totalCosts, 350000)

        analysis.addCostCategory("Категория3", 150000)
        self.assertEqual(analysis._totalCosts, 500000)

    def testCalculateCostDistribution(self):
        """Тест расчета распределения затрат"""
        analysis = CostAnalysis("CA001", "Q1 2024")

        # Добавляем категории
        analysis.addCostCategory("Материалы", 600000)  # 50%
        analysis.addCostCategory("Зарплаты", 400000)  # 33.33%
        analysis.addCostCategory("Аренда", 200000)  # 16.67%

        # Получаем распределение
        distribution = analysis.calculateCostDistribution()

        # Проверяем количество категорий в распределении
        self.assertEqual(len(distribution), 3)

        # Проверяем процентное распределение
        self.assertAlmostEqual(distribution["Материалы"], 50.0, places=2)
        self.assertAlmostEqual(distribution["Зарплаты"], 33.333333, places=2)
        self.assertAlmostEqual(distribution["Аренда"], 16.666666, places=2)

        # Проверяем, что сумма процентов равна 100
        total_percentage = sum(distribution.values())
        self.assertAlmostEqual(total_percentage, 100.0, places=2)

    def testCalculateCostDistributionZeroTotal(self):
        """Тест расчета распределения при нулевых затратах"""
        analysis = CostAnalysis("CA001", "Q1 2024")

        # Не добавляем категории, totalCosts = 0
        distribution = analysis.calculateCostDistribution()

        # Должен вернуться пустой словарь
        self.assertEqual(len(distribution), 0)

    def testCalculateCostDistributionSingleCategory(self):
        """Тест расчета распределения с одной категорией"""
        analysis = CostAnalysis("CA001", "Q1 2024")
        analysis.addCostCategory("Материалы", 1000000)

        distribution = analysis.calculateCostDistribution()

        # Должен быть 100% для единственной категории
        self.assertEqual(len(distribution), 1)
        self.assertEqual(distribution["Материалы"], 100.0)

    def testGetAnalysisReport(self):
        """Тест получения отчета анализа"""
        analysis = CostAnalysis("CA001", "Q1 2024")

        # Добавляем категории
        analysis.addCostCategory("Материалы", 600000)
        analysis.addCostCategory("Зарплаты", 400000)

        # Получаем отчет
        report = analysis.getAnalysisReport()

        # Проверяем структуру отчета
        self.assertEqual(report["analysisId"], "CA001")
        self.assertEqual(report["analysisPeriod"], "Q1 2024")
        self.assertEqual(report["totalCosts"], 1000000)

        # Проверяем распределение в отчете
        self.assertEqual(len(report["costDistribution"]), 2)
        self.assertEqual(report["costDistribution"]["Материалы"], 60.0)
        self.assertEqual(report["costDistribution"]["Зарплаты"], 40.0)

    def testGetAnalysisReportEmpty(self):
        """Тест получения отчета без категорий"""
        analysis = CostAnalysis("CA001", "Q1 2024")

        report = analysis.getAnalysisReport()

        self.assertEqual(report["analysisId"], "CA001")
        self.assertEqual(report["analysisPeriod"], "Q1 2024")
        self.assertEqual(report["totalCosts"], 0.0)
        self.assertEqual(len(report["costDistribution"]), 0)

    def testUpdateExistingCategory(self):
        """Тест обновления существующей категории"""
        analysis = CostAnalysis("CA001", "Q1 2024")

        # Добавляем категорию
        analysis.addCostCategory("Материалы", 500000)
        self.assertEqual(analysis._costBreakdown["Материалы"], 500000)
        self.assertEqual(analysis._totalCosts, 500000)

        # Добавляем ту же категорию снова - должно добавиться
        analysis.addCostCategory("Материалы", 300000)
        self.assertEqual(analysis._costBreakdown["Материалы"], 300000)  # Перезаписывается
        self.assertEqual(analysis._totalCosts, 800000)  # 500000 + 300000

    def testComplexScenario(self):
        """Тест сложного сценария с множеством категорий"""
        analysis = CostAnalysis("CA001", "2024 год")

        # Добавляем множество категорий
        categories = {
            "Материалы": 1500000,
            "Зарплаты": 1200000,
            "Аренда": 800000,
            "Коммунальные услуги": 300000,
            "Транспорт": 200000,
            "Маркетинг": 500000,
            "Налоги": 700000,
            "Прочее": 300000
        }

        for category, amount in categories.items():
            analysis.addCostCategory(category, amount)

        # Проверяем общую сумму
        total_expected = sum(categories.values())
        self.assertEqual(analysis._totalCosts, total_expected)

        # Проверяем распределение
        distribution = analysis.calculateCostDistribution()

        # Проверяем, что все категории присутствуют
        self.assertEqual(len(distribution), len(categories))

        # Проверяем, что сумма процентов равна 100
        total_percentage = sum(distribution.values())
        self.assertAlmostEqual(total_percentage, 100.0, places=2)

        # Проверяем конкретные значения
        materials_percentage = (categories["Материалы"] / total_expected) * 100
        self.assertAlmostEqual(distribution["Материалы"], materials_percentage, places=2)


if __name__ == '__main__':
    unittest.main()
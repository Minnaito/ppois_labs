import unittest
from config import constants
from models.quality.DefectReport import DefectReport


class TestDefectReport(unittest.TestCase):

    def testDefectReportInitialization(self):
        """Тест инициализации отчета о дефектах"""
        report = DefectReport("DR001", "PART001", "INSP001")

        self.assertEqual(report._report_id, "DR001")
        self.assertEqual(report._part_id, "PART001")
        self.assertEqual(report._inspector_id, "INSP001")
        self.assertEqual(len(report._defects), 0)

    def testAddDefect(self):
        """Тест добавления дефекта"""
        report = DefectReport("DR001", "PART001", "INSP001")

        # Добавляем дефекты
        report.add_defect("Царапина на поверхности")
        report.add_defect("Несоответствие размерам")
        report.add_defect("Дефект покраски")

        # Проверяем количество дефектов
        self.assertEqual(len(report._defects), 3)

        # Проверяем содержание дефектов
        self.assertEqual(report._defects[0], "Царапина на поверхности")
        self.assertEqual(report._defects[1], "Несоответствие размерам")
        self.assertEqual(report._defects[2], "Дефект покраски")

    def testCalculateRepairCost(self):
        """Тест расчета стоимости ремонта"""
        report = DefectReport("DR001", "PART001", "INSP001")

        # Без дефектов
        cost = report.calculate_repair_cost()
        expected_cost = constants.BASE_REPAIR_COST + (0 * constants.MATERIAL_COST_MULTIPLIER)
        self.assertEqual(cost, expected_cost)

        # С одним дефектом
        report.add_defect("Царапина")
        cost = report.calculate_repair_cost()
        expected_cost = constants.BASE_REPAIR_COST + (1 * constants.MATERIAL_COST_MULTIPLIER)
        self.assertEqual(cost, expected_cost)

        # С несколькими дефектами
        report.add_defect("Трещина")
        report.add_defect("Деформация")
        cost = report.calculate_repair_cost()
        expected_cost = constants.BASE_REPAIR_COST + (3 * constants.MATERIAL_COST_MULTIPLIER)
        self.assertEqual(cost, expected_cost)

    def testCalculateRepairCostManyDefects(self):
        """Тест расчета стоимости ремонта при большом количестве дефектов"""
        report = DefectReport("DR001", "PART001", "INSP001")

        # Добавляем 10 дефектов
        for i in range(10):
            report.add_defect(f"Дефект {i + 1}")

        cost = report.calculate_repair_cost()
        expected_cost = constants.BASE_REPAIR_COST + (10 * constants.MATERIAL_COST_MULTIPLIER)
        self.assertEqual(cost, expected_cost)

    def testGetSummary(self):
        """Тест получения сводки отчета"""
        report = DefectReport("DR001", "PART001", "INSP001")

        # Добавляем дефекты
        report.add_defect("Царапина")
        report.add_defect("Трещина")

        # Получаем сводку
        summary = report.get_summary()

        # Проверяем структуру сводки
        self.assertEqual(summary["report_id"], "DR001")
        self.assertEqual(summary["part_id"], "PART001")
        self.assertEqual(summary["defects_count"], 2)

        # Проверяем стоимость ремонта
        expected_cost = constants.BASE_REPAIR_COST + (2 * constants.MATERIAL_COST_MULTIPLIER)
        self.assertEqual(summary["repair_cost"], expected_cost)

    def testGetSummaryNoDefects(self):
        """Тест получения сводки без дефектов"""
        report = DefectReport("DR001", "PART001", "INSP001")

        summary = report.get_summary()

        self.assertEqual(summary["report_id"], "DR001")
        self.assertEqual(summary["part_id"], "PART001")
        self.assertEqual(summary["defects_count"], 0)

        expected_cost = constants.BASE_REPAIR_COST
        self.assertEqual(summary["repair_cost"], expected_cost)

    def testGetSummaryManyDefects(self):
        """Тест получения сводки с большим количеством дефектов"""
        report = DefectReport("DR001", "PART001", "INSP001")

        # Добавляем много дефектов
        defect_count = 25
        for i in range(defect_count):
            report.add_defect(f"Дефект типа {i % 5}")

        summary = report.get_summary()

        self.assertEqual(summary["defects_count"], defect_count)

        expected_cost = constants.BASE_REPAIR_COST + (defect_count * constants.MATERIAL_COST_MULTIPLIER)
        self.assertEqual(summary["repair_cost"], expected_cost)

    def testDefectReportProperties(self):
        """Тест свойств отчета о дефектах"""
        report = DefectReport("DR001", "PART001", "INSP001")

        # Проверяем начальные свойства
        self.assertEqual(report._report_id, "DR001")
        self.assertEqual(report._part_id, "PART001")
        self.assertEqual(report._inspector_id, "INSP001")

        # Изменяем свойства (если это возможно в реальном коде)
        # В данном классе свойства защищенные, но мы можем проверить через методы

        # Добавляем дефект и проверяем через сводку
        report.add_defect("Тестовый дефект")
        summary = report.get_summary()
        self.assertEqual(summary["defects_count"], 1)

    def testMultipleReports(self):
        """Тест работы с несколькими отчетами"""
        reports = []

        # Создаем несколько отчетов
        for i in range(5):
            report = DefectReport(f"DR{i + 1:03d}", f"PART{i + 1:03d}", f"INSP{i + 1:03d}")

            # Добавляем разное количество дефектов
            for j in range(i + 1):
                report.add_defect(f"Дефект {j + 1} отчета {i + 1}")

            reports.append(report)

        # Проверяем каждый отчет
        for i, report in enumerate(reports):
            expected_defects = i + 1
            expected_cost = constants.BASE_REPAIR_COST + (expected_defects * constants.MATERIAL_COST_MULTIPLIER)

            summary = report.get_summary()

            self.assertEqual(summary["report_id"], f"DR{i + 1:03d}")
            self.assertEqual(summary["part_id"], f"PART{i + 1:03d}")
            self.assertEqual(summary["defects_count"], expected_defects)
            self.assertEqual(summary["repair_cost"], expected_cost)

    def testDefectTypes(self):
        """Тест с разными типами дефектов"""
        report = DefectReport("DR001", "PART001", "INSP001")

        # Разные типы дефектов
        defect_types = [
            "Царапина поверхности",
            "Глубокая трещина",
            "Деформация конструкции",
            "Несоответствие размерам ±0.5мм",
            "Дефект покрытия",
            "Коррозия",
            "Отсутствие детали",
            "Неправильная сборка"
        ]

        for defect in defect_types:
            report.add_defect(defect)

        self.assertEqual(len(report._defects), len(defect_types))

        # Проверяем, что все дефекты сохранены правильно
        for i, expected_defect in enumerate(defect_types):
            self.assertEqual(report._defects[i], expected_defect)

        # Проверяем стоимость ремонта
        summary = report.get_summary()
        expected_cost = constants.BASE_REPAIR_COST + (len(defect_types) * constants.MATERIAL_COST_MULTIPLIER)
        self.assertEqual(summary["repair_cost"], expected_cost)


if __name__ == '__main__':
    unittest.main()
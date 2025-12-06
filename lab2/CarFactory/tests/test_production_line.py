import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.production.ProductionLine import ProductionLine


class TestProductionLine(unittest.TestCase):

    def testProductionLineInitialization(self):
        line = ProductionLine("PL001", "Основная линия", 100)

        self.assertEqual(line._line_id, "PL001")
        self.assertEqual(line._name, "Основная линия")
        self.assertEqual(line._capacity, 100)
        self.assertEqual(line._produced, 0)
        self.assertTrue(line._is_active)

    def testProductionLineProduceSuccess(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        result = line.produce(50)

        self.assertTrue(result)
        self.assertEqual(line._produced, 50)

    def testProductionLineProduceExceedsCapacity(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        line.produce(80)
        result = line.produce(30)

        self.assertFalse(result)
        self.assertEqual(line._produced, 80)

    def testProductionLineProduceMultiple(self):
        line = ProductionLine("PL001", "Основная линия", 200)

        self.assertTrue(line.produce(50))
        self.assertEqual(line._produced, 50)

        self.assertTrue(line.produce(70))
        self.assertEqual(line._produced, 120)

        self.assertTrue(line.produce(30))
        self.assertEqual(line._produced, 150)

        self.assertFalse(line.produce(60))
        self.assertEqual(line._produced, 150)

    def testProductionLineCalculateUtilization(self):
        line = ProductionLine("PL001", "Основная линия", 100)

        utilization = line.calculate_utilization()
        self.assertEqual(utilization, 0.0)

        line.produce(25)
        utilization = line.calculate_utilization()
        self.assertEqual(utilization, 25.0)

        line.produce(25)
        utilization = line.calculate_utilization()
        self.assertEqual(utilization, 50.0)

        line.produce(50)
        utilization = line.calculate_utilization()
        self.assertEqual(utilization, 100.0)

    def testProductionLineCalculateUtilizationZeroCapacity(self):
        line = ProductionLine("PL002", "Пустая линия", 0)
        utilization = line.calculate_utilization()
        self.assertEqual(utilization, 0.0)

    def testProductionLineStartStop(self):
        line = ProductionLine("PL001", "Основная линия", 100)

        start_result = line.start_line()
        self.assertIn("запущена", start_result)
        self.assertTrue(line._is_active)

        stop_result = line.stop_line()
        self.assertIn("остановлена", stop_result)
        self.assertFalse(line._is_active)

    def testProductionLineProduceWhenInactive(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        line.stop_line()

        result = line.produce(50)
        self.assertFalse(result)
        self.assertEqual(line._produced, 0)

    def testProductionLineGetInfo(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        line.produce(30)

        info = line.get_info()

        self.assertEqual(info["id"], "PL001")
        self.assertEqual(info["name"], "Основная линия")
        self.assertEqual(info["capacity"], 100)
        self.assertEqual(info["produced"], 30)
        self.assertEqual(info["utilization"], 30.0)
        self.assertTrue(info["is_active"])

    def testProductionLineCalculateEfficiency(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        line.produce(80)

        efficiency = line.calculate_efficiency(100)
        self.assertEqual(efficiency, 80.0)

        efficiency2 = line.calculate_efficiency(50)
        self.assertEqual(efficiency2, 100.0)

        efficiency3 = line.calculate_efficiency(0)
        self.assertEqual(efficiency3, 0.0)

    def testProductionLinePredictCompletionDate(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        line.produce(60)

        date = line.predict_completion_date(10)
        self.assertIsInstance(date, str)
        self.assertIn("-", date)

    def testProductionLineCalculateDowntimeCost(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        cost = line.calculate_downtime_cost(5, 1000)
        self.assertEqual(cost, 5000.0)

    def testProductionLineOptimizeSchedule(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        orders = [30, 40, 50]

        schedule = line.optimize_schedule(orders)
        self.assertIn("total_orders", schedule)
        self.assertIn("estimated_days", schedule)
        self.assertEqual(schedule["total_orders"], 120)

    def testProductionLineGenerateReport(self):
        line = ProductionLine("PL001", "Основная линия", 100)
        line.produce(75)

        report = line.generate_report()

        self.assertEqual(report["line_id"], "PL001")
        self.assertEqual(report["name"], "Основная линия")
        self.assertEqual(report["produced"], 75)
        self.assertEqual(report["capacity"], 100)
        self.assertEqual(report["utilization"], 75.0)
        self.assertEqual(report["available"], 25)


if __name__ == '__main__':
    unittest.main()
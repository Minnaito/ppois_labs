import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.utilities.DateUtils import DateUtils


class TestDateUtils(unittest.TestCase):
    """Тесты для утилит даты"""

    def testGetCurrentDate(self):
        date = DateUtils.getCurrentDate()
        self.assertEqual(len(date), 10)  # YYYY-MM-DD
        self.assertIn("-", date)

    def testAddDaysToDate(self):
        new_date = DateUtils.addDaysToDate("2024-01-01", 5)
        self.assertEqual(new_date, "2024-01-06")

    def testAddDaysToDateNegative(self):
        """Тест вычитания дней"""
        new_date = DateUtils.addDaysToDate("2024-01-10", -5)
        self.assertEqual(new_date, "2024-01-05")

    def testAddDaysToDateMonthBoundary(self):
        """Тест перехода через границу месяца"""
        new_date = DateUtils.addDaysToDate("2024-01-31", 1)
        self.assertEqual(new_date, "2024-02-01")

    def testAddDaysToDateYearBoundary(self):
        """Тест перехода через границу года"""
        new_date = DateUtils.addDaysToDate("2023-12-31", 1)
        self.assertEqual(new_date, "2024-01-01")

    def testAddZeroDays(self):
        """Тест добавления нуля дней"""
        new_date = DateUtils.addDaysToDate("2024-01-01", 0)
        self.assertEqual(new_date, "2024-01-01")

    def testGetCurrentDateFormats(self):
        """Тест что дата в правильном формате"""
        date = DateUtils.getCurrentDate()
        parts = date.split("-")
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[0]), 4)  # Год
        self.assertEqual(len(parts[1]), 2)  # Месяц
        self.assertEqual(len(parts[2]), 2)  # День

    def testAddDaysToInvalidDate(self):
        """Тест с невалидной датой"""
        # Должен обработать без ошибки
        result = DateUtils.addDaysToDate("invalid-date", 5)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
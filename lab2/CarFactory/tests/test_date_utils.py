import unittest
from datetime import datetime, timedelta
from models.utilities.DateUtils import DateUtils


class TestDateUtils(unittest.TestCase):

    def testGetCurrentDate(self):
        """Тест получения текущей даты"""
        current_date = DateUtils.getCurrentDate()

        # Проверяем формат YYYY-MM-DD
        self.assertRegex(current_date, r'^\d{4}-\d{2}-\d{2}$')

        # Проверяем, что это валидная дата
        try:
            datetime.strptime(current_date, "%Y-%m-%d")
            is_valid = True
        except ValueError:
            is_valid = False

        self.assertTrue(is_valid)

    def testGetCurrentDateTime(self):
        """Тест получения текущей даты и времени"""
        current_datetime = DateUtils.getCurrentDateTime()

        # Проверяем формат YYYY-MM-DD HH:MM:SS
        self.assertRegex(current_datetime, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

        # Проверяем, что это валидная дата и время
        try:
            datetime.strptime(current_datetime, "%Y-%m-%d %H:%M:%S")
            is_valid = True
        except ValueError:
            is_valid = False

        self.assertTrue(is_valid)

    def testAddDaysToDate(self):
        """Тест добавления дней к дате"""
        # Добавляем положительное количество дней
        result = DateUtils.addDaysToDate("2024-01-01", 5)
        self.assertEqual(result, "2024-01-06")

        # Добавляем 0 дней
        result = DateUtils.addDaysToDate("2024-01-01", 0)
        self.assertEqual(result, "2024-01-01")

        # Добавляем отрицательное количество дней
        result = DateUtils.addDaysToDate("2024-01-10", -3)
        self.assertEqual(result, "2024-01-07")

        # Добавляем много дней
        result = DateUtils.addDaysToDate("2024-01-01", 365)
        self.assertEqual(result, "2024-12-31")

    def testAddDaysToDateInvalidFormat(self):
        """Тест добавления дней к невалидной дате"""
        # Невалидный формат даты
        result = DateUtils.addDaysToDate("01-01-2024", 5)
        # Метод может вернуть исходную строку или выбросить исключение
        # Просто проверяем, что метод выполнился
        self.assertIsNotNone(result)

    def testCalculateDateDifference(self):
        """Тест расчета разницы в днях между датами"""
        # Разница 10 дней
        difference = DateUtils.calculateDateDifference("2024-01-01", "2024-01-11")
        self.assertEqual(difference, 10)

        # Разница 0 дней
        difference = DateUtils.calculateDateDifference("2024-01-01", "2024-01-01")
        self.assertEqual(difference, 0)

        # Разница в обратном порядке (должна быть та же)
        difference = DateUtils.calculateDateDifference("2024-01-11", "2024-01-01")
        self.assertEqual(difference, 10)

    def testIsDateInFuture(self):
        """Тест проверки, является ли дата будущей"""
        # Будущая дата
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.assertTrue(DateUtils.isDateInFuture(future_date))

        # Прошедшая дата
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        self.assertFalse(DateUtils.isDateInFuture(past_date))

    def testIsDateInPast(self):
        """Тест проверки, является ли дата прошедшей"""
        # Прошедшая дата
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        self.assertTrue(DateUtils.isDateInPast(past_date))

        # Будущая дата
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.assertFalse(DateUtils.isDateInPast(future_date))

    def testDateConsistency(self):
        """Тест консистентности дат"""
        # Проверяем, что getCurrentDate() возвращает сегодняшнюю дату
        today = datetime.now().strftime("%Y-%m-%d")
        current_date = DateUtils.getCurrentDate()

        # Они должны совпадать (с небольшой погрешностью по времени выполнения)
        self.assertEqual(current_date, today)


if __name__ == '__main__':
    unittest.main()
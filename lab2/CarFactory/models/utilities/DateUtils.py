from datetime import datetime, timedelta


class DateUtils:

    @staticmethod
    def getCurrentDate() -> str:
        """Получение текущей даты в формате YYYY-MM-DD"""
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def getCurrentDateTime() -> str:
        """Получение текущей даты и времени"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def addDaysToDate(startDate: str, daysToAdd: int) -> str:
        """Добавление дней к дате"""
        try:
            start = datetime.strptime(startDate, "%Y-%m-%d")
            newDate = start + timedelta(days=daysToAdd)
            return newDate.strftime("%Y-%m-%d")
        except ValueError:
            return startDate

    @staticmethod
    def calculateDateDifference(date1: str, date2: str) -> int:
        """Расчет разницы в днях между двумя датами"""
        try:
            d1 = datetime.strptime(date1, "%Y-%m-%d")
            d2 = datetime.strptime(date2, "%Y-%m-%d")
            return abs((d2 - d1).days)
        except ValueError:
            return 0

    @staticmethod
    def isDateInFuture(targetDate: str) -> bool:
        """Проверка, является ли дата будущей"""
        try:
            target = datetime.strptime(targetDate, "%Y-%m-%d")
            current = datetime.now()
            return target > current
        except ValueError:
            return False

    @staticmethod
    def isDateInPast(targetDate: str) -> bool:
        """Проверка, является ли дата прошедшей"""
        try:
            target = datetime.strptime(targetDate, "%Y-%m-%d")
            current = datetime.now()
            return target < current
        except ValueError:
            return False
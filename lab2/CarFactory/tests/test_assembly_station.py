import unittest
from models.production.AssemblyStation import AssemblyStation


class TestAssemblyStation(unittest.TestCase):

    def testAssemblyStationInitialization(self):
        """Тест инициализации сборочной станции"""
        station = AssemblyStation("AS001", "Роботизированная")
        self.assertEqual(station._stationIdentifier, "AS001")
        self.assertEqual(station._stationType, "Роботизированная")
        self.assertEqual(station._partsCount, 0)

    def testAddPart(self):
        """Тест добавления детали на станцию"""
        station = AssemblyStation("AS001", "Роботизированная")

        # Добавляем детали
        for i in range(5):
            result = station.addPart()
            self.assertTrue(result)

        # Проверяем количество деталей
        self.assertEqual(station._partsCount, 5)

    def testAssembleWithParts(self):
        """Тест сборки при наличии деталей"""
        station = AssemblyStation("AS001", "Роботизированная")

        # Добавляем детали
        station.addPart()
        station.addPart()

        # Пытаемся собрать
        result = station.assemble()
        self.assertTrue(result)

    def testAssembleWithoutParts(self):
        """Тест сборки без деталей"""
        station = AssemblyStation("AS001", "Роботизированная")

        # Пытаемся собрать без деталей
        result = station.assemble()
        self.assertFalse(result)

    def testMultipleAddAndAssemble(self):
        """Тест множественного добавления и сборки"""
        station = AssemblyStation("AS001", "Роботизированная")

        # Добавляем детали
        for i in range(10):
            station.addPart()

        self.assertEqual(station._partsCount, 10)

        # Собираем
        result = station.assemble()
        self.assertTrue(result)

    def testStationProperties(self):
        """Тест свойств станции"""
        station = AssemblyStation("AS001", "Конвейерная линия")

        self.assertEqual(station._stationIdentifier, "AS001")
        self.assertEqual(station._stationType, "Конвейерная линия")

        # Проверяем, что можно изменить количество деталей
        station._partsCount = 15
        self.assertEqual(station._partsCount, 15)


if __name__ == '__main__':
    unittest.main()
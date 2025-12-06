import unittest
import sys
import os

# Добавляем путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from exceptions.QualityExceptions.DefectivePartError import DefectivePartError

    DEFECTIVE_PART_ERROR_AVAILABLE = True
except ImportError:
    DEFECTIVE_PART_ERROR_AVAILABLE = False
    print("DefectivePartError не доступен для тестирования")


@unittest.skipIf(not DEFECTIVE_PART_ERROR_AVAILABLE, "DefectivePartError не доступен")
class TestDefectivePartError(unittest.TestCase):

    def testDefectivePartErrorInitialization(self):
        """Тест инициализации ошибки дефектной детали"""
        error = DefectivePartError("ENG001", "Трещина в блоке цилиндров")

        # Проверяем основные атрибуты
        self.assertTrue(hasattr(error, 'part_id') or hasattr(error, 'partId'))

        # Проверяем, что ошибка создана
        self.assertIsInstance(error, DefectivePartError)
        self.assertIsInstance(error, Exception)

    def testDefectivePartErrorStringRepresentation(self):
        """Тест строкового представления ошибки"""
        error = DefectivePartError("ENG001", "Трещина в блоке цилиндров")
        error_str = str(error)

        # Проверяем, что строка содержит информацию об ошибке
        self.assertIsInstance(error_str, str)
        self.assertGreater(len(error_str), 0)

        # Проверяем, что содержит ID детали
        self.assertIn("ENG001", error_str)

    def testDefectivePartErrorDifferentDescriptions(self):
        """Тест ошибки с разными описаниями дефектов"""
        test_cases = [
            ("PART001", "Царапина на поверхности"),
            ("PART002", "Несоответствие размеров"),
        ]

        for part_id, description in test_cases:
            error = DefectivePartError(part_id, description)
            self.assertIsInstance(error, DefectivePartError)

    def testDefectivePartErrorInheritance(self):
        """Тест наследования ошибки"""
        error = DefectivePartError("ENG001", "Трещина")

        # Проверяем, что это исключение
        self.assertIsInstance(error, Exception)

    def testDefectivePartErrorRaising(self):
        """Тест выбрасывания исключения"""
        with self.assertRaises(DefectivePartError) as context:
            raise DefectivePartError("TEST001", "Тестовый дефект")

        exception = context.exception
        self.assertIsInstance(exception, DefectivePartError)

    def testDefectivePartErrorInTryExcept(self):
        """Тест обработки исключения в try-except блоке"""
        try:
            raise DefectivePartError("TRY001", "Дефект для теста обработки")
        except DefectivePartError as e:
            # Успешно поймали ожидаемое исключение
            self.assertIsInstance(e, DefectivePartError)
        except Exception:
            self.fail("Неожиданный тип исключения")


if __name__ == '__main__':
    unittest.main()
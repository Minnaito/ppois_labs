# tests/test_main.py
import unittest
import sys
import os
import tempfile
import shutil
from datetime import datetime
import re

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import CadastralMenu
from constants import Constants


class TestCadastralMenuBasic(unittest.TestCase):
    """Базовые тесты для класса CadastralMenu без использования mock"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        # Создаем временную директорию для данных
        self.temp_dir = tempfile.mkdtemp()

        # Патчим os.makedirs вручную через замену атрибута
        self.original_makedirs = os.makedirs
        self.makedirs_called = False
        self.makedirs_args = None

        def fake_makedirs(path, exist_ok=False):
            self.makedirs_called = True
            self.makedirs_args = (path, exist_ok)
            # Создаем реальную директорию для тестов
            self.original_makedirs(path, exist_ok=exist_ok)

        os.makedirs = fake_makedirs

        # Создаем экземпляр меню
        self.menu = CadastralMenu()

    def tearDown(self):
        """Очистка после каждого теста"""
        # Восстанавливаем оригинальную функцию
        os.makedirs = self.original_makedirs
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_creates_data_directory(self):
        """Тест создания директории при инициализации"""
        self.assertTrue(self.makedirs_called)
        self.assertEqual(self.makedirs_args[0], "./data")
        self.assertTrue(self.makedirs_args[1])

    def test_init_sets_up_dictionaries(self):
        """Тест инициализации словарей выбора"""
        self.assertEqual(len(self.menu.organs), 4)
        self.assertEqual(len(self.menu.right_types), 3)
        self.assertEqual(len(self.menu.building_purposes), 2)
        self.assertEqual(len(self.menu.land_categories), 4)
        self.assertEqual(len(self.menu.permitted_uses), 4)
        self.assertEqual(len(self.menu.fire_classes), 4)
        self.assertEqual(len(self.menu.energy_classes), 5)
        self.assertEqual(len(self.menu.land_states), 4)

    def test_validate_date_valid(self):
        """Тест _validate_date с валидными датами"""
        self.assertTrue(self.menu._validate_date("01.01.2023"))
        self.assertTrue(self.menu._validate_date("31.12.2023"))
        self.assertTrue(self.menu._validate_date("15.06.2020"))

    def test_validate_date_invalid(self):
        """Тест _validate_date с невалидными датами"""
        self.assertFalse(self.menu._validate_date("32.01.2023"))
        self.assertFalse(self.menu._validate_date("01.13.2023"))
        self.assertFalse(self.menu._validate_date("01.01.1800"))
        self.assertFalse(self.menu._validate_date("abc"))
        self.assertFalse(self.menu._validate_date(""))

    def test_format_date_iso(self):
        """Тест форматирования ISO даты"""
        result = self.menu._format_date("2023-01-15T10:30:00")
        self.assertEqual(result, "15.01.2023")

    def test_format_date_dmy(self):
        """Тест форматирования даты в формате ДД.ММ.ГГГГ"""
        result = self.menu._format_date("15.01.2023")
        self.assertEqual(result, "15.01.2023")

    def test_format_date_ymd(self):
        """Тест форматирования даты в формате ГГГГ-ММ-ДД"""
        result = self.menu._format_date("2023-01-15")
        self.assertEqual(result, "15.01.2023")

    def test_format_date_invalid(self):
        """Тест форматирования невалидной даты"""
        result = self.menu._format_date("invalid")
        self.assertEqual(result, "invalid")

    def test_format_date_none(self):
        """Тест форматирования None - исправлено"""
        result = self.menu._format_date(None)
        self.assertEqual(result, None)  # Метод возвращает None для None

    def test_get_iznos_level(self):
        """Тест определения уровня износа"""
        self.assertEqual(self.menu._get_iznos_level(5), "Отличное")
        self.assertEqual(self.menu._get_iznos_level(15), "Хорошее")
        self.assertEqual(self.menu._get_iznos_level(35), "Удовлетворительное")
        self.assertEqual(self.menu._get_iznos_level(55), "Неудовлетворительное")
        self.assertEqual(self.menu._get_iznos_level(75), "Аварийное")

    def test_print_header_exists(self):
        """Тест наличия метода print_header"""
        self.assertTrue(hasattr(self.menu, 'print_header'))
        self.assertTrue(callable(self.menu.print_header))

    def test_print_menu_exists(self):
        """Тест наличия метода print_menu"""
        self.assertTrue(hasattr(self.menu, 'print_menu'))
        self.assertTrue(callable(self.menu.print_menu))

    def test_run_exists(self):
        """Тест наличия метода run"""
        self.assertTrue(hasattr(self.menu, 'run'))
        self.assertTrue(callable(self.menu.run))

    def test_issue_cadastral_number_exists(self):
        """Тест наличия метода issue_cadastral_number"""
        self.assertTrue(hasattr(self.menu, 'issue_cadastral_number'))
        self.assertTrue(callable(self.menu.issue_cadastral_number))

    def test_update_docs_exists(self):
        """Тест наличия метода update_docs"""
        self.assertTrue(hasattr(self.menu, 'update_docs'))
        self.assertTrue(callable(self.menu.update_docs))

    def test_get_info_exists(self):
        """Тест наличия метода get_info"""
        self.assertTrue(hasattr(self.menu, 'get_info'))
        self.assertTrue(callable(self.menu.get_info))

    def test_list_objects_exists(self):
        """Тест наличия метода list_objects"""
        self.assertTrue(hasattr(self.menu, 'list_objects'))
        self.assertTrue(callable(self.menu.list_objects))

    def test_exit_program_exists(self):
        """Тест наличия метода exit_program"""
        self.assertTrue(hasattr(self.menu, 'exit_program'))
        self.assertTrue(callable(self.menu.exit_program))

    def test_input_required_exists(self):
        """Тест наличия метода _input_required"""
        self.assertTrue(hasattr(self.menu, '_input_required'))
        self.assertTrue(callable(self.menu._input_required))

    def test_input_positive_number_exists(self):
        """Тест наличия метода _input_positive_number"""
        self.assertTrue(hasattr(self.menu, '_input_positive_number'))
        self.assertTrue(callable(self.menu._input_positive_number))

    def test_input_integer_exists(self):
        """Тест наличия метода _input_integer"""
        self.assertTrue(hasattr(self.menu, '_input_integer'))
        self.assertTrue(callable(self.menu._input_integer))

    def test_input_date_exists(self):
        """Тест наличия метода _input_date"""
        self.assertTrue(hasattr(self.menu, '_input_date'))
        self.assertTrue(callable(self.menu._input_date))

    def test_get_choice_exists(self):
        """Тест наличия метода _get_choice"""
        self.assertTrue(hasattr(self.menu, '_get_choice'))
        self.assertTrue(callable(self.menu._get_choice))

    def test_input_object_uid_exists(self):
        """Тест наличия метода _input_object_uid"""
        self.assertTrue(hasattr(self.menu, '_input_object_uid'))
        self.assertTrue(callable(self.menu._input_object_uid))

    def test_input_owner_uid_exists(self):
        """Тест наличия метода _input_owner_uid"""
        self.assertTrue(hasattr(self.menu, '_input_owner_uid'))
        self.assertTrue(callable(self.menu._input_owner_uid))

    def test_show_objects_short_exists(self):
        """Тест наличия метода _show_objects_short"""
        self.assertTrue(hasattr(self.menu, '_show_objects_short'))
        self.assertTrue(callable(self.menu._show_objects_short))

    def test_show_owners_short_exists(self):
        """Тест наличия метода _show_owners_short"""
        self.assertTrue(hasattr(self.menu, '_show_owners_short'))
        self.assertTrue(callable(self.menu._show_owners_short))

    def test_input_building_params_exists(self):
        """Тест наличия метода _input_building_params"""
        self.assertTrue(hasattr(self.menu, '_input_building_params'))
        self.assertTrue(callable(self.menu._input_building_params))

    def test_input_land_params_exists(self):
        """Тест наличия метода _input_land_params"""
        self.assertTrue(hasattr(self.menu, '_input_land_params'))
        self.assertTrue(callable(self.menu._input_land_params))


if __name__ == '__main__':
    unittest.main()
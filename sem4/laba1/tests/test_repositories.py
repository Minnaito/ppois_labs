# tests/test_repositories.py
import unittest
import tempfile
import shutil
import os
import json
from datetime import datetime

# Добавляем путь к проекту
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exceptions.exceptions import NotFoundError
from models.zdanie import zdanie
from models.zemelnyj_uchastok import zemelnyj_uchastok
from models.vladeshec import vladeshec
from models.pravo_ustanavlivayushchij_dokument import pravo_ustanavlivayushchij_dokument
from models.kadastrovyj_nomer import kadastrovyj_nomer
from services.object_repository import object_repository
from services.owner_repository import owner_repository
from services.right_document_repository import right_document_repository
from services.cadastral_number_repository import cadastral_number_repository
from services.base_repository import base_repository
from constants import Constants


class TestBaseRepositoryDetailed(unittest.TestCase):
    """Детальное тестирование базового репозитория"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(self.temp_dir, "test.json")

        class SimpleModel:
            def __init__(self, name, value, uid=None):
                self._name = name
                self._value = value
                self._uid = uid or str(hash(name))

            @property
            def uid(self):
                return self._uid

            @property
            def name(self):
                return self._name

            @property
            def value(self):
                return self._value

        self.model_class = SimpleModel

        # Создаем простой репозиторий для тестов
        class SimpleRepo(base_repository):
            def _to_dict(self, obj):
                return {'name': obj.name, 'value': obj.value, 'uid': obj.uid}

            def _from_dict(self, data):
                return self.cls(data.get('name'), data.get('value'), uid=data.get('uid'))

        self.repo = SimpleRepo(self.file_path, self.model_class)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_load_non_existent_file(self):
        """Тест загрузки из несуществующего файла"""
        # Должно создаться пустое хранилище без ошибок
        self.assertEqual(len(self.repo._items), 0)

    def test_add_and_get(self):
        """Тест добавления и получения"""
        obj = self.model_class("test", 123)
        self.repo.add(obj)

        retrieved = self.repo.get(obj.uid)
        self.assertEqual(retrieved.uid, obj.uid)
        self.assertEqual(retrieved.name, obj.name)

    def test_get_not_found(self):
        """Тест получения несуществующего объекта"""
        with self.assertRaises(NotFoundError):
            self.repo.get("non-existent")

    def test_update(self):
        """Тест обновления"""
        obj = self.model_class("original", 123)
        self.repo.add(obj)

        # Создаем обновленный объект с тем же UID
        updated_obj = self.model_class("updated", 456, uid=obj.uid)
        self.repo.update(updated_obj)

        retrieved = self.repo.get(obj.uid)
        self.assertEqual(retrieved.name, "updated")
        self.assertEqual(retrieved.value, 456)

    def test_update_not_found(self):
        """Тест обновления несуществующего объекта"""
        obj = self.model_class("test", 123, uid="nonexistent")
        with self.assertRaises(NotFoundError):
            self.repo.update(obj)

    def test_delete(self):
        """Тест удаления"""
        obj = self.model_class("test", 123)
        self.repo.add(obj)
        self.repo.delete(obj.uid)

        with self.assertRaises(NotFoundError):
            self.repo.get(obj.uid)

    def test_list_all(self):
        """Тест списка всех объектов"""
        obj1 = self.model_class("test1", 1)
        obj2 = self.model_class("test2", 2)

        self.repo.add(obj1)
        self.repo.add(obj2)

        all_objs = self.repo.list_all()
        self.assertEqual(len(all_objs), 2)


class TestObjectRepositoryDetailed(unittest.TestCase):
    """Детальное тестирование репозитория объектов"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = object_repository(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_zdanie(self):
        """Тест добавления здания"""
        building = zdanie(
            adres="Test address",
            ploshchad=150.5,
            kolichestvo_etazhej=3,
            material_sten="бетон",
            naznachenie="nezhiloe",
            god_postrojki=2010
        )

        self.repo.add(building)

        # Проверяем, что объект добавился
        self.assertEqual(len(self.repo._items), 1)

        # Получаем объект из репозитория
        loaded = self.repo.get(building.uid)
        self.assertEqual(loaded.adres, building.adres)
        self.assertEqual(loaded.ploshchad, building.ploshchad)

    def test_add_land(self):
        """Тест добавления участка"""
        land = zemelnyj_uchastok(
            adres="Land address",
            ploshchad=1000.0,
            kategoriya_zemel="Сельхоз",
            vid_razreshonnogo_ispolzovaniya="ИЖС"
        )

        self.repo.add(land)

        loaded = self.repo.get(land.uid)
        self.assertEqual(loaded.adres, land.adres)
        self.assertEqual(loaded.ploshchad, land.ploshchad)

    def test_update_object(self):
        """Тест обновления объекта"""
        building = zdanie(
            adres="Original",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )

        self.repo.add(building)

        # Обновляем через прямое изменение и сохранение
        building.adres = "Updated"
        building.ploshchad = 200
        self.repo.update(building)

        loaded = self.repo.get(building.uid)
        self.assertEqual(loaded.adres, "Updated")
        self.assertEqual(loaded.ploshchad, 200)

    def test_delete_object(self):
        """Тест удаления объекта"""
        building = zdanie(
            adres="Test",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )

        self.repo.add(building)
        self.assertEqual(len(self.repo.list_all()), 1)

        self.repo.delete(building.uid)
        self.assertEqual(len(self.repo.list_all()), 0)

        with self.assertRaises(NotFoundError):
            self.repo.get(building.uid)

    def test_list_all_empty(self):
        """Тест списка всех объектов для пустого репозитория"""
        self.assertEqual(len(self.repo.list_all()), 0)

    def test_list_all_multiple(self):
        """Тест списка всех объектов с несколькими объектами"""
        building = zdanie(
            adres="Test1",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )

        land = zemelnyj_uchastok(
            adres="Land",
            ploshchad=1000,
            kategoriya_zemel="Сельхоз",
            vid_razreshonnogo_ispolzovaniya="ИЖС"
        )

        self.repo.add(building)
        self.repo.add(land)

        all_objs = self.repo.list_all()
        self.assertEqual(len(all_objs), 2)


class TestOwnerRepositoryDetailed(unittest.TestCase):
    """Детальное тестирование репозитория владельцев"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = owner_repository(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_owner(self):
        """Тест добавления владельца"""
        owner = vladeshec(
            identificator="1234567890",
            fio="Иванов Иван Иванович",
            rekvizity_svyazi="ivan@mail.ru"
        )

        self.repo.add(owner)

        loaded = self.repo.get(owner.uid)
        self.assertEqual(loaded.identificator, owner.identificator)
        self.assertEqual(loaded.fio, owner.fio)

    def test_add_multiple_owners(self):
        """Тест добавления нескольких владельцев"""
        owner1 = vladeshec("111", "Иванов И.И.", "ivan@mail.ru")
        owner2 = vladeshec("222", "Петров П.П.", "petr@mail.ru")

        self.repo.add(owner1)
        self.repo.add(owner2)

        all_owners = self.repo.list_all()
        self.assertEqual(len(all_owners), 2)

    def test_update_owner(self):
        """Тест обновления владельца"""
        owner = vladeshec("123", "Иванов И.И.", "ivan@mail.ru")
        self.repo.add(owner)

        owner.fio = "Иванов Петр Иванович"
        self.repo.update(owner)

        loaded = self.repo.get(owner.uid)
        self.assertEqual(loaded.fio, "Иванов Петр Иванович")

    def test_delete_owner(self):
        """Тест удаления владельца"""
        owner = vladeshec("123", "Иванов И.И.", "ivan@mail.ru")
        self.repo.add(owner)
        self.assertEqual(len(self.repo.list_all()), 1)

        self.repo.delete(owner.uid)
        self.assertEqual(len(self.repo.list_all()), 0)


class TestRightDocumentRepositoryDetailed(unittest.TestCase):
    """Детальное тестирование репозитория правоустанавливающих документов"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = right_document_repository(self.temp_dir)

        # Создаем связанные объекты
        self.owner1 = vladeshec("111", "Иванов И.И.", "ivan@mail.ru")
        self.owner2 = vladeshec("222", "Петров П.П.", "petr@mail.ru")

        self.building = zdanie(
            adres="Test",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )

        # Создаем документ
        self.doc = pravo_ustanavlivayushchij_dokument(
            tip_prava="sobstvennost",
            dolya_v_prave=0.5,
            svyazannyj_objekt=self.building,
            spisok_vladelcev=[self.owner1, self.owner2],
            nomer_dokumenta="DOC-001",
            data_vydachi="01.01.2023",
            organ_vydachi="Росреестр"
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_document(self):
        """Тест добавления документа"""
        self.repo.add(self.doc)

        loaded = self.repo.get(self.doc.uid)
        self.assertEqual(loaded.tip_prava, self.doc.tip_prava)
        self.assertEqual(loaded.dolya_v_prave, self.doc.dolya_v_prave)
        self.assertEqual(loaded.nomer_dokumenta, self.doc.nomer_dokumenta)

    def test_add_multiple_documents(self):
        """Тест добавления нескольких документов"""
        doc2 = pravo_ustanavlivayushchij_dokument(
            tip_prava="arenda",
            dolya_v_prave=1.0,
            svyazannyj_objekt=self.building,
            spisok_vladelcev=[self.owner1],
            nomer_dokumenta="DOC-002",
            data_vydachi="01.02.2023",
            organ_vydachi="Нотариус"
        )

        self.repo.add(self.doc)
        self.repo.add(doc2)

        all_docs = self.repo.list_all()
        self.assertEqual(len(all_docs), 2)

    def test_update_document(self):
        """Тест обновления документа"""
        self.repo.add(self.doc)

        self.doc.tip_prava = "arenda"
        self.doc.dolya_v_prave = 1.0
        self.repo.update(self.doc)

        loaded = self.repo.get(self.doc.uid)
        self.assertEqual(loaded.tip_prava, "arenda")
        self.assertEqual(loaded.dolya_v_prave, 1.0)

    def test_delete_document(self):
        """Тест удаления документа"""
        self.repo.add(self.doc)
        self.assertEqual(len(self.repo.list_all()), 1)

        self.repo.delete(self.doc.uid)
        self.assertEqual(len(self.repo.list_all()), 0)


class TestCadastralNumberRepositoryDetailed(unittest.TestCase):
    """Детальное тестирование репозитория кадастровых номеров"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = cadastral_number_repository(self.temp_dir)

        self.building = zdanie(
            adres="Test",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )

        self.cad_number1 = kadastrovyj_nomer(
            nomer_kvartala="000123",
            unikalnyj_nomer_v_kvartale="001",
            status_nomera="aktivnyy",
            vladeshec_nomera=self.building
        )

        self.cad_number2 = kadastrovyj_nomer(
            nomer_kvartala="000123",
            unikalnyj_nomer_v_kvartale="002",
            status_nomera="zarezervirovannyy"
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_cadastral_number(self):
        """Тест добавления кадастрового номера"""
        self.repo.add(self.cad_number1)

        loaded = self.repo.get(self.cad_number1.uid)
        self.assertEqual(loaded.nomer_kvartala, self.cad_number1.nomer_kvartala)
        self.assertEqual(loaded.unikalnyj_nomer_v_kvartale, self.cad_number1.unikalnyj_nomer_v_kvartale)
        self.assertEqual(loaded.status_nomera, self.cad_number1.status_nomera)

    def test_add_multiple_numbers(self):
        """Тест добавления нескольких номеров"""
        self.repo.add(self.cad_number1)
        self.repo.add(self.cad_number2)

        all_numbers = self.repo.list_all()
        self.assertEqual(len(all_numbers), 2)

    def test_delete_cadastral_number(self):
        """Тест удаления кадастрового номера"""
        self.repo.add(self.cad_number1)
        self.assertEqual(len(self.repo.list_all()), 1)

        self.repo.delete(self.cad_number1.uid)
        self.assertEqual(len(self.repo.list_all()), 0)


def run_repository_tests():
    """Запуск всех тестов репозиториев"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestBaseRepositoryDetailed))
    suite.addTests(loader.loadTestsFromTestCase(TestObjectRepositoryDetailed))
    suite.addTests(loader.loadTestsFromTestCase(TestOwnerRepositoryDetailed))
    suite.addTests(loader.loadTestsFromTestCase(TestRightDocumentRepositoryDetailed))
    suite.addTests(loader.loadTestsFromTestCase(TestCadastralNumberRepositoryDetailed))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    run_repository_tests()
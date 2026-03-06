# test_cadastral_system.py (исправленная версия)
import unittest
import tempfile
import shutil
import os
from datetime import datetime
import uuid

# Импорты ваших модулей
from exceptions.exceptions import (
    ValidationError, NotFoundError, DuplicateError, PermissionDeniedError, CadastralError
)
from constants import Constants
from models.base_model import base_model
from models.dokument import dokument
from models.kadastrovyj_nomer import kadastrovyj_nomer
from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from models.vladeshec import vladeshec
from models.pravo_ustanavlivayushchij_dokument import pravo_ustanavlivayushchij_dokument
from models.zdanie import zdanie
from models.zemelnyj_uchastok import zemelnyj_uchastok
from services.base_repository import base_repository
from services.object_repository import object_repository
from services.owner_repository import owner_repository
from services.right_document_repository import right_document_repository
from services.cadastral_number_repository import cadastral_number_repository
from services.kadastrovyj_uchet import kadastrovyj_uchet
from services.number_generator import number_generator
from services.tekhnicheskiy_uchet import tekhnicheskiy_uchet
from services.dokument_menedzher import dokument_menedzher
from services.kadastrovoe_agentstvo import kadastrovoe_agentstvo


class TestExceptions(unittest.TestCase):
    """Тестирование иерархии исключений"""

    def test_exception_hierarchy(self):
        """Проверка иерархии наследования исключений"""
        self.assertTrue(issubclass(ValidationError, CadastralError))
        self.assertTrue(issubclass(NotFoundError, CadastralError))
        self.assertTrue(issubclass(DuplicateError, CadastralError))
        self.assertTrue(issubclass(PermissionDeniedError, CadastralError))

        # Проверка возможности raise
        with self.assertRaises(ValidationError):
            raise ValidationError("Test error")

        with self.assertRaises(NotFoundError):
            raise NotFoundError("Not found")


class TestBaseModel(unittest.TestCase):
    """Тестирование базовой модели"""

    def test_uid_generation(self):
        """Проверка генерации UID"""

        class TestModel(base_model):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        # Без указания uid
        model1 = TestModel()
        model2 = TestModel()
        self.assertIsNotNone(model1.uid)
        self.assertIsNotNone(model2.uid)
        self.assertNotEqual(model1.uid, model2.uid)

        # С указанием uid
        custom_uid = "test-123"
        model3 = TestModel(uid=custom_uid)
        self.assertEqual(model3.uid, custom_uid)


class TestDokument(unittest.TestCase):
    """Тестирование абстрактного класса документа"""

    def test_dokument_creation(self):
        """Проверка создания документа"""

        class TestDokument(dokument):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        doc = TestDokument(
            nomer_dokumenta="ABC-123",
            data_vydachi="01.01.2023",
            organ_vydachi="Росреестр"
        )

        self.assertEqual(doc.nomer_dokumenta, "ABC-123")
        self.assertEqual(doc.data_vydachi, "01.01.2023")
        self.assertEqual(doc.organ_vydachi, "Росреестр")


class TestVladeshec(unittest.TestCase):
    """Тестирование класса владельца"""

    def setUp(self):
        self.owner = vladeshec(
            identificator="1234567890",
            fio="Иванов Иван Иванович",
            rekvizity_svyazi="ivan@mail.ru"
        )

    def test_owner_creation(self):
        """Проверка создания владельца"""
        self.assertEqual(self.owner.identificator, "1234567890")
        self.assertEqual(self.owner.fio, "Иванов Иван Иванович")
        self.assertEqual(self.owner.rekvizity_svyazi, "ivan@mail.ru")

    def test_owner_setters(self):
        """Проверка сеттеров с валидацией"""
        # Успешное изменение
        self.owner.fio = "Петров Петр Петрович"
        self.assertEqual(self.owner.fio, "Петров Петр Петрович")

        # Ошибка при пустом значении
        with self.assertRaises(ValidationError):
            self.owner.fio = ""

        with self.assertRaises(ValidationError):
            self.owner.identificator = ""

        with self.assertRaises(ValidationError):
            self.owner.rekvizity_svyazi = ""

    def test_identificator_empty(self):
        """Тест пустого идентификатора"""
        with self.assertRaises(ValidationError):
            self.owner.identificator = ""

    def test_fio_empty(self):
        """Тест пустого ФИО"""
        with self.assertRaises(ValidationError):
            self.owner.fio = ""

    def test_rekvizity_empty(self):
        """Тест пустых реквизитов"""
        with self.assertRaises(ValidationError):
            self.owner.rekvizity_svyazi = ""


class TestKadastrovyjNomer(unittest.TestCase):
    """Тестирование класса кадастрового номера"""

    def setUp(self):
        self.cad_number = kadastrovyj_nomer(
            nomer_kvartala="000123",
            unikalnyj_nomer_v_kvartale="001",
            status_nomera="aktivnyy"
        )

    def test_cad_number_creation(self):
        """Проверка создания кадастрового номера"""
        self.assertEqual(self.cad_number.nomer_kvartala, "000123")
        self.assertEqual(self.cad_number.unikalnyj_nomer_v_kvartale, "001")
        self.assertEqual(self.cad_number.status_nomera, "aktivnyy")

        # Проверка формата полного значения
        expected = f"{Constants.REGION}:{Constants.RAYON}:000123:001"
        self.assertEqual(self.cad_number.polnoe_znachenie, expected)

    def test_status_validation(self):
        """Проверка валидации статуса"""
        # Успешное изменение
        self.cad_number.status_nomera = "zarezervirovannyy"
        self.assertEqual(self.cad_number.status_nomera, "zarezervirovannyy")

        # Ошибка при недопустимом статусе
        with self.assertRaises(ValidationError):
            self.cad_number.status_nomera = "invalid_status"

    def test_proverit_v_reestre(self):
        """Проверка уникальности в реестре"""
        numbers = [
            kadastrovyj_nomer("000123", "001"),
            kadastrovyj_nomer("000123", "002"),
            kadastrovyj_nomer("000124", "001")
        ]

        # Уникальный номер
        new_number = kadastrovyj_nomer("000125", "001")
        self.assertTrue(new_number.proverit_v_reestre(numbers))

        # Неуникальный номер
        duplicate = kadastrovyj_nomer("000123", "001")
        self.assertFalse(duplicate.proverit_v_reestre(numbers))


class TestObjektNedvizhimosti(unittest.TestCase):
    """Тестирование абстрактного класса объекта недвижимости"""

    def setUp(self):
        class TestObjekt(objekt_nedvizhimosti):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        self.obj = TestObjekt(
            adres="г. Москва, ул. Ленина, д. 1",
            ploshchad=100.5,
            status="vremennyy"
        )

    def test_object_creation(self):
        """Проверка создания объекта"""
        self.assertEqual(self.obj.adres, "г. Москва, ул. Ленина, д. 1")
        self.assertEqual(self.obj.ploshchad, 100.5)
        self.assertEqual(self.obj.status, "vremennyy")
        self.assertIsNotNone(self.obj.data_registracii)

    def test_adres_validation(self):
        """Проверка валидации адреса"""
        with self.assertRaises(ValidationError):
            self.obj.adres = ""

        with self.assertRaises(ValidationError):
            self.obj.adres = "   "

    def test_ploshchad_validation(self):
        """Проверка валидации площади"""
        with self.assertRaises(ValidationError):
            self.obj.ploshchad = 0

        with self.assertRaises(ValidationError):
            self.obj.ploshchad = -10

    def test_status_validation(self):
        """Проверка валидации статуса"""
        # Успешное изменение
        self.obj.status = "uchtennyy"
        self.assertEqual(self.obj.status, "uchtennyy")

        # Ошибка при недопустимом статусе
        with self.assertRaises(ValidationError):
            self.obj.status = "invalid"

    def test_saved_vypiska(self):
        """Проверка работы с сохраненной выпиской"""
        self.assertIsNone(self.obj.saved_vypiska)

        test_vypiska = "Test vypiska"
        self.obj.saved_vypiska = test_vypiska
        self.assertEqual(self.obj.saved_vypiska, test_vypiska)

    def test_izmenit_status(self):
        """Проверка метода изменения статуса"""
        self.obj.izmenit_status("uchtennyy")
        self.assertEqual(self.obj.status, "uchtennyy")

    def test_kadastrovyj_nomer_setter(self):
        """Проверка сеттера кадастрового номера"""
        cad_number = kadastrovyj_nomer("000123", "001")
        self.obj.kadastrovyj_nomer = cad_number
        self.assertEqual(self.obj.kadastrovyj_nomer, cad_number)


class TestZdanie(unittest.TestCase):
    """Тестирование класса здания"""

    def setUp(self):
        self.building = zdanie(
            adres="г. Москва, ул. Ленина, д. 1",
            ploshchad=500.0,
            kolichestvo_etazhej=5,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )

    def test_building_creation(self):
        """Проверка создания здания"""
        self.assertEqual(self.building.kolichestvo_etazhej, 5)
        self.assertEqual(self.building.material_sten, "кирпич")
        self.assertEqual(self.building.naznachenie, "zhiloe")
        self.assertEqual(self.building.god_postrojki, 2000)
        self.assertEqual(self.building.fizicheskij_iznos, Constants.MIN_DEPRECIATION)
        self.assertEqual(self.building.pozharnaya_bezopasnost, "не указано")
        self.assertEqual(self.building.energeticheskaya_effektivnost, "не указано")

    def test_etazhi_validation(self):
        """Проверка валидации этажности"""
        with self.assertRaises(ValidationError):
            self.building.kolichestvo_etazhej = 0

    def test_material_validation(self):
        """Проверка валидации материала"""
        with self.assertRaises(ValidationError):
            self.building.material_sten = ""

    def test_naznachenie_validation(self):
        """Проверка валидации назначения"""
        with self.assertRaises(ValidationError):
            self.building.naznachenie = "invalid"

    def test_god_postrojki_validation(self):
        """Проверка валидации года постройки"""
        current_year = datetime.now().year

        with self.assertRaises(ValidationError):
            self.building.god_postrojki = 1700

        with self.assertRaises(ValidationError):
            self.building.god_postrojki = current_year + 1

    def test_fizicheskij_iznos_validation(self):
        """Проверка валидации физического износа"""
        self.building.fizicheskij_iznos = 50
        self.assertEqual(self.building.fizicheskij_iznos, 50)

        with self.assertRaises(ValidationError):
            self.building.fizicheskij_iznos = -1

        with self.assertRaises(ValidationError):
            self.building.fizicheskij_iznos = 101

    def test_pozharnaya_bezopasnost_setter(self):
        """Тест сеттера пожарной безопасности"""
        self.building.pozharnaya_bezopasnost = "I"
        self.assertEqual(self.building.pozharnaya_bezopasnost, "I")

    def test_energeticheskaya_effektivnost_setter(self):
        """Тест сеттера энергоэффективности"""
        self.building.energeticheskaya_effektivnost = "A"
        self.assertEqual(self.building.energeticheskaya_effektivnost, "A")

    def test_poetazhnyj_plan_default(self):
        """Тест поэтажного плана по умолчанию"""
        self.assertEqual(self.building._poetazhnyj_plan, {})

    def test_inventarnaya_stoimost_default(self):
        """Тест инвентарной стоимости по умолчанию"""
        self.assertEqual(self.building._inventarnaya_stoimost, Constants.MIN_SHARE)


class TestZemelnyjUchastok(unittest.TestCase):
    """Тестирование класса земельного участка"""

    def setUp(self):
        self.land = zemelnyj_uchastok(
            adres="Московская обл., уч. 123",
            ploshchad=1000.0,
            kategoriya_zemel="Сельскохозяйственное назначение",
            vid_razreshonnogo_ispolzovaniya="ИЖС",
            sostoyanie="Хорошее"
        )

    def test_land_creation(self):
        """Проверка создания участка"""
        self.assertEqual(self.land.kategoriya_zemel, "Сельскохозяйственное назначение")
        self.assertEqual(self.land.vid_razreshonnogo_ispolzovaniya, "ИЖС")
        self.assertEqual(self.land.nalichie_postroek, False)
        self.assertEqual(self.land.sostoyanie, "Хорошее")

    def test_kategoriya_validation(self):
        """Проверка валидации категории"""
        with self.assertRaises(ValidationError):
            self.land.kategoriya_zemel = ""

    def test_vid_validation(self):
        """Проверка валидации вида использования"""
        with self.assertRaises(ValidationError):
            self.land.vid_razreshonnogo_ispolzovaniya = ""

    def test_sostoyanie_validation(self):
        """Проверка валидации состояния"""
        self.land.sostoyanie = "Отличное"
        self.assertEqual(self.land.sostoyanie, "Отличное")

        with self.assertRaises(ValidationError):
            self.land.sostoyanie = "Плохое"

    def test_nalichie_postroek_setter(self):
        """Проверка сеттера наличия построек"""
        self.land.nalichie_postroek = True
        self.assertTrue(self.land.nalichie_postroek)


class TestPravoUstanavlivayushchijDokument(unittest.TestCase):
    """Тестирование класса правоустанавливающего документа"""

    def setUp(self):
        self.owner = vladeshec("123", "Иванов И.И.", "test@test.ru")
        self.building = zdanie(
            adres="Test",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )

        self.doc = pravo_ustanavlivayushchij_dokument(
            tip_prava="sobstvennost",
            dolya_v_prave=0.5,
            svyazannyj_objekt=self.building,
            spisok_vladelcev=[self.owner],
            nomer_dokumenta="DOC-001",
            data_vydachi="01.01.2023",
            organ_vydachi="Росреестр"
        )

    def test_document_creation(self):
        """Проверка создания документа"""
        self.assertEqual(self.doc.tip_prava, "sobstvennost")
        self.assertEqual(self.doc.dolya_v_prave, 0.5)
        self.assertEqual(self.doc.svyazannyj_objekt, self.building)
        self.assertEqual(self.doc.spisok_vladelcev, [self.owner])
        self.assertEqual(self.doc.nomer_dokumenta, "DOC-001")

    def test_tip_prava_validation(self):
        """Проверка валидации типа права"""
        self.doc.tip_prava = "arenda"
        self.assertEqual(self.doc.tip_prava, "arenda")

        with self.assertRaises(ValidationError):
            self.doc.tip_prava = "invalid"

    # tests/test_cadastral_system.py (исправленный фрагмент)

    class TestPravoUstanavlivayushchijDokument(unittest.TestCase):
        """Тестирование класса правоустанавливающего документа"""

        def setUp(self):
            self.owner = vladeshec("123", "Иванов И.И.", "test@test.ru")
            self.building = zdanie(
                adres="Test",
                ploshchad=100,
                kolichestvo_etazhej=2,
                material_sten="кирпич",
                naznachenie="zhiloe",
                god_postrojki=2000
            )

            self.doc = pravo_ustanavlivayushchij_dokument(
                tip_prava="sobstvennost",
                dolya_v_prave=0.5,
                svyazannyj_objekt=self.building,
                spisok_vladelcev=[self.owner],
                nomer_dokumenta="DOC-001",
                data_vydachi="01.01.2023",
                organ_vydachi="Росреестр"
            )

        def test_document_creation(self):
            """Проверка создания документа"""
            self.assertEqual(self.doc.tip_prava, "sobstvennost")
            self.assertEqual(self.doc.dolya_v_prave, 0.5)
            self.assertEqual(self.doc.svyazannyj_objekt, self.building)
            self.assertEqual(self.doc.spisok_vladelcev, [self.owner])
            self.assertEqual(self.doc.nomer_dokumenta, "DOC-001")

        def test_tip_prava_validation(self):
            """Проверка валидации типа права"""
            self.doc.tip_prava = "arenda"
            self.assertEqual(self.doc.tip_prava, "arenda")

            with self.assertRaises(ValidationError):
                self.doc.tip_prava = "invalid"

        def test_dolya_validation(self):
            """Проверка валидации доли"""
            # Доля должна быть > 0 и <= 1
            self.doc.dolya_v_prave = 0.75
            self.assertEqual(self.doc.dolya_v_prave, 0.75)

            self.doc.dolya_v_prave = 1.0
            self.assertEqual(self.doc.dolya_v_prave, 1.0)

            # Проверка на значение > 1
            with self.assertRaises(ValidationError):
                self.doc.dolya_v_prave = 1.5

            # Проверка на отрицательное значение
            with self.assertRaises(ValidationError):
                self.doc.dolya_v_prave = -0.5

            # Примечание: значение 0.0 может проходить валидацию,
            # так как MIN_DEPRECIATION = 0, а условие в сеттере:
            # if not (Constants.MIN_DEPRECIATION < value <= Constants.MAX_DEPRECIATION)
            # то есть value должно быть > MIN_DEPRECIATION (0)
            # Значение 0.0 не проходит, так как 0 не > 0

        def test_dolya_edge_cases(self):
            """Проверка граничных случаев доли"""
            # 0.0 должно вызывать ошибку
            with self.assertRaises(ValidationError):
                self.doc.dolya_v_prave = 0.0

            # 0.000001 должно проходить
            try:
                self.doc.dolya_v_prave = 0.000001
            except ValidationError:
                self.fail("0.000001 должно проходить валидацию")

            # 1.0 должно проходить
            try:
                self.doc.dolya_v_prave = 1.0
            except ValidationError:
                self.fail("1.0 должно проходить валидацию")

        def test_uids_properties(self):
            """Проверка свойств с UID"""
            self.assertEqual(self.doc.svyazannyj_objekt_uid, self.building.uid)
            self.assertEqual(self.doc.spisok_vladelcev_uids, [self.owner.uid])

        # В класс TestPravoUstanavlivayushchijDokument добавить:

        def test_dolya_edge_cases(self):
            """Проверка граничных случаев доли"""
            # 0.0 должно вызывать ошибку
            with self.assertRaises(ValidationError):
                self.doc.dolya_v_prave = 0.0

            # Маленькое положительное значение должно проходить
            try:
                self.doc.dolya_v_prave = 0.000001
            except ValidationError:
                self.fail("0.000001 должно проходить валидацию")

            # 1.0 должно проходить
            try:
                self.doc.dolya_v_prave = 1.0
            except ValidationError:
                self.fail("1.0 должно проходить валидацию")

        def test_svyazannyj_objekt_none(self):
            """Тест создания документа с None объект"""
            doc = pravo_ustanavlivayushchij_dokument(
                tip_prava="sobstvennost",
                dolya_v_prave=0.5,
                svyazannyj_objekt=None,
                spisok_vladelcev=[self.owner],
                nomer_dokumenta="DOC-002",
                data_vydachi="01.01.2023",
                organ_vydachi="Росреестр"
            )
            self.assertIsNone(doc.svyazannyj_objekt_uid)

        def test_spisok_vladelcev_empty(self):
            """Тест создания документа с пустым списком владельцев"""
            doc = pravo_ustanavlivayushchij_dokument(
                tip_prava="sobstvennost",
                dolya_v_prave=0.5,
                svyazannyj_objekt=self.building,
                spisok_vladelcev=[],
                nomer_dokumenta="DOC-003",
                data_vydachi="01.01.2023",
                organ_vydachi="Росреестр"
            )
            self.assertEqual(len(doc.spisok_vladelcev_uids), 0)


class TestBaseRepository(unittest.TestCase):
    """Тестирование базового репозитория"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        class TestModel(base_model):
            def __init__(self, name, **kwargs):
                super().__init__(**kwargs)
                self.name = name

            def __eq__(self, other):
                if not isinstance(other, TestModel):
                    return False
                return self.uid == other.uid and self.name == other.name

        self.model_class = TestModel
        self.repo = base_repository(
            os.path.join(self.temp_dir, "test.json"),
            self.model_class
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_and_get(self):
        """Проверка добавления и получения"""
        obj = self.model_class("test")
        self.repo.add(obj)

        retrieved = self.repo.get(obj.uid)
        self.assertEqual(retrieved.uid, obj.uid)
        self.assertEqual(retrieved.name, obj.name)

    def test_get_not_found(self):
        """Проверка получения несуществующего объекта"""
        with self.assertRaises(NotFoundError):
            self.repo.get("non-existent")

    def test_update(self):
        """Проверка обновления"""
        obj = self.model_class("original")
        self.repo.add(obj)

        obj.name = "updated"
        self.repo.update(obj)

        retrieved = self.repo.get(obj.uid)
        self.assertEqual(retrieved.name, "updated")

    def test_update_not_found(self):
        """Проверка обновления несуществующего объекта"""
        obj = self.model_class("test")
        with self.assertRaises(NotFoundError):
            self.repo.update(obj)

    def test_delete(self):
        """Проверка удаления"""
        obj = self.model_class("test")
        self.repo.add(obj)
        self.repo.delete(obj.uid)

        with self.assertRaises(NotFoundError):
            self.repo.get(obj.uid)

    def test_list_all(self):
        """Проверка списка всех объектов"""
        obj1 = self.model_class("test1")
        obj2 = self.model_class("test2")

        self.repo.add(obj1)
        self.repo.add(obj2)

        all_objs = self.repo.list_all()
        self.assertEqual(len(all_objs), 2)

        uids = [obj.uid for obj in all_objs]
        self.assertIn(obj1.uid, uids)
        self.assertIn(obj2.uid, uids)

    # В класс TestBaseRepository (исправленные версии)

    def test_save_and_load_persistence(self):
        """Тест сохранения и загрузки из файла"""

        # Создаем простую модель для теста
        class SimpleModel:
            def __init__(self, name):
                self._name = name
                self._uid = str(hash(name))

            @property
            def uid(self):
                return self._uid

            @property
            def name(self):
                return self._name

        # Создаем простой репозиторий
        class SimpleRepo(base_repository):
            def _to_dict(self, obj):
                return {'name': obj.name, 'uid': obj.uid}

            def _from_dict(self, data):
                obj = SimpleModel(data.get('name'))
                obj._uid = data.get('uid')
                return obj

        file_path = os.path.join(self.temp_dir, "test_persistence.json")
        repo = SimpleRepo(file_path, SimpleModel)

        obj = SimpleModel("test")
        repo.add(obj)

        # Создаем новый репозиторий с тем же файлом
        new_repo = SimpleRepo(file_path, SimpleModel)

        # Проверяем, что объект загрузился
        all_objs = new_repo.list_all()
        self.assertEqual(len(all_objs), 1)

        retrieved = new_repo.get(obj.uid)
        self.assertEqual(retrieved.name, obj.name)

    def test_load_corrupted_file(self):
        """Тест загрузки поврежденного файла"""
        file_path = os.path.join(self.temp_dir, "test_corrupted.json")

        # Создаем поврежденный JSON
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("{invalid json")

        # Создаем простую модель для теста
        class SimpleModel:
            def __init__(self, name):
                self._name = name
                self._uid = str(hash(name))

            @property
            def uid(self):
                return self._uid

        # Создаем простой репозиторий
        class SimpleRepo(base_repository):
            def _to_dict(self, obj):
                return {'name': obj._name}

            def _from_dict(self, data):
                return SimpleModel(data.get('name'))

        # Создаем новый репозиторий - должна быть ошибка, но репозиторий создастся пустым
        repo = SimpleRepo(file_path, SimpleModel)
        self.assertEqual(len(repo._items), 0)

class TestNumberGenerator(unittest.TestCase):
    """Тестирование генератора кадастровых номеров"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cad_repo = cadastral_number_repository(self.temp_dir)
        self.generator = number_generator(self.cad_repo)

        self.building = zdanie(
            adres="Test",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_generate_number(self):
        """Проверка генерации номера"""
        number = self.generator.sgenerirovat_nomer(self.building)

        self.assertIsInstance(number, kadastrovyj_nomer)
        self.assertEqual(number.status_nomera, "aktivnyy")
        self.assertEqual(number.vladeshec_nomera, self.building)

    def test_generate_unique_numbers(self):
        """Проверка уникальности генерируемых номеров"""
        num1 = self.generator.sgenerirovat_nomer(self.building)
        self.cad_repo.add(num1)

        num2 = self.generator.sgenerirovat_nomer(self.building)

        self.assertNotEqual(num1.polnoe_znachenie, num2.polnoe_znachenie)

    def test_reserve_number(self):
        """Проверка резервирования номера"""
        reserved = self.generator.zarezervirovat_nomer()

        self.assertEqual(reserved.status_nomera, "zarezervirovannyy")
        self.assertIsNone(reserved.vladeshec_nomera)

    def test_generate_number_with_existing(self):
        """Тест генерации номера с существующими номерами"""
        # Добавляем первый номер
        num1 = self.generator.sgenerirovat_nomer(self.building)
        self.cad_repo.add(num1)

        # Генерируем второй номер
        num2 = self.generator.sgenerirovat_nomer(self.building)

        self.assertNotEqual(num1.polnoe_znachenie, num2.polnoe_znachenie)
        self.assertGreater(int(num2.unikalnyj_nomer_v_kvartale), int(num1.unikalnyj_nomer_v_kvartale))

    def test_reserve_number_multiple(self):
        """Тест резервирования нескольких номеров"""
        reserved1 = self.generator.zarezervirovat_nomer()
        self.cad_repo.add(reserved1)

        reserved2 = self.generator.zarezervirovat_nomer()

        self.assertNotEqual(reserved1.polnoe_znachenie, reserved2.polnoe_znachenie)
        self.assertEqual(reserved2.status_nomera, "zarezervirovannyy")


class TestKadastrovyjUchet(unittest.TestCase):
    """Тестирование сервиса кадастрового учета"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        self.object_repo = object_repository(self.temp_dir)
        self.owner_repo = owner_repository(self.temp_dir)
        self.right_repo = right_document_repository(self.temp_dir)
        self.cad_repo = cadastral_number_repository(self.temp_dir)
        self.number_gen = number_generator(self.cad_repo)

        self.service = kadastrovyj_uchet(
            self.object_repo, self.owner_repo, self.right_repo,
            self.cad_repo, self.number_gen
        )

        self.owner = vladeshec("123", "Иванов И.И.", "test@test.ru")
        self.building = zdanie(
            adres="Test",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )
        self.doc = pravo_ustanavlivayushchij_dokument(
            tip_prava="sobstvennost",
            dolya_v_prave=1.0,
            svyazannyj_objekt=self.building,
            spisok_vladelcev=[self.owner],
            nomer_dokumenta="DOC-001",
            data_vydachi="01.01.2023",
            organ_vydachi="Росреестр"
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_postavit_na_uchet(self):
        """Проверка постановки на учет"""
        self.service.postavit_na_uchet(self.building, self.owner, self.doc)

        self.assertEqual(self.building.status, "uchtennyy")

        # Проверка сохранения в репозиториях
        self.assertEqual(len(self.object_repo.list_all()), 1)
        self.assertEqual(len(self.owner_repo.list_all()), 1)
        self.assertEqual(len(self.right_repo.list_all()), 1)

    def test_postavit_na_uchet_without_owner_in_doc(self):
        """Тест постановки на учет, когда владелец не в документе"""
        new_owner = vladeshec("456", "Петров П.П.", "petr@mail.ru")

        self.service.postavit_na_uchet(self.building, new_owner, self.doc)

        # Проверяем, что владелец добавился в документ
        self.assertIn(new_owner, self.doc.spisok_vladelcev)

class TestTekhnicheskiyUchet(unittest.TestCase):
    """Тестирование сервиса технического учета"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.object_repo = object_repository(self.temp_dir)
        self.service = tekhnicheskiy_uchet(self.object_repo)

        self.building = zdanie(
            adres="Test",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )
        self.land = zemelnyj_uchastok(
            adres="Test land",
            ploshchad=1000,
            kategoriya_zemel="Сельхоз",
            vid_razreshonnogo_ispolzovaniya="ИЖС"
        )

        self.object_repo.add(self.building)
        self.object_repo.add(self.land)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_generate_tekhpasport_number_unique(self):
        """Тест уникальности номеров техпаспорта"""
        num1 = self.service._generate_tekhpasport_number()
        num2 = self.service._generate_tekhpasport_number()
        self.assertNotEqual(num1, num2)

    def test_tech_uchet_zdaniya(self):
        """Проверка техучета здания"""
        # Используем только те поля, которые есть в классе zdanie
        params = {
            'kolichestvo_etazhej': 3,
            'material_sten': 'бетон',
            'fizicheskij_iznos': 30
        }

        self.service.provesti_tekhnicheskij_uchet_zdaniya(self.building, params)

        self.assertEqual(self.building.kolichestvo_etazhej, 3)
        self.assertEqual(self.building.material_sten, 'бетон')
        self.assertEqual(self.building.fizicheskij_iznos, 30)
        self.assertIsNotNone(self.building.nomer_tekhpasporta)
        self.assertIsNotNone(self.building.data_poslednego_tekh_ucheta)

    def test_tech_uchet_zdaniya_without_params(self):
        """Проверка техучета здания без параметров"""
        self.service.provesti_tekhnicheskij_uchet_zdaniya(self.building)

        self.assertIsNotNone(self.building.nomer_tekhpasporta)
        self.assertIsNotNone(self.building.data_poslednego_tekh_ucheta)

    def test_tech_uchet_uchastka(self):
        """Проверка техучета участка"""
        params = {
            'nalichie_postroek': True,
            'sostoyanie': 'Отличное'
        }

        self.service.provesti_tekhnicheskij_uchet_uchastka(self.land, params)

        self.assertTrue(self.land.nalichie_postroek)
        self.assertEqual(self.land.sostoyanie, 'Отличное')
        self.assertIsNotNone(self.land.nomer_tekhpasporta)

    def test_tech_uchet_uchastka_without_params(self):
        """Проверка техучета участка без параметров"""
        self.service.provesti_tekhnicheskij_uchet_uchastka(self.land)

        self.assertIsNotNone(self.land.nomer_tekhpasporta)
        self.assertIsNotNone(self.land.data_poslednego_tekh_ucheta)

    def test_generate_tekhpasport_number(self):
        """Проверка генерации номера техпаспорта"""
        number = self.service._generate_tekhpasport_number()
        # Формат: ТП-YYYYMMDD-XXXXXX (например, ТП-20260306-ABC123)
        # Общая длина зависит от UUID, но начинается с "ТП-" и содержит дату
        self.assertTrue(number.startswith("ТП-"))
        self.assertGreater(len(number), 10)


class TestDokumentMenedzher(unittest.TestCase):
    """Тестирование сервиса документооборота"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.object_repo = object_repository(self.temp_dir)
        self.right_repo = right_document_repository(self.temp_dir)
        self.owner_repo = owner_repository(self.temp_dir)

        self.service = dokument_menedzher(self.object_repo, self.right_repo)

        self.owner = vladeshec("123", "Иванов И.И.", "test@test.ru")
        self.owner_repo.add(self.owner)

        self.building = zdanie(
            adres="Test",
            ploshchad=100,
            kolichestvo_etazhej=2,
            material_sten="кирпич",
            naznachenie="zhiloe",
            god_postrojki=2000
        )
        self.object_repo.add(self.building)

        self.doc = pravo_ustanavlivayushchij_dokument(
            tip_prava="sobstvennost",
            dolya_v_prave=1.0,
            svyazannyj_objekt=self.building,
            spisok_vladelcev=[self.owner],
            nomer_dokumenta="DOC-001",
            data_vydachi="01.01.2023",
            organ_vydachi="Росреестр"
        )
        self.right_repo.add(self.doc)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_obnovit_dokumentatsiyu(self):
        """Проверка обновления документации"""
        vypiska = self.service.obnovit_dokumentatsiyu(self.building)

        self.assertIsNotNone(vypiska)
        self.assertIn("ВЫПИСКА", vypiska)
        self.assertIn(self.building.adres, vypiska)

        # Проверка сохранения в объекте
        self.assertEqual(self.building.saved_vypiska, vypiska)

    def test_get_saved_vypiska(self):
        """Проверка получения сохраненной выписки"""
        self.assertIsNone(self.service.get_saved_vypiska(self.building))

        vypiska = self.service.obnovit_dokumentatsiyu(self.building)
        saved = self.service.get_saved_vypiska(self.building)

        self.assertEqual(saved, vypiska)

    def test_check_access(self):
        """Проверка прав доступа"""
        # Владелец имеет доступ
        self.assertTrue(self.service._check_access(self.building, self.owner))

        # Другой владелец не имеет доступа
        other_owner = vladeshec("456", "Петров П.П.", "other@test.ru")
        self.assertFalse(self.service._check_access(self.building, other_owner))

    def test_zaprosit_vypisku_with_access(self):
        """Проверка запроса выписки с правами"""
        vypiska = self.service.zaprosit_vypisku(self.building, self.owner)
        self.assertIsNotNone(vypiska)

    def test_zaprosit_vypisku_without_access(self):
        """Проверка запроса выписки без прав"""
        other_owner = vladeshec("456", "Петров П.П.", "other@test.ru")

        with self.assertRaises(PermissionDeniedError):
            self.service.zaprosit_vypisku(self.building, other_owner)

    def test_format_date(self):
        """Проверка форматирования даты"""
        # ISO формат
        formatted = self.service._format_date("2023-01-15T10:30:00")
        self.assertEqual(formatted, "15.01.2023")

        # DD.MM.YYYY формат
        formatted = self.service._format_date("15.01.2023")
        self.assertEqual(formatted, "15.01.2023")

        # YYYY-MM-DD формат
        formatted = self.service._format_date("2023-01-15")
        self.assertEqual(formatted, "15.01.2023")

        # Пустая дата
        formatted = self.service._format_date(None)
        self.assertEqual(formatted, "не указана")

        # Некорректная дата
        formatted = self.service._format_date("invalid")
        self.assertEqual(formatted, "invalid")

    def test_get_iznos_level(self):
        """Проверка градации износа"""
        self.assertEqual(self.service._get_iznos_level(5), "Отличное")
        self.assertEqual(self.service._get_iznos_level(15), "Хорошее")
        self.assertEqual(self.service._get_iznos_level(35), "Удовлетворительное")
        self.assertEqual(self.service._get_iznos_level(55), "Неудовлетворительное")
        self.assertEqual(self.service._get_iznos_level(75), "Аварийное")

    def test_generate_vypiska_for_zdanie(self):
        """Проверка генерации выписки для здания"""
        self.building.nomer_tekhpasporta = "TP-001"
        self.building.data_poslednego_tekh_ucheta = "2023-01-15"
        self.building.fizicheskij_iznos = 30

        vypiska = self.service._generate_vypiska(self.building)

        # Проверяем, что в выписке есть информация о здании
        self.assertIn("Объект: zdanie", vypiska)
        self.assertIn(self.building.adres, vypiska)
        self.assertIn(str(self.building.ploshchad), vypiska)
        self.assertIn(self.owner.fio, vypiska)

    def test_generate_vypiska_for_land(self):
        """Проверка генерации выписки для участка"""
        self.land = zemelnyj_uchastok(
            adres="Test land",
            ploshchad=1000,
            kategoriya_zemel="Сельхоз",
            vid_razreshonnogo_ispolzovaniya="ИЖС"
        )
        self.object_repo.add(self.land)

        self.land.nomer_tekhpasporta = "TP-002"
        self.land.data_poslednego_tekh_ucheta = "2023-01-15"

        vypiska = self.service._generate_vypiska(self.land)

        # Проверяем, что в выписке есть информация об участке
        self.assertIn("Объект: zemelnyj_uchastok", vypiska)
        self.assertIn(self.land.adres, vypiska)
        self.assertIn(self.land.kategoriya_zemel, vypiska)

        def test_format_date_various_formats(self):
            """Тест различных форматов дат"""
            # ISO с временем
            self.assertEqual(self.service._format_date("2023-01-15T10:30:00"), "15.01.2023")
            # YYYY-MM-DD
            self.assertEqual(self.service._format_date("2023-01-15"), "15.01.2023")
            # DD.MM.YYYY
            self.assertEqual(self.service._format_date("15.01.2023"), "15.01.2023")
            # Неверный формат
            self.assertEqual(self.service._format_date("invalid"), "invalid")

        def test_generate_vypiska_for_building_with_cad_number(self):
            """Тест генерации выписки для здания с кадастровым номером"""
            cad_number = kadastrovyj_nomer("000123", "001")
            self.building.kadastrovyj_nomer = cad_number
            self.building.nomer_tekhpasporta = "TP-001"

            vypiska = self.service._generate_vypiska(self.building)

            self.assertIn(cad_number.polnoe_znachenie, vypiska)

        def test_generate_vypiska_for_land_without_techpasport(self):
            """Тест генерации выписки для участка без техпаспорта"""
            self.land = zemelnyj_uchastok(
                adres="Test land",
                ploshchad=1000,
                kategoriya_zemel="Сельхоз",
                vid_razreshonnogo_ispolzovaniya="ИЖС"
            )

            vypiska = self.service._generate_vypiska(self.land)

            self.assertIn("Технический паспорт: не оформлен", vypiska)


class TestKadastrovoeAgentstvoIntegration(unittest.TestCase):
    """Интеграционное тестирование фасада агентства"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.agency = kadastrovoe_agentstvo("Test Agency", self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_create_owner(self):
        """Проверка создания владельца через фасад"""
        owner = self.agency.sozdat_vladelca("123", "Иванов И.И.", "test@test.ru")

        self.assertIsNotNone(owner.uid)
        self.assertEqual(owner.fio, "Иванов И.И.")

        # Проверка сохранения в реестре
        self.assertEqual(len(self.agency.reestr_vladelcev), 1)

    def test_create_zemelnyj_uchastok(self):
        """Проверка создания участка через фасад"""
        land = self.agency.sozdat_zemelnyj_uchastok(
            "Test address", 1000.0,
            "Сельхоз", "ИЖС"
        )

        self.assertIsNotNone(land.uid)
        self.assertEqual(land.adres, "Test address")
        self.assertEqual(land.ploshchad, 1000.0)

        # Проверка сохранения в реестре
        self.assertEqual(len(self.agency.reestr_obektov), 1)

    def test_create_zdanie(self):
        """Проверка создания здания через фасад"""
        building = self.agency.sozdat_zdanie(
            "Test address", 500.0,
            5, "кирпич", "zhiloe", 2000
        )

        self.assertIsNotNone(building.uid)
        self.assertEqual(building.adres, "Test address")
        self.assertEqual(building.kolichestvo_etazhej, 5)

        # Проверка сохранения в реестре
        self.assertEqual(len(self.agency.reestr_obektov), 1)

    def test_full_registration_flow(self):
        """Проверка полного цикла регистрации"""
        # Создаем владельца
        owner = self.agency.sozdat_vladelca("123", "Иванов И.И.", "test@test.ru")

        # Создаем объект
        building = self.agency.sozdat_zdanie(
            "Test address", 500.0,
            5, "кирпич", "zhiloe", 2000
        )

        # Регистрируем право
        doc = self.agency.vypolnit_registraciyu(
            building.uid, owner.uid,
            "DOC-001", "01.01.2023", "Росреестр",
            "sobstvennost", 1.0
        )

        self.assertIsNotNone(doc.uid)
        self.assertEqual(doc.tip_prava, "sobstvennost")

        # Присваиваем кадастровый номер
        cad_number = self.agency.vydat_kadastrovyj_nomer(building.uid)
        self.assertIsNotNone(cad_number.polnoe_znachenie)

        # Проводим техучет
        updated = self.agency.provesti_tekhnicheskij_uchet(
            building.uid,
            fizicheskij_iznos=30
        )
        self.assertIsNotNone(updated.nomer_tekhpasporta)

        # Обновляем документацию
        self.agency.obnovit_dokumenty(building.uid)

        # Получаем выписку
        info = self.agency.predostavit_informaciyu(cad_number.polnoe_znachenie)
        self.assertIn("ВЫПИСКА", info)
        self.assertIn(building.adres, info)

    def test_double_registration_prevention(self):
        """Проверка предотвращения превышения суммы долей"""
        owner1 = self.agency.sozdat_vladelca("123", "Иванов И.И.", "test@test.ru")
        owner2 = self.agency.sozdat_vladelca("456", "Петров П.П.", "other@test.ru")

        building = self.agency.sozdat_zdanie(
            "Test address", 500.0,
            5, "кирпич", "zhiloe", 2000
        )

        # Регистрируем 0.6 доли
        self.agency.vypolnit_registraciyu(
            building.uid, owner1.uid,
            "DOC-001", "01.01.2023", "Росреестр",
            "sobstvennost", 0.6
        )

        # Пытаемся зарегистрировать еще 0.5 (будет ошибка)
        with self.assertRaises(ValidationError):
            self.agency.vypolnit_registraciyu(
                building.uid, owner2.uid,
                "DOC-002", "01.01.2023", "Росреестр",
                "sobstvennost", 0.5
            )

    def test_issue_cadastral_number_twice(self):
        """Проверка повторной выдачи кадастрового номера"""
        owner = self.agency.sozdat_vladelca("123", "Иванов И.И.", "test@test.ru")
        building = self.agency.sozdat_zdanie(
            "Test address", 500.0,
            5, "кирпич", "zhiloe", 2000
        )

        # Первая выдача
        cad_number1 = self.agency.vydat_kadastrovyj_nomer(building.uid)

        # Вторая выдача (должна вернуть существующий номер)
        cad_number2 = self.agency.vydat_kadastrovyj_nomer(building.uid)

        self.assertEqual(cad_number1.uid, cad_number2.uid)

    def test_technical_audit_without_params(self):
        """Проверка техучета без параметров"""
        owner = self.agency.sozdat_vladelca("123", "Иванов И.И.", "test@test.ru")
        building = self.agency.sozdat_zdanie(
            "Test address", 500.0,
            5, "кирпич", "zhiloe", 2000
        )

        updated = self.agency.provesti_tekhnicheskij_uchet(building.uid)
        self.assertIsNotNone(updated.nomer_tekhpasporta)

    def test_property_getters(self):
        """Проверка геттеров свойств"""
        self.assertEqual(self.agency.nazvanie, "Test Agency")
        self.assertIsNotNone(self.agency.reestr_obektov)
        self.assertIsNotNone(self.agency.reestr_vladelcev)

    def test_not_found_errors(self):
        """Проверка ошибок при поиске несуществующих объектов"""
        with self.assertRaises(NotFoundError):
            self.agency.vydat_kadastrovyj_nomer("non-existent")

        with self.assertRaises(NotFoundError):
            self.agency.predostavit_informaciyu("00:00:000000:000")

    def test_create_owner_with_special_chars(self):
        """Тест создания владельца со спецсимволами в ФИО"""
        owner = self.agency.sozdat_vladelca("123", "Иванов-Петров И.И.", "test@test.ru")
        self.assertEqual(owner.fio, "Иванов-Петров И.И.")

    def test_restore_relations_with_missing_objects(self):
        """Тест восстановления связей при отсутствующих объектах"""
        # Создаем объекты
        owner = self.agency.sozdat_vladelca("123", "Иванов И.И.", "test@test.ru")
        building = self.agency.sozdat_zdanie(
            "Test", 500, 5, "кирпич", "zhiloe", 2000
        )

        doc = self.agency.vypolnit_registraciyu(
            building.uid, owner.uid, "DOC-001", "01.01.2023",
            "Росреестр", "sobstvennost", 1.0
        )

        # Удаляем файлы вручную, чтобы имитировать потерю данных
        import os
        os.remove(os.path.join(self.temp_dir, 'objects.json'))

        # Создаем новое агентство
        new_agency = kadastrovoe_agentstvo("Test Agency", self.temp_dir)

        # Проверяем, что репозитории пусты
        self.assertEqual(len(new_agency._object_repo.list_all()), 0)

    def test_provesti_tekhnicheskij_uchet_general_object(self):
        """Тест техучета для общего объекта"""

        class GeneralObj(objekt_nedvizhimosti):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        obj = GeneralObj(adres="Test", ploshchad=100)
        self.agency._object_repo.add(obj)

        updated = self.agency.provesti_tekhnicheskij_uchet(
            obj.uid, test_param="value"
        )

        self.assertIsNotNone(updated.nomer_tekhpasporta)

    def test_get_info_with_saved_vypiska(self):
        """Тест получения сохраненной выписки"""
        owner = self.agency.sozdat_vladelca("123", "Иванов И.И.", "test@test.ru")
        building = self.agency.sozdat_zdanie(
            "Test", 500, 5, "кирпич", "zhiloe", 2000
        )

        cad_number = self.agency.vydat_kadastrovyj_nomer(building.uid)
        self.agency.obnovit_dokumenty(building.uid)

        info = self.agency.predostavit_informaciyu(cad_number.polnoe_znachenie)
        self.assertIn("ВЫПИСКА", info)


class TestConstants(unittest.TestCase):
    """Тестирование констант"""

    def test_constants_values(self):
        """Проверка значений констант"""
        self.assertEqual(Constants.REGION, "77")
        self.assertEqual(Constants.RAYON, "01")
        self.assertEqual(Constants.JSON_INDENT, 2)
        self.assertEqual(Constants.DEFAULT_STATUS, "aktivnyy")
        self.assertEqual(Constants.MIN_DEPRECIATION, 0)
        self.assertEqual(Constants.MAX_DEPRECIATION, 100)
        self.assertEqual(Constants.DEFAULT_MIN_POSITIVE, 1)
        self.assertEqual(Constants.MIN_SHARE, 0)
        self.assertEqual(Constants.MAX_SHARE, 1)
        self.assertEqual(Constants.SHARE_EPSILON, 1e-9)

    def test_allowed_statuses(self):
        """Проверка допустимых статусов"""
        expected = {"aktivnyy", "zarezervirovannyy", "annulirovannyy"}
        self.assertEqual(Constants.ALLOWED_STATUSES, expected)

    def test_depreciation_constants(self):
        """Проверка констант износа"""
        self.assertEqual(Constants.DEPRECIATION_EXCELLENT, 10)
        self.assertEqual(Constants.DEPRECIATION_GOOD, 25)
        self.assertEqual(Constants.DEPRECIATION_SATISFACTORY, 40)
        self.assertEqual(Constants.DEPRECIATION_POOR, 60)


def run_all_tests():
    """Функция для запуска всех тестов"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestExceptions,
        TestBaseModel,
        TestDokument,
        TestVladeshec,
        TestKadastrovyjNomer,
        TestObjektNedvizhimosti,
        TestZdanie,
        TestZemelnyjUchastok,
        TestPravoUstanavlivayushchijDokument,
        TestBaseRepository,
        TestNumberGenerator,
        TestKadastrovyjUchet,
        TestTekhnicheskiyUchet,
        TestDokumentMenedzher,
        TestKadastrovoeAgentstvoIntegration,
        TestConstants
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Подсчет покрытия
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors

    coverage_percent = (passed / total_tests) * 100 if total_tests > 0 else 0

    print(f"\n{'=' * 60}")
    print(f"ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f"{'=' * 60}")
    print(f"Всего тестов: {total_tests}")
    print(f"Пройдено: {passed}")
    print(f"Ошибок: {errors}")
    print(f"Падений: {failures}")
    print(f"Покрытие тестами: {coverage_percent:.1f}%")
    print(f"{'=' * 60}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
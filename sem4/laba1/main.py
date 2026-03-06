#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Главный модуль для запуска интерактивного меню кадастрового агентства.
"""

import sys
import os
import re
from datetime import datetime

from services.kadastrovoe_agentstvo import kadastrovoe_agentstvo
from exceptions.exceptions import NotFoundError, ValidationError
from models.zdanie import zdanie
from models.zemelnyj_uchastok import zemelnyj_uchastok
from constants import Constants


class CadastralMenu:
    """Интерактивное меню для работы с кадастровым агентством"""

    def __init__(self):
        os.makedirs("./data", exist_ok=True)
        self.agency = kadastrovoe_agentstvo("Городское кадастровое агентство", data_dir="./data")

        # Словари для выбора
        self.organs = {
            '1': {'name': 'Суд', 'value': 'Суд'},
            '2': {'name': 'Нотариус', 'value': 'Нотариус'},
            '3': {'name': 'Росреестр', 'value': 'Росреестр'},
            '4': {'name': 'Орган местного самоуправления', 'value': 'ОМСУ'}
        }

        self.right_types = {
            '1': {'name': 'Собственность', 'value': 'sobstvennost'},
            '2': {'name': 'Аренда', 'value': 'arenda'},
            '3': {'name': 'Наследство', 'value': 'nasledstvo'}
        }

        self.building_purposes = {
            '1': {'name': 'Жилое', 'value': 'zhiloe'},
            '2': {'name': 'Нежилое', 'value': 'nezhiloe'}
        }

        self.land_categories = {
            '1': {'name': 'Земли сельскохозяйственного назначения', 'value': 'Сельскохозяйственное назначение'},
            '2': {'name': 'Земли населённых пунктов', 'value': 'Населённые пункты'},
            '3': {'name': 'Земли промышленности', 'value': 'Промышленное назначение'},
            '4': {'name': 'Земли особо охраняемых территорий', 'value': 'Особо охраняемые территории'}
        }

        self.permitted_uses = {
            '1': {'name': 'Для индивидуального жилищного строительства', 'value': 'ИЖС'},
            '2': {'name': 'Для ведения личного подсобного хозяйства', 'value': 'ЛПХ'},
            '3': {'name': 'Для садоводства', 'value': 'Садоводство'},
            '4': {'name': 'Для коммерческой застройки', 'value': 'Коммерческая'}
        }

        self.fire_classes = {str(i): {'name': v, 'value': v} for i, v in enumerate(['I', 'II', 'III', 'IV'], 1)}
        self.energy_classes = {str(i): {'name': v, 'value': v} for i, v in enumerate(['A', 'B', 'C', 'D', 'E'], 1)}
        self.land_states = {str(i): {'name': v, 'value': v} for i, v in enumerate(['Отличное', 'Хорошее', 'Удовлетворительное', 'Неудовлетворительное'], 1)}


    def _input_required(self, prompt: str, error_msg: str = "Значение не может быть пустым") -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print(f"Ошибка: {error_msg}. Попробуйте снова.")

    def _input_positive_number(self, prompt: str, field_name: str = "Значение") -> float:
        while True:
            value = input(prompt).strip()
            try:
                num = float(value)
                if num > Constants.MIN_DEPRECIATION:
                    return num
                print(f"Ошибка: {field_name} должно быть положительным числом.")
            except ValueError:
                print(f"Ошибка: {field_name} должно быть числом.")

    def _input_integer(self, prompt: str, field_name: str = "Значение", min_val: int = Constants.DEFAULT_MIN_POSITIVE) -> int:
        while True:
            value = input(prompt).strip()
            try:
                num = int(float(value))
                if num >= min_val:
                    return num
                print(f"Ошибка: {field_name} должно быть не меньше {min_val}.")
            except ValueError:
                print(f"Ошибка: {field_name} должно быть целым числом.")

    def _input_date(self, prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if self._validate_date(value):
                return value
            print("Ошибка: Неверный формат даты. Используйте ДД.ММ.ГГГГ (например, 22.03.2020).")

    def _validate_date(self, date_str: str) -> bool:
        pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$'
        if not re.match(pattern, date_str):
            return False
        try:
            datetime.strptime(date_str, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    def _get_choice(self, prompt: str, options: dict, allow_custom: bool = False) -> str:
        print(prompt)
        for key, option in options.items():
            print(f"  {key}. {option['name']}")
        if allow_custom:
            print("  Или введите свой вариант")
        while True:
            choice = input("Ваш выбор: ").strip()
            if choice in options:
                return options[choice]['value']
            if allow_custom and choice:
                return choice
            print("Неверный выбор. Пожалуйста, выберите из предложенных вариантов.")

    def _input_object_uid(self, prompt: str = "Введите UID объекта недвижимости") -> str:
        while True:
            uid = input(f"{prompt}: ").strip()
            if not uid:
                print("Ошибка: UID не может быть пустым. Попробуйте снова.")
                continue
            try:
                self.agency._object_repo.get(uid)
                return uid
            except NotFoundError:
                print(f"Ошибка: Объект с UID {uid} не найден. Попробуйте снова.")

    def _input_owner_uid(self, prompt: str = "Введите UID владельца") -> str:
        while True:
            uid = input(f"{prompt}: ").strip()
            if not uid:
                print("Ошибка: UID не может быть пустым. Попробуйте снова.")
                continue
            try:
                self.agency._owner_repo.get(uid)
                return uid
            except NotFoundError:
                print(f"Ошибка: Владелец с UID {uid} не найден. Попробуйте снова.")


    def print_header(self):
        print("=" * 70)
        print("КАДАСТРОВОЕ АГЕНТСТВО - СИСТЕМА УПРАВЛЕНИЯ НЕДВИЖИМОСТЬЮ")
        print("=" * 70)

    def print_menu(self):
        print("\nГЛАВНОЕ МЕНЮ:")
        print("-" * 70)
        print("1. Создать нового владельца")
        print("2. Создать земельный участок")
        print("3. Создать здание")
        print("4. Зарегистрировать право собственности")
        print("5. Присвоить кадастровый номер")
        print("6. Провести технический учёт")
        print("7. Обновить документацию")
        print("8. Получить выписку по кадастровому номеру")
        print("9. Показать список всех объектов")
        print("10. Показать список всех владельцев")
        print("0. Выход")
        print("-" * 70)

    def run(self):
        self.print_header()
        menu_actions = {
            '1': self.create_vladesec,
            '2': self.create_zemelnyj_uchastok,
            '3': self.create_zdanie,
            '4': self.register_vladesecship,
            '5': self.issue_cadastral_number,
            '6': self.tehnicheskiy_uchet,
            '7': self.update_docs,
            '8': self.get_info,
            '9': self.list_objects,
            '10': self.list_vladeshecs,
            '0': self.exit_program
        }
        while True:
            try:
                self.print_menu()
                choice = input("Выберите пункт меню: ").strip()
                action = menu_actions.get(choice)
                if action:
                    if not action():
                        break
                else:
                    print("Ошибка: Неверный пункт меню. Пожалуйста, выберите от 0 до 10.")
                    input("\nНажмите Enter, чтобы продолжить...")
            except KeyboardInterrupt:
                print("\n\nПрограмма завершена пользователем.")
                break
            except Exception as e:
                print(f"Непредвиденная ошибка: {e}")
                input("Нажмите Enter, чтобы продолжить...")

    def create_vladesec(self):
        print("\n--- СОЗДАНИЕ НОВОГО ВЛАДЕЛЬЦА ---")
        try:
            identificator = self._input_required("Введите идентификатор (ИНН/паспорт): ")

            while True:
                fio = self._input_required("Введите ФИО: ")
                if re.match(r'^[а-яА-ЯёЁa-zA-Z\s\-]+$', fio) and len(fio.split()) >= 2:
                    break
                print("Ошибка: ФИО должно содержать только буквы, пробелы, дефисы и состоять минимум из двух слов.")

            rekvizity = self._input_required("Введите реквизиты связи (телефон/email): ")

            owner = self.agency.sozdat_vladelca(identificator, fio, rekvizity)
            print(f"✓ Владелец успешно создан! UID: {owner.uid}")
        except Exception as e:
            print(f"Ошибка при создании владельца: {e}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def create_zemelnyj_uchastok(self):
        print("\n--- СОЗДАНИЕ ЗЕМЕЛЬНОГО УЧАСТКА ---")
        try:
            adres = self._input_required("Введите адрес участка: ")
            ploshchad = self._input_positive_number("Введите площадь (кв.м): ", "Площадь")
            kategoriya = self._get_choice("Выберите категорию земель:", self.land_categories)
            vid = self._get_choice("Выберите вид разрешенного использования:", self.permitted_uses)

            obj = self.agency.sozdat_zemelnyj_uchastok(adres, ploshchad, kategoriya, vid)
            print(f"✓ Земельный участок успешно создан! UID: {obj.uid}")
        except ValidationError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Ошибка при создании участка: {e}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def create_zdanie(self):
        print("\n--- СОЗДАНИЕ ЗДАНИЯ ---")
        try:
            adres = self._input_required("Введите адрес здания: ")
            ploshchad = self._input_positive_number("Введите площадь (кв.м): ", "Площадь")
            etazhi = self._input_integer("Введите количество этажей: ", "Этажей")
            material = self._input_required("Введите материал стен: ")
            naznachenie = self._get_choice("Выберите назначение здания:", self.building_purposes)

            current_year = datetime.now().year
            while True:
                god = self._input_integer("Введите год постройки: ", "Год", min_val=1800)
                if god <= current_year:
                    break
                print(f"Ошибка: Год постройки не может быть больше {current_year}.")

            obj = self.agency.sozdat_zdanie(adres, ploshchad, etazhi, material, naznachenie, god)
            print(f"✓ Здание успешно создано! UID: {obj.uid}")
        except ValidationError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Ошибка при создании здания: {e}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def register_vladesecship(self):
        print("\n--- РЕГИСТРАЦИЯ ПРАВА СОБСТВЕННОСТИ ---")
        self._show_objects_short()
        self._show_owners_short()

        try:
            objekt_id = self._input_object_uid()
            owner_id = self._input_owner_uid()

            print("\n--- Данные правоустанавливающего документа ---")
            doc_nomer = self._input_required("Номер документа: ")
            doc_data = self._input_date("Дата выдачи (ДД.ММ.ГГГГ): ")
            doc_organ = self._get_choice("Выберите орган выдачи:", self.organs, allow_custom=True)
            tip_prava = self._get_choice("Выберите тип права:", self.right_types)

            obj = self.agency._object_repo.get(objekt_id)

            while True:
                try:
                    dolya = float(self._input_required("Доля в праве (например, 1 для целой, 0.5 для половины): "))
                    if not (Constants.MIN_DEPRECIATION < dolya <= Constants.DEFAULT_MIN_POSITIVE):
                        print("Ошибка: Доля должна быть больше 0 и не больше 1.")
                        continue

                    current_sum = Constants.MIN_SHARE
                    for doc in self.agency._right_repo.list_all():
                        if doc.svyazannyj_objekt == obj:
                            current_sum += doc.dolya_v_prave

                    if current_sum + dolya > Constants.MAX_SHARE + Constants.SHARE_EPSILON:
                        print(f"Ошибка: Сумма долей по объекту не может превышать 1. "
                              f"Текущая сумма: {current_sum:.2f}, добавляемая доля: {dolya:.2f}")
                        continue

                    break
                except ValueError:
                    print("Ошибка: Введите число.")

            doc = self.agency.vypolnit_registraciyu(objekt_id, owner_id, doc_nomer, doc_data, doc_organ, tip_prava,
                                                    dolya)
            print(f"✓ Право собственности зарегистрировано! Документ UID: {doc.uid}")
        except NotFoundError as e:
            print(f"Ошибка: {e}")
        except ValidationError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def issue_cadastral_number(self):
        print("\n--- ПРИСВОЕНИЕ КАДАСТРОВОГО НОМЕРА ---")
        self._show_objects_short()
        try:
            objekt_id = self._input_object_uid()
            obj = self.agency._object_repo.get(objekt_id)
            if obj.kadastrovyj_nomer:
                print(f"У объекта уже есть кадастровый номер: {obj.kadastrovyj_nomer.polnoe_znachenie}")
            else:
                cad_number = self.agency.vydat_kadastrovyj_nomer(objekt_id)
                print(f"✓ Кадастровый номер присвоен: {cad_number.polnoe_znachenie}")
                print(f"  Статус номера: {self._translate_status(cad_number.status_nomera)}")
                print(f"  Дата присвоения: {self._format_date(cad_number.data_prisvoeniya)}")
        except NotFoundError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Ошибка при присвоении номера: {e}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def _input_building_params(self):
        params = {}
        print("\n--- ПАРАМЕТРЫ ТЕХНИЧЕСКОГО ОБСЛЕДОВАНИЯ ЗДАНИЯ ---")
        params['kolichestvo_etazhej'] = self._input_integer("Количество этажей: ", "Этажей")
        params['material_sten'] = self._input_required("Материал стен: ")

        while True:
            try:
                iznos = int(self._input_required("Физический износ (в процентах, 0-100): "))
                if Constants.MIN_DEPRECIATION <= iznos <= Constants.MAX_DEPRECIATION:
                    params['fizicheskij_iznos'] = iznos
                    break
                print("Ошибка: Износ должен быть от 0 до 100%.")
            except ValueError:
                print("Ошибка: Введите целое число.")

        params['pozharnaya_bezopasnost'] = self._get_choice("Класс пожарной безопасности:", self.fire_classes)
        params['energeticheskaya_effektivnost'] = self._get_choice("Класс энергоэффективности:", self.energy_classes)
        return params

    def _input_land_params(self):
        params = {}
        print("\n--- ПАРАМЕТРЫ ТЕХНИЧЕСКОГО ОБСЛЕДОВАНИЯ УЧАСТКА ---")
        while True:
            postrojki = input("Наличие построек на участке (да/нет): ").strip().lower()
            if postrojki == 'да':
                params['nalichie_postroek'] = True
                break
            elif postrojki == 'нет':
                params['nalichie_postroek'] = False
                break
            print("Ошибка: Введите 'да' или 'нет'.")

        params['sostoyanie'] = self._get_choice("Состояние участка:", self.land_states)
        return params

    def tehnicheskiy_uchet(self):
        print("\n--- ТЕХНИЧЕСКИЙ УЧЁТ (ОБСЛЕДОВАНИЕ ОБЪЕКТА) ---")
        self._show_objects_short()

        try:
            objekt_id = self._input_object_uid()
            obj = self.agency._object_repo.get(objekt_id)

            params = {}
            print("\n--- ОСНОВНЫЕ ХАРАКТЕРИСТИКИ (можно пропустить) ---")
            adres = input(f"Новый адрес [{obj.adres}]: ").strip()
            if adres:
                params['adres'] = adres

            ploshchad = input(f"Новая площадь [{obj.ploshchad}]: ").strip()
            if ploshchad:
                try:
                    p = float(ploshchad)
                    if p > Constants.MIN_DEPRECIATION:
                        params['ploshchad'] = p
                    else:
                        print("Площадь не изменена - должна быть положительной.")
                except ValueError:
                    print("Площадь не изменена - некорректное значение.")

            if isinstance(obj, zdanie):
                params.update(self._input_building_params())
            elif isinstance(obj, zemelnyj_uchastok):
                params.update(self._input_land_params())

            updated_obj = self.agency.provesti_tekhnicheskij_uchet(objekt_id, **params)

            print(f"\n✓ Технический учёт успешно завершён!")
            print(f"   Объект: {'Здание' if isinstance(updated_obj, zdanie) else 'Земельный участок'}")
            print(f"   Адрес: {updated_obj.adres}")
            print(f"   Технический паспорт: №{updated_obj.nomer_tekhpasporta}")
            print(f"   Дата обследования: {self._format_date(updated_obj.data_poslednego_tekh_ucheta)}")

            if isinstance(updated_obj, zdanie):
                iznos_level = self._get_iznos_level(updated_obj.fizicheskij_iznos)
                print(f"\n   Результаты обследования:")
                print(f"   • Этажность: {updated_obj.kolichestvo_etazhej}")
                print(f"   • Материал стен: {updated_obj.material_sten}")
                print(f"   • Физический износ: {updated_obj.fizicheskij_iznos}% ({iznos_level})")
                print(f"   • Пожарная безопасность: класс {updated_obj.pozharnaya_bezopasnost}")
                print(f"   • Энергоэффективность: класс {updated_obj.energeticheskaya_effektivnost}")
            else:
                print(f"\n   Характеристики участка:")
                print(f"   • Категория земель: {updated_obj.kategoriya_zemel}")
                print(f"   • Вид использования: {updated_obj.vid_razreshonnogo_ispolzovaniya}")
                print(f"   • Наличие построек: {'Да' if updated_obj.nalichie_postroek else 'Нет'}")
                print(f"   • Состояние: {updated_obj.sostoyanie}")

        except Exception as e:
            print(f"Ошибка при техучёте: {e}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def update_docs(self):
        print("\n--- ОБНОВЛЕНИЕ ДОКУМЕНТАЦИИ ---")
        self._show_objects_short()
        try:
            objekt_id = self._input_object_uid()
            obj = self.agency._object_repo.get(objekt_id)
            self.agency.obnovit_dokumenty(objekt_id)
            print(f"✓ Документация объекта {objekt_id} успешно обновлена")
            print(f"  Объект: {obj.adres}")
            print(f"  Для просмотра выписки используйте пункт 8 меню")
        except Exception as e:
            print(f"Ошибка при обновлении документации: {e}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def get_info(self):
        print("\n--- ПОЛУЧЕНИЕ ВЫПИСКИ ПО КАДАСТРОВОМУ НОМЕРУ ---")
        objects = self.agency.reestr_obektov
        objects_with_numbers = [obj for obj in objects if obj.kadastrovyj_nomer]

        if objects_with_numbers:
            print("\nДоступные объекты с кадастровыми номерами:")
            print("-" * 70)
            type_names = {'ZemelnyjUchastok': 'Земельный участок', 'Zdanie': 'Здание'}
            for i, obj in enumerate(objects_with_numbers, 1):
                obj_type = type_names.get(obj.__class__.__name__, obj.__class__.__name__)
                cad_number = obj.kadastrovyj_nomer.polnoe_znachenie
                print(f"{i}. {obj_type}")
                print(f"   Адрес: {obj.adres}")
                print(f"   Кадастровый номер: {cad_number}")
                print(f"   Статус: {self._translate_status(obj.status)}")
                print()
        else:
            print("\nНет объектов с присвоенными кадастровыми номерами.")
            print("Сначала присвойте кадастровые номера объектам (пункт меню 5).")

        try:
            kad_num = input("\nВведите кадастровый номер (формат АА:ББ:CCCCCC:DD): ").strip()
            if not kad_num:
                raise ValidationError("Кадастровый номер не может быть пустым")
            info = self.agency.predostavit_informaciyu(kad_num)
            print("\n" + "=" * 70)
            print(info)
            print("=" * 70)
        except NotFoundError as e:
            print(f"Ошибка: {e}")
            print("\nПроверьте правильность введённого кадастрового номера.")
            print("Кадастровый номер должен быть в формате: 77:01:000123:001")
        except ValidationError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Ошибка при получении информации: {e}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def list_objects(self):
        print("\n--- СПИСОК ВСЕХ ОБЪЕКТОВ НЕДВИЖИМОСТИ ---")
        objects = self.agency.reestr_obektov
        if not objects:
            print("Объекты не найдены.")
        else:
            type_names = {
                'ZemelnyjUchastok': 'Земельный участок',
                'Zdanie': 'Здание',
                'ObjektNedvizhimosti': 'Объект недвижимости'
            }
            status_names = {
                'uchtennyy': 'Учтённый',
                'vremennyy': 'Временный',
                'arkhivnyy': 'Архивный'
            }
            for i, obj in enumerate(objects, 1):
                obj_type = type_names.get(obj.__class__.__name__, obj.__class__.__name__)
                status = status_names.get(obj.status, obj.status)
                print(f"\n{i}. {obj_type}")
                print(f"   UID: {obj.uid}")
                print(f"   Адрес: {obj.adres}")
                print(f"   Площадь: {obj.ploshchad} кв.м")
                print(f"   Статус: {status}")
                print(f"   Дата регистрации: {self._format_date(obj.data_registracii)}")
                if obj.kadastrovyj_nomer:
                    print(f"   Кадастровый номер: {obj.kadastrovyj_nomer.polnoe_znachenie}")
                else:
                    print(f"   Кадастровый номер: не присвоен")
                if obj.nomer_tekhpasporta:
                    data_tekh = self._format_date(obj.data_poslednego_tekh_ucheta) if obj.data_poslednego_tekh_ucheta else "неизвестно"
                    print(f"   Техпаспорт: №{obj.nomer_tekhpasporta} от {data_tekh}")
                else:
                    print(f"   Техпаспорт: не оформлен")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def list_vladeshecs(self):
        print("\n--- СПИСОК ВСЕХ ВЛАДЕЛЬЦЕВ ---")
        owners = self.agency.reestr_vladelcev
        if not owners:
            print("Владельцы не найдены.")
        else:
            for i, owner in enumerate(owners, 1):
                print(f"\n{i}. {owner.fio}")
                print(f"   UID: {owner.uid}")
                print(f"   Идентификатор: {owner.identificator}")
                print(f"   Контакты: {owner.rekvizity_svyazi}")
        input("\nНажмите Enter, чтобы продолжить...")
        return True

    def exit_program(self):
        print("\nСпасибо за использование системы кадастрового агентства!")
        return False


    def _show_objects_short(self):
        objects = self.agency.reestr_obektov
        if objects:
            print("\nСуществующие объекты:")
            type_names = {'ZemelnyjUchastok': 'Земельный участок', 'Zdanie': 'Здание'}
            for i, obj in enumerate(objects, 1):
                obj_type = type_names.get(obj.__class__.__name__, obj.__class__.__name__)
                print(f"  {i}. {obj.uid} - {obj.adres} ({obj_type})")
        else:
            print("\nНет зарегистрированных объектов.")

    def _show_owners_short(self):
        owners = self.agency.reestr_vladelcev
        if owners:
            print("\nСуществующие владельцы:")
            for i, owner in enumerate(owners, 1):
                print(f"  {i}. {owner.uid} - {owner.fio}")
        else:
            print("\nНет зарегистрированных владельцев.")

    def _format_date(self, date_str: str) -> str:
        try:
            if 'T' in date_str:
                dt = datetime.fromisoformat(date_str)
                return dt.strftime('%d.%m.%Y')
            for fmt in ['%Y-%m-%d', '%d.%m.%Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%d.%m.%Y')
                except ValueError:
                    continue
            return date_str
        except:
            return date_str

    def _translate_status(self, status: str) -> str:
        status_map = {
            'aktivnyy': 'Активный',
            'uchtennyy': 'Учтённый',
            'vremennyy': 'Временный'
        }
        return status_map.get(status, status)

    def _get_iznos_level(self, iznos: int) -> str:
        if iznos < Constants.DEPRECIATION_EXCELLENT:
            return "Отличное"
        if iznos < Constants.DEPRECIATION_GOOD:
            return "Хорошее"
        if iznos < Constants.DEPRECIATION_SATISFACTORY:
            return "Удовлетворительное"
        if iznos < Constants.DEPRECIATION_POOR:
            return "Неудовлетворительное"
        return "Аварийное"


def main():
    menu = CadastralMenu()
    menu.run()


if __name__ == "__main__":
    main()
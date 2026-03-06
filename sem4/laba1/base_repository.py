import json
import os
from typing import List, TypeVar, Generic, Type, Dict

from exceptions.exceptions import NotFoundError
from models.base_model import base_model
from constants import Constants
from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from models.zemelnyj_uchastok import zemelnyj_uchastok
from models.zdanie import zdanie

T = TypeVar('T', bound=base_model)

class base_repository(Generic[T]):
    """Базовый репозиторий для хранения сущностей в JSON."""

    def __init__(self, file_path: str, cls: Type[T]):
        self.file_path = file_path
        self.cls = cls
        self._items: Dict[str, T] = {}
        self._load()

    def _load(self) -> None:
        """Загрузить данные из файла."""
        if not os.path.exists(self.file_path):
            self._items = {}
            return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for uid, item_data in data.items():
                try:
                    obj = self._from_dict(item_data)
                    if obj:
                        self._items[uid] = obj
                except Exception as e:
                    print(f"Ошибка загрузки объекта {uid}: {e}")
                    continue
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка чтения файла {self.file_path}: {e}")
            self._items = {}

    def _save(self) -> None:
        """Сохранить данные в файл."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        data = {uid: self._to_dict(obj) for uid, obj in self._items.items()}
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=Constants.JSON_INDENT)

    def _to_dict(self, obj: T) -> dict:
        """Преобразовать объект в словарь для сериализации."""
        result = {}
        for key, value in obj.__dict__.items():
            if key.startswith('_'):
                key = key[Constants.DEFAULT_MIN_POSITIVE:]

            if key == 'kadastrovyj_nomer' and value is not None:
                if hasattr(value, 'uid'):
                    result[key] = value.uid
                else:
                    result[key] = None
            elif isinstance(value, base_model):
                result[key] = value.uid
            elif isinstance(value, list) and all(isinstance(v, base_model) for v in value):
                result[key] = [v.uid for v in value]
            else:
                result[key] = value
        return result

    def _from_dict(self, data: dict) -> objekt_nedvizhimosti:
        obj_type = data.pop('_type', None)

        clean_data = {}
        for key, value in data.items():
            if key.startswith('_') or key.endswith('_uid'):
                continue
            clean_data[key] = value

        clean_data.pop('kadastrovyj_nomer', None)
        clean_data.pop('svyazannyj_objekt', None)
        clean_data.pop('spisok_vladelcev', None)

        try:
            if obj_type == 'ZemelnyjUchastok':
                obj = zemelnyj_uchastok(**clean_data)
            elif obj_type == 'Zdanie':
                obj = zdanie(**clean_data)
            else:
                obj = objekt_nedvizhimosti(**clean_data)
            print(f"Создан объект: {obj}, тип: {type(obj)}")
            return obj
        except Exception as e:
            print(f"Ошибка создания объекта: {e}")
            raise

    def add(self, obj: T) -> None:
        self._items[obj.uid] = obj
        self._save()

    def update(self, obj: T) -> None:
        if obj.uid not in self._items:
            raise NotFoundError(f"Объект с uid {obj.uid} не найден")
        self._items[obj.uid] = obj
        self._save()

    def delete(self, uid: str) -> None:
        if uid in self._items:
            del self._items[uid]
            self._save()

    def get(self, uid: str) -> T:
        if uid not in self._items:
            raise NotFoundError(f"Объект с uid {uid} не найден")
        return self._items[uid]

    def list_all(self) -> List[T]:
        return list(self._items.values())
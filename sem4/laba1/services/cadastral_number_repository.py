import os
from models.kadastrovyj_nomer import kadastrovyj_nomer
from services.base_repository import base_repository


class cadastral_number_repository(base_repository[kadastrovyj_nomer]):
    def __init__(self, data_dir: str):
        super().__init__(os.path.join(data_dir, 'cadastral_numbers.json'), kadastrovyj_nomer)

    def _to_dict(self, obj: kadastrovyj_nomer) -> dict:
        data = super()._to_dict(obj)
        if 'vladeshec_nomera' in data and data['vladeshec_nomera'] is not None:
            if hasattr(data['vladeshec_nomera'], 'uid'):
                data['vladeshec_nomera'] = data['vladeshec_nomera'].uid
        return data

    def _from_dict(self, data: dict) -> kadastrovyj_nomer:
        print(f"CadastralNumberRepository._from_dict получил данные: {data}")

        clean_data = {}
        exclude_fields = {'uid', 'vladeshec_nomera'}

        for key, value in data.items():
            if key.startswith('_') or key in exclude_fields:
                continue
            clean_data[key] = value

        try:
            from models.kadastrovyj_nomer import kadastrovyj_nomer
            obj = kadastrovyj_nomer(**clean_data)

            if 'uid' in data:
                obj._uid = data['uid']
            if 'vladeshec_nomera' in data:
                obj._vladeshec_nomera = data['vladeshec_nomera']

            return obj
        except Exception as e:
            print(f"Ошибка создания кадастрового номера: {e}")
            raise
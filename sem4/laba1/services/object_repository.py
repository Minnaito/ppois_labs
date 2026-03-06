import os
from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from services.base_repository import base_repository


class object_repository(base_repository[objekt_nedvizhimosti]):
    def __init__(self, data_dir: str):
        file_path = os.path.join(data_dir, 'objects.json')
        super().__init__(file_path, objekt_nedvizhimosti)

    def _to_dict(self, obj: objekt_nedvizhimosti) -> dict:
        data = super()._to_dict(obj)
        data['_type'] = obj.__class__.__name__


        return data

    def _from_dict(self, data: dict) -> objekt_nedvizhimosti:
        obj_type = data.pop('_type', None)

        clean_data = {}

        exclude_fields = {'kadastrovyj_nomer', 'saved_vypiska', 'uid',
                          'data_poslednego_tekh_ucheta', 'nomer_tekhpasporta',
                          'poetazhnyj_plan', 'fizicheskij_iznos', 'inventarnaya_stoimost',
                          'granicy'}

        for key, value in data.items():
            if key.startswith('_') or key in exclude_fields:
                continue
            clean_data[key] = value

        try:
            if obj_type == 'ZemelnyjUchastok':
                from models.zemelnyj_uchastok import zemelnyj_uchastok
                obj = zemelnyj_uchastok(**clean_data)
            elif obj_type == 'Zdanie':
                from models.zdanie import zdanie
                obj = zdanie(**clean_data)
            else:
                return None

            if 'uid' in data:
                obj._uid = data['uid']
            if 'kadastrovyj_nomer' in data:
                obj._kadastrovyj_nomer = data[
                    'kadastrovyj_nomer']
            if 'saved_vypiska' in data:
                obj._saved_vypiska = data['saved_vypiska']
            if 'data_poslednego_tekh_ucheta' in data:
                obj._data_poslednego_tekh_ucheta = data['data_poslednego_tekh_ucheta']
            if 'nomer_tekhpasporta' in data:
                obj._nomer_tekhpasporta = data['nomer_tekhpasporta']

            return obj

        except Exception as e:
            print(f"Ошибка создания объекта: {e}")
            raise
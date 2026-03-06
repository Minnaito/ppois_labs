import os
from models.pravo_ustanavlivayushchij_dokument import pravo_ustanavlivayushchij_dokument
from services.base_repository import base_repository


class right_document_repository(base_repository[pravo_ustanavlivayushchij_dokument]):
    def __init__(self, data_dir: str):
        super().__init__(os.path.join(data_dir, 'right_docs.json'), pravo_ustanavlivayushchij_dokument)

    def _to_dict(self, obj: pravo_ustanavlivayushchij_dokument) -> dict:
        data = super()._to_dict(obj)

        if hasattr(obj, '_svyazannyj_objekt') and obj._svyazannyj_objekt is not None:
            if hasattr(obj._svyazannyj_objekt, 'uid'):
                data['svyazannyj_objekt'] = obj._svyazannyj_objekt.uid
            else:
                data['svyazannyj_objekt'] = None
        else:
            data['svyazannyj_objekt'] = None

        if hasattr(obj, '_spisok_vladelcev') and obj._spisok_vladelcev:
            data['spisok_vladelcev'] = [v.uid if hasattr(v, 'uid') else v for v in obj._spisok_vladelcev]
        else:
            data['spisok_vladelcev'] = []

        return data

    def _from_dict(self, data: dict) -> pravo_ustanavlivayushchij_dokument:
        print(f"RightDocumentRepository._from_dict получил данные: {data}")

        clean_data = {}
        exclude_fields = {'uid', 'svyazannyj_objekt', 'spisok_vladelcev'}

        for key, value in data.items():
            if key.startswith('_') or key in exclude_fields:
                continue
            clean_data[key] = value

        try:
            from models.pravo_ustanavlivayushchij_dokument import pravo_ustanavlivayushchij_dokument
            obj = pravo_ustanavlivayushchij_dokument(**clean_data)

            if 'uid' in data:
                obj._uid = data['uid']
            if 'svyazannyj_objekt' in data:
                obj._svyazannyj_objekt_uid = data['svyazannyj_objekt']
            if 'spisok_vladelcev' in data:
                obj._spisok_vladelcev_uids = data['spisok_vladelcev']

            return obj
        except Exception as e:
            print(f"Ошибка создания документа: {e}")
            raise
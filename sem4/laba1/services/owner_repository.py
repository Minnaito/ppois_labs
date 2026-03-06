import os
from models.vladeshec import vladeshec
from services.base_repository import base_repository


class owner_repository(base_repository[vladeshec]):
    def __init__(self, data_dir: str):
        super().__init__(os.path.join(data_dir, 'owners.json'), vladeshec)

    def _from_dict(self, data: dict) -> vladeshec:
        clean_data = {}
        exclude_fields = {'uid'}

        for key, value in data.items():
            if key.startswith('_') or key in exclude_fields:
                continue
            clean_data[key] = value

        try:
            from models.vladeshec import vladeshec
            obj = vladeshec(**clean_data)

            if 'uid' in data:
                obj._uid = data['uid']

            return obj
        except Exception as e:
            raise
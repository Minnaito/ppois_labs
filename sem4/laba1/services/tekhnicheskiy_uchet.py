import uuid
from datetime import datetime
from models.zemelnyj_uchastok import zemelnyj_uchastok
from models.zdanie import zdanie
from services.object_repository import object_repository


class tekhnicheskiy_uchet:
    def __init__(self, object_repo: object_repository):
        self._object_repo = object_repo

    def _generate_tekhpasport_number(self) -> str:
        """Генерирует уникальный номер техпаспорта."""
        return f"ТП-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    def provesti_tekhnicheskij_uchet_zdaniya(self, zdanie: zdanie, parametry: dict = None) -> None:
        """Провести техучёт здания."""
        if parametry is None:
            parametry = {}

        for key, value in parametry.items():
            if hasattr(zdanie, key) and key not in ['uid', 'kadastrovyj_nomer']:
                setattr(zdanie, key, value)

        zdanie.data_poslednego_tekh_ucheta = datetime.now().isoformat()
        zdanie.nomer_tekhpasporta = self._generate_tekhpasport_number()

        self._object_repo.update(zdanie)

    def provesti_tekhnicheskij_uchet_uchastka(self, uchastok: zemelnyj_uchastok, parametry: dict = None) -> None:
        """Провести техучёт земельного участка."""
        if parametry is None:
            parametry = {}

        for key, value in parametry.items():
            if hasattr(uchastok, key) and key not in ['uid', 'kadastrovyj_nomer']:
                setattr(uchastok, key, value)

        uchastok.data_poslednego_tekh_ucheta = datetime.now().isoformat()
        uchastok.nomer_tekhpasporta = self._generate_tekhpasport_number()

        self._object_repo.update(uchastok)